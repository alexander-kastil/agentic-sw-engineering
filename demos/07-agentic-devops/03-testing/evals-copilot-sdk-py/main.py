import asyncio
import sys

from menu_assistant import MenuAssistant


async def main() -> None:
    assistant = MenuAssistant()
    if len(sys.argv) > 1:
        print(await assistant.ask(" ".join(sys.argv[1:])))
        return
    while True:
        question = input("> ").strip()
        if not question:
            break
        print(await assistant.ask(question))


asyncio.run(main())
