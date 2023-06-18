import cv2

def detect_faces(image_path):
    # Load the cascade (pre-trained face detection model)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Load the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Save the resulting image with detected faces
    cv2.imwrite("output.jpg", img)

    # Print the number of faces detected
    print(f"Number of faces detected: {len(faces)}")

# Example usage:
detect_faces("path_to_your_image.jpg")