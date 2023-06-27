## File Management Functions

Here are 10 file management functions:

1. `create_file(file_path)`: Creates a new file at the specified file path.

```python
import os

def create_file(file_path):
    with open(file_path, 'w') as file:
        pass
```

2. `delete_file(file_path)`: Deletes the file located at the specified file path.

```python
import os

def delete_file(file_path):
    os.remove(file_path)
```

3. `copy_file(source_path, destination_path)`: Copies a file from the source path to the destination path.

```python
import shutil

def copy_file(source_path, destination_path):
    shutil.copyfile(source_path, destination_path)
```

4. `move_file(source_path, destination_path)`: Moves a file from the source path to the destination path.

```python
import shutil

def move_file(source_path, destination_path):
    shutil.move(source_path, destination_path)
```

5. `rename_file(file_path, new_name)`: Renames a file located at the specified file path with a new name.

```python
import os

def rename_file(file_path, new_name):
    folder, old_name = os.path.split(file_path)
    new_path = os.path.join(folder, new_name)
    os.rename(file_path, new_path)
```

6. `get_file_size(file_path)`: Retrieves the size of a file located at the specified file path.

```python
import os

def get_file_size(file_path):
    return os.path.getsize(file_path)
```

7. `read_file_text(file_path)`: Reads and returns the text content of a file located at the specified file path.

```python

def read_file_text(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content
```

8. `write_file_text(file_path, content)`: Writes the provided content to a file located at the specified file path.

```python

def write_file_text(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
```

9. `list_files_in_directory(directory_path)`: Lists all the files (excluding directories) in the specified directory path.

```python
import os

def list_files_in_directory(directory_path):
    files = []
    for file in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, file)):
            files.append(file)
    return files
```

10. `get_file_metadata(file_path)`: Retrieves the metadata information (e.g., creation date, last modified date, file permissions) of a file located at the specified file path.

```python
import os

def get_file_metadata(file_path):
    metadata = {
        'size': os.path.getsize(file_path),
        'created': os.path.getctime(file_path),
        'modified': os.path.getmtime(file_path),
        'permissions': os.stat(file_path).st_mode
    }
    return metadata
```
