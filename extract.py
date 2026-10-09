import cv2
import mediapipe as mp
import json
import os
import glob
import numpy as np

# Set up MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

TARGET_FRAMES = 15 # Normalize all signs to 15 frames

def extract_landmarks(video_path):
    cap = cv2.VideoCapture(video_path)
    frames_landmarks = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert BGR to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        
        if results.multi_hand_landmarks:
            # We just take the first hand detected
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Normalize to make it translation-invariant (relative to wrist)
            wrist = hand_landmarks.landmark[0]
            lm_list = [
                {
                    "x": lm.x - wrist.x, 
                    "y": lm.y - wrist.y, 
                    "z": lm.z - wrist.z
                } for lm in hand_landmarks.landmark
            ]
            frames_landmarks.append(lm_list)
            
    cap.release()
    
    if len(frames_landmarks) == 0:
        return None
        
    # Sample to TARGET_FRAMES
    indices = np.linspace(0, len(frames_landmarks) - 1, TARGET_FRAMES, dtype=int)
    sampled_landmarks = [frames_landmarks[i] for i in indices]
    
    return sampled_landmarks

def main():
    base_dir = "Dictionary"
    dictionary_data = {}
    
    # Process a few videos from A and B folders
    video_files = glob.glob(os.path.join(base_dir, "**", "*.mp4"), recursive=True)
    
    # Take 10 videos max for our hackathon MVP to test the pipeline (e.g., Boy, Burger, etc.)
    test_videos = video_files[:5] + video_files[-5:] if len(video_files) > 10 else video_files
    
    print(f"Found {len(video_files)} videos. Processing {len(test_videos)} for the MVP...")
    
    for vp in test_videos:
        word = os.path.splitext(os.path.basename(vp))[0]
        print(f"Processing: {word}")
        landmarks = extract_landmarks(vp)
        if landmarks:
            dictionary_data[word] = landmarks
            print(f" -> Success! Extracted {len(landmarks)} frames.")
        else:
            print(f" -> Failed. No hand detected.")
            
    with open("isl_dictionary.json", "w") as f:
        json.dump(dictionary_data, f)
    print("Saved isl_dictionary.json!")

if __name__ == "__main__":
    main()
