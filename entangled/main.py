import argh  # type: ignore
import logging

try:
    from rich.logging import RichHandler
    from rich.highlighter import RegexHighlighter

    WITH_RICH = True
except ImportError:
    WITH_RICH = False


from .commands import tangle, stitch, sync, watch


if WITH_RICH:

    class BackTickHighlighter(RegexHighlighter):
        highlights = [r"`(?P<bold>[^`]*)`"]


def configure(debug=False):
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    if WITH_RICH:
        FORMAT = "%(message)s"
        logging.basicConfig(
            level=level,
            format=FORMAT,
            datefmt="[%X]",
            handlers=[RichHandler(show_path=debug, highlighter=BackTickHighlighter())],
        )
        logging.debug("Rich logging enabled")
    else:
        logging.basicConfig(level=level)
        logging.debug("Plain logging enabled")

    logging.info("Welcome to Entangled (https://entangled.github.io/)")


def cli():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", action="store_true", help="enable debug messages"
    )
    argh.add_commands(parser, [tangle, stitch, sync, watch])
    args = parser.parse_args()
    configure(args.debug)
    argh.dispatch(parser)


if __name__ == "__main__":
    cli()
