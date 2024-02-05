from rich.console import Console
from rich.markdown import Markdown
import sys

if __name__ == "__main__":
    console = Console(markup=False, highlight=False, color_system="256")
    logging_path = sys.argv[1]
    with open(logging_path, 'r') as f:
        text = f.read()
        console.print(Markdown(text), width=72)