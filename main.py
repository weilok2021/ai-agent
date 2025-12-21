import os
from dotenv import load_dotenv
import argparse # to handle cli arguments
from google.genai import types
from google import genai


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
        model='gemini-2.5-flash', contents=messages 
    )
    
    if response.usage_metadata is None:
        raise RuntimeError("Can't access token limit. Some error occur when accessing usage_metadata")
    usage = response.usage_metadata
    
    # if user include --verbose flag in cli
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
