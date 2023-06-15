import pandas as pd
import pyautogui as pag
import time

def automate_data_entry(file_path, fields_coordinates, delay=1):
    """
    Automation of data entry from a CSV file using the PyAutoGUI library.

    :param file_path: The path to the CSV file containing data.
    :param fields_coordinates: A list of tuples containing the x, y screen coordinates of the fields to be filled.
    :param delay: Delay (in seconds) between actions to account for processing time. Default is 1 sec.
    """

    # Read the CSV file using pandas
    data = pd.read_csv(file_path)

    # Iterate through each row in the CSV file
    for index, row in data.iterrows():
        # Fill each field with the corresponding data from the CSV file
        for i, field_coordinates in enumerate(fields_coordinates):
            x, y = field_coordinates
            # Move the cursor to the field's position
            pag.moveTo(x, y)
            # Click to select the field
            pag.click()

            # Type the data
            pag.typewrite(str(row[i]), interval=0.1)

        # Move to the submit/save button (assuming you know its coordinates)
        submit_button_x, submit_button_y = 100, 200  # Replace with the actual coordinates
        pag.moveTo(submit_button_x, submit_button_y)
        pag.click()

        # Add a delay before the next entry to account for processing/loading times
        time.sleep(delay)

# Example usage:
fields_coordinates = [(100, 100), (200, 100), (300, 100)]  # Replace with the actual field coordinates
automate_data_entry("data.csv", fields_coordinates)