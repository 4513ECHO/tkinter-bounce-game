import enum
import time
from tkinter import Canvas, Tk
from typing import Optional, Protocol


class Drawable(Protocol):
    id: int
    role: str

    def draw(self) -> None:
        ...


class State(enum.Enum):
    Starting = enum.auto()
    Runnning = enum.auto()
    Paused = enum.auto()
    Quited = enum.auto()


class Context:
    def __init__(self) -> None:
        self._tk = Tk()
        self._tk.title("Bounce Game")
        self._tk.resizable(False, False)
        self._tk.wm_attributes("-topmost", True)
        self._tk.protocol("WM_DELETE_WINDOW", self._quit)
        self.canvas = Canvas(
            self._tk, width=500, height=400, bd=0, highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind_all("<KeyPress-space>", self._start)
        self._tk.update()
        self._sprites: list[Drawable] = []
        self._showing = True
        self.canvas_height: int = self.canvas.winfo_height()
        self.canvas_width: int = self.canvas.winfo_width()
        self.state = State.Starting
        self.point = 0

    def get_sprite(self, role: str) -> Optional[Drawable]:
        for sprite in self._sprites:
            if sprite.role == role:
                return sprite
        return None

    def register_sprite(self, sprite: Drawable) -> None:
        self._sprites.append(sprite)

    def point_up(self) -> None:
        self.point += 10

    def mainloop(self) -> None:
        while self._showing:
            if self.state == State.Runnning:
                for sprite in self._sprites:
                    sprite.draw()
            self._tk.update_idletasks()
            self._tk.update()
            time.sleep(0.01)

    def _start(self, event: object) -> None:
        if self.state == State.Starting:
            self.state = State.Runnning

    def _quit(self) -> None:
        self._showing = False
        self._tk.destroy()
