import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { TripService } from '../services/trip.service';
import { VehicleService } from '../services/vehicle.service';
import { DriverService } from '../services/driver.service';

@Component({
  selector: 'app-trips',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './trips.html',
  styleUrl: './trips.css'
})
export class TripsComponent implements OnInit {
  private tripService = inject(TripService);
  private vehicleService = inject(VehicleService);
  private driverService = inject(DriverService);

  activeTab = signal<string>('active');
  activeTrips = signal<any[]>([]);
  historyTrips = signal<any[]>([]);
  loading = signal<boolean>(true);

  availableVehicles = signal<any[]>([]);
  availableDrivers = signal<any[]>([]);

  origin = '';
  destination = '';
  distanceKm = 0;
  selectedVehicleId = '';
  selectedDriverId = '';
  startDate = '';
  startTime = '';
  initialStatus = 'PLANEJADA';

  filterStatus: string[] = ['CONCLUIDA'];
  filterDate = '';

  statusOptions = ['PLANEJADA', 'AGENDADA', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA'];

  successMessage = signal<string | null>(null);
  errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    const today = new Date();
    this.startDate = today.toISOString().split('T')[0];
    this.startTime = today.toTimeString().split(' ')[0].substring(0, 5);
    this.loadActiveTrips();
  }

  loadActiveTrips(): void {
    this.loading.set(true);
    this.tripService.getTrips(['PLANEJADA', 'EM_ANDAMENTO', 'AGENDADA']).subscribe({
      next: (data) => {
        this.activeTrips.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      }
    });
  }

  loadHistoryTrips(): void {
    this.loading.set(true);
    this.tripService.getTrips(this.filterStatus, this.filterDate || undefined).subscribe({
      next: (data) => {
        this.historyTrips.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      }
    });
  }

  loadResources(): void {
    this.vehicleService.getAll().subscribe(data => {
      this.availableVehicles.set(data.filter(v => v.status === 'ATIVO'));
    });
    this.driverService.getAll().subscribe(data => {
      this.availableDrivers.set(data.filter(d => d.status === 'ATIVO'));
    });
  }

  setTab(tab: string): void {
    this.activeTab.set(tab);
    this.clearMessages();

    if (tab === 'active') {
      this.loadActiveTrips();
    } else if (tab === 'history') {
      this.loadHistoryTrips();
    } else if (tab === 'new') {
      this.loadResources();
    }
  }

  clearMessages(): void {
    this.successMessage.set(null);
    this.errorMessage.set(null);
  }

  toggleStatusFilter(status: string): void {
    const index = this.filterStatus.indexOf(status);
    if (index > -1) {
      this.filterStatus.splice(index, 1);
    } else {
      this.filterStatus.push(status);
    }
    this.loadHistoryTrips();
  }

  updateStatus(tripId: number, status: string): void {
    this.clearMessages();
    this.tripService.update(tripId, { status }).subscribe({
      next: () => {
        this.successMessage.set('Status da viagem atualizado com sucesso!');
        this.loadActiveTrips();
      },
      error: (err) => {
        this.errorMessage.set(err.error || 'Erro ao atualizar status.');
      }
    });
  }

  onCreate(): void {
    this.clearMessages();
    if (!this.origin || !this.destination) {
      this.errorMessage.set('Preencha origem e destino!');
      return;
    }
    if (this.distanceKm <= 0) {
      this.errorMessage.set('A distância deve ser maior que zero!');
      return;
    }
    if (!this.selectedVehicleId || !this.selectedDriverId) {
      this.errorMessage.set('Selecione um veículo e um motorista ativos!');
      return;
    }

    const startDateTime = `${this.startDate}T${this.startTime}:00`;

    const payload = {
      origin: this.origin,
      destination: this.destination,
      distanceKm: this.distanceKm,
      vehicleId: Number(this.selectedVehicleId),
      driverId: Number(this.selectedDriverId),
      startDate: startDateTime,
      status: this.initialStatus
    };

    this.tripService.create(payload).subscribe({
      next: () => {
        this.successMessage.set('Viagem registrada com sucesso!');
        this.origin = '';
        this.destination = '';
        this.distanceKm = 0;
        this.selectedVehicleId = '';
        this.selectedDriverId = '';
        this.loadResources();
      },
      error: (err) => {
        this.errorMessage.set(err.error || 'Erro ao registrar viagem.');
      }
    });
  }

  exportCsv(): void {
    if (this.historyTrips().length === 0) return;

    let csvContent = 'ID,Origem,Destino,Veículo,Motorista,Data Início,Data Fim,Distância (km),Status\n';

    this.historyTrips().forEach(t => {
      const vText = `"${t.vehicle.model} (${t.vehicle.plate})"`;
      const dText = `"${t.driver.name}"`;
      const startDateText = new Date(t.startDate).toLocaleString('pt-BR');
      const endDateText = t.endDate ? new Date(t.endDate).toLocaleString('pt-BR') : 'N/A';
      
      csvContent += `${t.id},"${t.origin}","${t.destination}",${vText},${dText},${startDateText},${endDateText},${t.distanceKm},${t.status}\n`;
    });

    const blob = new Blob([new Uint8Array([0xEF, 0xBB, 0xBF]), csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `viagens_historico_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}
