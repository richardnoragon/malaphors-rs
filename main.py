import sys

from malaphor_cli import main as cli_main
from malaphor_ui import MalaphorApp

if __name__ == "__main__":
    if len(sys.argv) > 1:
        raise SystemExit(cli_main(sys.argv[1:]))

    app = MalaphorApp()
    app.run()