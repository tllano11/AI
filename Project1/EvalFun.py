 def betterEval(self, board):
        """Invent a better evaluator than the one above.
        count virtually won boards the same as winning boards
        higher scores for expanding to a row/col that hasn't yet been occupied by the color
        place at center for first move
        for first few moves, placing pieces w gap of 1 has higher score
        djust countconnected to take side into account, and only count nodes connected in the correct direction
        """
        
        moves_made = self.game.size ** 2 - len(self.game.getPossibleMoves(board))
        if moves_made <= 2:#prefer boards where piece is placed in the middle for turn 1
            reference = self.game.size/2
            if self.game.size % 2 == 0:
                board1 = board[reference, reference]
                board2 = board[reference - 1, reference]
                board3 = board[reference, reference - 1]
                board4 = board[reference - 1, reference - 1]
                if self.side == -1 and -1 in [board1, board2, board3, board4]:
                  return -1 * (self.game.size ** 3)
                elif self.side == 1 and 1 in [board1, board2, board3, board4]:
                  return self.game.size ** 3

            if self.game.size % 2 == 1:

                board1 = board[reference, reference] 
                board2 = board[reference - 1, reference] 
                board3 = board[reference + 1, reference] 
                board4 = board[reference, reference - 1] 
                board5 = board[reference, reference + 1] 
                if self.side == -1 and -1 in [board1, board2, board3, board4, board5]:
                  return -1 * (self.game.size ** 3)
                elif self.side == 1 and 1 in [board1, board2, board3, board4, board5]:
                  return self.game.size ** 3

        if self.side == -1:
            adjuststage = 1
        else:
            adjuststage = 0

        if moves_made > 2 and moves_made <= self.game.size + adjuststage:#prefer fast expansion in early stage of game
            
            return (self.game.countConnectedGap(board, self.side) + self.game.expansionScore(board, self.side))

        if self.game.blackWins(board):
            return self.game.size ** 3
        elif self.game.whiteWins(board):
            return (-1 * (self.game.size ** 3))
        else:
            return (self.game.betterCountConnected(board, self.side) + self.game.expansionScore(board, self.side))

       

