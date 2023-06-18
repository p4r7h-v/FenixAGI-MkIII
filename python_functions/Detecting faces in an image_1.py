import cv2

def detect_faces(image_path, cascade_path='haarcascade_frontalface_default.xml'):
    # Load the image from the given path
    image = cv2.imread(image_path)
    if image is None:
        print(f"Image not found at {image_path}")
        return []

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load the Haar Cascade classifier
    face_cascade = cv2.CascadeClassifier(cascade_path)

    if face_cascade.empty():
        print(f"Cascade file not found at {cascade_path}")
        return []

    # Detect faces in the image using the classifier
    faces = face_cascade.detectMultiScale(
        gray_image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    return faces