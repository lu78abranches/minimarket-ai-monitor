package com.minimarket.backend_api.controller;

import java.time.LocalDateTime;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.minimarket.backend_api.dto.EventoDTO;
import com.minimarket.backend_api.model.Evento;
import com.minimarket.backend_api.repository.EventoRepository;

import jakarta.transaction.Transactional;

@RestController
@RequestMapping("/api/events")
public class MonitoramentoController {

    // Injetando a interface que fala com o MySQL
    @Autowired
    private EventoRepository repository;

    @PostMapping
    @Transactional
    public ResponseEntity<Void> registrarEvento(@RequestBody EventoDTO dto) {

        // 1. Converter o DTO (que vem do Python) para a Entity (que vai pro Banco)
        Evento novoEvento = new Evento();
        novoEvento.setPersonId(dto.personId());
        novoEvento.setAction(dto.action());
        novoEvento.setLocation(dto.location());
        novoEvento.setTimestamp(LocalDateTime.now());

        System.out.println(">>> Tentando salvar no MySQL...");
        repository.save(novoEvento);
        System.out.println(">>> Salvo com sucesso!");

        // 3. Retornar 201 Created para o Python saber que deu certo
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }
}
