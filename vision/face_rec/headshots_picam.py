import cv2
import os
import time

# Configurable
name = "Your_Name"               # Set your name here
save_path = f"photos/{name}" # Folder to store photos
num_photos = 10              # Number of photos to take
delay = 2                    # Delay between shots in seconds

# Setup
os.makedirs(save_path, exist_ok=True)
cam = cv2.VideoCapture(0)

print(f"Starting auto-capture for {name}...")
time.sleep(2)  # Optional: allow camera to warm up

for i in range(num_photos):
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    filename = f"{save_path}/{i}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[{i+1}/{num_photos}] Saved {filename}")
    time.sleep(delay)

cam.release()
cv2.destroyAllWindows()
print("Done.")
