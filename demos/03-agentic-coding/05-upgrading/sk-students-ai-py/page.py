from html import escape
from pathlib import Path
from string import Template

TEMPLATE = Template((Path(__file__).parent / "templates" / "index.html").read_text(encoding="utf-8"))


def render(reply: str | None = None) -> str:
    block = f'<p class="reply" id="reply">{escape(reply)}</p>' if reply else ""
    return TEMPLATE.substitute(reply=block)
