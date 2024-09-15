import random
import copy


class TeekoPlayer:
    """An object representation for an AI game player for the game Teeko."""

    board = [[" " for j in range(5)] for i in range(5)]
    pieces = ["b", "r"]

    def __init__(self):
        """Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def succ(self, state, opp):
        drop_phase = True
        count = 0
        i = 0
        j = 0
        while i < 5:
            if state[i][j] != " ":
                count += 1
            j += 1
            if j >= 5:
                i += 1
                j = 0
        if count >= 8:
            drop_phase = False
        move_succs = []
        succs = []
        i = 0
        j = 0
        x = self.my_piece
        if opp:
            x = self.opp
        if drop_phase:
            while i < 5:
                if state[i][j] == " ":
                    new = copy.deepcopy(state)
                    new[i][j] = x
                    move_succs.append([(i, j)])
                    succs.append(new)
                j += 1
                if j >= 5:
                    i += 1
                    j = 0
        else:
            directions = [
                [-1, -1],
                [-1, 0],
                [-1, 1],
                [0, -1],
                [0, 1],
                [1, -1],
                [1, 0],
                [1, 1],
            ]
            while i < 5:
                if state[i][j] == x:
                    for a, b in directions:
                        if (
                            0 <= i + a < 5
                            and 0 <= j + b < 5
                            and state[i + a][j + b] == " "
                        ):
                            new = copy.deepcopy(state)
                            move = []
                            move.insert(0, (i + a, j + b))
                            move.insert(1, (i, j))
                            move_succs.append(move)
                            new[i][j], new[i + a][j + b] = new[i + a][j + b], new[i][j]
                            succs.append(new)
                j += 1
                if j >= 5:
                    i += 1
                    j = 0
        return move_succs, succs

    def make_move(self, state):
        """Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        _, move = self.max_value(state, 0, float("-inf"), float("inf"))
        return move

    def opponent_move(self, move):
        """Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception("Illegal move: Can only move to an adjacent space")
        if self.board[move[0][0]][move[0][1]] != " ":
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = " "
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """Formatted printing for the board"""
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != " " and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if (
                    state[i][col] != " "
                    and state[i][col]
                    == state[i + 1][col]
                    == state[i + 2][col]
                    == state[i + 3][col]
                ):
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        start_left = [[0, 0], [0, 1], [1, 0], [1, 1]]
        for i, j in start_left:
            if (
                state[i][j] != " "
                and state[i][j]
                == state[i + 1][j + 1]
                == state[i + 2][j + 2]
                == state[i + 3][j + 3]
            ):
                return 1 if state[i][j] == self.my_piece else -1

        # check / diagonal wins
        start_right = [[0, 3], [0, 4], [1, 3], [1, 4]]
        for i, j in start_right:
            if (
                state[i][j] != " "
                and state[i][j]
                == state[i + 1][j - 1]
                == state[i + 2][j - 2]
                == state[i + 3][j - 3]
            ):
                return 1 if state[i][j] == self.my_piece else -1

        # check box wins
        i = 0
        j = 0
        while i < 4:
            if (
                state[i][j] != " "
                and state[i][j]
                == state[i + 1][j]
                == state[i + 1][j + 1]
                == state[i][j + 1]
            ):
                return 1 if state[i][j] == self.my_piece else -1
            j += 1
            if j >= 4:
                i += 1
                j = 0

        return 0  # no winner yet

    def heuristic_game_value(self, state):
        """
        Checks the current board status for the closest value to the win value 1
        compared to the opposition. Both have values in [0.0,1.0] and their difference
        is the value that defines how close we are to the win compared to the opposition.

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            float: 1.0 if this TeekoPlayer wins, -1.0 if the opponent wins, (1.0,-1.0) for a non-terminal state
            that implies how close the player is to winning compared to the opponent.
        """
        my_val = 0.0
        opp_val = 0.0

        # check horizontal wins
        for row in state:
            for i in range(2):
                my_cnt = 0
                opp_cnt = 0
                for j in range(4):
                    if row[i + j] == self.my_piece:
                        my_cnt += 1
                    elif row[i + j] == self.opp:
                        opp_cnt += 1
                my_val = max(my_val, my_cnt / 4)
                opp_val = max(opp_val, opp_cnt / 4)

        # check vertical wins
        for col in range(5):
            for i in range(2):
                my_cnt = 0
                opp_cnt = 0
                for j in range(4):
                    if state[i + j][col] == self.my_piece:
                        my_cnt += 1
                    elif state[i + j][col] == self.opp:
                        opp_cnt += 1
                my_val = max(my_val, my_cnt / 4)
                opp_val = max(opp_val, opp_cnt / 4)

        # check \ diagonal wins
        start_left = [[0, 0], [0, 1], [1, 0], [1, 1]]
        for i, j in start_left:
            my_cnt = 0
            opp_cnt = 0
            for k in range(4):
                if state[i + k][j + k] == self.my_piece:
                    my_cnt += 1
                elif state[i + k][j + k] == self.opp:
                    opp_cnt += 1
            my_val = max(my_val, my_cnt / 4)
            opp_val = max(opp_val, opp_cnt / 4)

        # check / diagonal wins
        start_right = [[0, 3], [0, 4], [1, 3], [1, 4]]
        for i, j in start_right:
            my_cnt = 0
            opp_cnt = 0
            for k in range(4):
                if state[i + k][j - k] == self.my_piece:
                    my_cnt += 1
                elif state[i + k][j - k] == self.opp:
                    opp_cnt += 1
            my_val = max(my_val, my_cnt / 4)
            opp_val = max(opp_val, opp_cnt / 4)

        # check box wins
        directions = [[0, 0], [1, 0], [1, 1], [0, 1]]
        i = 0
        j = 0
        while i < 4:
            my_cnt = 0
            opp_cnt = 0
            for a, b in directions:
                if state[i + a][j + b] == self.my_piece:
                    my_cnt += 1
                elif state[i + a][j + b] == self.opp:
                    opp_cnt += 1
            my_val = max(my_val, my_cnt / 4)
            opp_val = max(opp_val, opp_cnt / 4)
            j += 1
            if j >= 4:
                i += 1
                j = 0

        if my_val < 1:
            return my_val - opp_val
        return my_val

    def max_value(self, state, depth, alpha, beta):
        val = self.game_value(state)
        if val == 1 or val == -1:
            return val, None
        elif depth == 4:
            return self.heuristic_game_value(state), None
        best_move = None
        moves, succ = self.succ(state, False)
        for m, s in zip(moves, succ):
            score, _ = self.min_value(s, depth + 1, alpha, beta)
            if score > alpha:
                alpha = score
                best_move = m
            if alpha >= beta:
                return beta, best_move
        return alpha, best_move

    def min_value(self, state, depth, alpha, beta):
        val = self.game_value(state)
        if val == 1 or val == -1:
            return val, None
        elif depth == 4:
            return self.heuristic_game_value(state), None
        best_move = None
        moves, succ = self.succ(state, True)
        for m, s in zip(moves, succ):
            score, _ = self.max_value(s, depth + 1, alpha, beta)
            if score < beta:
                beta = score
                best_move = m
            if alpha >= beta:
                return alpha, best_move
        return beta, best_move


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print("Hello, this is Samaritan")
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:
        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(
                ai.my_piece
                + " moved at "
                + chr(move[0][1] + ord("A"))
                + str(move[0][0])
            )
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move(
                        [(int(player_move[1]), ord(player_move[0]) - ord("A"))]
                    )
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:
        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(
                ai.my_piece
                + " moved from "
                + chr(move[1][1] + ord("A"))
                + str(move[1][0])
            )
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move(
                        [
                            (int(move_to[1]), ord(move_to[0]) - ord("A")),
                            (int(move_from[1]), ord(move_from[0]) - ord("A")),
                        ]
                    )
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")

if __name__ == "__main__":
    main()
