import os

from google.genai import types



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


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


