import sys
import pygame
from constants import *
import numpy as np
import random
import copy

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC-TAC-TOE AI')
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares  # List of empty squares
        self.mark_sqrs = 0  # Number of marked squares
        
    def final_state(self):
        '''
        Determine the final state of the board.
        
        Returns:
            0 if there is no winner yet
            1 if player 1 has won
            2 if player 2 has won
        '''
        
        # Vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
            
        # Horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]
            
        # Descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        
        # Ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]
        
        # It's a tie if no one has won
        return 0
        
    def mark_sqr(self, row, col, player):
        '''
        Mark a square with a player's mark.
        
        Args:
            row: The row index of the square.
            col: The column index of the square.
            player: The player number.
        '''
        self.squares[row][col] = player
        self.mark_sqrs += 1
        
    def empty_sqr(self, row, col):
        '''
        Check if a square is empty.
        
        Args:
            row: The row index of the square.
            col: The column index of the square.
            
        Returns:
            True if the square is empty, False otherwise.
        '''
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        '''
        Get a list of empty squares on the board.
        
        Returns:
            A list of tuples representing the coordinates of empty squares.
        '''
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs
    
    def full(self):
        """
        Check if all squares are marked.
        Returns:
            bool: True if all squares are marked, False otherwise.
        """
        return self.mark_sqrs == 9
    
    def is_empty(self):
        """
        Check if the grid is empty.

        Returns:
            bool: True if the grid is empty, False otherwise.
        """
        return self.mark_sqrs == 0
    
class AI:
    """
    Represents an AI player in a game.
    """

    def __init__(self, level=1, player=2):
        """
        Initializes the AI player with the given level and player number.

        Args:
            level (int): The level of the AI player.
            player (int): The player number of the AI player.
        """
        self.level = level
        self.player = player

    def ai_choice(self, board):
        """
        Makes a random choice for the AI player.

        Args:
            board: The game board.

        Returns:
            tuple: The chosen move as (row, col).
        """
        empty_sqrs = board.get_empty_sqrs()
        index = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[index]  # returning (row, col)

    def minimax(self, board, maximizing):
        """
        Implements the Minimax algorithm for the AI player.

        Args:
            board: The game board.
            maximizing (bool): True if the AI player is maximizing, False if minimizing.

        Returns:
            tuple: The evaluation and the best move as (eval, move).
        """
        # terminal case
        case = board.final_state()

        # player one wins
        if case == 1:
            return 1, None  # eval, move
        # player two wins
        if case == 2:
            return -1, None
        # tie
        elif board.full():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        """
        Evaluates the best move for the AI player.

        Args:
            main_board: The main game board.

        Returns:
            tuple: The chosen move as (row, col).
        """
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.ai_choice(main_board)
        else:
            # minimax choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen {move} with an eval of {eval}')

        return move  # (row, col)

class Game:
    def __init__(self):
        """
        Initializes the Game class.

        The Game class represents the game state and controls the flow of the game.
        It initializes the board, AI, player, game mode, running status, and shows lines on the screen.
        """
        self.board = Board()
        self.ai = AI()
        self.player = 1 
        self.gamemode = 'ai' # 'pvp' or ai
        self.running = True
        self.show_lines()
        
    def make_move(self, row, col):
        """
        Makes a move in the game.

        Args:
            row (int): The row index of the square where the move is made.
            col (int): The column index of the square where the move is made.
        """
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()
    
    def show_lines(self):
        """
        Shows the lines on the screen.

        This function is responsible for drawing the vertical and horizontal lines on the game screen.
        """
        #BG_FILL
        screen.fill(BG_COLOR)
        
        #vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        
        #horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)
        
    def draw_fig(self, row, col):
        """
        Draws the figure (cross or circle) on the screen.

        Args:
            row (int): The row index of the square where the figure is drawn.
            col (int): The column index of the square where the figure is drawn.
        """
        if self.player == 1:
            #draw cross
            #descending line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            
            #ascending line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        
        elif self.player == 2:
            #draw circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
        
    def next_turn(self):
        """
        Switches to the next player's turn.
        """
        self.player = self.player % 2 + 1
        
    def change_gamemode(self):
        """
        Changes the game mode between player vs player (pvp) and player vs AI (ai).
        """
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
        
    def reset(self):
        """
        Resets the game state to the initial state.
        """
        self.__init__()
        
class main():
    
    game = Game()
    board = game.board
    ai = game.ai
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                if board.empty_sqr(row, col):
                    game.make_move(row, col)
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    game.change_gamemode()
                    
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1
                
                    
            if game.gamemode == 'ai' and game.player == ai.player:
                # update the screen
                pygame.display.update()
                
                # ai method
                row, col = ai.eval(board)
                game.make_move(row, col)
                
        pygame.display.update()


