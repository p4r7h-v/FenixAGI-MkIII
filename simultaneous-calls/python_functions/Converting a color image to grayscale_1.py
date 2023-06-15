from PIL import Image

def convert_to_grayscale(image_path, save_path=None):
    """
    Converts a color image to grayscale.

    Args:
    image_path (str): Path of the color image to be converted.
    save_path (str, optional): Path to save the grayscale image. If None, the grayscale image will not be saved.

    Returns:
    Image.Image: Grayscale PIL Image object.
    """
    # Open the image using the Image module
    image = Image.open(image_path)

    # Convert the image to grayscale
    grayscale_image = image.convert('L')

    # Save the grayscale image if save_path is provided
    if save_path:
        grayscale_image.save(save_path)

    return grayscale_image

# Example usage:
grayscale_img = convert_to_grayscale("color_image.jpg", "grayscale_image.jpg")
grayscale_img.show()