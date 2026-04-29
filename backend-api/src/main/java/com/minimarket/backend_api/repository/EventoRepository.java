package com.minimarket.backend_api.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.minimarket.backend_api.model.Evento;

public interface EventoRepository extends JpaRepository<Evento, Long> {

    List<Evento> findByPersonIdOrderByTimestampAsc(String personId);

}
