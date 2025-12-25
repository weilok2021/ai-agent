import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs

        if not valid_target_dir:
            # target_dir_items_metadata.append(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
            # return "\n\t".join(target_dir_items_metadata)
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'        
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # If the file name doesn't end with .py, return an error string:
        if file_path.split('.')[-1] != "py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]
        # if any arguments is provided
        if args:    
            command.extend(args)
            
        # Run the command
        completed_process = subprocess.run(
            command,                   # The command (can be list or string)
            cwd=working_directory,        # Set working directory
            capture_output=True,          # Capture both stdout and stderr
            text=True,                    # Decode bytes → string automatically
            timeout=30                    # Prevent infinite execution
        )
        
        output = ""
        if completed_process.returncode != 0:
            output += "Process exited with code {completed_process.returncode}\n"
        if not completed_process.stderr and not completed_process.stdout:
            output += "No output produced\n"
        elif completed_process.stdout:
            output += f"STDOUT: {completed_process.stdout}\n"
        elif completed_process.stderr:
            output += f"STDERR: {completed_process.stderr}\n"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
