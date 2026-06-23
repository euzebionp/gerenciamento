import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './layout.html',
  styleUrl: './layout.css'
})
export class LayoutComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  username = this.authService.getUsername() || 'Usuário';
  role = this.authService.getRole() || 'USER';

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
