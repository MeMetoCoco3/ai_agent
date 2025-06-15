from google.genai import types
import os

def write_file(working_directory:str, file_path:str, content:str):
    abs_working = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file):
        try:
            os.makedirs(os.path.dirname(abs_file), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"


    if os.path.exists(abs_file) and os.path.isdir(abs_file):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(abs_file, "w") as f:
            _ = f.write(content)
    except Exception as e:
        return f'Error: {e}'
    else: 
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)


