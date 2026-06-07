package com.minimarket.backend_api.controller;

import java.time.LocalDateTime;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.minimarket.backend_api.dto.EventoDTO;
import com.minimarket.backend_api.dto.JornadaClienteDTO;
import com.minimarket.backend_api.model.Evento;
import com.minimarket.backend_api.repository.EventoRepository;
import com.minimarket.backend_api.service.AuditoriaService;

import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
@RequestMapping("/api/events")
public class MonitoramentoController {

    private static final Logger logger = LoggerFactory.getLogger(MonitoramentoController.class);

    @Autowired
    private EventoRepository repository;

    @PostMapping
    @Transactional
    public ResponseEntity<Void> registrarEvento(@RequestBody EventoDTO dto) {
        try {
            // 1. Converter o DTO (que vem do Python) para a Entity (que vai pro Banco)
            Evento novoEvento = new Evento();
            novoEvento.setPersonId(dto.personId());
            novoEvento.setAction(dto.action());
            novoEvento.setLocation(dto.location());
            novoEvento.setTimestamp(LocalDateTime.now());

            logger.info(">>> Recebendo evento: person_id={}, action={}, location={}",
                    dto.personId(), dto.action(), dto.location());

            // Salvar no banco de dados
            Evento eventoSalvo = repository.save(novoEvento);
            logger.info(">>> EVENTO PERSISTIDO COM SUCESSO! ID={}", eventoSalvo.getId());

            // 3. Retornar 201 Created para o Python saber que deu certo
            return ResponseEntity.status(HttpStatus.CREATED).build();

        } catch (Exception e) {
            logger.error(">>> ERRO AO SALVAR EVENTO: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @Autowired
    private AuditoriaService auditoriaService;

    @GetMapping("/report/{personId}")
    public ResponseEntity<JornadaClienteDTO> obterRelatorio(@PathVariable String personId) {
        JornadaClienteDTO relatorio = auditoriaService.gerarRelatorioCliente(personId);
        if (relatorio == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(relatorio);
    }

}
