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
import chess
import chess.pgn

RESULTS = "./results_MegMovevMegMain"


def main():
    print(f"Compiling results from {RESULTS}")
    files = [os.path.join(RESULTS, f) for f in os.listdir(RESULTS)]
    with open(files[0]) as file:
        game = chess.pgn.read_game(file)
        eng1 = game.headers["White"]
        eng2 = game.headers["Black"]
    eng1_score = 0
    eng2_score = 0
    for f in files:
        with open(f) as file:
            game = chess.pgn.read_game(file)
            result = game.headers["Result"]
            w = game.headers["White"]
            b = game.headers["Black"]
            if w == eng1:
                if result == "0-1":
                    eng2_score += 1
                elif result == "1-0":
                    eng1_score += 1
            else:
                if result == "0-1":
                    eng1_score += 1
                elif result == "1-0":
                    eng2_score += 1
            if result == "1/2-1/2":
                eng1_score += 0.5
                eng2_score += 0.5

    eng1_elo = 0
    eng2_elo = (eng2_score*400-eng1_score*400) / (eng1_score+eng2_score)
    print(f"Engine 1: {eng1}, ELO: {eng1_elo}")
    print(f"Engine 2: {eng2}, ELO: {eng2_elo}")


main()
