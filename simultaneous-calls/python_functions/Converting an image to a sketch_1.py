import cv2

def image_to_sketch(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    inverted_gray_image = 255 - gray_image

    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(inverted_gray_image, (13, 13), 0)

    # Invert the blurred image
    inverted_blurred_image = 255 - blurred_image

    # Create the sketch
    sketch = cv2.divide(gray_image, inverted_blurred_image, scale=256.0)

    # Save the sketch to output file
    cv2.imwrite(output_path, sketch)