package com.example.fleet.controllers;

import com.example.fleet.entities.Vehicle;
import com.example.fleet.repositories.VehicleRepository;
import com.example.fleet.repositories.TripRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/vehicles")
public class VehicleController {

    @Autowired
    private VehicleRepository vehicleRepository;

    @Autowired
    private TripRepository tripRepository;

    @GetMapping
    public List<Vehicle> getAllVehicles() {
        return vehicleRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Vehicle> getVehicleById(@PathVariable Long id) {
        return vehicleRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<?> createVehicle(@RequestBody Vehicle vehicle) {
        if (vehicleRepository.findByPlate(vehicle.getPlate()).isPresent()) {
            return ResponseEntity.badRequest().body("Erro: Placa já cadastrada.");
        }
        Vehicle savedVehicle = vehicleRepository.save(vehicle);
        return ResponseEntity.ok(savedVehicle);
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateVehicle(@PathVariable Long id, @RequestBody Vehicle vehicleDetails) {
        Optional<Vehicle> optionalVehicle = vehicleRepository.findById(id);
        if (optionalVehicle.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        Vehicle vehicle = optionalVehicle.get();
        
        // If plate changed, verify uniqueness
        if (!vehicle.getPlate().equals(vehicleDetails.getPlate())) {
            if (vehicleRepository.findByPlate(vehicleDetails.getPlate()).isPresent()) {
                return ResponseEntity.badRequest().body("Esta placa já está cadastrada em outro veículo!");
            }
            vehicle.setPlate(vehicleDetails.getPlate());
        }

        vehicle.setModel(vehicleDetails.getModel());
        vehicle.setCapacity(vehicleDetails.getCapacity());
        vehicle.setType(vehicleDetails.getType());
        vehicle.setStatus(vehicleDetails.getStatus());

        Vehicle updatedVehicle = vehicleRepository.save(vehicle);
        return ResponseEntity.ok(updatedVehicle);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteVehicle(@PathVariable Long id) {
        Optional<Vehicle> optionalVehicle = vehicleRepository.findById(id);
        if (optionalVehicle.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        long tripsCount = tripRepository.countByVehicleId(id);
        if (tripsCount > 0) {
            return ResponseEntity.badRequest().body("Este veículo possui " + tripsCount + " viagem(ns) registrada(s). Não é possível excluir.");
        }

        vehicleRepository.delete(optionalVehicle.get());
        return ResponseEntity.ok().body("Veículo excluído com sucesso!");
    }
}
