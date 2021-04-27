#
#  ELO Testing
#  Testing the ELO difference of chess engines.
#  Copyright Megalodon Chess 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
import time
import random
import multiprocessing
import chess
import chess.engine
import chess.pgn

ENG1 = "./engines/Meg1"
ENG2 = "./engines/MegRand"
OPENINGS = "./openings/"
RESULTS = "./results_Meg1vMegRand/"
CORES = multiprocessing.cpu_count()
TIME_CTRL = (5, 3)
OPTIONS = {}

curr_game = 0


def play_games():
    while True:
        if random.random() > 0.5:
            wpath = ENG1
            bpath = ENG2
        else:
            wpath = ENG2
            bpath = ENG1

        white = chess.engine.SimpleEngine.popen_uci(wpath)
        black = chess.engine.SimpleEngine.popen_uci(bpath)
        white.configure(OPTIONS)
        black.configure(OPTIONS)

        board = chess.Board()
        with open(os.path.join(OPENINGS, random.choice(os.listdir(OPENINGS)))) as file:
            game = chess.pgn.read_game(file)
            for move in game.mainline_moves():
                board.push(move)
        board.push(random.choice(list(board.generate_legal_moves())))
        board.push(random.choice(list(board.generate_legal_moves())))

        wtime = TIME_CTRL[0] * 60
        btime = TIME_CTRL[0] * 60
        winc = TIME_CTRL[1]
        binc = TIME_CTRL[1]
        while True:
            try:
                start = time.time()
                if board.turn:
                    limit = chess.engine.Limit(white_clock=wtime, black_clock=btime, white_inc=winc, black_inc=binc)
                    board.push(white.play(board, limit).move)
                    wtime -= time.time() - start
                    wtime += winc
                    if wtime < 0:
                        result = "0-1"
                        break
                else:
                    limit = chess.engine.Limit(white_clock=wtime, black_clock=btime, white_inc=winc, black_inc=binc)
                    board.push(black.play(board, limit).move)
                    btime -= time.time() - start
                    btime += binc
                    if btime < 0:
                        result = "1-0"
                        break
            except chess.engine.EngineError:
                print(f"Game illegal move! Continuing to next game.")
                result = "*"
                break

            if board.is_game_over():
                result = board.result()
                break
        white.quit()
        black.quit()

        print(f"Game finished in {len(board.move_stack)} plies. Result is {result}.")
        fname = os.path.join(RESULTS, str(curr_game)+".pgn")
        curr_game += 1
        with open(fname, "w") as file:
            game = chess.pgn.Game()
            game.headers["Event"] = "ELO Testing"
            game.headers["White"] = wpath
            game.headers["Black"] = bpath
            game.headers["Result"] = result
            node = game.add_variation(board.move_stack[0])
            for move in board.move_stack[1:]:
                node = node.add_variation(move)
            print(game, file=file)


def main():
    os.makedirs(RESULTS, exist_ok=True)
    print(f"ELO Testing - {CORES} cores.")
    print(f"Contenders: {ENG1}, {ENG2}")
    print(f"Openings: {OPENINGS}")
    print(f"Time control: {TIME_CTRL[0]}|{TIME_CTRL[1]}")

    for i in range(CORES):
        multiprocessing.Process(target=play_games).start()


main()
