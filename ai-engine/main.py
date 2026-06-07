import cv2
import numpy as np
import supervision as sv
import time
import os
from app.core.monitor import MarketMonitor
from app.services.event_service import EventService

def run():
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8082/api/events")
    headless = os.getenv("HEADLESS", "False").lower() == "true"
    video_source = os.getenv("VIDEO_SOURCE", "0")
    test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
    
    # Convert video_source to int if it's a digit (for webcam index)
    if video_source.isdigit():
        video_source = int(video_source)

    # Test mode: send sample events without needing a camera
    if test_mode:
        print("[TEST MODE] Sending sample events to backend...")
        event_service = EventService(backend_url)
        
        test_events = [
            ("person_001", "ENTER"),
            ("person_001", "FRIDGE_INTERACTION"),
            ("person_001", "EXIT"),
        ]
        
        for person_id, action in test_events:
            event_service.send_event(person_id=person_id, action=action)
            time.sleep(2)
        
        print("[TEST MODE] Test events sent successfully!")
        return

    cap = cv2.VideoCapture(video_source) 
    
    if not cap.isOpened():
        print(f"[ERROR] Could not open video source: {video_source}")
        print("[INFO] For Render deployment without camera:")
        print("[INFO] Set environment variable TEST_MODE=true")
        print("[INFO] Or provide VIDEO_SOURCE=/path/to/video.mp4")
        return
    
    monitor = MarketMonitor()
    event_service = EventService(backend_url)

    zonas_monitoradas = {
        # Zonas bem maiores para facilitar o teste (ocupando partes laterais da tela)
        "GELADEIRA_ESQUERDA": np.array([[0, 100], [250, 100], [250, 500], [0, 500]]),
        "GELADEIRA_DIREITA": np.array([[400, 100], [640, 100], [640, 500], [400, 500]])
    }

    for nome, area in zonas_monitoradas.items():
        monitor.add_fridge_zone(area, nome)

    # Controle de frequência de envio (Cooldown)
    last_event_time = 0
    cooldown_seconds = 3

    print(f"--- SISTEMA INICIADO (Headless: {headless}) ---")
    print(f"Conectado ao Backend em: {backend_url}")
    print("Aguardando detecção de pessoas...")

    if not cap.isOpened():
        print(f"ERRO: Não foi possível abrir a fonte de vídeo: {video_source}")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo ou falha na captura.")
            break

        # Processa IA
        annotated_frame, entered, exited, detections = monitor.process_frame(frame)
        current_time = time.time()

        # Lógica de Interação com a Geladeira
        if monitor.check_fridge_interaction(detections):
            if current_time - last_event_time > cooldown_seconds:
                # Tentamos pegar o ID do rastreador, se não houver, enviamos como 'desconhecido'
                p_id = "unknown"
                if detections.tracker_id is not None and len(detections.tracker_id) > 0:
                    p_id = str(detections.tracker_id[0])
                
                print(f"!!! INTERAÇÃO DETECTADA !!! Enviando evento para ID: {p_id}")
                event_service.send_event(person_id=p_id, action="FRIDGE_INTERACTION")
                last_event_time = current_time 

        if any(entered):
            print(">>> Evento: ENTRADA DETECTADA")
            event_service.send_event(person_id="unknown", action="ENTER")
        
        if any(exited):
            print("<<< Evento: SAÍDA DETECTADA")
            event_service.send_event(person_id="unknown", action="EXIT")

        # Exibe o vídeo (Apenas se não for headless)
        if not headless:
            cv2.imshow("Minimercado AI - Monitoramento", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            # Em modo headless, podemos apenas logar que o processamento está ocorrendo
            pass

    cap.release()
    if not headless:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run()


