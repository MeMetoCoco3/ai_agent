from google.genai import types
import os, subprocess

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



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to run.",
            ),
        },
    ),
)
