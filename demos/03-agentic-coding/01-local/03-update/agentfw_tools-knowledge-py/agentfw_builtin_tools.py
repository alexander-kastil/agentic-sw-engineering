"""
Built-in Tools Demo - Code Interpreter and Web Search

⚠️ IMPORTANT LIMITATION:
This demo attempts to use HostedCodeInterpreterTool and HostedWebSearchTool
with AzureOpenAIChatClient, but these tools are NOT SUPPORTED with ChatCompletion API.

These hosted tools only work with:
- AzureOpenAIResponsesClient (supports HostedCodeInterpreterTool)
- Azure AI Agents Service (supports BingGroundingTool for web search)

For working web search example, see: agentfw_bing_search.py

This file is kept for educational purposes to show what doesn't work.
"""

import asyncio
import os
import logging
from dotenv import load_dotenv

from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import HostedCodeInterpreterTool, HostedWebSearchTool
from utils.log_util import LogUtil, vdebug

# Load environment variables
load_dotenv()

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-07-01-preview")


async def main():
    """Interactive demo: Agent with built-in Code Interpreter and Web Search tools."""
    
    # Setup logging (use verbose=True to see debug logs including tool calls)
    log_util = LogUtil()
    log_util.setup_logging(verbose=True)
    
    print("\n" + "="*70)
    print("🛠️ DEMO: Built-in Tools - Code Interpreter & Web Search")
    print("="*70)
    print("""
This demo combines two powerful built-in tools:

1. 🐍 CODE INTERPRETER
   - Execute Python code in a sandboxed environment
   - Perform data analysis, calculations, and visualizations
   - Handle complex mathematical computations

2. 🌐 WEB SEARCH
   - Search the web for current information
   - Get real-time data and facts
   - Answer questions about recent events

Examples to try:
- "Search for the latest news about AI agents"
- "Calculate the fibonacci sequence up to 20 using Python"
- "What is the weather in Seattle today?"
- "Write Python code to plot a sine wave"
    """)
    
    # Create agent with both built-in tools
    agent = AzureOpenAIChatClient(
        endpoint=ENDPOINT,
        deployment_name=DEPLOYMENT,
        api_key=API_KEY,
        api_version=API_VERSION
    ).create_agent(
        instructions=(
            "You are a helpful assistant with access to code interpreter and web search tools. "
            "Use code interpreter for mathematical calculations, data analysis, and code execution. "
            "Use web search for current events, real-time information, and factual queries. "
            "Always choose the most appropriate tool for the task. "
            "When presenting formulas or equations, use LaTeX with \\[ and \\] for display math "
            "and \\( and \\) for inline math. Keep explanations concise."
        ),
        name="BuiltinToolsBot",
        tools=[
            HostedCodeInterpreterTool(),
            HostedWebSearchTool()
        ]
    )
    
    print("\n✅ Agent created with built-in tools:")
    print("   🐍 Code Interpreter")
    print("   🌐 Web Search (Bing)")
    
    print("\n" + "="*70)
    print("💬 Interactive Chat (Type 'quit' to exit)")
    print("="*70 + "\n")
    
    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            print("\n👋 Received EOF - exiting.")
            break
        except KeyboardInterrupt:
            print("\n👋 Interrupted - exiting.")
            break
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not user_input.strip():
            continue
        
        logging.info(f"User query: {user_input}")
        print("Agent: ", end="", flush=True)
        
        async for chunk in agent.run_stream(user_input):
            # Log tool calls
            if hasattr(chunk, 'tool_calls') and chunk.tool_calls:
                for tool_call in chunk.tool_calls:
                    logging.info(f"🔧 Tool called: {tool_call.type}")
                    vdebug(f"Tool call details: {tool_call}")
            
            # Log tool outputs
            if hasattr(chunk, 'tool_outputs') and chunk.tool_outputs:
                for tool_output in chunk.tool_outputs:
                    logging.info(f"📤 Tool output received")
                    vdebug(f"Tool output details: {tool_output}")
            
            if chunk.text:
                print(chunk.text, end="", flush=True)
        
        print("\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 See you again soon.")
