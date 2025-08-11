import cv2
import mediapipe as mp
import threading
import sounddevice as sd
import wave
import numpy as np

# Khởi tạo các giải pháp của MediaPipe
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Mở webcam
cap = cv2.VideoCapture(1)

# Đường dẫn tới file âm thanh của bạn (phải là định dạng .wav)
AUDIO_FILE = 'xinchao.wav'

# Biến cờ để kiểm soát việc phát âm thanh
is_playing_audio = False

# Biến cờ để theo dõi trạng thái khuôn mặt trong khung hình
face_detected_in_frame = False

def play_audio():
    """Phát file âm thanh trong một thread riêng."""
    global is_playing_audio
    is_playing_audio = True
    try:
        with wave.open(AUDIO_FILE, 'rb') as wf:
            data = wf.readframes(wf.getnframes())
            audio_data = np.frombuffer(data, dtype=np.int16)
            sd.play(audio_data, wf.getframerate())
            sd.wait()
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file âm thanh tại đường dẫn {AUDIO_FILE}")
    except Exception as e:
        print(f"Lỗi khi phát âm thanh: {e}")
    finally:
        is_playing_audio = False

with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:

    threshold_area = 0.05 

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Không thể đọc khung hình từ webcam.")
            break

        image = cv2.flip(image, 1)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False

        results = face_detection.process(image_rgb)
        
        image.flags.writeable = True

        # Kiểm tra xem có khuôn mặt nào được phát hiện không
        current_face_detected = False
        best_detection = None
        max_score = 0.0

        if results.detections:
            for detection in results.detections:
                bbox_data = detection.location_data.relative_bounding_box
                bbox_area = bbox_data.width * bbox_data.height
                
                if bbox_area > threshold_area:
                    current_face_detected = True
                    center_x = bbox_data.xmin + bbox_data.width / 2
                    center_y = bbox_data.ymin + bbox_data.height / 2
                    
                    frame_center_x = 0.5
                    frame_center_y = 0.5
                    
                    center_distance = ((center_x - frame_center_x)**2 + (center_y - frame_center_y)**2)
                    
                    current_score = bbox_area / (center_distance + 0.001)
                    
                    if current_score > max_score:
                        max_score = current_score
                        best_detection = detection
        
        # Logic để phát âm thanh chỉ một lần
        if current_face_detected and not face_detected_in_frame:
            # Nếu có khuôn mặt xuất hiện và trước đó không có, hãy chào
            if not is_playing_audio:
                audio_thread = threading.Thread(target=play_audio)
                audio_thread.start()
        
        # Cập nhật trạng thái khuôn mặt
        face_detected_in_frame = current_face_detected

        # Vẽ hộp giới hạn cho khuôn mặt tốt nhất
        if best_detection:
            mp_drawing.draw_detection(image, best_detection)

        cv2.imshow('MediaPipe Face Detection', image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()