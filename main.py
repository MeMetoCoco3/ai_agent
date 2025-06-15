import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from agent_functions import avaliable_functions
from call_function import call_function, avaliable_functions
from config import system_prompt, MAX_CANDIDATES

def main():
    _ = load_dotenv()
    if not sys.argv[1:]:
            print("AI Code Assistant")
            print('\nUsage: python main.py "your prompt here"')
            print('Example: python main.py "How do I build a calculator app?"')
            sys.exit(1)

    flags : list[str]= []
    if len(sys.argv) > 2:
        flags = sys.argv[2:]
    verbose = "--verbose" in sys.argv

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    if verbose:
        print(f"User prompt: {user_prompt}")

    for i in range(0, MAX_CANDIDATES):
        try:
            final_response =  generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")
    

def generate_content(client:genai.Client, messages: list[types.Content], verbose:bool)->str|None:
    model = "gemini-2.0-flash-001"

    respose = client.models.generate_content(
        config=types.GenerateContentConfig(
                tools =[avaliable_functions], 
                system_instruction=system_prompt
        ), model=model, contents=messages
    )
    if respose.candidates:
        for candidate in respose.candidates: 
            function_call_content = candidate.content
            if function_call_content: messages.append(function_call_content)

    if verbose:
        print(f"Prompt tokens: {respose.usage_metadata.prompt_token_count}") 
        print(f"Response tokens: {respose.usage_metadata.candidates_token_count}")


    if not respose.function_calls:
        if respose.text: return respose.text
        return "No respose generated"
 
    function_responses =[]
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
    messages.append(types.Content(role="tool", parts=function_responses))

if __name__ == "__main__":
    main()
