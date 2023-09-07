from .context import Context
from .sprite import Ball, OverlayText, Paddle, PointCounter


def main() -> None:
    context = Context()
    context.register_sprite(Ball())
    context.register_sprite(Paddle())
    context.register_sprite(PointCounter())
    context.register_sprite(OverlayText())
    try:
        context.mainloop()
    except KeyboardInterrupt:
        return


main()
