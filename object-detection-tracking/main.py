import cv2
import time
import argparse
from detector import ObjectDetector
from tracker import ObjectTracker
from utils import draw_tracks, display_info


def main():
    parser = argparse.ArgumentParser(description='Real-Time Object Detection and Tracking')
    parser.add_argument('--source', type=str, default='0', 
                       help='Video source: 0 for webcam, or path to video file')
    parser.add_argument('--output', type=str, default=None, 
                       help='Path to save output video')
    parser.add_argument('--conf', type=float, default=0.5, 
                       help='Confidence threshold for detection')
    parser.add_argument('--model', type=str, default='yolov8n.pt', 
                       help='YOLOv8 model path')
    parser.add_argument('--show-conf', action='store_true',
                       help='Show confidence scores on labels')
    parser.add_argument('--classes', type=str, default=None,
                       help='Filter by class names (comma-separated), e.g., "person,car,dog"')
    
    args = parser.parse_args()
    
    detector = ObjectDetector(model_path=args.model, conf_threshold=args.conf)
    tracker = ObjectTracker(max_age=30)
    
    class_filter = None
    if args.classes:
        class_filter = [c.strip().lower() for c in args.classes.split(',')]
    
    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)
    
    if not cap.isOpened():
        print(f"Error: Cannot open video source {args.source}")
        return
    
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    writer = None
    if args.output:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(args.output, fourcc, fps, (width, height))
    
    print("Starting detection and tracking...")
    print("Press 'q' to quit")
    
    prev_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        detections = detector.detect(frame)
        
        if class_filter:
            detections = [d for d in detections if d['class'].lower() in class_filter]
        
        tracks = tracker.update_tracks(detections, frame)
        tracked_objects = tracker.get_tracked_objects(tracks, detector.class_names, detections)
        
        frame = draw_tracks(frame, tracked_objects, args.show_conf)
        
        curr_time = time.time()
        fps_display = 1 / (curr_time - prev_time)
        prev_time = curr_time
        
        frame = display_info(frame, fps_display, len(tracked_objects))
        
        cv2.imshow('Object Detection and Tracking', frame)
        
        if writer:
            writer.write(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()
    
    print("Processing completed!")


if __name__ == '__main__':
    main()