import cv2
import numpy as np


def draw_detections(frame, detections):
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        conf = det['confidence']
        class_name = det['class']
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        label = f"{class_name}: {conf:.2f}"
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        cv2.rectangle(frame, (x1, y1 - text_size[1] - 10), 
                     (x1 + text_size[0], y1), (0, 255, 0), -1)
        cv2.putText(frame, label, (x1, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    return frame


def draw_tracks(frame, tracked_objects, show_confidence=False):
    for obj in tracked_objects:
        x1, y1, x2, y2 = obj['bbox']
        track_id = obj['track_id']
        class_name = obj['class']
        confidence = obj.get('confidence', 0)
        
        color = get_color_for_id(track_id)
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        if show_confidence:
            label = f"ID:{track_id} {class_name} {confidence:.2f}"
        else:
            label = f"ID:{track_id} {class_name}"
        
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        cv2.rectangle(frame, (x1, y1 - text_size[1] - 10), 
                     (x1 + text_size[0], y1), color, -1)
        cv2.putText(frame, label, (x1, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return frame


def get_color_for_id(track_id):
    track_id_int = int(track_id) if isinstance(track_id, str) else track_id
    np.random.seed(track_id_int)
    color = tuple(map(int, np.random.randint(50, 255, 3)))
    return color


def display_info(frame, fps, num_objects):
    info_text = f"FPS: {fps:.1f} | Objects: {num_objects}"
    cv2.putText(frame, info_text, (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    return frame