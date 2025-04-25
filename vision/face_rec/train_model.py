# save as `train_model.py`
import face_recognition
import os
import pickle

known_encodings = []
known_names = []

photos_dir = "photos"
for person in os.listdir(photos_dir):
    person_dir = os.path.join(photos_dir, person)
    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(person)

data = {"encodings": known_encodings, "names": known_names}
with open("encodings.pickle", "wb") as f:
    pickle.dump(data, f)

print("Training complete.")
