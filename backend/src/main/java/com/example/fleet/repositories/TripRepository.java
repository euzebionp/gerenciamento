package com.example.fleet.repositories;

import com.example.fleet.entities.Trip;
import com.example.fleet.entities.TripStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface TripRepository extends JpaRepository<Trip, Long> {
    
    List<Trip> findByStatusIn(List<TripStatus> statuses);
    
    List<Trip> findByStatusInAndStartDateGreaterThanEqualOrderByStartDateDesc(List<TripStatus> statuses, LocalDateTime startDate);
    
    List<Trip> findByStartDateGreaterThanEqualOrderByStartDateDesc(LocalDateTime startDate);
    
    List<Trip> findAllByOrderByStartDateDesc();
    
    List<Trip> findByStartDateBetween(LocalDateTime start, LocalDateTime end);
    
    long countByVehicleId(Long vehicleId);
    
    long countByDriverId(Long driverId);
}
