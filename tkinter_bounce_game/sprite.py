from __future__ import annotations

import random
from tkinter import Event, Misc
from typing import Callable, Optional

from .context import Context, Drawable, State


class Ball(Drawable):
    role = "ball"

    def __init__(self, *, color: str = "red", speed: int = 3) -> None:
        self.__color = color
        self.__speed = speed
        self.__x = random.choice([-3, -2, -1, 1, 2, 3])
        self.__y = -self.__speed
        self.__paddle: Optional[Drawable] = None

    def draw(self, context: Context) -> None:
        if context.state == State.Starting:
            self.id: int = context.canvas.create_oval(10, 10, 25, 25, fill=self.__color)
            context.canvas.move(self.id, 245, 100)
            return
        context.canvas.move(self.id, self.__x, self.__y)
        pos = context.canvas.coords(self.id)
        if pos[1] <= 0:
            self.__y = self.__speed
        if pos[3] >= context.canvas_height:
            context.state = State.Quited
        if self.__is_hit_paddle(pos, context):
            context.point_up()
            self.__y = -self.__speed
        if pos[0] <= 0:
            self.__x = self.__speed
        if pos[2] >= context.canvas_width:
            self.__x = -self.__speed

    def __is_hit_paddle(self, pos: list[float], context: Context) -> bool:
        self.__paddle = self.__paddle or context.get_sprite("paddle")
        if self.__paddle is None:
            return False
        paddle_pos = context.canvas.coords(self.__paddle.id)
        return (
            pos[2] >= paddle_pos[0]
            and pos[0] <= paddle_pos[2]
            and paddle_pos[3] >= pos[3] >= paddle_pos[1]
        )


class Paddle(Drawable):
    role = "paddle"

    def __init__(self, *, color: str = "blue", speed: int = 3) -> None:
        self.__color = color
        self.__speed = speed
        self.__x = 0

    def draw(self, context: Context) -> None:
        if context.state == State.Starting:
            self.id: int = context.canvas.create_rectangle(
                0, 0, 100, 10, fill=self.__color
            )
            context.canvas.move(self.id, 200, 300)
            context.canvas.bind_all("<KeyPress-Left>", self.__turn(context))
            context.canvas.bind_all("<KeyPress-Right>", self.__turn(context))
            return
        context.canvas.move(self.id, self.__x, 0)
        pos = context.canvas.coords(self.id)
        if pos[0] <= 0 or pos[2] >= context.canvas_width:
            self.__x = 0

    def __turn(self, context: Context) -> Callable[[Event[Misc]], None]:
        def inner(event: Event[Misc]) -> None:
            pos = context.canvas.coords(self.id)
            match event.keysym:
                case "Left" if not pos[0] <= 0:
                    self.__x = -self.__speed
                case "Right" if not pos[2] >= context.canvas_width:
                    self.__x = self.__speed

        return inner


class PointCounter(Drawable):
    role = "pointcounter"

    def draw(self, context: Context) -> None:
        if context.state == State.Starting:
            self.id = context.canvas.create_text(
                20, 10, text="{:>4}".format(context.point), font=("Monospace", 10)
            )
            return
        context.canvas.itemconfigure(self.id, text="{:>4}".format(context.point))


class OverlayText(Drawable):
    role = "overlaytext"

    def __init__(self) -> None:
        self.__hidden = False

    def draw(self, context: Context) -> None:
        match context.state:
            case State.Starting:
                self.id = context.canvas.create_text(
                    250,
                    200,
                    text="Press <Space> to start",
                    font=("Monospace", 15),
                    state="normal",
                )
            case State.Runnning if not self.__hidden:
                self.__hidden = True
                context.canvas.itemconfigure(
                    self.id,
                    state="hidden",
                )
            case State.Quited:
                context.canvas.itemconfigure(
                    self.id,
                    text="Game Over",
                    fill="red",
                    font=("Monospace", 30),
                    state="normal",
                )
