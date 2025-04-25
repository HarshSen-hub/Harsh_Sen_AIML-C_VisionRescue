import threading
import cv2
from deepface import DeepFace

# Receiving video input from camera and setting parameters
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

counter = 0
face_match = False

# Image file path for reference image for recognition
reference_img = cv2.imread("img.jpg")

# Check if the image was loaded properly
if reference_img is None:
    print("Error: Could not load reference image. Check the file path.")
    exit()

# Load pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Matching and recognizing face with reference image
def check_face(frame, face_roi):
    global face_match

    try:
        if DeepFace.verify(face_roi, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False

while True:
    ret, frame = cap.read()

    if ret:
        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                # Draw a rectangle around the face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

                # Get the Region of Interest (ROI) for the face
                face_roi = frame[y:y+h, x:x+w]

                # Use threading to check if the face matches the reference image
                try:
                    threading.Thread(target=check_face, args=(frame.copy(), face_roi)).start()
                except ValueError:
                    pass

        if counter % 38 == 8:
            # Display text based on face recognition
            if face_match:
                cv2.putText(frame, "Face Detected!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "NO Face Found!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 3)

        counter += 1
        cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
