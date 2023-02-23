from .context import Context
from .sprite import Ball, OverlayText, Paddle, PointCounter


def main() -> None:
    context = Context()
    context.register_sprite(Ball(context))
    context.register_sprite(Paddle(context))
    context.register_sprite(PointCounter(context))
    context.register_sprite(OverlayText(context))
    try:
        context.mainloop()
    except KeyboardInterrupt:
        return


main()
