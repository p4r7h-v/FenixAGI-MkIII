from PIL import Image

def convert_to_grayscale(image_path, save_path=None):
    """
    Convert a color image to grayscale.

    :param image_path: Path to the color image file
    :type image_path: str
    :param save_path: Path to save the grayscale image; optional, defaults to None
    :type save_path: str, optional
    :return: Grayscale image object
    :rtype: Image.Image
    """
    try:
        # Load the color image
        color_image = Image.open(image_path)

        # Convert the color image to grayscale
        grayscale_image = color_image.convert('L')

        # Save the grayscale image if a save path is specified
        if save_path:
            grayscale_image.save(save_path)

        return grayscale_image

    except Exception as e:
        print(f"Error: {e}")
        return None

# Usage example:
grayscale_image = convert_to_grayscale("color_image.jpg", "grayscale_image.jpg")