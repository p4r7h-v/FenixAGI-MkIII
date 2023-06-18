import gzip
import shutil

def compress_file(input_file_path, output_file_path):
    """
    Compresses the given input_file_path and saves it at output_file_path.

    :param input_file_path: The file path of the file to be compressed
    :type input_file_path: str
    :param output_file_path: The file path to save the compressed file
    :type output_file_path: str
    """

    with open(input_file_path, 'rb') as f_in:
        with gzip.open(output_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f"File '{input_file_path}' has been compressed and saved as '{output_file_path}'")

# Example usage:
compress_file('example.txt', 'example.txt.gz')