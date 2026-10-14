import os
from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    working_directory_ab = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([working_directory_ab, target_path]) != working_directory_ab:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",  
        "description": "Reads and return the content of a speficied file relative to the working directory",        
        "parameters": {
            "type": "object",
    "properties": {
        "file_path": {
            "type": "string",
            "description": "The path to the file to read, relative to the working directory.",
        },
    },
    "required": ["file_path"],
},
},
}
