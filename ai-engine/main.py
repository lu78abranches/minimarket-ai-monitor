import cv2
import numpy as np
import supervision as sv
import time  # <--- NOVO IMPORT
from app.core.monitor import MarketMonitor
from app.services.event_service import EventService

def run():
    cap = cv2.VideoCapture(0) 
    monitor = MarketMonitor()
    event_service = EventService("http://localhost:8082/api/events")

    zonas_monitoradas = {
    "GELADEIRA_01": np.array([...]), # Geladeira 1
    "GELADEIRA_02": np.array([...]), # Geladeira 2
    "GELADEIRA_03": np.array([...]), # Geladeira 3
    "GELADEIRA_04": np.array([...]), # Geladeira 4
    "MOVEL_PRINCIPAL_2M": np.array([...]), # O gigante de 2m x 1.80m
    "MOVEL_SECUNDARIO_A": np.array([...]), # O de 1.5m x 1.0m
    "MOVEL_SECUNDARIO_B": np.array([...])  # O outro de 1.5m x 1.0m
}

for nome, area in zonas_monitoradas.items():
    monitor.add_fridge_zone(area, nome)

    # Controle de frequência de envio (Cooldown)
    last_event_time = 0
    cooldown_seconds = 5  # Envia no máximo 1 evento a cada 5 segundos por tipo

    fridge_area = np.array([
        [100, 100], [500, 100], [500, 400], [100, 400]
    ])
    monitor.add_fridge_zone(fridge_area)

    print("--- SISTEMA INICIADO ---")
    print("Aguardando detecção de pessoas...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Processa IA
        annotated_frame, entered, exited, detections = monitor.process_frame(frame)
        current_time = time.time()

        # Lógica de Interação com a Geladeira
        if monitor.check_fridge_interaction(detections):
            # Só tenta enviar se respeitar o tempo de cooldown
            if current_time - last_event_time > cooldown_seconds:
                if detections.tracker_id is not None and len(detections.tracker_id) > 0:
                    p_id = str(detections.tracker_id[0])
                    print(f"!!! GATILHO ACIONADO !!! Enviando ID: {p_id}")
                    
                    # Envia ao Spring
                    event_service.send_event(person_id=p_id, action="FRIDGE_INTERACTION")
                    
                    # Atualiza o cronômetro do último envio
                    last_event_time = current_time 
                else:
                    print("Pessoa na zona, aguardando estabilização do ID...")

        # Lógica de Entrada (Linha Virtual) - Também com cooldown simples
        if any(entered):
            print(">>> Evento: ENTRADA DETECTADA")
            event_service.send_event(person_id="unknown", action="ENTER")
        
        # Lógica de Saída (Linha Virtual)
        if any(exited):
            print("<<< Evento: SAÍDA DETECTADA")
            event_service.send_event(person_id="unknown", action="EXIT")

        # Exibe o vídeo
        cv2.imshow("Minimercado AI - Monitoramento", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()


