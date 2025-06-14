from google.genai import types
import os

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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specificed file, constrained to the working directory, if not found, it will create it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to overwrite.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file path.",
            ),
        },
    ),
)


