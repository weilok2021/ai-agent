import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
        print(target_file_path)
        with open(target_file_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    

# We'll use this to build a "declaration" or "schema" for each of our functions. Again,
# this basically just tells the LLM how the function should be called. 
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content into a file with file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to get content from, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to be written into file with argument file_path",
            )
        },
        required=["file_path", "content"],
    ),
)