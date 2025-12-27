import os
from dotenv import load_dotenv
import argparse # to handle cli arguments
from google.genai import types
from google import genai
from prompts.prompts import system_prompt 
from functions.available_functions import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY") # get api key from .env
    
    if api_key is None:
        raise RuntimeError("API key is not found!")
    
    client = genai.Client(api_key=api_key)
     
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    # store list of messages, this would be the context window for now.    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # args.user_prompt is the argument entered in cli
    response = client.models.generate_content(
        model = 'gemini-2.5-flash', 
        contents = messages,
        config = types.GenerateContentConfig(
            tools = [available_functions], system_instruction=system_prompt
        )    
)
    
    if response.usage_metadata is None:
        raise RuntimeError("Can't access token limit. Some error occur when accessing usage_metadata")
    usage = response.usage_metadata
    
    # if user include --verbose flag in cli
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")
    
    if response.function_calls:
        # for function_call in response.function_calls:
        #     print(f"Calling function: {function_call.name}({function_call.args})")

        function_results = []  # ← create this before the loop

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)

            # Validation checks
            if not function_call_result.parts:
                raise Exception("types.Content object returned from call_function does not have a .parts list!")
            if function_call_result.parts[0].function_response is None:
                raise Exception("There should be a FunctionResponse object!")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("There is no actual function result returned!")

            # ✅ Now add it to a list of function results
            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(f"response: {response.text}")
        return f"The response.function_calls is None!"
    

if __name__ == "__main__":
    main()
