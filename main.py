import pygame.display

from board import Board
from pieces import *


def draw_board():
    pygame.init()

    n = 8  # This is an NxN chess board.
    display_size = 720  # Proposed physical surface size.
    square_size = display_size // n  # sq_sz is length of a square.
    display_size = n * square_size  # Adjust to exactly fit n squares.

    # Create the surface of (width, height), and its window.
    surface: Surface | SurfaceType = pygame.display.set_mode((display_size, display_size))

    board: Board = Board(surface)
    board.draw_pieces(surface)

    counter = 0

    piece_to_move: Piece | None = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                piece_to_move = board.get_piece_at_coordinates(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:
                board.snap_to_position(surface, piece_to_move, pygame.mouse.get_pos())
                piece_to_move = None
                pygame.display.flip()

        if piece_to_move:
            board.move_piece_to_coordinates(surface, piece_to_move, pygame.mouse.get_pos())
            pygame.display.flip()

        # counter += 1
        # if counter == 1_000_000:
        #     board.move_piece_to_position(surface, (0, 1), (0, 3))
        # elif counter == 2_000_000:
        #     board.delete_piece(surface, (0, 0))


if __name__ == "__main__":
    draw_board()
