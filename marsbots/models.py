from dataclasses import dataclass


@dataclass
class Message:
    text: str
    user: str
    delineator_left: str = "<"
    delineator_right: str = ">"

    def __str__(self):
        return f"{self.delineator_left}{self.user}{self.delineator_right} {self.text}"
