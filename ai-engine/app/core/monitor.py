import supervision as sv
from ultralytics import YOLO
import numpy as np

class MarketMonitor:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()
        self.fridge_zones = []
        
        # Definindo a linha (Ex: Horizontal no meio da tela 640x480)
        self.line_start = sv.Point(0, 300)  # Ponto inicial da esquerda
        self.line_end = sv.Point(1280, 300) # Estica até o fim (mesmo se a cam for 640 ou 720)
        self.line_zone = sv.LineZone(start=self.line_start, end=self.line_end)
        
        # Anotadores para visualização
        self.box_annotator = sv.BoxAnnotator()
        self.line_annotator = sv.LineZoneAnnotator()
        self.zone_annotator = sv.PolygonZoneAnnotator()
    
    def add_fridge_zone(self, polygon: np.ndarray):
        # Cria um verificador de zona baseado no polígono enviado
        zone = sv.PolygonZone(polygon=polygon)
        self.fridge_zones.append(zone)

    def check_fridge_interaction(self, detections: sv.Detections):
        for zone in self.fridge_zones:
            # O trigger retorna um array booleano para cada detecção
            is_inside = zone.trigger(detections=detections)
            if any(is_inside):
                return True
        return False     

    def process_frame(self, frame):
        results = self.model(frame, verbose=False)[0] # Adicionamos o [0] aqui para pegar o primeiro resultado
        detections = sv.Detections.from_ultralytics(results)
    
        detections = detections[detections.class_id == 0] # Filtra pessoas
        detections = self.tracker.update_with_detections(detections)

        # DEBUG: Veja se o tracker está funcionando
        if len(detections) > 0:
            print(f"Detectado: {len(detections)} pessoa(s) com IDs: {detections.tracker_id}")

        crossed_in, crossed_out = self.line_zone.trigger(detections)
        
        # Desenha na imagem
        annotated_frame = self.box_annotator.annotate(scene=frame.copy(), detections=detections)
        self.line_annotator.annotate(frame=annotated_frame, line_counter=self.line_zone)

        for zone in self.fridge_zones:
            annotated_frame = self.zone_annotator.annotate(
                scene=annotated_frame, 
                zone=zone
            )
        
        return annotated_frame, crossed_in, crossed_out
