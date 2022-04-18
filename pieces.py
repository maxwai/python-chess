from enum import Enum
import pygame
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

    def add_image(self, surface: Surface | SurfaceType):
        surface.blit(self.image, (self.x * self.square_size + self.shift, self.y * self.square_size + self.shift))


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
