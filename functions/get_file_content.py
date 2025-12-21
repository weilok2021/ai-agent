import os
# from get_files_info import get_files_info
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    """@args
        working_directory: the working_directory provided to AI agent
        file_path: the targeted relative file path
    """
    
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

        if not valid_target_dir:
            # target_dir_items_metadata.append(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
            # return "\n\t".join(target_dir_items_metadata)
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        content = ""
        with open(target_file_path, encoding="utf-8") as f:
            content += f.read(MAX_CHARS) # Only read up to MAX_CHARS character from file
            # After reading the first MAX_CHARS, if next character does exist, which means reading has been truncated
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"
