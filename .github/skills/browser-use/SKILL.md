---
name: browser-use
description: Automate browser interactions and tasks using CLI or Python. Use when testing web applications, capturing screenshots, extracting data, automating workflows, testing forms, or running autonomous browser agents. Supports local (Chromium, real Chrome) and cloud (remote) browsers. Keywords: browser automation, web scraping, screenshot, form submission, web testing, browser agent, automation workflow.
---

# Browser Automation with browser-use

Powerful browser automation for testing, data extraction, and autonomous task completion. Run browser commands persistently across sessions or use AI agents for complex workflows.

Use this skill when:

- Testing web applications and UI workflows
- Extracting data from websites
- Automating form submissions and interactions
- Taking screenshots and visual regression testing
- Running autonomous browser agents for complex tasks
- Using authenticated sessions (real Chrome with existing logins)
- Cloud-based browser automation with geographic proxies

## Installation

One-line install (recommended):

```
curl -fsSL https://browser-use.com/cli/install.sh | bash
```

This interactive installer configures everything automatically. Choose installation mode:

- Local-only: Fast, isolated Chromium (best for local development)
- Remote-only: Cloud browser via API (best for CI, no GUI required)
- Full: Both modes available (maximum flexibility)

Or install via pip:

```
uv pip install "browser-use[cli]"
browser-use install  # Install browser dependencies
```

Verify installation:

```
browser-use doctor
```

## Setup

Configure once:

```
browser-use setup                         # Interactive setup
browser-use setup --mode local            # Configure for local browser
browser-use setup --mode remote           # Configure for cloud browser
browser-use setup --api-key YOUR_KEY      # Set API key for cloud features
browser-use init                          # Generate template files
```

API key configuration (for cloud tasks):

1. Set via `--api-key` flag during commands
2. Set `BROWSER_USE_API_KEY` environment variable
3. Save to `~/.config/browser-use/config.json`

## Quick Start

Basic commands:

```
browser-use open https://example.com           # Navigate to URL
browser-use state                              # Get page elements with indices
browser-use click 5                            # Click element by index
browser-use type "Hello World"                 # Type in focused element
browser-use screenshot                        # Take screenshot
browser-use close                             # Close browser
```

## Core Workflow

Persistent session workflow:

1. Navigate: `browser-use open <url>` - opens URL and starts browser if needed
2. Inspect: `browser-use state` - returns clickable elements with indices
3. Interact: Use indices from state output to interact (click, type, etc.)
4. Verify: `browser-use state` or `browser-use screenshot` to confirm actions
5. Repeat: Browser stays open between commands, reusing session

The browser stays open across commands, maintaining session state, cookies, and history.

## Browser Modes

Choose the right browser for your task:

```
browser-use --browser chromium open <url>              # Fast, isolated, headless
browser-use --browser chromium --headed open <url>     # Visible window
browser-use --browser real open <url>                  # Your Chrome with logins
browser-use --browser remote open <url>                # Cloud browser (API key required)
```

Mode characteristics:

- chromium: Fast, clean, ideal for automation. No existing logins.
- real: Uses your actual Chrome with cookies, extensions, logged-in sessions
- remote: Cloud-hosted browser with proxy support, geographic flexibility

## Commands

### Navigation

```
browser-use open <url>                       # Navigate to URL
browser-use back                             # Go back in history
browser-use scroll down                      # Scroll down (default: 500px)
browser-use scroll up                        # Scroll up
browser-use scroll down --amount 1000        # Scroll specific pixel amount
```

### Page State and Inspection

```
browser-use state                            # Get URL, title, and clickable elements
browser-use screenshot                       # Take screenshot (outputs base64)
browser-use screenshot path.png              # Save screenshot to file
browser-use screenshot --full path.png       # Full page screenshot
browser-use get title                        # Get page title
browser-use get html                         # Get full page HTML
browser-use get html --selector "h1"         # Get HTML of specific element
```

### Interactions (use indices from state)

```
browser-use click <index>                    # Click element
browser-use type "text"                      # Type in focused element
browser-use input <index> "text"             # Click element, then type
browser-use keys "Enter"                     # Send keyboard key
browser-use keys "Control+a"                 # Send key combination
browser-use select <index> "option"          # Select dropdown option
browser-use hover <index>                    # Hover over element
browser-use dblclick <index>                 # Double-click element
browser-use rightclick <index>               # Right-click (context menu)
```

### Wait and Conditions

```
browser-use wait selector "h1"               # Wait for element visible
browser-use wait selector ".loading" --state hidden  # Wait for element to disappear
browser-use wait text "Success"              # Wait for text on page
browser-use wait selector "h1" --timeout 5000      # Custom timeout in ms
```

### Tab Management

```
browser-use switch <tab>                     # Switch to tab by index
browser-use close-tab                        # Close current tab
browser-use close-tab <tab>                  # Close specific tab
```

### Cookies

```
browser-use cookies get                      # Get all cookies
browser-use cookies set <name> <value>       # Set a cookie
browser-use cookies export <file>            # Export all cookies to JSON
browser-use cookies import <file>            # Import cookies from JSON
browser-use cookies clear                    # Clear all cookies
```

### Python Execution (Persistent Session)

Run Python code with persistent state:

```
browser-use python "x = 42"                  # Set variable
browser-use python "print(x)"                # Access variable (outputs: 42)
browser-use python "print(browser.url)"      # Access browser object
browser-use python --file script.py          # Execute Python file
```

Browser object provides:

- `browser.url` - Current page URL
- `browser.title` - Page title
- `browser.goto(url)` - Navigate to URL
- `browser.click(index)` - Click element
- `browser.type(text)` - Type text
- `browser.input(index, text)` - Click and type
- `browser.screenshot(path)` - Take screenshot
- `browser.scroll(direction, amount)` - Scroll
- `browser.wait(seconds)` - Pause execution
- `browser.extract(query)` - Extract data using LLM (requires API key)

## Autonomous Browser Agents

Run AI agents to complete complex browser tasks automatically (requires API key):

```
browser-use run "Fill the contact form with test data"
browser-use run "Extract all product prices" --max-steps 50
browser-use run "Log into GitHub and create a new repository"
```

Agent options:

```
browser-use -b remote run "task" --llm gpt-4o             # Specify LLM model
browser-use -b remote run "task" --proxy-country gb       # UK proxy
browser-use -b remote run "task" --start-url <url>        # Start from URL
browser-use -b remote run "task" --no-wait                # Async execution
browser-use -b remote run "task" --stream                 # Stream status updates
browser-use -b remote run "task" --thinking               # Extended reasoning mode
```

### Parallel Agents (Remote Mode)

Run multiple independent browser agents simultaneously:

```
# Start 3 research agents in parallel
browser-use -b remote run "Research competitor A pricing" --no-wait
# → task_id: task-1, session_id: sess-a

browser-use -b remote run "Research competitor B pricing" --no-wait
# → task_id: task-2, session_id: sess-b

browser-use -b remote run "Research competitor C pricing" --no-wait
# → task_id: task-3, session_id: sess-c

# Monitor progress
browser-use task list --status running
browser-use task status task-1
browser-use task status task-2
browser-use task status task-3
```

### Task Management

```
browser-use task list                        # List recent tasks
browser-use task status <task-id>            # Get task status
browser-use task status <task-id> -c         # Compact view (full reasoning)
browser-use task status <task-id> -v         # Verbose view (actions + URLs)
browser-use task stop <task-id>              # Stop a running task
browser-use task logs <task-id>              # Get task execution logs
```

### Session Management

```
browser-use session list                     # List active cloud sessions
browser-use session get <session-id>         # Get session details
browser-use session stop <session-id>        # Stop a session
browser-use session create                   # Create new cloud session
browser-use session share <session-id>       # Create public share URL for collaboration
```

## Real Chrome Profiles (Logged-In Sessions)

Use your actual Chrome with existing logins and extensions:

```
browser-use -b real profile list             # List available Chrome profiles
browser-use -b real --profile "Work" open https://gmail.com   # Use specific profile
browser-use --browser real open https://github.com            # Fresh profile (no logins)
```

Each Chrome profile maintains separate cookies, history, and logged-in sessions. Ask the user which profile they want to use.

## Cloud Profiles (Remote Mode)

Store browser state in cloud for persistence across sessions:

```
browser-use -b remote profile list           # List cloud profiles
browser-use -b remote profile create --name "My Profile"  # Create profile
browser-use -b remote --profile <id> open https://example.com
```

Cloud profiles preserve cookies across sessions, useful for maintaining authentication state.

## Exposing Local Dev Servers

Test local dev servers with cloud browsers:

```
npm run dev &                                # Start local dev server (localhost:3000)
browser-use tunnel 3000                      # Expose via Cloudflare tunnel
# → url: https://abc.trycloudflare.com

browser-use --browser remote open https://abc.trycloudflare.com  # Cloud browser reaches local server
```

Tunnel commands:

```
browser-use tunnel <port>                    # Start tunnel
browser-use tunnel list                      # Show active tunnels
browser-use tunnel stop <port>               # Stop tunnel
```

## Multi-Session Workflows

Run multiple independent browser sessions in parallel:

```
browser-use --session work open https://work.example.com
browser-use --session personal open https://personal.example.com
browser-use --session work state             # Check work session
browser-use --session personal state         # Check personal session
browser-use close --all                      # Close both
```

Each `--session NAME` maintains its own browser instance and state.

## Examples

### Form Submission

```
browser-use open https://example.com/contact
browser-use state
# Shows: [0] input "Name", [1] input "Email", [2] textarea "Message", [3] button "Submit"
browser-use input 0 "John Doe"
browser-use input 1 "john@example.com"
browser-use input 2 "Hello, this is a test message."
browser-use click 3
browser-use state  # Verify success
```

### Screenshot Loop for Visual Testing

```
browser-use open https://example.com
for i in 1 2 3 4 5; do
  browser-use scroll down
  browser-use screenshot "page_$i.png"
done
```

### Data Extraction with Python

```
browser-use open https://example.com/products
browser-use python "products = []"
browser-use python "
for i in range(20):
    browser.scroll('down')
    # Extract product data
"
browser-use screenshot products.png
```

### Using Real Browser with Logins

```
browser-use -b real open https://gmail.com
# Already logged in with your Gmail account!
browser-use state                            # See your inbox
browser-use input 0 "Your reply text"       # Compose email
```

## Tips

1. Always run `browser-use state` first to see available elements and indices
2. Use `--headed` with chromium mode to see browser actions in real-time
3. Sessions persist - browser stays open between commands
4. Use `--json` flag to parse output programmatically
5. Python variables persist across `browser-use python` commands in same session
6. Real browser mode preserves logins and extensions
7. CLI aliases work: `bu`, `browser`, `browseruse` (shortcuts for `browser-use`)

## Cleanup

Always close the browser when done:

```
browser-use close              # Close current session
browser-use session stop --all # Close all cloud sessions
```
