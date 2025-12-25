import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        directory_name = directory
        if directory_name == '.':
            directory_name = "current"
        target_dir_items_metadata = [f"Result for '{directory_name}' directory:"]

        if not valid_target_dir:
            target_dir_items_metadata.append(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return "\n\t".join(target_dir_items_metadata)
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            target_dir_items_metadata.append(f'Error: "{directory}" is not a directory')
            return "\n\t".join(target_dir_items_metadata)
        
        target_dir_items = os.listdir(target_dir) 
        
        for item in target_dir_items:
            meta_data = f"- {item}: file_size={os.path.getsize(os.path.join(target_dir, item))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, item))}"
            target_dir_items_metadata.append(meta_data)
            # print(f"- {item}: file_size={os.path.getsize(os.path.join(target_dir, item))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, item))}")
            # print(dir_contents)
        
        metadata_string = "\n\t".join(target_dir_items_metadata)
        return metadata_string
    
    except Exception as e:
        return f"Error: {e}"


# We'll use this to build a "declaration" or "schema" for each of our functions. Again,
# this basically just tells the LLM how the function should be called. 
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)