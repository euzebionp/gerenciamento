import { Component, inject, OnInit, signal, OnDestroy } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ReportService } from '../services/report.service';
import { Chart } from 'chart.js/auto';

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reports.html',
  styleUrl: './reports.css'
})
export class ReportsComponent implements OnInit, OnDestroy {
  private reportService = inject(ReportService);

  activeTab = signal<string>('status');
  loading = signal<boolean>(true);

  startDate = '';
  endDate = '';

  totalTrips = signal<number>(0);
  completedTrips = signal<number>(0);
  totalDistance = signal<number>(0);
  activeVehicles = signal<number>(0);

  statusTable: any[] = [];
  vehiclesTable: any[] = [];
  driversTable: any[] = [];
  dailyTable: any[] = [];

  private statusChart: Chart | null = null;
  private vehicleTripsChart: Chart | null = null;
  private vehicleDistanceChart: Chart | null = null;
  private driverTripsChart: Chart | null = null;
  private dailyTripsChart: Chart | null = null;
  private dailyDistanceChart: Chart | null = null;

  ngOnInit(): void {
    const today = new Date();
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(today.getDate() - 30);

    this.startDate = thirtyDaysAgo.toISOString().split('T')[0];
    this.endDate = today.toISOString().split('T')[0];

    this.loadAnalytics();
  }

  ngOnDestroy(): void {
    this.destroyCharts();
  }

  destroyCharts(): void {
    if (this.statusChart) this.statusChart.destroy();
    if (this.vehicleTripsChart) this.vehicleTripsChart.destroy();
    if (this.vehicleDistanceChart) this.vehicleDistanceChart.destroy();
    if (this.driverTripsChart) this.driverTripsChart.destroy();
    if (this.dailyTripsChart) this.dailyTripsChart.destroy();
    if (this.dailyDistanceChart) this.dailyDistanceChart.destroy();
  }

  loadAnalytics(): void {
    this.loading.set(true);
    this.destroyCharts();

    this.reportService.getAnalytics(this.startDate, this.endDate).subscribe({
      next: (data) => {
        this.totalTrips.set(data.totalTrips);
        this.completedTrips.set(data.completedTrips);
        this.totalDistance.set(data.totalDistance);
        this.activeVehicles.set(data.activeVehicles);

        this.statusTable = Object.keys(data.statusCounts).map(k => ({ status: k, count: data.statusCounts[k] }));
        this.vehiclesTable = data.vehicleStats;
        this.driversTable = data.driverStats;
        this.dailyTable = data.dailyStats;

        this.loading.set(false);

        setTimeout(() => {
          this.createCharts(data);
        }, 100);
      },
      error: () => {
        this.loading.set(false);
      }
    });
  }

  setTab(tab: string): void {
    this.activeTab.set(tab);
  }

  createCharts(data: any): void {
    this.destroyCharts();

    // 1. Status Chart
    const statusCanvas = document.getElementById('statusChart') as HTMLCanvasElement;
    if (statusCanvas && Object.keys(data.statusCounts).length > 0) {
      const labels = Object.keys(data.statusCounts);
      const values = Object.values(data.statusCounts);
      this.statusChart = new Chart(statusCanvas, {
        type: 'pie',
        data: {
          labels,
          datasets: [{
            data: values,
            backgroundColor: ['#60a5fa', '#22d3ee', '#fbbf24', '#34d399', '#f87171'],
            borderWidth: 1,
            borderColor: 'rgba(255, 255, 255, 0.1)'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'bottom', labels: { color: '#94a3b8' } }
          }
        }
      });
    }

    // 2. Vehicle Charts
    const vTripsCanvas = document.getElementById('vehicleTripsChart') as HTMLCanvasElement;
    if (vTripsCanvas && data.vehicleStats.length > 0) {
      const labels = data.vehicleStats.map((s: any) => s.vehicle);
      const trips = data.vehicleStats.map((s: any) => s.trips);
      this.vehicleTripsChart = new Chart(vTripsCanvas, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Viagens',
            data: trips,
            backgroundColor: 'rgba(52, 211, 153, 0.7)',
            borderColor: '#34d399',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } }
          },
          plugins: { legend: { display: false } }
        }
      });
    }

    const vDistCanvas = document.getElementById('vehicleDistanceChart') as HTMLCanvasElement;
    if (vDistCanvas && data.vehicleStats.length > 0) {
      const labels = data.vehicleStats.map((s: any) => s.vehicle);
      const dist = data.vehicleStats.map((s: any) => s.distance);
      this.vehicleDistanceChart = new Chart(vDistCanvas, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Distânia (km)',
            data: dist,
            backgroundColor: 'rgba(96, 165, 250, 0.7)',
            borderColor: '#60a5fa',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } }
          },
          plugins: { legend: { display: false } }
        }
      });
    }

    // 3. Driver Chart
    const dTripsCanvas = document.getElementById('driverTripsChart') as HTMLCanvasElement;
    if (dTripsCanvas && data.driverStats.length > 0) {
      const labels = data.driverStats.map((s: any) => s.driver);
      const trips = data.driverStats.map((s: any) => s.trips);
      this.driverTripsChart = new Chart(dTripsCanvas, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Viagens',
            data: trips,
            backgroundColor: 'rgba(139, 92, 246, 0.7)',
            borderColor: '#8b5cf6',
            borderWidth: 1
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          scales: {
            x: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } },
            y: { grid: { display: false }, ticks: { color: '#94a3b8' } }
          },
          plugins: { legend: { display: false } }
        }
      });
    }

    // 4. Trend Charts
    const tTripsCanvas = document.getElementById('trendTripsChart') as HTMLCanvasElement;
    if (tTripsCanvas && data.dailyStats.length > 0) {
      const labels = data.dailyStats.map((s: any) => s.date);
      const trips = data.dailyStats.map((s: any) => s.trips);
      this.dailyTripsChart = new Chart(tTripsCanvas, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: 'Viagens por Dia',
            data: trips,
            fill: false,
            borderColor: '#3b82f6',
            tension: 0.1,
            pointBackgroundColor: '#3b82f6'
          }]
        },
        options: {
          responsive: true,
          scales: {
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } }
          }
        }
      });
    }

    const tDistCanvas = document.getElementById('trendDistanceChart') as HTMLCanvasElement;
    if (tDistCanvas && data.dailyStats.length > 0) {
      const labels = data.dailyStats.map((s: any) => s.date);
      const dist = data.dailyStats.map((s: any) => s.distance);
      this.dailyDistanceChart = new Chart(tDistCanvas, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: 'Distância por Dia (km)',
            data: dist,
            fill: true,
            backgroundColor: 'rgba(249, 115, 22, 0.1)',
            borderColor: '#f97316',
            tension: 0.1,
            pointBackgroundColor: '#f97316'
          }]
        },
        options: {
          responsive: true,
          scales: {
            x: { grid: { display: false }, ticks: { color: '#94a3b8' } },
            y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#94a3b8' } }
          }
        }
      });
    }
  }

  exportReportCsv(): void {
    if (this.vehiclesTable.length === 0 && this.driversTable.length === 0) return;

    let csvContent = 'Relatorio de Frota\n';
    csvContent += `Periodo: ${this.startDate} a ${this.endDate}\n\n`;

    csvContent += 'RESUMO GERAL\n';
    csvContent += `Total de Viagens,${this.totalTrips()}\n`;
    csvContent += `Viagens Concluidas,${this.completedTrips()}\n`;
    csvContent += `Distancia Total (km),${this.totalDistance()}\n`;
    csvContent += `Veiculos Ativos,${this.activeVehicles()}\n\n`;

    csvContent += 'DESEMPENHO POR VEICULO\n';
    csvContent += 'Veiculo,Viagens,Distancia (km),Concluidas\n';
    this.vehiclesTable.forEach(v => {
      csvContent += `"${v.vehicle}",${v.trips},${v.distance},${v.completed}\n`;
    });
    csvContent += '\n';

    csvContent += 'DESEMPENHO POR MOTORISTA\n';
    csvContent += 'Motorista,Viagens,Distancia (km),Concluidas,Taxa de Conclusao (%)\n';
    this.driversTable.forEach(d => {
      csvContent += `"${d.driver}",${d.trips},${d.distance},${d.completed},${d.completionRate}\n`;
    });

    const blob = new Blob([new Uint8Array([0xEF, 0xBB, 0xBF]), csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `relatorio_analitico_${this.startDate}_a_${this.endDate}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}
