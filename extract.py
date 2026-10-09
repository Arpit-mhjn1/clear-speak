import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import json
import os
import glob
import numpy as np
import concurrent.futures

TARGET_FRAMES = 15

def extract_landmarks(video_path):
    # Initialize detector inside the worker to avoid thread issues
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
    detector = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(video_path)
    frames_landmarks = []
    
    frame_idx = 0
    while cap.isOpened() and frame_idx < 45:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Speed Optimization: Run AI on 1 out of every 3 frames
        if frame_idx % 3 == 0:
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            
            detection_result = detector.detect(mp_image)
            
            if detection_result.hand_landmarks:
                hand_landmarks = detection_result.hand_landmarks[0]
                wrist = hand_landmarks[0]
                lm_list = [
                    {
                        "x": lm.x - wrist.x, 
                        "y": lm.y - wrist.y, 
                        "z": lm.z - wrist.z
                    } for lm in hand_landmarks
                ]
                frames_landmarks.append(lm_list)
                
        frame_idx += 1
            
    cap.release()
    
    if len(frames_landmarks) == 0:
        return None
        
    indices = np.linspace(0, len(frames_landmarks) - 1, TARGET_FRAMES, dtype=int)
    sampled_landmarks = [frames_landmarks[i] for i in indices]
    
    return sampled_landmarks

def process_video(vp):
    word = os.path.splitext(os.path.basename(vp))[0]
    landmarks = extract_landmarks(vp)
    return word, landmarks

def main():
    base_dir = "Dictionary"
    dictionary_data = {}
    
    video_files = glob.glob(os.path.join(base_dir, "**", "*.mp4"), recursive=True)
    
    dict_file = "isl_dictionary.json"
    if os.path.exists(dict_file):
        with open(dict_file, "r") as f:
            dictionary_data = json.load(f)
            
    # Filter videos that are already processed
    videos_to_process = [vp for vp in video_files if os.path.splitext(os.path.basename(vp))[0] not in dictionary_data]
    print(f"Resuming... {len(video_files) - len(videos_to_process)} already processed. {len(videos_to_process)} left to process.")

    completed = 0
    # Use ThreadPoolExecutor to process 4 videos concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_video, vp): vp for vp in videos_to_process}
        
        for future in concurrent.futures.as_completed(futures):
            word, landmarks = future.result()
            completed += 1
            
            if landmarks:
                dictionary_data[word] = landmarks
                print(f"[{completed}/{len(videos_to_process)}] {word}: Success")
            else:
                print(f"[{completed}/{len(videos_to_process)}] {word}: Failed (No hand)")
                
            # Checkpoint every 20 videos
            if completed % 20 == 0:
                with open(dict_file, "w") as f:
                    json.dump(dictionary_data, f)
                    
    with open(dict_file, "w") as f:
        json.dump(dictionary_data, f)
    print("Finished! Total signs:", len(dictionary_data))

if __name__ == "__main__":
    main()
