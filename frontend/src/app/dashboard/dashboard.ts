import { Component, inject, OnInit, signal } from '@angular/core';
import { ReportService } from '../services/report.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class DashboardComponent implements OnInit {
  private reportService = inject(ReportService);

  totalVehicles = signal<number>(0);
  activeVehicles = signal<number>(0);
  totalDrivers = signal<number>(0);
  activeTrips = signal<number>(0);
  loading = signal<boolean>(true);

  ngOnInit(): void {
    this.loadMetrics();
  }

  loadMetrics(): void {
    this.loading.set(true);
    this.reportService.getDashboardMetrics().subscribe({
      next: (data) => {
        this.totalVehicles.set(data.totalVehicles);
        this.activeVehicles.set(data.activeVehicles);
        this.totalDrivers.set(data.totalDrivers);
        this.activeTrips.set(data.activeTrips);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
      }
    });
  }
}
