package com.minimarket.backend_api.controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import com.minimarket.backend_api.BackendApiApplication;
import com.minimarket.backend_api.repository.EventoRepository;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest(classes = BackendApiApplication.class)
@AutoConfigureMockMvc
public class MonitoramentoControllerTest {

    @Autowired
    private EventoRepository repository;

    @Autowired
    private MockMvc mockMvc;

    long contagemAntes = repository.count();

    @Test
    public void deveRegistrarEventoComSucesso() throws Exception {
        String eventoJson = """
                {
                    "personId": "1",
                    "action": "ENTER",
                    "location": "ENTRADA_PRINCIPAL"
                }
                """;

        mockMvc.perform(post("/api/events")
                .contentType(MediaType.APPLICATION_JSON)
                .content(eventoJson))
                .andExpect(status().isCreated()); // Esperamos 201 Created

        // O teste agora verifica se o banco tem um novo registro
        assertEquals(contagemAntes + 1, repository.count());
    }
}
