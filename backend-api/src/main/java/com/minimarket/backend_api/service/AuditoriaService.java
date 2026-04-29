package com.minimarket.backend_api.service;

import com.minimarket.backend_api.dto.JornadaClienteDTO;
import com.minimarket.backend_api.model.Evento;
import com.minimarket.backend_api.repository.EventoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class AuditoriaService {

    @Autowired
    private EventoRepository repository;

    public JornadaClienteDTO gerarRelatorioCliente(String personId) {
        List<Evento> eventos = repository.findByPersonIdOrderByTimestampAsc(personId);

        if (eventos.isEmpty())
            return null;

        // Calcula tempo na loja
        String permanencia = calcularTempo(eventos);

        // Mapeia locais acessados
        List<String> locais = eventos.stream()
                .map(Evento::getLocation)
                .distinct()
                .collect(Collectors.toList());

        // Regra do coração: pegou algo e não pagou?
        String status = determinarStatus(eventos);

        return new JornadaClienteDTO(personId, permanencia, locais, status);
    }

    private String calcularTempo(List<Evento> eventos) {
        var primeiro = eventos.get(0).getTimestamp();
        var ultimo = eventos.get(eventos.size() - 1).getTimestamp();
        Duration duracao = Duration.between(primeiro, ultimo);
        return duracao.toMinutes() + " min e " + (duracao.toSeconds() % 60) + " seg";
    }

    private String determinarStatus(List<Evento> eventos) {
        boolean interagiu = eventos.stream().anyMatch(e -> e.getAction().contains("INTERACTION"));
        boolean saiu = eventos.stream().anyMatch(e -> e.getAction().equals("EXIT"));

        if (interagiu && saiu)
            return "SUSPEITO: Interagiu e saiu";
        return "OK ou Em andamento";
    }
}
