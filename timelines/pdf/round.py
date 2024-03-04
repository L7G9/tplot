from enum import Enum


class Round(Enum):
    """Enumeration class to specify if unit should be rounded up or down."""
    UP = 1
    DOWN = 2

    def up(self):
        return self.value == 1

    def down(self):
        return self.value == 2
