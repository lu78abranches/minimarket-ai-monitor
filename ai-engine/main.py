import cv2
from app.core.monitor import MarketMonitor
from app.services.event_service import EventService

def run():
    cap = cv2.VideoCapture(0) # 0 para Webcam
    monitor = MarketMonitor()
    event_service = EventService()

    # 1. Definindo uma zona de geladeira (Ex: um quadrado no canto superior esquerdo)
# Coordenadas [x, y]
fridge_area = np.array([
    [10, 10], [200, 10], [200, 200], [10, 200]
])
monitor.add_fridge_zone(fridge_area)

    print("Sistema de Monitoramento Iniciado... Pressione 'q' para sair.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Processa IA
        annotated_frame, entered, exited = monitor.process_frame(frame)

        if monitor.check_fridge_interaction(detections): # Note: você precisará passar 'detections' aqui
            print("ALERTA: Alguém interagindo com a geladeira!")
            # event_service.send_event(person_id=p_id, action="FRIDGE_INTERACTION")

        # Verifica eventos de entrada/saída
        if any(entered):
            event_service.send_event(person_id="unknown", action="ENTER")
        
        if any(exited):
            event_service.send_event(person_id="unknown", action="EXIT")

        # Exibe o vídeo
        cv2.imshow("Minimercado AI", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
