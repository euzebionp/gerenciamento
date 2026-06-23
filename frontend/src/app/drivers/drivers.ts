import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { DriverService } from '../services/driver.service';

@Component({
  selector: 'app-drivers',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './drivers.html',
  styleUrl: './drivers.css'
})
export class DriversComponent implements OnInit {
  private driverService = inject(DriverService);

  activeTab = signal<string>('list');
  drivers = signal<any[]>([]);
  loading = signal<boolean>(true);

  newName = '';
  newCpf = '';
  newCnh = '';
  newPhone = '';
  newStatus = 'ATIVO';

  selectedDriverId = signal<number | null>(null);
  selectedDriver: any = null;
  editName = '';
  editCpf = '';
  editCnh = '';
  editPhone = '';
  editStatus = 'ATIVO';

  confirmDelete = false;

  successMessage = signal<string | null>(null);
  errorMessage = signal<string | null>(null);

  driverStatuses = ['ATIVO', 'FERIAS', 'AFASTADO'];

  ngOnInit(): void {
    this.loadDrivers();
  }

  loadDrivers(): void {
    this.loading.set(true);
    this.driverService.getAll().subscribe({
      next: (data) => {
        this.drivers.set(data);
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

    if (tab === 'edit' && this.drivers().length > 0) {
      this.onDriverSelect(this.drivers()[0].id);
    }
  }

  clearMessages(): void {
    this.successMessage.set(null);
    this.errorMessage.set(null);
  }

  onDriverSelect(id: number): void {
    this.selectedDriverId.set(id);
    this.selectedDriver = this.drivers().find(d => d.id === id);
    if (this.selectedDriver) {
      this.editName = this.selectedDriver.name;
      this.editCpf = this.selectedDriver.cpf;
      this.editCnh = this.selectedDriver.cnh;
      this.editPhone = this.selectedDriver.phone || '';
      this.editStatus = this.selectedDriver.status;
    }
    this.confirmDelete = false;
  }

  validateInputs(name: string, cpf: string, cnh: string): boolean {
    if (!name || !cpf || !cnh) {
      this.errorMessage.set('Preencha todos os campos obrigatórios!');
      return false;
    }
    if (cpf.length !== 11 || !/^\d+$/.test(cpf)) {
      this.errorMessage.set('CPF deve conter exatamente 11 dígitos numéricos!');
      return false;
    }
    if (cnh.length < 9 || !/^\d+$/.test(cnh)) {
      this.errorMessage.set('CNH deve conter pelo menos 9 dígitos numéricos!');
      return false;
    }
    return true;
  }

  onCreate(): void {
    this.clearMessages();
    if (!this.validateInputs(this.newName, this.newCpf, this.newCnh)) {
      return;
    }

    const payload = {
      name: this.newName,
      cpf: this.newCpf,
      cnh: this.newCnh,
      phone: this.newPhone,
      status: this.newStatus
    };

    this.driverService.create(payload).subscribe({
      next: (res) => {
        this.successMessage.set(`Motorista ${res.name} cadastrado com sucesso!`);
        this.newName = '';
        this.newCpf = '';
        this.newCnh = '';
        this.newPhone = '';
        this.newStatus = 'ATIVO';
        this.loadDrivers();
      },
      error: (err) => {
        this.errorMessage.set(err.error || 'Erro ao cadastrar motorista.');
      }
    });
  }

  onUpdate(): void {
    this.clearMessages();
    const id = this.selectedDriverId();
    if (!id) return;

    if (!this.validateInputs(this.editName, this.editCpf, this.editCnh)) {
      return;
    }

    const payload = {
      name: this.editName,
      cpf: this.editCpf,
      cnh: this.editCnh,
      phone: this.editPhone,
      status: this.editStatus
    };

    this.driverService.update(id, payload).subscribe({
      next: (res) => {
        this.successMessage.set(`Motorista ${res.name} atualizado com sucesso!`);
        this.loadDrivers();
      },
      error: (err) => {
        this.errorMessage.set(err.error || 'Erro ao atualizar motorista.');
      }
    });
  }

  onDelete(): void {
    this.clearMessages();
    const id = this.selectedDriverId();
    if (!id) return;

    this.driverService.delete(id).subscribe({
      next: (msg) => {
        this.successMessage.set(msg);
        this.loadDrivers();
        setTimeout(() => {
          this.setTab('list');
        }, 1500);
      },
      error: (err) => {
        this.errorMessage.set(err.error || 'Erro ao excluir motorista.');
      }
    });
  }
}
