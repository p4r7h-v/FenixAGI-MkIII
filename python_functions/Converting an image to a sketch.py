import cv2

def convert_image_to_sketch(image_path, output_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur
    blurred_image = cv2.GaussianBlur(gray_image, (13, 13), 0)

    # Detect edges using the Canny algorithm
    edges = cv2.Canny(blurred_image, 30, 150)

    # Apply an inverted binary threshold to create the sketch effect
    _, sketch = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY_INV)

    # Save the sketch image
    cv2.imwrite(output_path, sketch)

    return output_path

# Example usage:
input_image = "path/to/your/image.jpg"
output_sketch = "path/to/save/sketch.jpg"
output_path = convert_image_to_sketch(input_image, output_sketch)

print(f"The sketch was saved at {output_path}")