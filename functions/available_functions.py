from google.genai import types
from .get_files_info import schema_get_files_info
from .get_file_content import schema_get_files_content
from .write_file import schema_write_file
from .run_python_file import schema_run_python_file


# Now that we're building declarations for our functions, 
# we can include those in a list of available functions to provide to the LLM.
available_functions = types.Tool(
    function_declarations = [
        schema_get_files_info,         
        schema_get_files_content, 
        schema_write_file, 
        schema_run_python_file,
    ]
)