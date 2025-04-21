import cv2
import face_recognition
import pickle
import os

# Load known encodings once at module load
ENCODINGS_PATH = os.path.join(os.path.dirname(__file__), "encodings.pickle")
with open(ENCODINGS_PATH, "rb") as f:
    data = pickle.load(f)

def recognize_faces_in_frame(frame):
    """
    Detect and label known faces in a frame.

    Args:
        frame (np.array): BGR image from OpenCV camera capture.

    Returns:
        annotated_frame (np.array): Frame with rectangles and names drawn.
        names (list): List of recognized names.
    """
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []

    for (box, encoding) in zip(boxes, encodings):
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                counts[data["names"][i]] = counts.get(data["names"][i], 0) + 1
            name = max(counts, key=counts.get)

        names.append(name)

        top, right, bottom, left = box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame, names

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        annotated_frame, names = recognize_faces_in_frame(frame)

        cv2.imshow("Frame", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
