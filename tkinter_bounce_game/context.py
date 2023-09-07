from __future__ import annotations

import enum
import time
from tkinter import Canvas, Event, Misc, Tk
from typing import Optional, Protocol


class Drawable(Protocol):
    id: int
    role: str

    def draw(self, context: Context) -> None:
        ...


class State(enum.Enum):
    Starting = enum.auto()
    Runnning = enum.auto()
    Paused = enum.auto()
    Quited = enum.auto()


class Context:
    def __init__(self) -> None:
        self.__tk = Tk()
        self.__tk.title("Bounce Game")
        self.__tk.resizable(False, False)
        self.__tk.wm_attributes("-topmost", True)
        self.__tk.protocol("WM_DELETE_WINDOW", self.__quit)
        self.__canvas = Canvas(
            self.__tk, width=500, height=400, bd=0, highlightthickness=0
        )
        self.__canvas.pack()
        self.__canvas.bind_all("<KeyPress-space>", self.__start)
        self.__tk.update()
        self.__sprites: list[Drawable] = []
        self.__showing = True
        self.__canvas_height: int = self.__canvas.winfo_height()
        self.__canvas_width: int = self.__canvas.winfo_width()
        self.state = State.Starting
        self.__point = 0

    @property
    def canvas(self) -> Canvas:
        return self.__canvas

    @property
    def canvas_height(self) -> int:
        return self.__canvas_height

    @property
    def canvas_width(self) -> int:
        return self.__canvas_width

    def get_sprite(self, role: str) -> Optional[Drawable]:
        for sprite in self.__sprites:
            if sprite.role == role:
                return sprite
        return None

    def register_sprite(self, sprite: Drawable) -> None:
        self.__sprites.append(sprite)

    @property
    def point(self) -> int:
        return self.__point

    def point_up(self) -> None:
        self.__point += 10

    def mainloop(self) -> None:
        for sprite in self.__sprites:
            sprite.draw(self)
        while self.__showing:
            if self.state == State.Runnning:
                for sprite in self.__sprites:
                    sprite.draw(self)
            self.__tk.update_idletasks()
            self.__tk.update()
            time.sleep(0.01)

    def __start(self, event: Event[Misc]) -> None:
        if self.state == State.Starting:
            self.state = State.Runnning

    def __quit(self) -> None:
        self.__showing = False
        self.__tk.destroy()
