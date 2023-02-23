from __future__ import annotations

import random
from tkinter import Event, Misc
from typing import Optional

from .context import Context, Drawable, State


class Ball:
    role = "ball"

    def __init__(self, context: Context, *, color: str = "red", speed: int = 3) -> None:
        self._context = context
        self.id: int = context.canvas.create_oval(10, 10, 25, 25, fill=color)
        context.canvas.move(self.id, 245, 100)
        self._speed = speed
        self._x = random.choice([-3, -2, -1, 1, 2, 3])
        self._y = -self._speed
        self._paddle: Optional[Drawable] = None

    def draw(self) -> None:
        self._context.canvas.move(self.id, self._x, self._y)
        pos = self._context.canvas.coords(self.id)
        if pos[1] <= 0:
            self._y = self._speed
        if pos[3] >= self._context.canvas_height:
            self._context.state = State.Quited
        if self._is_hit_paddle(pos):
            self._context.point_up()
            self._y = -self._speed
        if pos[0] <= 0:
            self._x = self._speed
        if pos[2] >= self._context.canvas_width:
            self._x = -self._speed

    def _is_hit_paddle(self, pos: list[float]) -> bool:
        if self._paddle is None:
            self._paddle = self._context.get_sprite("paddle")
            if self._paddle is None:
                return False
        paddle_pos = self._context.canvas.coords(self._paddle.id)
        return (
            pos[2] >= paddle_pos[0]
            and pos[0] <= paddle_pos[2]
            and paddle_pos[3] >= pos[3] >= paddle_pos[1]
        )


class Paddle:
    role = "paddle"

    def __init__(
        self, context: Context, *, color: str = "blue", speed: int = 3
    ) -> None:
        self._context = context
        self.id: int = context.canvas.create_rectangle(0, 0, 100, 10, fill=color)
        context.canvas.move(self.id, 200, 300)
        self._speed = speed
        self._x = 0
        context.canvas.bind_all("<KeyPress-Left>", self._turn)
        context.canvas.bind_all("<KeyPress-Right>", self._turn)

    def draw(self) -> None:
        self._context.canvas.move(self.id, self._x, 0)
        pos = self._context.canvas.coords(self.id)
        if pos[0] <= 0:
            self._x = 0
        if pos[2] >= self._context.canvas_width:
            self._x = 0

    def _turn(self, event: Event[Misc]) -> None:
        pos = self._context.canvas.coords(self.id)
        match event.keysym:
            case "Left" if pos[0] >= 0:
                self._x = -self._speed
            case "Right" if pos[2] <= self._context.canvas_width:
                self._x = self._speed


class PointCounter:
    role = "pointcounter"

    def __init__(self, context: Context) -> None:
        self._context = context
        self.id = context.canvas.create_text(
            20, 10, text="{:>4}".format(self._context.point), font=("Monospace", 10)
        )

    def draw(self) -> None:
        self._context.canvas.itemconfigure(
            self.id, text="{:>4}".format(self._context.point)
        )


class OverlayText:
    role = "overlaytext"

    def __init__(self, context: Context) -> None:
        self._context = context
        self.id = context.canvas.create_text(
            250,
            200,
            text="Press <Space> to start",
            font=("Monospace", 15),
            state="normal",
        )
        self._hidden = False

    def draw(self) -> None:
        match self._context.state:
            case State.Runnning if not self._hidden:
                self._hidden = True
                self._context.canvas.itemconfigure(
                    self.id,
                    state="hidden",
                )
            case State.Quited:
                self._context.canvas.itemconfigure(
                    self.id,
                    text="Game Over",
                    fill="red",
                    font=("Monospace", 30),
                    state="normal",
                )
