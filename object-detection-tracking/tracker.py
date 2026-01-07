from deep_sort_realtime.deepsort_tracker import DeepSort


class ObjectTracker:
    def __init__(self, max_age=30):
        self.tracker = DeepSort(
            max_age=max_age,
            n_init=3,
            nms_max_overlap=1.0,
            max_cosine_distance=0.3,
            nn_budget=None,
            embedder="mobilenet",
            half=False,
            bgr=True,
            embedder_gpu=False
        )

    def update_tracks(self, detections, frame):
        raw_detections = []
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            confidence = det['confidence']
            class_id = det['class_id']
            
            raw_detections.append(([x1, y1, x2-x1, y2-y1], confidence, class_id))
        
        tracks = self.tracker.update_tracks(raw_detections, frame=frame)
        
        return tracks

    def get_tracked_objects(self, tracks, class_names, detections):
        tracked_objects = []
        
        for track in tracks:
            if not track.is_confirmed():
                continue
            
            track_id = track.track_id
            ltrb = track.to_ltrb()
            class_id = track.get_det_class()
            
            confidence = 0
            for det in detections:
                if det['class_id'] == class_id:
                    confidence = det['confidence']
                    break
            
            tracked_objects.append({
                'track_id': track_id,
                'bbox': [int(ltrb[0]), int(ltrb[1]), int(ltrb[2]), int(ltrb[3])],
                'class': class_names[class_id] if class_id is not None else "Unknown",
                'class_id': class_id,
                'confidence': confidence
            })
        
        return tracked_objects