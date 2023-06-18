import shutil
import os
import datetime

# Define the function to backup data
def backup_data(source, destination):
    """
    Python function to backup a directory.

    Args:
    source (str): Source directory.
    destination (str): Destination directory.

    Returns:
    None
    """ 
    
    #create a backup directory named with current date and time
    curr_time = datetime.datetime.now()
    timestampStr = curr_time.strftime("%d-%b-%Y-%H-%M-%S")
    backup_dir = os.path.join(destination, f"backup_{timestampStr}")

    try:
        # Copy the directory
        shutil.copytree(source, backup_dir)
        print(f'Backup of {source} successfully created at {backup_dir}')
    except Exception as e:
        print(f'Error occurred during backup: {str(e)}')

# Define your source and destination directories
source_dir = '/path/to/source'
destination_dir = '/path/to/destination'

# Call the function for data backup
backup_data(source_dir, destination_dir)