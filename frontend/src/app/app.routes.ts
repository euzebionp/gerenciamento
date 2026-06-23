import { Routes } from '@angular/router';
import { LoginComponent } from './login/login';
import { LayoutComponent } from './layout/layout';
import { DashboardComponent } from './dashboard/dashboard';
import { VehiclesComponent } from './vehicles/vehicles';
import { DriversComponent } from './drivers/drivers';
import { TripsComponent } from './trips/trips';
import { ReportsComponent } from './reports/reports';
import { AdminComponent } from './admin/admin';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  {
    path: '',
    component: LayoutComponent,
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: DashboardComponent },
      { path: 'vehicles', component: VehiclesComponent },
      { path: 'drivers', component: DriversComponent },
      { path: 'trips', component: TripsComponent },
      { path: 'reports', component: ReportsComponent },
      { path: 'admin', component: AdminComponent }
    ]
  },
  { path: '**', redirectTo: '' }
];
