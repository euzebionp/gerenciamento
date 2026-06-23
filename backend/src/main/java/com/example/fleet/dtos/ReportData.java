package com.example.fleet.dtos;

import java.util.List;
import java.util.Map;

public class ReportData {
    private long totalTrips;
    private long completedTrips;
    private double totalDistance;
    private long activeVehicles;
    private Map<String, Long> statusCounts;
    private List<VehicleStat> vehicleStats;
    private List<DriverStat> driverStats;
    private List<DailyStat> dailyStats;

    public long getTotalTrips() {
        return totalTrips;
    }

    public void setTotalTrips(long totalTrips) {
        this.totalTrips = totalTrips;
    }

    public long getCompletedTrips() {
        return completedTrips;
    }

    public void setCompletedTrips(long completedTrips) {
        this.completedTrips = completedTrips;
    }

    public double getTotalDistance() {
        return totalDistance;
    }

    public void setTotalDistance(double totalDistance) {
        this.totalDistance = totalDistance;
    }

    public long getActiveVehicles() {
        return activeVehicles;
    }

    public void setActiveVehicles(long activeVehicles) {
        this.activeVehicles = activeVehicles;
    }

    public Map<String, Long> getStatusCounts() {
        return statusCounts;
    }

    public void setStatusCounts(Map<String, Long> statusCounts) {
        this.statusCounts = statusCounts;
    }

    public List<VehicleStat> getVehicleStats() {
        return vehicleStats;
    }

    public void setVehicleStats(List<VehicleStat> vehicleStats) {
        this.vehicleStats = vehicleStats;
    }

    public List<DriverStat> getDriverStats() {
        return driverStats;
    }

    public void setDriverStats(List<DriverStat> driverStats) {
        this.driverStats = driverStats;
    }

    public List<DailyStat> getDailyStats() {
        return dailyStats;
    }

    public void setDailyStats(List<DailyStat> dailyStats) {
        this.dailyStats = dailyStats;
    }

    public static class VehicleStat {
        private String vehicle;
        private long trips;
        private double distance;
        private long completed;

        public VehicleStat(String vehicle, long trips, double distance, long completed) {
            this.vehicle = vehicle;
            this.trips = trips;
            this.distance = distance;
            this.completed = completed;
        }

        public String getVehicle() {
            return vehicle;
        }

        public void setVehicle(String vehicle) {
            this.vehicle = vehicle;
        }

        public long getTrips() {
            return trips;
        }

        public void setTrips(long trips) {
            this.trips = trips;
        }

        public double getDistance() {
            return distance;
        }

        public void setDistance(double distance) {
            this.distance = distance;
        }

        public long getCompleted() {
            return completed;
        }

        public void setCompleted(long completed) {
            this.completed = completed;
        }
    }

    public static class DriverStat {
        private String driver;
        private long trips;
        private double distance;
        private long completed;
        private double completionRate;

        public DriverStat(String driver, long trips, double distance, long completed, double completionRate) {
            this.driver = driver;
            this.trips = trips;
            this.distance = distance;
            this.completed = completed;
            this.completionRate = completionRate;
        }

        public String getDriver() {
            return driver;
        }

        public void setDriver(String driver) {
            this.driver = driver;
        }

        public long getTrips() {
            return trips;
        }

        public void setTrips(long trips) {
            this.trips = trips;
        }

        public double getDistance() {
            return distance;
        }

        public void setDistance(double distance) {
            this.distance = distance;
        }

        public long getCompleted() {
            return completed;
        }

        public void setCompleted(long completed) {
            this.completed = completed;
        }

        public double getCompletionRate() {
            return completionRate;
        }

        public void setCompletionRate(double completionRate) {
            this.completionRate = completionRate;
        }
    }

    public static class DailyStat {
        private String date;
        private long trips;
        private double distance;

        public DailyStat(String date, long trips, double distance) {
            this.date = date;
            this.trips = trips;
            this.distance = distance;
        }

        public String getDate() {
            return date;
        }

        public void setDate(String date) {
            this.date = date;
        }

        public long getTrips() {
            return trips;
        }

        public void setTrips(long trips) {
            this.trips = trips;
        }

        public double getDistance() {
            return distance;
        }

        public void setDistance(double distance) {
            this.distance = distance;
        }
    }
}
