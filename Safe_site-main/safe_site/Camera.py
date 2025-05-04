import requests
from urllib.parse import urlencode
import cv2
import time
import datetime
from Mqtt import publish_alarm

# Set up the video capture
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('10.140.223.182')

# Set up the face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Set up the body cascade classifier
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

# Set up frame counter and interval
frame_counter = 0
interval_seconds = 2

Redflag = False
CommetFlag = True
# Define the allowed region coordinates (top-left and bottom-right)
allowed_region = [(100, 100), (450, 450)]

while True:
    # Read a frame from the video capture
    _, frame = cap.read()

    # Draw the allowed region on the frame
    if Redflag == False:
        cv2.rectangle(frame, allowed_region[0], allowed_region[1], (0, 255, 0), 2)
    else:
        cv2.rectangle(frame, allowed_region[0], allowed_region[1], (0, 0, 255), 2)

    # Convert the frame to grayscale for processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection on the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Perform body detection on the grayscale frame
    bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Check if any detected face or body is outside the allowed region
    for (x, y, w, h) in faces:
        if x < allowed_region[0][0] or y < allowed_region[0][1] or x + w > allowed_region[1][0] or y + h > allowed_region[1][1]:
            # If the worker is outside the allowed region, perform the necessary actions
            #print("Worker's face outside allowed region!")
            pass

        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    for (x, y, w, h) in bodies:
        if x < allowed_region[0][0] or y < allowed_region[0][1] or x + w > allowed_region[1][0] or y + h > allowed_region[1][1]:
            # If the worker is outside the allowed region, perform the necessary actions
            #print("Worker's body outside allowed region!")
            pass

        # Draw a rectangle around the body
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow("Camera", frame)

    # Save the frame every specified interval
    if x < allowed_region[0][0] or y < allowed_region[0][1] or x + w > allowed_region[1][0] or y + h > allowed_region[1][1]:
        if frame_counter % (interval_seconds * cap.get(cv2.CAP_PROP_FPS)) == 0:
            current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            file_name = f"frame_{current_time}.jpg"
            cv2.imwrite(file_name, frame)
            print(f"Saved {file_name}")
            publish_alarm()
            cv2.rectangle(frame, allowed_region[0], allowed_region[1], (0, 0, 255), 2)
            Redflag = True

            while CommetFlag:
                # Endpoint URL
                url = 'https://www.fullstack.co.il/smsGateWay2.php'

                # Custom parameters
                params = {
                    'token': 'ytr',
                    'to': '0584880391',
                    'message': 'Worker outside allowed region!'

                }
                print("not work")

                # URL encode the parameters
                encoded_params = urlencode(params)

                # Construct the final URL with encoded parameters
                request_url = f'{url}?{encoded_params}'

                # Make the GET request
                response = requests.get(request_url)

                # Check the response status code
                if response.status_code == 200:
                    print('Request successful')
                    print('Response:', response.text)
                else:
                    print('Request failed')
                    print('Response status code:', response.status_code)
                CommetFlag = False

    else:
        Redflag = False

    # Increment the frame counter
    frame_counter += 1

    # Check if 'q' is pressed to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()