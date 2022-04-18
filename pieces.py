from enum import Enum
import pygame
from pygame.rect import Rect, RectType
from pygame.surface import Surface, SurfaceType


class Team(Enum):
    BLACK = "b"
    WHITE = "w"


class Piece:
    def __init__(self, team: Team, x: int, y: int, name: str, square_size: int):
        self.team: Team = team
        self.square_size = square_size
        self.shift = self.square_size * 0.05
        self.image: Surface | SurfaceType = pygame.image.load(f"images/{self.team.value}_{name}.svg")
        self.image = pygame.transform.scale(self.image, (square_size * 0.9, square_size * 0.9))
        self.x: int = x
        self.y: int = y
        self.rect: Rect | RectType | None = pygame.Rect((self.x * self.square_size + self.shift,
                                                         (7 - self.y) * self.square_size + self.shift,
                                                         self.square_size * 0.9, self.square_size * 0.9))

    def add_image(self, surface: Surface | SurfaceType, update: bool = True):
        surface.blit(self.image, self.rect)
        if update:
            pygame.display.update(self.rect)

    def move_image(self, surface: Surface | SurfaceType, new_position: (float, float), update: bool = True):
        self.rect.center = new_position
        self.add_image(surface, update=update)

    def get_position(self) -> (int, int):
        return self.x, self.y

    def set_position(self, surface: Surface | SurfaceType, new_position: (int, int), update: bool = True):
        (self.x, self.y) = new_position
        self.rect = pygame.Rect((self.x * self.square_size + self.shift,
                                 (7 - self.y) * self.square_size + self.shift,
                                 self.square_size * 0.9, self.square_size * 0.9))
        self.add_image(surface, update=update)


class Pawn(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(Pawn, self).__init__(team, x, y, "pawn", square_size)


class King(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(King, self).__init__(team, x, y, "king", square_size)


class Rook(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(Rook, self).__init__(team, x, y, "rook", square_size)


class Bishop(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(Bishop, self).__init__(team, x, y, "bishop", square_size)


class Queen(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(Queen, self).__init__(team, x, y, "queen", square_size)


class Knight(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(Knight, self).__init__(team, x, y, "knight", square_size)
