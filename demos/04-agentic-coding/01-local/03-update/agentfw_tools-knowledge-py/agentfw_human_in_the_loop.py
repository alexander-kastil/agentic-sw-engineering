"""
NEW 07: Human-in-the-Loop Approval (Interactive Demo)

Simple real example with 2 functions:
1. create_file() - No approval needed (safe operation)
2. delete_file() - Requires approval (dangerous operation)

This uses a custom ApprovalRequiredTool wrapper (same pattern as file 11)
"""

import asyncio
import os
from typing import Annotated, Callable
from pydantic import Field
from dotenv import load_dotenv
from pathlib import Path

from agent_framework.azure import AzureOpenAIChatClient

# Load environment variables
load_dotenv()

# Configuration
ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
DEPLOYMENT = os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT_NAME')
API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')

# Create output directory for file operations, from env var OUTPUT_PATH
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "").strip()
if OUTPUT_PATH:
    DEMO_DIR = Path(OUTPUT_PATH)
else:
    DEMO_DIR = Path(__file__).parent / "output"
DEMO_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# Approval System: Wrapper for functions requiring human approval
# ============================================================================

class ApprovalRequiredTool:
    """Wrapper for a function tool that requires human approval before execution."""
    
    def __init__(self, func: Callable, description: str = None):
        self.original_func = func
        self.func_name = func.__name__
        self.description = description or func.__doc__ or "No description"
        self.approval_callback = None
    
    def set_approval_callback(self, callback: Callable):
        """Set the callback function that asks user for approval."""
        self.approval_callback = callback
    
    def __call__(self, *args, **kwargs):
        """Execute the function with approval check."""
        # Debug: show what we received
        print(f"[DEBUG] Wrapper called with args={args}, kwargs={kwargs}")
        
        # Handle nested argument structure from agent framework
        # The framework may pass: kwargs={'args': 'value', 'kwargs': '{}'}
        if 'args' in kwargs and 'kwargs' in kwargs:
            # Unwrap nested structure
            nested_args = kwargs.get('args', '')
            nested_kwargs_str = kwargs.get('kwargs', '{}')
            
            print(f"[DEBUG] Detected nested structure - unwrapping...")
            print(f"[DEBUG] nested_args={nested_args}, nested_kwargs={nested_kwargs_str}")
            
            # Convert nested_kwargs string to dict if needed
            import json
            if isinstance(nested_kwargs_str, str) and nested_kwargs_str:
                try:
                    nested_kwargs = json.loads(nested_kwargs_str) if nested_kwargs_str.strip() else {}
                except:
                    nested_kwargs = {}
            else:
                nested_kwargs = nested_kwargs_str if isinstance(nested_kwargs_str, dict) else {}
            
            # Map 'args' to the actual parameter name
            # For delete_file_impl, the parameter is 'filename'
            import inspect
            sig = inspect.signature(self.original_func)
            param_names = list(sig.parameters.keys())
            
            if param_names and nested_args:
                # Use the first parameter name
                actual_kwargs = {param_names[0]: nested_args}
                actual_kwargs.update(nested_kwargs)
            else:
                actual_kwargs = nested_kwargs
            
            print(f"[DEBUG] Unwrapped to: {actual_kwargs}")
            
            # Prepare approval request info
            approval_info = {
                "function_name": self.func_name,
                "description": self.description,
                "arguments": {
                    "args": (),
                    "kwargs": actual_kwargs
                }
            }
        else:
            # Normal call - no unwrapping needed
            actual_kwargs = kwargs
            approval_info = {
                "function_name": self.func_name,
                "description": self.description,
                "arguments": {
                    "args": args,
                    "kwargs": kwargs
                }
            }
        
        # Ask for approval
        if self.approval_callback:
            approved = self.approval_callback(approval_info)
        else:
            # Default: auto-approve if no callback set
            print(f"⚠️ No approval callback set, auto-approving: {self.func_name}")
            approved = True
        
        if approved:
            print(f"✅ APPROVED: Executing {self.func_name}")
            try:
                if 'args' in kwargs and 'kwargs' in kwargs:
                    # Use unwrapped arguments
                    result = self.original_func(**actual_kwargs)
                else:
                    # Use original arguments
                    result = self.original_func(*args, **kwargs)
                print(f"[DEBUG] Function returned: {result}")
                return result
            except Exception as e:
                import traceback
                error_msg = f"❌ Error executing {self.func_name}: {e}"
                print(f"[DEBUG] {error_msg}")
                print(f"[DEBUG] Traceback: {traceback.format_exc()}")
                return error_msg
        else:
            print(f"❌ REJECTED: Not executing {self.func_name}")
            return f"⛔ Function '{self.func_name}' was rejected by the user."


# ============================================================================
# Function 1: CREATE FILE - No approval needed (safe operation)
# ============================================================================

def create_file(
    filename: Annotated[str, Field(description="Name of file to create")],
    content: Annotated[str, Field(description="Content to write in file")]
) -> str:
    """Create a new file with content. Safe operation - no approval needed."""
    try:
        file_path = DEMO_DIR / filename
        file_path.write_text(content, encoding='utf-8')
        return f"✅ File '{filename}' created successfully with {len(content)} characters"
    except Exception as e:
        return f"❌ Error creating file: {e}"


# ============================================================================
# Function 2: DELETE FILE - Implementation (requires approval via wrapper)
# ============================================================================

def delete_file_impl(
    filename: Annotated[str, Field(description="Name of file to delete")]
) -> str:
    """Delete a file. This function will be wrapped with approval requirement."""
    try:
        # Debug: show what we received
        print(f"[DEBUG] delete_file_impl called with filename='{filename}' (type: {type(filename)})")
        
        file_path = DEMO_DIR / filename
        print(f"[DEBUG] File path: {file_path}")
        print(f"[DEBUG] File exists: {file_path.exists()}")
        
        if file_path.exists():
            file_path.unlink()
            return f"🗑️ File '{filename}' deleted successfully"
        else:
            return f"⚠️ File '{filename}' not found in {DEMO_DIR}"
    except Exception as e:
        import traceback
        print(f"[DEBUG] Exception: {e}")
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return f"❌ Error deleting file: {e}"


# ============================================================================
# Approval Callback
# ============================================================================

def ask_user_approval(approval_info: dict) -> bool:
    """Ask the user to approve or reject a function call."""
    print("\n" + "="*70)
    print("🚨 APPROVAL REQUIRED")
    print("="*70)
    print(f"📝 Function: {approval_info['function_name']}")
    print(f"📊 Arguments:")
    
    args = approval_info['arguments']
    if args['args']:
        for i, arg in enumerate(args['args']):
            print(f"   - Arg {i+1}: {arg}")
    if args['kwargs']:
        for key, value in args['kwargs'].items():
            print(f"   - {key}: {value}")
    
    print("-" * 70)
    
    while True:
        try:
            response = input("⚠️ Do you want to APPROVE this action? (yes/no): ").strip().lower()
        except EOFError:
            print("\n👋 Received EOF - treating as 'no'.")
            return False
        except KeyboardInterrupt:
            print("\n👋 Interrupted - treating as 'no'.")
            return False
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("   Please enter 'yes' or 'no'")


# ============================================================================
# Main Demo
# ============================================================================

async def main():
    """Run the Human-in-the-Loop demo."""
    
    print("\n" + "="*70)
    print("🔒 DEMO: Human-in-the-Loop - Create vs Delete")
    print("="*70)
    print("\n📋 This demo has 2 functions:")
    print("   ✅ create_file() - Runs immediately (no approval)")
    print("   🔒 delete_file() - Requires your approval first")
    
    # Wrap delete_file with approval requirement
    delete_file_approval = ApprovalRequiredTool(delete_file_impl, "Delete a file from the system")
    delete_file_approval.set_approval_callback(ask_user_approval)
    
    # Create agent with both functions
    # create_file runs immediately, delete_file asks for approval
    agent = AzureOpenAIChatClient(
        endpoint=ENDPOINT,
        deployment_name=DEPLOYMENT,
        api_key=API_KEY,
        api_version=API_VERSION
    ).create_agent(
        instructions="""You are a file management assistant with access to file operations.

IMPORTANT: You MUST call the functions directly. Do NOT ask the user for permission in chat.

Rules:
1. When user asks to create a file: IMMEDIATELY call create_file() function
2. When user asks to delete a file: IMMEDIATELY call delete_file_impl() function
3. Do NOT ask for confirmation in the chat - the system will handle approvals automatically
4. Just call the function and report the result""",
        name="FileBot",
        tools=[create_file, delete_file_approval]
    )
    
    print(f"\n✅ Agent created with 2 functions")
    print(f"📁 Files will be created in: {DEMO_DIR.absolute()}/")
    
    print("\n" + "="*70)
    print("💬 Interactive Chat (Type 'quit' to exit)")
    print("="*70)
    print("\n💡 Try these commands:")
    print("   • Create a file named test.txt with some content")
    print("   • Delete test.txt")
    print("   • Create file notes.txt saying 'Hello World'")
    print("   • Delete notes.txt")
    
    # Chat loop
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except EOFError:
            print("\n👋 Received EOF - exiting.")
            break
        except KeyboardInterrupt:
            print("\n👋 Interrupted - exiting.")
            break
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        print("Agent: ", end="", flush=True)
        
        # Stream the response
        async for chunk in agent.run_stream(user_input):
            print(chunk, end="", flush=True)
        
        print()  # New line after response


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 See you again soon.")
