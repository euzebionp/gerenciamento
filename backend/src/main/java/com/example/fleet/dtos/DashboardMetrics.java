package com.example.fleet.dtos;

public class DashboardMetrics {
    private long totalVehicles;
    private long activeVehicles;
    private long totalDrivers;
    private long activeTrips;

    public DashboardMetrics(long totalVehicles, long activeVehicles, long totalDrivers, long activeTrips) {
        this.totalVehicles = totalVehicles;
        this.activeVehicles = activeVehicles;
        this.totalDrivers = totalDrivers;
        this.activeTrips = activeTrips;
    }

    public long getTotalVehicles() {
        return totalVehicles;
    }

    public void setTotalVehicles(long totalVehicles) {
        this.totalVehicles = totalVehicles;
    }

    public long getActiveVehicles() {
        return activeVehicles;
    }

    public void setActiveVehicles(long activeVehicles) {
        this.activeVehicles = activeVehicles;
    }

    public long getTotalDrivers() {
        return totalDrivers;
    }

    public void setTotalDrivers(long totalDrivers) {
        this.totalDrivers = totalDrivers;
    }

    public long getActiveTrips() {
        return activeTrips;
    }

    public void setActiveTrips(long activeTrips) {
        this.activeTrips = activeTrips;
    }
}
