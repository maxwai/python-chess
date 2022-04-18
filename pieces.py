from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum

import pygame
from pygame.rect import Rect, RectType
from pygame.surface import Surface, SurfaceType


class Team(Enum):
    BLACK = "b"
    WHITE = "w"


class Piece(ABC):
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

    @abstractmethod
    def get_possible_moves(self, pieces: list[Piece]) -> list[(int, int)]:
        pass

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

    def _check_straights(self, pieces: list[Piece]) -> list[(int, int)]:
        possible_moves: list[(int, int)] = list()
        for i in range(self.x + 1, 8):
            piece_on_position: list[Piece] = [piece for piece in pieces if piece.get_position() == (i, self.y)]
            if piece_on_position:
                if piece_on_position[0].team != self.team:
                    possible_moves.append((i, self.y))
                break
            possible_moves.append((i, self.y))
        for i in range(self.x - 1, -1, -1):
            piece_on_position: list[Piece] = [piece for piece in pieces if piece.get_position() == (i, self.y)]
            if piece_on_position:
                if piece_on_position[0].team != self.team:
                    possible_moves.append((i, self.y))
                break
            possible_moves.append((i, self.y))
        for i in range(self.y + 1, 8):
            piece_on_position: list[Piece] = [piece for piece in pieces if piece.get_position() == (self.x, i)]
            if piece_on_position:
                if piece_on_position[0].team != self.team:
                    possible_moves.append((self.x, i))
                break
            possible_moves.append((self.x, i))
        for i in range(self.y - 1, -1, -1):
            piece_on_position: list[Piece] = [piece for piece in pieces if piece.get_position() == (self.x, i)]
            if piece_on_position:
                if piece_on_position[0].team != self.team:
                    possible_moves.append((self.x, i))
                break
            possible_moves.append((self.x, i))
        return possible_moves

    def _check_diagonals(self, pieces: list[Piece]) -> list[(int, int)]:
        possible_moves: list[(int, int)] = list()
        for i in range(1, 8):
            if self.x + i < 8 and self.y + i < 8:
                piece_on_position: list[Piece] = [piece for piece in pieces if
                                                  piece.get_position() == (self.x + i, self.y + i)]
                if piece_on_position:
                    if piece_on_position[0].team != self.team:
                        possible_moves.append((self.x + i, self.y + i))
                    break
                possible_moves.append((self.x + i, self.y + i))
        for i in range(1, 8):
            if self.x - i > -1 and self.y + i < 8:
                piece_on_position: list[Piece] = [piece for piece in pieces if
                                                  piece.get_position() == (self.x - i, self.y + i)]
                if piece_on_position:
                    if piece_on_position[0].team != self.team:
                        possible_moves.append((self.x - i, self.y + i))
                    break
                possible_moves.append((self.x - i, self.y + i))
        for i in range(1, 8):
            if self.x + i < 8 and self.y - i > -1:
                piece_on_position: list[Piece] = [piece for piece in pieces if
                                                  piece.get_position() == (self.x + i, self.y - i)]
                if piece_on_position:
                    if piece_on_position[0].team != self.team:
                        possible_moves.append((self.x + i, self.y - i))
                    break
                possible_moves.append((self.x + i, self.y - i))
        for i in range(1, 8):
            if self.x - i > -1 and self.y - i > -1:
                piece_on_position: list[Piece] = [piece for piece in pieces if
                                                  piece.get_position() == (self.x - i, self.y - i)]
                if piece_on_position:
                    if piece_on_position[0].team != self.team:
                        possible_moves.append((self.x - i, self.y - i))
                    break
                possible_moves.append((self.x - i, self.y - i))

        return possible_moves


class Pawn(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(Pawn, self).__init__(team, x, y, "pawn", square_size)

    def get_possible_moves(self, pieces: list[Piece]) -> list[(int, int)]:
        # TODO: add en-passant, promotion
        possible_moves: list[(int, int)] = list()

        if self.team == Team.WHITE:
            positions_to_test: list[(int, int)] = [(self.x + 1, self.y + 1), (self.x - 1, self.y + 1)]
        else:
            positions_to_test: list[(int, int)] = [(self.x - 1, self.y - 1), (self.x + 1, self.y - 1)]

        for (x, y) in positions_to_test:
            if -1 < x < 8 and -1 < y < 8 and [piece for piece in pieces if
                                              piece.get_position() == (x, y) and piece.team != self.team]:
                possible_moves.append((x, y))

        positions_to_test: list[(int, int)] = [(self.x, self.y + (1 if self.team == Team.WHITE else -1)),
                                               (self.x, self.y + (2 if self.team == Team.WHITE else -2))]

        if self.y != 7 and not [piece for piece in pieces if piece.get_position() == positions_to_test[0]]:
            possible_moves.append(positions_to_test[0])
            if self.y == 1 and not [piece for piece in pieces if piece.get_position() == positions_to_test[1]]:
                possible_moves.append(positions_to_test[1])
        return possible_moves


class King(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(King, self).__init__(team, x, y, "king", square_size)

    def get_possible_moves(self, pieces: list[Piece]) -> list[(int, int)]:
        # TODO: add Castle
        possible_moves: list[(int, int)] = list()

        positions_to_test: list[(int, int)] = [(self.x, self.y + 1), (self.x, self.y - 1),
                                               (self.x + 1, self.y), (self.x - 1, self.y)]

        for (x, y) in positions_to_test:
            if -1 < x < 8 and -1 < y < 8 and not [piece for piece in pieces if
                                                  piece.get_position() == (x, y) and piece.team == self.team]:
                possible_moves.append((x, y))
        return possible_moves


class Rook(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(Rook, self).__init__(team, x, y, "rook", square_size)

    def get_possible_moves(self, pieces: list[Piece]) -> list[(int, int)]:
        return super()._check_straights(pieces)


class Bishop(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(Bishop, self).__init__(team, x, y, "bishop", square_size)

    def get_possible_moves(self, pieces: list[Piece]) -> list[(int, int)]:
        return super()._check_diagonals(pieces)


class Queen(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(Queen, self).__init__(team, x, y, "queen", square_size)

    def get_possible_moves(self, pieces: list[Piece]) -> list[(int, int)]:
        return super()._check_straights(pieces) + super()._check_diagonals(pieces)


class Knight(Piece):
    def __init__(self, team: Team, x: int, y: int, square_size: int):
        super(Knight, self).__init__(team, x, y, "knight", square_size)

    def get_possible_moves(self, pieces: list[Piece]) -> list[(int, int)]:
        possible_moves: list[(int, int)] = list()

        positions_to_test: list[(int, int)] = [(self.x + 2, self.y + 1), (self.x - 2, self.y + 1),
                                               (self.x + 2, self.y - 1), (self.x - 2, self.y - 1),
                                               (self.x + 1, self.y + 2), (self.x - 1, self.y + 2),
                                               (self.x + 1, self.y - 2), (self.x - 1, self.y - 2)]

        for (x, y) in positions_to_test:
            if -1 < x < 8 and -1 < y < 8 and not [piece for piece in pieces if
                                                  piece.get_position() == (x, y) and piece.team == self.team]:
                possible_moves.append((x, y))
        return possible_moves
