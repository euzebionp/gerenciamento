import { Component, inject, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AdminService } from '../services/admin.service';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin.html',
  styleUrl: './admin.css'
})
export class AdminComponent implements OnInit {
  private adminService = inject(AdminService);
  private authService = inject(AuthService);

  activeTab = signal<string>('users');
  users = signal<any[]>([]);
  loading = signal<boolean>(true);

  newUsername = '';
  newPassword = '';
  newRole = 'USER';

  oldPassword = '';
  changeNewPassword = '';
  changeConfirmPassword = '';

  confirmDeleteId = signal<number | null>(null);

  successMessage = signal<string | null>(null);
  errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.loading.set(true);
    this.adminService.getUsers().subscribe({
      next: (data) => {
        this.users.set(data);
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
    if (tab === 'users') {
      this.loadUsers();
    }
  }

  clearMessages(): void {
    this.successMessage.set(null);
    this.errorMessage.set(null);
  }

  onCreateUser(): void {
    this.clearMessages();
    if (!this.newUsername || !this.newPassword) {
      this.errorMessage.set('Preencha todos os campos obrigatórios!');
      return;
    }

    this.adminService.register({
      username: this.newUsername,
      password: this.newPassword,
      role: this.newRole
    }).subscribe({
      next: (msg) => {
        this.successMessage.set('Usuário criado com sucesso!');
        this.newUsername = '';
        this.newPassword = '';
        this.newRole = 'USER';
        this.loadUsers();
      },
      error: (err) => {
        this.errorMessage.set(err.error || 'Erro ao criar usuário.');
      }
    });
  }

  onDeleteUser(id: number): void {
    this.clearMessages();
    this.adminService.deleteUser(id).subscribe({
      next: (msg) => {
        this.successMessage.set(msg);
        this.confirmDeleteId.set(null);
        this.loadUsers();
      },
      error: (err) => {
        this.errorMessage.set(err.error || 'Erro ao excluir usuário.');
      }
    });
  }

  onChangePassword(): void {
    this.clearMessages();
    if (!this.oldPassword || !this.changeNewPassword) {
      this.errorMessage.set('Preencha todos os campos!');
      return;
    }
    if (this.changeNewPassword.length < 4) {
      this.errorMessage.set('A nova senha deve ter pelo menos 4 caracteres.');
      return;
    }
    if (this.changeNewPassword !== this.changeConfirmPassword) {
      this.errorMessage.set('A confirmação da nova senha não corresponde.');
      return;
    }

    this.adminService.changePassword({
      oldPassword: this.oldPassword,
      newPassword: this.changeNewPassword
    }).subscribe({
      next: (msg) => {
        this.successMessage.set('Senha alterada com sucesso!');
        this.oldPassword = '';
        this.changeNewPassword = '';
        this.changeConfirmPassword = '';
      },
      error: (err) => {
        this.errorMessage.set(err.error || 'Erro ao alterar senha.');
      }
    });
  }
}
