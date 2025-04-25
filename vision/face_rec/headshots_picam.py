import cv2
import os
import time
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Capture headshots using your webcam.")
parser.add_argument('--name', required=True, help='Name of the person being photographed')
parser.add_argument('--num_photos', type=int, default=10, help='Number of photos to capture')
parser.add_argument('--delay', type=int, default=2, help='Delay between each photo in seconds')
args = parser.parse_args()

# Configurable
name = args.name
num_photos = args.num_photos
delay = args.delay
save_path = f"photos/{name}"

# Setup
os.makedirs(save_path, exist_ok=True)
cam = cv2.VideoCapture(0)

print(f"Starting auto-capture for {name}...")
time.sleep(2)  # Allow camera to warm up

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
