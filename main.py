from call_function import available_functions, call_function
from prompts import system_prompt
import argparse 
import os
from dotenv import load_dotenv
from openai import OpenAI

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
      raise RuntimeError("API key not found in environment variables")

    client = OpenAI(
       base_url="https://openrouter.ai/api/v1",
       api_key=api_key,
    )

    messages =[ {"role": "system", "content": system_prompt}, 
    {"role": "user", "content": args.user_prompt},
    ] 

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages= messages, 
            tools=available_functions,
        )

        if response.usage is None:
            raise RuntimeError("some helpful message")

        if args.verbose:  
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if not result_message["content"]:
                    raise Exception(f"Empty response from function call: {tool_call.function.name}")
                if args.verbose :
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            print(message.content)
            return 
    print("Maximum iterations reached without a final response")
    sys.exit(1)



if __name__ == "__main__":
    main()

