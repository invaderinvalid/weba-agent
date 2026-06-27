import os
import json
from openai import OpenAI
from browser_tools import BrowserState
from schemas import SCRAPER_TOOLS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenRouter client (ensure your API key is in your environment variables)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# We use a reliable model for tool-calling. 
# You can change this to anthropic/claude-3.5-sonnet or meta-llama/llama-3.1-70b-instruct
MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free" 

def run_agent(user_task: str):
    print(f"🤖 Starting Task: {user_task}\n" + "-"*40)
    
    # Initialize our browser from the tools file
    browser = BrowserState()
    
    # Create a mapping so the string name of the tool triggers the actual function
    available_functions = {
        "navigate": browser.navigate,
        "get_page_content": browser.get_page_content
    }

    # The System Prompt tells the agent who it is and how to behave
    messages = [
        {"role": "system", "content": "You are an autonomous web-scraping agent. Use your tools to navigate the web, extract information, and answer the user's prompt. Once you have the answer, summarize it for the user."},
        {"role": "user", "content": user_task}
    ]

    # The ReAct Loop
    while True:
        print("🧠 Thinking...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=SCRAPER_TOOLS,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        messages.append(response_message) # Save the AI's response to memory

        # ACT: Did the model decide to use a tool?
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Trigger the actual Python function
                function_to_call = available_functions[function_name]
                print(f"🛠️ Tool Call: {function_name}({function_args})")
                
                # Execute the function and get the result (the Observation)
                if function_name == "navigate":
                    function_response = function_to_call(url=function_args.get("url"))
                elif function_name == "get_page_content":
                    function_response = function_to_call()
                
                # OBSERVE: Pass the tool's output back to the LLM
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
        else:
            # If no tools were called, the agent is done reasoning and has our final answer
            print("\n✅ Final Answer:")
            print(response_message.content)
            break