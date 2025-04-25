
import threading
import cv2 
import os
from deepface import DeepFace

reference_folder = "refs"

reference_images = []

for filename in os.listdir(reference_folder):
    img_path = os.path.join(reference_folder, filename)
    if os.path.isfile(img_path):
        img = cv2.imread(img_path)
        if img is not None:
            reference_images.append(img)
        else:
            print(f"Could not load image: {img_path}")


if not reference_images:
    print("Error: No reference images loaded. Check the folder.")
    exit()


cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

def check_face(frame):
    global face_match
    face_match = False

    try:
        for ref_img in reference_images:
            if DeepFace.verify(frame, ref_img.copy())['verified']:
                face_match = True
                break
    except ValueError:
        face_match = False

while True:
    ret, frame = cap.read()

    if ret:
        if counter % 38 == 8:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start() 
            except ValueError:
                pass
        counter += 1

        if face_match:
            cv2.putText(frame, "Face Detected!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO Face Found!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
