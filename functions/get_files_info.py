import os
import subprocess

MAX_CHARS = 10000

def run_python_file(working_directory:str, file_path:str)->str:
    abs_working = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file.startswith(abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file):
        return f'Error: File "{file_path}" not found.'
    if not abs_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        res = subprocess.run(args=["python", file_path], timeout=30, cwd=abs_working, text=True)

        output = ""
        if res.stdout:
            output += f'STDOUT:{res.stdout}'
        if res.stderr:
            output += f'STDERR:{res.stderr}'
        if res.returncode!= 0:
            output+= f'Process exited with code {res.returncode}'
    except Exception as e:
        return f"Error: executing Python file: {e}"
    else:
        if not output:
            output = "No output produced."
        return output


def get_files_info(working_directory:str, directory:str|None=None)-> str:
    target_path = os.path.abspath(working_directory)
    content = os.listdir(working_directory)
    if directory:
        abs_working = os.path.abspath(working_directory)
        abs_directory = os.path.abspath(os.path.join(working_directory, directory))
        
        if not abs_directory.startswith(abs_working):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'
        target_path = abs_directory
        content = os.listdir(target_path)

    files_data = ""
    for file in content:     
        full_path = os.path.join(target_path, file)
        try:
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            files_data += f'- {file}: file_size={file_size} bytes, is_dir={is_dir}\n'
        except Exception as e:
            files_data += f'- {file}: Error accessing file info: {e}\n'

    return files_data


def get_file_content(working_directory:str, file_path:str)->str:
    abs_working = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_directory.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_directory):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    file_content = ""
    with open(abs_directory, "r") as f:
        file_content = f.read(MAX_CHARS)

    if len(file_content) == MAX_CHARS:
        file_content += f'[...File "{file_path}" truncated at 10000 characters]'
    return file_content

 

def write_file(working_directory:str, file_path:str, content:str):
    abs_working = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_directory.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    parent_dir = os.path.dirname(abs_directory)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    try:
        with open(abs_directory, "w") as f:
            _ = f.write(content)
    except Exception as e:
        return f'Error: {e}'
    else: 
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


