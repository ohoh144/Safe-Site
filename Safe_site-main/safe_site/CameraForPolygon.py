import cv2
import time
import datetime
import numpy as np



# Set up the video capture
cap = cv2.VideoCapture(0)

# Set up the face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Set up the body cascade classifier
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

# Prompt the user to define the safe and danger regions
num_safe_polygons = int(input("Enter the number of safe polygons: "))
safe_polygons = []
for i in range(num_safe_polygons):
    print(f"Enter the coordinates for safe polygon {i+1}:")
    polygon_points = []
    for j in range(4):
        x = int(input(f"Enter x-coordinate for point {j+1}: "))
        y = int(input(f"Enter y-coordinate for point {j+1}: "))
        polygon_points.append((x, y))
    safe_polygons.append(np.array(polygon_points))

num_danger_polygons = int(input("Enter the number of danger polygons: "))
danger_polygons = []
for i in range(num_danger_polygons):
    print(f"Enter the coordinates for danger polygon {i+1}:")
    polygon_points = []
    for j in range(4):
        x = int(input(f"Enter x-coordinate for point {j+1}: "))
        y = int(input(f"Enter y-coordinate for point {j+1}: "))
        polygon_points.append((x, y))
    danger_polygons.append(np.array(polygon_points))

while True:
    # Read a frame from the video capture
    _, frame = cap.read()

    # Draw the safe polygons on the frame
    for polygon in safe_polygons:
        cv2.polylines(frame, [polygon], True, (0, 255, 0), 2)

    # Draw the danger polygons on the frame
    for polygon in danger_polygons:
        cv2.polylines(frame, [polygon], True, (0, 0, 255), 2)

    # Convert the frame to grayscale for processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection on the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Perform body detection on the grayscale frame
    bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Check if any detected face or body falls within the safe or danger regions
    for (x, y, w, h) in faces:
        face_center = (int(x + w // 2), int(y + h // 2))  # Ensure integer values for the center point

        for polygon in safe_polygons:
            if cv2.pointPolygonTest(polygon, face_center, False) < 0:

                # If the worker's face is outside the safe region, perform the necessary actions
                print("Worker's face outside safe region!")

        for polygon in danger_polygons:
            if cv2.pointPolygonTest(polygon, face_center, False) >= 0:
                # If the worker's face is inside the danger region, perform the necessary actions
                print("Worker's face inside danger region!")

        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    for (x, y, w, h) in bodies:
        body_center = (int(x + w // 2), int(y + h // 2))  # Ensure integer values for the center point

        for polygon in safe_polygons:
            if cv2.pointPolygonTest(polygon, body_center, False) < 0:
                # If the worker's body is outside the safe region, perform the necessary actions
                print("Worker's body outside safe region!")

        for polygon in danger_polygons:
            if cv2.pointPolygonTest(polygon, body_center, False) >= 0:
                # If the worker's body is inside the danger region, perform the necessary actions
                print("Worker's body inside danger region!")

        # Draw a rectangle around the body
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow("Camera", frame)

    # Check if 'q' is pressed to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
