
import threading
import cv2
from deepface import DeepFace
import os


cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

counter = 0
face_match = False


reference_folder = "refs"


reference_images = []
for filename in os.listdir(reference_folder):
    if filename.endswith((".jpg", ".png", ".jpeg")):  
        img_path = os.path.join(reference_folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            reference_images.append(img)


if len(reference_images) == 0:
    print("Error: No valid reference images found in the folder.")
    exit()


def check_face(frame):
    global face_match

    try:
      
        for ref_img in reference_images:
            if DeepFace.verify(frame, ref_img.copy())['verified']:
                face_match = True
                return
        face_match = False
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
            cv2.putText(frame, "Face Recognised!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "Not matched", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
