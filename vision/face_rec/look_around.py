import argparse
import cv2
import time
from hackerbot import Hackerbot
from facial_req import recognize_faces_in_frame


def look_around_with_camera(
    bot,
    target_name,
    speed=15,
    pan_range=(100.0, 260.0),
    tilt_range=(200.0, 250.0),
    pan_step=10.0,
    tilt_step=10.0,
    camera_index=0,
    delay=0.3
):
    """
    Performs a serpentine head scan using the Hackerbot camera
    to find the target_name via facial recognition.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("[ERROR] Cannot access camera.")
        return

    pan_positions = list(range(int(pan_range[0]), int(pan_range[1]) + 1, int(pan_step)))
    tilt_positions = list(range(int(tilt_range[0]), int(tilt_range[1]) + 1, int(tilt_step)))

    try:
        bot.base.start()
        while True:
            for i, tilt in enumerate(tilt_positions):
                pan_sweep = pan_positions if i % 2 == 0 else pan_positions[::-1]

                for pan in pan_sweep:
                    print(f"[SCAN] Pan: {pan}, Tilt: {tilt}")
                    bot.head.look(float(pan), float(tilt), speed)
                    time.sleep(delay)

                    ret, frame = cap.read()
                    if not ret:
                        print("[WARN] Failed to grab frame.")
                        continue

                    _, recognized_names = recognize_faces_in_frame(frame)
                    print("[INFO] Detected:", recognized_names)

                    if target_name in recognized_names:
                        print(f"✅ Found: {target_name} at Pan {pan}, Tilt {tilt}")
                        bot.head.look(float(pan), float(tilt), 60)
                        time.sleep(1.0)
                        return

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("[EXIT] User terminated scan.")
                        return

            print("[ACTION] Rotating for a new scan pass...")
            bot.base.drive(0, 65)
            tilt_positions.reverse()

    except KeyboardInterrupt:
        print("\n[INTERRUPT] Scan aborted.")
    finally:
        cap.release()


def main():
    parser = argparse.ArgumentParser(description="Hackerbot Facial Recognition Scanner")
    parser.add_argument('--name', required=True, help="Name to detect and confirm")
    args = parser.parse_args()

    bot = Hackerbot()
    look_around_with_camera(bot, target_name=args.name)
    bot.base.destroy()


if __name__ == "__main__":
    main()
