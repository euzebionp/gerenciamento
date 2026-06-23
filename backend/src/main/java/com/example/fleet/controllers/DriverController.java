package com.example.fleet.controllers;

import com.example.fleet.entities.Driver;
import com.example.fleet.repositories.DriverRepository;
import com.example.fleet.repositories.TripRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/drivers")
public class DriverController {

    @Autowired
    private DriverRepository driverRepository;

    @Autowired
    private TripRepository tripRepository;

    @GetMapping
    public List<Driver> getAllDrivers() {
        return driverRepository.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Driver> getDriverById(@PathVariable Long id) {
        return driverRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<?> createDriver(@RequestBody Driver driver) {
        if (driver.getCpf() == null || driver.getCpf().length() != 11 || !driver.getCpf().matches("\\d+")) {
            return ResponseEntity.badRequest().body("CPF deve conter exatamente 11 dígitos numéricos!");
        }
        if (driver.getCnh() == null || driver.getCnh().length() < 9 || !driver.getCnh().matches("\\d+")) {
            return ResponseEntity.badRequest().body("CNH deve conter pelo menos 9 dígitos numéricos!");
        }

        if (driverRepository.findByCpf(driver.getCpf()).isPresent() || driverRepository.findByCnh(driver.getCnh()).isPresent()) {
            return ResponseEntity.badRequest().body("Erro: CPF ou CNH já cadastrados.");
        }

        Driver savedDriver = driverRepository.save(driver);
        return ResponseEntity.ok(savedDriver);
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateDriver(@PathVariable Long id, @RequestBody Driver driverDetails) {
        Optional<Driver> optionalDriver = driverRepository.findById(id);
        if (optionalDriver.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        Driver driver = optionalDriver.get();

        if (driverDetails.getCpf() == null || driverDetails.getCpf().length() != 11 || !driverDetails.getCpf().matches("\\d+")) {
            return ResponseEntity.badRequest().body("CPF deve conter exatamente 11 dígitos numéricos!");
        }
        if (driverDetails.getCnh() == null || driverDetails.getCnh().length() < 9 || !driverDetails.getCnh().matches("\\d+")) {
            return ResponseEntity.badRequest().body("CNH deve conter pelo menos 9 dígitos numéricos!");
        }

        if (!driver.getCpf().equals(driverDetails.getCpf())) {
            if (driverRepository.findByCpf(driverDetails.getCpf()).isPresent()) {
                return ResponseEntity.badRequest().body("Este CPF já está cadastrado em outro motorista!");
            }
            driver.setCpf(driverDetails.getCpf());
        }

        if (!driver.getCnh().equals(driverDetails.getCnh())) {
            if (driverRepository.findByCnh(driverDetails.getCnh()).isPresent()) {
                return ResponseEntity.badRequest().body("Esta CNH já está cadastrada em outro motorista!");
            }
            driver.setCnh(driverDetails.getCnh());
        }

        driver.setName(driverDetails.getName());
        driver.setPhone(driverDetails.getPhone());
        driver.setStatus(driverDetails.getStatus());
        driver.setCnhExpiry(driverDetails.getCnhExpiry());

        Driver updatedDriver = driverRepository.save(driver);
        return ResponseEntity.ok(updatedDriver);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteDriver(@PathVariable Long id) {
        Optional<Driver> optionalDriver = driverRepository.findById(id);
        if (optionalDriver.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        long tripsCount = tripRepository.countByDriverId(id);
        if (tripsCount > 0) {
            return ResponseEntity.badRequest().body("Este motorista possui " + tripsCount + " viagem(ns) registrada(s). Não é possível excluir.");
        }

        driverRepository.delete(optionalDriver.get());
        return ResponseEntity.ok().body("Motorista excluído com sucesso!");
    }
}
