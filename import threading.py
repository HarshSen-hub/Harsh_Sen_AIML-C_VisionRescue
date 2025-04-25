#VisionRescue: AI-Powered Missing Persons Detection System


#importing necesaary modules
import threading
import cv2 
from deepface import DeepFace

#receiving video input from camera and setting parameters
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

counter = 0
face_match = False

#Image file path for reference image for recognition
reference_img = cv2.imread("img.jpg")

# Check if the image was loaded properly
if reference_img is None:
    print("Error: Could not load reference image. Check the file path.")
    exit()

#Matching and recognising face with reference image
def check_face(frame):
    global face_match

    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
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
            cv2.putText(frame, "Face Detected!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO Face Found!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()