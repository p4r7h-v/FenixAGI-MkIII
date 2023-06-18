import cv2
import numpy as np

def image_segmentation(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Remove small white regions
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Identify the background region
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Compute the distance transform and normalize it
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    # Identify the unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Label the markers
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1

    # Mark the unknown region as 0
    markers[unknown == 255] = 0

    # Apply the Watershed algorithm
    cv2.watershed(image, markers)

    # Color the segmented regions
    image[markers == -1] = [0, 0, 255]

    # Show the segmented image
    cv2.imshow('Segmented Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_segmentation('path/to/your/image.jpg')