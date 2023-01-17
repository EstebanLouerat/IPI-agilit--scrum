from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace

import pytermgui as ptg

PALETTE_LIGHT = "#FCBA03"
PALETTE_MID = "#8C6701"
PALETTE_DARK = "#4D4940"
PALETTE_DARKER = "#242321"


def _process_arguments(argv: list[str] | None = None) -> Namespace:
    """Processes command line arguments.
    Note that you don't _have to_ use the bultin argparse module for this; it
    is just what the module uses.
    Args:
        argv: A list of command line arguments, not including the binary path
            (sys.argv[0]).
    """

    parser = ArgumentParser(description="My first PTG application.")

    return parser.parse_args(argv)


def _create_aliases() -> None:
    """Creates all the TIM aliases used by the application.
    Aliases should generally follow the following format:
        namespace.item
    For example, the title color of an app named "myapp" could be something like:
        myapp.title
    """
    ptg.tim.alias("app.title", f"bold {PALETTE_LIGHT}")
    ptg.tim.alias("app.footer", f"@{PALETTE_DARKER}")


def _configure_widgets() -> None:
    """Defines all the global widget configurations.
    Some example lines you could use here:
        ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
        ptg.Splitter.set_char("separator", " ")
        ptg.Button.styles.label = "myapp.button.label"
        ptg.Container.styles.border__corner = "myapp.border"
    """

    ptg.boxes.SINGLE.set_chars_of(ptg.Window)


def _define_layout() -> ptg.Layout:
    """Defines the application layout.
    Layouts work based on "slots" within them. Each slot can be given dimensions for
    both width and height. Integer values are interpreted to mean a static width, float
    values will be used to "scale" the relevant terminal dimension, and giving nothing
    will allow PTG to calculate the corrent dimension.
    """

    layout = ptg.Layout()

    # A header slot with a height of 1
    layout.add_slot("Header", height=1)
    layout.add_break()

    # A body slot that will fill the entire width, and the height is remaining
    layout.add_slot("Body", width=0.5)

    # A slot in the same row as body, using the full non-occupied height and
    # 20% of the terminal's width.
    layout.add_slot("Body right", width=0.5)

    layout.add_break()

    # A footer with a static height of 1
    layout.add_slot("Footer", height=1)

    return layout

def _confirm_quit(manager: ptg.WindowManager) -> None:
    """Creates an "Are you sure you want to quit" modal window"""

    modal = ptg.Window(
        "[app.title]Are you sure you want to quit?",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: manager.stop()),
                ptg.Button("No", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)
    
def _add_command(manager: ptg.WindowManager, text: str) -> None:
    modal = ptg.Window(
        f"[app.title] {text}",
        "",
        ptg.Button(" Afficher "),
        ptg.Button(" Modifier "),
        ptg.Button(" Supprimer "),
        ptg.Container(
            ptg.Splitter(
                ptg.Button("return", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)

def _view_tables(manager: ptg.WindowManager) -> None:

    modal = ptg.Window(
        f"[app.title] View Tables",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("-1-", lambda *_: _add_command(manager, "1")),
                ptg.Button("-2-", lambda *_: _add_command(manager, "2")),
                ptg.Button("-3-", lambda *_: _add_command(manager, "3")),
                ptg.Button("-4-", lambda *_: _add_command(manager, "4")),
            ),
        ),
        ptg.Container(
            ptg.Splitter(
                ptg.Button("-5-", lambda *_: _add_command(manager, "5")),
                ptg.Button("-6-", lambda *_: _add_command(manager, "6")),
                ptg.Button("-7-", lambda *_: _add_command(manager, "7")),
                ptg.Button("-8-", lambda *_: _add_command(manager, "8")),
            ),
        ),
        ptg.Container(
            ptg.Splitter(
                ptg.Button("-9-", lambda *_: _add_command(manager, "9")),
                ptg.Button("-10-", lambda *_: _add_command(manager, "10")),
            ),
        ),
        ptg.Container(
            ptg.Splitter(
                ptg.Button("return", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)


def main(argv: list[str] | None = None) -> None:
    """Runs the application."""

    _create_aliases()
    _configure_widgets()

    args = _process_arguments(argv)

    with ptg.WindowManager() as manager:
        manager.layout = _define_layout()

        header = ptg.Window(
            "Gestion de Restaurant ",
            box="EMPTY",
        )

        # Since header is the first defined slot, this will assign to the correct place
        manager.add(header)

        footer = ptg.Window(
            ptg.Button("Quit", lambda *_: _confirm_quit(manager)),
            box="EMPTY",
        )
        footer.styles.fill = "app.footer"

        # Since the second slot, body was not assigned to, we need to manually assign
        # to "footer"
        manager.add(footer, assign="footer")
        
        body_rigth = ptg.Window(
            ptg.Button("View tables", lambda *_: _view_tables(manager)),
            box="EMPTY"
        )
        
        body_rigth.select(1)
        manager.add(body_rigth, assign="body_right")

        body = ptg.Window(
            ptg.Button("Manage orders", lambda *_: _add_command(manager, "order")),
            "\n",
            ptg.Button("Manage order per table", lambda *_: _add_command(manager, "order")),
            "\n",
            ptg.Button("Manage menu", lambda *_: _add_command(manager, "menu")),
            "\n",
            ptg.Button("Price per table", lambda *_: _add_command(manager, "table")),
            box="EMPTY"
        )
        
        manager.add(body, assign="body")

    ptg.tim.print("[!gradient(210)]Goodbye!")


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # test