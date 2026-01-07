from ultralytics import YOLO
import cv2
import numpy as np


class ObjectDetector:
    def __init__(self, model_path='yolov8n.pt', conf_threshold=0.5):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.class_names = self.model.names

    def detect(self, frame):
        results = self.model(frame, conf=self.conf_threshold, verbose=False)[0]
        
        detections = []
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            class_name = self.class_names[cls]
            
            detections.append({
                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                'confidence': conf,
                'class': class_name,
                'class_id': cls
            })
        
        return detections

    def get_detection_for_tracking(self, detections):
        bboxes = []
        confidences = []
        class_ids = []
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            w = x2 - x1
            h = y2 - y1
            bboxes.append([x1, y1, w, h])
            confidences.append(det['confidence'])
            class_ids.append(det['class_id'])
        
        return bboxes, confidences, class_ids