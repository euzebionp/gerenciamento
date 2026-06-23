package com.example.fleet.repositories;

import com.example.fleet.entities.Driver;
import com.example.fleet.entities.DriverStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface DriverRepository extends JpaRepository<Driver, Long> {
    Optional<Driver> findByCpf(String cpf);
    Optional<Driver> findByCnh(String cnh);
    List<Driver> findByStatus(DriverStatus status);
}
