import json
import os
import shutil

def write_competitors_to_files(file_path, folder_name="", older_folder_name=""):
    folder_name = folder_name
    older_folder_name = older_folder_name
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if not os.path.exists(os.path.join(folder_name, older_folder_name)):
        os.makedirs(os.path.join(folder_name, older_folder_name))

    if os.listdir(folder_name):
        latest_folder_num = max([int(f) for f in os.listdir(os.path.join(folder_name, older_folder_name)) if os.path.isdir(os.path.join(folder_name, older_folder_name, f))] + [0])
        new_folder_name = str(latest_folder_num + 1)
        os.makedirs(os.path.join(folder_name, older_folder_name, new_folder_name))
        for filename in os.listdir(folder_name):
            if os.path.isfile(os.path.join(folder_name, filename)):
                shutil.move(os.path.join(folder_name, filename), os.path.join(folder_name, older_folder_name, new_folder_name, filename))

    with open(file_path) as json_file:
        data = json.load(json_file)
        for i in range(1, len(data)+1):
            with open(f'{folder_name}/{i}.py', 'w', encoding="utf-8", errors="ignore") as file:
                file.write(data[str(i)])
