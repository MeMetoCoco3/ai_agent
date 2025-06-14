import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from agent_functions import avaliable_functions
from call_function import call_function
from config import system_prompt

def main():
    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not sys.argv[1:]:
            print("AI Code Assistant")
            print('\nUsage: python main.py "your prompt here"')
            print('Example: python main.py "How do I build a calculator app?"')
            sys.exit(1)

    user_prompt = sys.argv[1]
    flags : list[str]= []
    if len(sys.argv) > 2:
        flags = sys.argv[2:]

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    verbose = "--verbose" in sys.argv
    if verbose:
        print(f"User prompt: {user_prompt}")

    print(generate_content(client, messages, verbose))

def generate_content(client:genai.Client, messages: list[types.Content], verbose:bool):
    model = "gemini-2.0-flash-001"
    respose = client.models.generate_content(
        config=types.GenerateContentConfig(
                tools =[avaliable_functions], 
                system_instruction=system_prompt
        ), model=model, contents=messages
    )

    if verbose:
        print(f"Prompt tokens: {respose.usage_metadata.prompt_token_count}") 
        print(f"Response tokens: {respose.usage_metadata.candidates_token_count}")


    if not respose.function_calls:
        return respose.text
 
    function_responses = []
    for function_call_part in respose.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Empty function call result.")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("No function responses generated.")


if __name__ == "__main__":
    main()
