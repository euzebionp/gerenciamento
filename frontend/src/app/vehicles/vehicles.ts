import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { VehicleService } from '../services/vehicle.service';

@Component({
  selector: 'app-vehicles',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './vehicles.html',
  styleUrl: './vehicles.css'
})
export class VehiclesComponent implements OnInit {
  private vehicleService = inject(VehicleService);

  activeTab = signal<string>('list');
  vehicles = signal<any[]>([]);
  loading = signal<boolean>(true);

  newPlate = '';
  newModel = '';
  newCapacity = 4;
  newType = 'Carro';
  newStatus = 'ATIVO';

  selectedVehicleId = signal<number | null>(null);
  selectedVehicle: any = null;
  editPlate = '';
  editModel = '';
  editCapacity = 4;
  editType = 'Carro';
  editStatus = 'ATIVO';

  confirmDelete = false;

  successMessage = signal<string | null>(null);
  errorMessage = signal<string | null>(null);

  vehicleTypes = ['Carro', 'Van', 'Ônibus', 'Caminhão'];
  vehicleStatuses = ['ATIVO', 'MANUTENCAO', 'INATIVO'];

  ngOnInit(): void {
    this.loadVehicles();
  }

  loadVehicles(): void {
    this.loading.set(true);
    this.vehicleService.getAll().subscribe({
      next: (data) => {
        this.vehicles.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      }
    });
  }

  setTab(tab: string): void {
    this.activeTab.set(tab);
    this.clearMessages();
    this.confirmDelete = false;

    if (tab === 'edit' && this.vehicles().length > 0) {
      this.onVehicleSelect(this.vehicles()[0].id);
    }
  }

  clearMessages(): void {
    this.successMessage.set(null);
    this.errorMessage.set(null);
  }

  onVehicleSelect(id: number): void {
    this.selectedVehicleId.set(id);
    this.selectedVehicle = this.vehicles().find(v => v.id === id);
    if (this.selectedVehicle) {
      this.editPlate = this.selectedVehicle.plate;
      this.editModel = this.selectedVehicle.model;
      this.editCapacity = this.selectedVehicle.capacity;
      this.editType = this.selectedVehicle.type;
      this.editStatus = this.selectedVehicle.status;
    }
    this.confirmDelete = false;
  }

  onCreate(): void {
    this.clearMessages();
    if (!this.newPlate || !this.newModel) {
      this.errorMessage.set('Preencha todos os campos obrigatórios!');
      return;
    }

    const payload = {
      plate: this.newPlate.toUpperCase(),
      model: this.newModel,
      capacity: this.newCapacity,
      type: this.newType,
      status: this.newStatus
    };

    this.vehicleService.create(payload).subscribe({
      next: (res) => {
        this.successMessage.set(`Veículo ${res.model} (${res.plate}) cadastrado com sucesso!`);
        this.newPlate = '';
        this.newModel = '';
        this.newCapacity = 4;
        this.newType = 'Carro';
        this.newStatus = 'ATIVO';
        this.loadVehicles();
      },
      error: (err) => {
        this.errorMessage.set(err.error || 'Erro ao cadastrar veículo.');
      }
    });
  }

  onUpdate(): void {
    this.clearMessages();
    const id = this.selectedVehicleId();
    if (!id || !this.editPlate || !this.editModel) {
      this.errorMessage.set('Preencha todos os campos obrigatórios!');
      return;
    }

    const payload = {
      plate: this.editPlate.toUpperCase(),
      model: this.editModel,
      capacity: this.editCapacity,
      type: this.editType,
      status: this.editStatus
    };

    this.vehicleService.update(id, payload).subscribe({
      next: (res) => {
        this.successMessage.set(`Veículo ${res.model} atualizado com sucesso!`);
        this.loadVehicles();
      },
      error: (err) => {
        this.errorMessage.set(err.error || 'Erro ao atualizar veículo.');
      }
    });
  }

  onDelete(): void {
    this.clearMessages();
    const id = this.selectedVehicleId();
    if (!id) return;

    this.vehicleService.delete(id).subscribe({
      next: (msg) => {
        this.successMessage.set(msg);
        this.loadVehicles();
        setTimeout(() => {
          this.setTab('list');
        }, 1500);
      },
      error: (err) => {
        this.errorMessage.set(err.error || 'Erro ao excluir veículo.');
      }
    });
  }
}
