# Real-Time Object Detection and Tracking

A professional object detection and tracking system built with YOLOv8 and Deep SORT for the CodeAlpha Internship project.

## Features

- Real-time object detection using YOLOv8
- Multi-object tracking with Deep SORT
- Unique tracking IDs for each object
- Support for webcam and video file input
- Configurable confidence threshold
- Video output recording capability
- FPS and object count display

## Project Structure

```
object-detection-tracking/
├── main.py                 # Main execution script
├── detector.py             # Object detection module
├── tracker.py              # Object tracking module
├── utils.py                # Visualization utilities
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── models/                # Model weights directory
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SyedUzema/object-detection-tracking.git
cd object-detection-tracking
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Using Webcam
```bash
python main.py --source 0
```

### Using Video File
```bash
python main.py --source path/to/video.mp4
```

### Save Output Video
```bash
python main.py --source 0 --output output/result.mp4
```

### Custom Configuration
```bash
# Higher confidence threshold (reduces false positives)
python main.py --source 0 --conf 0.65

# Show confidence scores
python main.py --source 0 --show-conf

# Track only specific classes
python main.py --source 0 --classes "person,car,dog"

# Combine options
python main.py --source 0 --conf 0.6 --show-conf --classes "person"
```

## Command Line Arguments

- `--source`: Video source (0 for webcam, or path to video file)
- `--output`: Path to save output video (optional)
- `--conf`: Confidence threshold for detection (default: 0.5, range: 0.0-1.0)
- `--model`: YOLOv8 model path (default: yolov8n.pt)
- `--show-conf`: Display confidence scores on labels (optional flag)
- `--classes`: Filter specific classes, comma-separated (optional, e.g., "person,car")

## Available YOLOv8 Models

- `yolov8n.pt` - Nano (fastest, less accurate)
- `yolov8s.pt` - Small
- `yolov8m.pt` - Medium
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (most accurate, slower)

## Technical Details

### Object Detection
- **Model**: YOLOv8 (You Only Look Once v8)
- **Framework**: Ultralytics
- **Features**: 80 COCO classes detection

### Object Tracking
- **Algorithm**: Deep SORT (Simple Online and Realtime Tracking with Deep Association Metric)
- **Features**: Consistent ID assignment, occlusion handling

## Requirements

- Python 3.8+
- OpenCV
- Ultralytics YOLOv8
- Deep SORT Realtime
- NumPy

## Controls

- Press `q` to quit the application

## Performance Tips

1. **Reduce Misclassifications**: Increase confidence threshold to 0.6-0.7
   ```bash
   python main.py --source 0 --conf 0.65
   ```

2. **Track Specific Objects**: Use class filtering to focus on relevant objects
   ```bash
   python main.py --source 0 --classes "person,car"
   ```

3. **Better Accuracy**: Use larger models (yolov8s or yolov8m) for improved detection
   ```bash
   python main.py --source 0 --model yolov8s.pt
   ```

4. **Faster Processing**: Stick with yolov8n for real-time performance on CPU

5. **Debug Detections**: Enable confidence display to understand model behavior
   ```bash
   python main.py --source 0 --show-conf
   ```

## Troubleshooting

### Webcam not opening
- Check if another application is using the webcam
- Try different source indices (0, 1, 2)

### Low FPS
- Use a lighter model (yolov8n instead of yolov8x)
- Reduce input video resolution
- Close other applications

### Model download issues
- Ensure stable internet connection
- Models are downloaded automatically on first run

## License

This project is created for educational purposes as part of the CodeAlpha Internship.

## Author

Syed Uzema Sadiq

## Acknowledgments

- Ultralytics for YOLOv8
- Deep SORT Realtime implementation
- CodeAlpha for the internship opportunity