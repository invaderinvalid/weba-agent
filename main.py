import os
from agent import run_agent

def main():
    # ⚠️ Double-check that your API key is set in the environment
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ Error: OPENROUTER_API_KEY environment variable is not set.")
        print("Please set it using: export OPENROUTER_API_KEY='your_key'")
        return

    # Define a simple, clear task for the scraper agent to test the loop
    task = "Go to https://example.com, read the page content, and tell me what the main heading is."
    
    # Run the Observe -> Reason -> Act loop
    run_agent(task)

if __name__ == "__main__":
    main()