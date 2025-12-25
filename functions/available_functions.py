from google.genai import types
from .get_files_info import schema_get_files_info


# Now that we're building declarations for our functions, 
# we can include those in a list of available functions to provide to the LLM.
available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)