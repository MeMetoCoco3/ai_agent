from typing import Required
from google.genai import types
import os


MAX_CHARS = 10000

def get_file_content(working_directory:str, file_path:str)->str:
    abs_working = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_directory.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_directory):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_directory, "r") as f:
            file_content = f.read(MAX_CHARS)

            if len(file_content) == MAX_CHARS:
                file_content += f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content
    
    except Exception as e:
            return f'Error reading file "{file_path}": {e}'
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Gets the first {MAX_CHARS} of a specified file, constrained to the working director.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get the content from.",
            ),
        },
        required = ["file_path"]
    ),
)


