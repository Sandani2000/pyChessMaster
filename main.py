# two player chess in python with pygame
# set up variables images and game loop

import pygame

pygame.init()
WIDTH = 640 + 160
HEIGHT = 640 + 80
screen = pygame.display.set_mode([WIDTH, HEIGHT])    # initialize window by setting window/screen size
pygame.display.set_caption("Chess Master")  # set window caption
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 36)
timer = pygame.time.Clock()
fps = 60    # fps: number of frames per second

# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []

# 0 - whites turn no selection
# 1 - whites turn piece selected
# 2 - black turn no selection
# 3 - black turn piece selected
turn_step = 0
selection = 1000
valid_moves = []

# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (70, 70))
black_queen_small = pygame.transform.scale(black_queen, (35, 35))
black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (70, 70))
black_king_small = pygame.transform.scale(black_king, (35, 35))
black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (70, 70))
black_rook_small = pygame.transform.scale(black_rook, (35, 35))
black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (70, 70))
black_bishop_small = pygame.transform.scale(black_bishop, (35, 35))
black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (70, 70))
black_knight_small = pygame.transform.scale(black_knight, (35, 35))
black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (55, 55))
black_pawn_small = pygame.transform.scale(black_pawn, (35, 35))
white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (70, 70))
white_queen_small = pygame.transform.scale(white_queen, (35, 35))
white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (70, 70))
white_king_small = pygame.transform.scale(white_king, (35, 35))
white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (70, 70))
white_rook_small = pygame.transform.scale(white_rook, (35, 35))
white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (70, 70))
white_bishop_small = pygame.transform.scale(white_bishop, (35, 35))
white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (70, 70))
white_knight_small = pygame.transform.scale(white_knight, (35, 35))
white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (55, 55))
white_pawn_small = pygame.transform.scale(white_pawn, (35, 35))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# draw main game board
def draw_board():
    for i in range(32):     # 1 2 3 4 5 6 7 8 9
        column = i % 4      # 0 1 2 3 0 1 2 3 0 1 2 3
        row = i // 4        # 0 0 0 0 1 1 1 1 2 2 2 2
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [480 - (column * 160), row * 80, 80, 80])
        else:
            pygame.draw.rect(screen, 'light gray', [560 - (column * 160), row * 80, 80, 80])
        pygame.draw.rect(screen, 'gray', [0, 640, WIDTH, 80])
        pygame.draw.rect(screen, 'gold', [0, 640, WIDTH, 80], 4)
        pygame.draw.rect(screen, 'gold', [640, 0, 160, HEIGHT], 4)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (18, 660))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 80 * i), (640, 80 * i), 2)    # for horizontal lines
            pygame.draw.line(screen, 'black', (80 * i, 0), (80 * i, 640), 2)    # for vertical lines

# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 80 + 18, white_locations[i][1] * 80 + 24))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 80 + 8, white_locations[i][1] * 80 + 8))

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 80 + 18, black_locations[i][1] * 80 + 24))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 80 + 8, black_locations[i][1] * 80 + 8))

# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('dark gray')
    draw_board()
    draw_pieces()

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()

