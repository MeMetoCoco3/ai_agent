import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types




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
model = "gemini-2.0-flash-001"

respose = client.models.generate_content(model=model, contents=messages)


if "--verbose" in flags:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {respose.usage_metadata.prompt_token_count}") 
    print(f"Response tokens: {respose.usage_metadata.candidates_token_count}")

print(f"Response: {respose.text}")

