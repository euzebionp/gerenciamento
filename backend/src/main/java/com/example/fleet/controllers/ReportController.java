package com.example.fleet.controllers;

import com.example.fleet.dtos.DashboardMetrics;
import com.example.fleet.dtos.ReportData;
import com.example.fleet.entities.*;
import com.example.fleet.repositories.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/reports")
public class ReportController {

    @Autowired
    private VehicleRepository vehicleRepository;

    @Autowired
    private DriverRepository driverRepository;

    @Autowired
    private TripRepository tripRepository;

    @GetMapping("/dashboard")
    public ResponseEntity<DashboardMetrics> getDashboardMetrics() {
        long totalVehicles = vehicleRepository.count();
        long activeVehicles = vehicleRepository.findByStatus(VehicleStatus.ATIVO).size();
        long totalDrivers = driverRepository.count();
        long activeTrips = tripRepository.findByStatusIn(Collections.singletonList(TripStatus.EM_ANDAMENTO)).size();

        return ResponseEntity.ok(new DashboardMetrics(totalVehicles, activeVehicles, totalDrivers, activeTrips));
    }

    @GetMapping("/analytics")
    public ResponseEntity<ReportData> getAnalytics(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {

        LocalDateTime start = startDate.atStartOfDay();
        LocalDateTime end = endDate.atTime(23, 59, 59);

        List<Trip> trips = tripRepository.findByStartDateBetween(start, end);

        ReportData reportData = new ReportData();
        reportData.setTotalTrips(trips.size());
        reportData.setCompletedTrips(trips.stream().filter(t -> t.getStatus() == TripStatus.CONCLUIDA).count());
        reportData.setTotalDistance(trips.stream().mapToDouble(Trip::getDistanceKm).sum());
        reportData.setActiveVehicles(vehicleRepository.findByStatus(VehicleStatus.ATIVO).size());

        // Status counts
        Map<String, Long> statusCounts = trips.stream()
                .collect(Collectors.groupingBy(t -> t.getStatus().name(), Collectors.counting()));
        
        for (TripStatus status : TripStatus.values()) {
            statusCounts.putIfAbsent(status.name(), 0L);
        }
        reportData.setStatusCounts(statusCounts);

        // Vehicle statistics
        Map<String, List<Trip>> tripsByVehicle = trips.stream()
                .collect(Collectors.groupingBy(t -> t.getVehicle().getModel() + " (" + t.getVehicle().getPlate() + ")"));
        List<ReportData.VehicleStat> vehicleStats = new ArrayList<>();
        tripsByVehicle.forEach((key, vehicleTrips) -> {
            long total = vehicleTrips.size();
            double distance = vehicleTrips.stream().mapToDouble(Trip::getDistanceKm).sum();
            long completed = vehicleTrips.stream().filter(t -> t.getStatus() == TripStatus.CONCLUIDA).count();
            vehicleStats.add(new ReportData.VehicleStat(key, total, distance, completed));
        });
        reportData.setVehicleStats(vehicleStats);

        // Driver statistics
        Map<String, List<Trip>> tripsByDriver = trips.stream()
                .collect(Collectors.groupingBy(t -> t.getDriver().getName()));
        List<ReportData.DriverStat> driverStats = new ArrayList<>();
        tripsByDriver.forEach((key, driverTrips) -> {
            long total = driverTrips.size();
            double distance = driverTrips.stream().mapToDouble(Trip::getDistanceKm).sum();
            long completed = driverTrips.stream().filter(t -> t.getStatus() == TripStatus.CONCLUIDA).count();
            double completionRate = total > 0 ? Math.round(((double) completed / total) * 1000.0) / 10.0 : 0.0;
            driverStats.add(new ReportData.DriverStat(key, total, distance, completed, completionRate));
        });
        reportData.setDriverStats(driverStats);

        // Daily statistics
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        Map<String, List<Trip>> tripsByDate = trips.stream()
                .collect(Collectors.groupingBy(t -> t.getStartDate().format(formatter)));
        
        List<ReportData.DailyStat> dailyStats = new ArrayList<>();
        tripsByDate.forEach((key, dailyTrips) -> {
            long total = dailyTrips.size();
            double distance = dailyTrips.stream().mapToDouble(Trip::getDistanceKm).sum();
            dailyStats.add(new ReportData.DailyStat(key, total, distance));
        });
        dailyStats.sort(Comparator.comparing(ReportData.DailyStat::getDate));
        reportData.setDailyStats(dailyStats);

        return ResponseEntity.ok(reportData);
    }
}
