package com.example.fleet.controllers;

import com.example.fleet.dtos.TripRequest;
import com.example.fleet.entities.Driver;
import com.example.fleet.entities.DriverStatus;
import com.example.fleet.entities.Trip;
import com.example.fleet.entities.TripStatus;
import com.example.fleet.entities.Vehicle;
import com.example.fleet.entities.VehicleStatus;
import com.example.fleet.repositories.DriverRepository;
import com.example.fleet.repositories.TripRepository;
import com.example.fleet.repositories.VehicleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/trips")
public class TripController {

    @Autowired
    private TripRepository tripRepository;

    @Autowired
    private DriverRepository driverRepository;

    @Autowired
    private VehicleRepository vehicleRepository;

    @GetMapping
    public List<Trip> getTrips(
            @RequestParam(required = false) List<String> status,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate) {

        List<TripStatus> tripStatuses = null;
        if (status != null && !status.isEmpty()) {
            tripStatuses = status.stream()
                    .map(TripStatus::valueOf)
                    .collect(Collectors.toList());
        }

        LocalDateTime startDateTime = null;
        if (startDate != null) {
            startDateTime = startDate.atStartOfDay();
        }

        if (tripStatuses != null && startDateTime != null) {
            return tripRepository.findByStatusInAndStartDateGreaterThanEqualOrderByStartDateDesc(tripStatuses, startDateTime);
        } else if (tripStatuses != null) {
            return tripRepository.findByStatusIn(tripStatuses);
        } else if (startDateTime != null) {
            return tripRepository.findByStartDateGreaterThanEqualOrderByStartDateDesc(startDateTime);
        } else {
            return tripRepository.findAllByOrderByStartDateDesc();
        }
    }

    @GetMapping("/{id}")
    public ResponseEntity<Trip> getTripById(@PathVariable Long id) {
        return tripRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<?> createTrip(@RequestBody TripRequest tripRequest) {
        if (tripRequest.getOrigin() == null || tripRequest.getOrigin().trim().isEmpty() ||
            tripRequest.getDestination() == null || tripRequest.getDestination().trim().isEmpty()) {
            return ResponseEntity.badRequest().body("Preencha origem e destino!");
        }

        if (tripRequest.getDistanceKm() == null || tripRequest.getDistanceKm() <= 0) {
            return ResponseEntity.badRequest().body("A distância deve ser maior que zero!");
        }

        Optional<Vehicle> optionalVehicle = vehicleRepository.findById(tripRequest.getVehicleId());
        if (optionalVehicle.isEmpty()) {
            return ResponseEntity.badRequest().body("Veículo não encontrado!");
        }

        Optional<Driver> optionalDriver = driverRepository.findById(tripRequest.getDriverId());
        if (optionalDriver.isEmpty()) {
            return ResponseEntity.badRequest().body("Motorista não encontrado!");
        }

        Vehicle vehicle = optionalVehicle.get();
        Driver driver = optionalDriver.get();

        if (vehicle.getStatus() != VehicleStatus.ATIVO) {
            return ResponseEntity.badRequest().body("Veículo selecionado não está ativo!");
        }
        if (driver.getStatus() != DriverStatus.ATIVO) {
            return ResponseEntity.badRequest().body("Motorista selecionado não está ativo!");
        }

        Trip trip = new Trip();
        trip.setOrigin(tripRequest.getOrigin());
        trip.setDestination(tripRequest.getDestination());
        trip.setDistanceKm(tripRequest.getDistanceKm());
        trip.setVehicle(vehicle);
        trip.setDriver(driver);
        trip.setStartDate(tripRequest.getStartDate() != null ? tripRequest.getStartDate() : LocalDateTime.now());
        trip.setStatus(tripRequest.getStatus() != null ? tripRequest.getStatus() : TripStatus.PLANEJADA);

        Trip savedTrip = tripRepository.save(trip);
        return ResponseEntity.ok(savedTrip);
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateTrip(@PathVariable Long id, @RequestBody Trip tripDetails) {
        Optional<Trip> optionalTrip = tripRepository.findById(id);
        if (optionalTrip.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        Trip trip = optionalTrip.get();
        
        if (tripDetails.getStatus() == TripStatus.CONCLUIDA && trip.getStatus() != TripStatus.CONCLUIDA && trip.getEndDate() == null) {
            trip.setEndDate(LocalDateTime.now());
        } else if (tripDetails.getStatus() != TripStatus.CONCLUIDA) {
            trip.setEndDate(null);
        }

        trip.setStatus(tripDetails.getStatus());
        if (tripDetails.getOrigin() != null) trip.setOrigin(tripDetails.getOrigin());
        if (tripDetails.getDestination() != null) trip.setDestination(tripDetails.getDestination());
        if (tripDetails.getDistanceKm() != null) trip.setDistanceKm(tripDetails.getDistanceKm());

        Trip updatedTrip = tripRepository.save(trip);
        return ResponseEntity.ok(updatedTrip);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteTrip(@PathVariable Long id) {
        return tripRepository.findById(id)
                .map(trip -> {
                    tripRepository.delete(trip);
                    return ResponseEntity.ok().body("Viagem excluída com sucesso!");
                })
                .orElse(ResponseEntity.notFound().build());
    }
}
