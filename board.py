from pygame.rect import Rect, RectType

from pieces import *

colors = [(238, 238, 210), (118, 150, 86)]


def get_square_color(row: int, col: int) -> (int, int, int):
    return colors[(row % 2 + col + 1) % 2]


class Board:

    def __init__(self, surface: Surface | SurfaceType):
        self.display_size: int = surface.get_size()[0]
        self.square_size: int = self.display_size // 8

        self.pieces: list[Piece] = list()
        for x in range(8):
            self.pieces.append(Pawn(Team.WHITE, x, 1, self.square_size))
            self.pieces.append(Pawn(Team.BLACK, x, 6, self.square_size))

        self.pieces.append(Rook(Team.WHITE, 0, 0, self.square_size))
        self.pieces.append(Rook(Team.WHITE, 7, 0, self.square_size))
        self.pieces.append(Rook(Team.BLACK, 0, 7, self.square_size))
        self.pieces.append(Rook(Team.BLACK, 7, 7, self.square_size))

        self.pieces.append(Bishop(Team.WHITE, 2, 0, self.square_size))
        self.pieces.append(Bishop(Team.WHITE, 5, 0, self.square_size))
        self.pieces.append(Bishop(Team.BLACK, 2, 7, self.square_size))
        self.pieces.append(Bishop(Team.BLACK, 5, 7, self.square_size))

        self.pieces.append(Knight(Team.WHITE, 1, 0, self.square_size))
        self.pieces.append(Knight(Team.WHITE, 6, 0, self.square_size))
        self.pieces.append(Knight(Team.BLACK, 1, 7, self.square_size))
        self.pieces.append(Knight(Team.BLACK, 6, 7, self.square_size))

        self.pieces.append(King(Team.WHITE, 3, 0, self.square_size))
        self.pieces.append(King(Team.BLACK, 3, 7, self.square_size))

        self.pieces.append(Queen(Team.WHITE, 4, 0, self.square_size))
        self.pieces.append(Queen(Team.BLACK, 4, 7, self.square_size))

        self.squares: dict[(int, int): Rect | RectType] = dict()
        for row in range(8):
            for col in range(8):
                self.squares[(row, col)] = surface.fill(get_square_color(row, col), self.get_square(row, col))
                pygame.display.update(self.squares[(row, col)])

    def get_square(self, x: int, y: int) -> (int, int, int, int):
        return x * self.square_size, (7 - y) * self.square_size, self.square_size, self.square_size

    def draw_pieces(self, surface: Surface | SurfaceType):
        for piece in self.pieces:
            piece.add_image(surface)

    def get_piece_at_coordinates(self, coordinates: (float, float)) -> Piece | None:
        for (position, square) in self.squares.items():
            if square.collidepoint(coordinates):
                return self.get_piece_at_position(*position)
        return None

    def get_piece_at_position(self, x: int, y: int) -> Piece | None:
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
        return None

    def move_piece_to_coordinates(self, surface: Surface | SurfaceType, piece_to_move: Piece, new_position: (float, float)):
        for (position, square) in self.squares.items():
            square: Rect | RectType
            if square.colliderect(piece_to_move.rect):
                self.squares[position] = surface.fill(get_square_color(*position),
                                                      self.get_square(*position))
                possible_piece = self.get_piece_at_position(*position)
                if possible_piece:
                    possible_piece.add_image(surface, update=False)

        piece_to_move.move_image(surface, new_position, update=False)

    def snap_to_position(self, surface: Surface | SurfaceType, piece_to_move: Piece, new_position: (float, float)):
        self.move_piece_to_coordinates(surface, piece_to_move, pygame.mouse.get_pos())
        for (position, square) in self.squares.items():
            square: Rect | RectType
            if square.colliderect(piece_to_move.rect):
                self.squares[position] = surface.fill(get_square_color(*position),
                                                      self.get_square(*position))
                possible_piece = self.get_piece_at_position(*position)
                if possible_piece:
                    possible_piece.add_image(surface, update=False)

        for (position, square) in self.squares.items():
            if square.collidepoint(new_position):
                piece_to_move.set_position(surface, position, update=False)

    def move_piece_to_position(self, surface: Surface | SurfaceType, current_position: (int, int),
                               new_position: (int, int)):
        piece_to_move: Piece | None = self.get_piece_at_position(*current_position)
        if not piece_to_move:
            return
        self.squares[current_position] = surface.fill(get_square_color(*current_position),
                                                      self.get_square(*current_position))
        pygame.display.update(self.squares[current_position])
        piece_to_move.set_position(surface, new_position)

    def delete_piece(self, surface: Surface | SurfaceType, current_position: (int, int)):
        piece_to_move: Piece | None = self.get_piece_at_position(*current_position)
        if not piece_to_move:
            return
        self.pieces.remove(piece_to_move)
        self.squares[current_position] = surface.fill(get_square_color(*current_position),
                                                      self.get_square(*current_position))
        pygame.display.update(self.squares[current_position])
