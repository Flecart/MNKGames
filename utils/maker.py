#! /usr/bin/python3

"""
Questo modulo aiuta a compilare ed eseguire tutti i file, senza stare
ad utilizzare l'interfaccia ultraverbosa di java.
"""

import os
import sys
import argparse
import subprocess
import pdb

def main():
    parser = argparse.ArgumentParser(description='aiuta ad eseguire i file in modo più semplice')
    parser.add_argument('-d', '--delete', help='elimina tutti i file class', action='store_true')
    parser.add_argument('-c', '--compile', help='compila tutti i file .java', action='store_true')
    parser.add_argument('-b', '--board', help='size della board', nargs='+', type=int)
    parser.add_argument('-t', '--time', help='il tempo massimo per mossa', type=int, default=10)
    parser.add_argument('-r', '--rounds', help='il numero di ripetizioni a partite', type=int, default=1)
    parser.add_argument('-v', '--verbose', help='verbose', action='store_true')
    parser.add_argument('--human', help='human player', action='store_true')
    parser.add_argument('-p1', '--player1', help='player 1', default=None)
    parser.add_argument('-p2', '--player2', help='player 2', default=None)
    parser.add_argument('-a', '--all', help='simulate prof. test', action='store_true')
    parser.add_argument('-s', '--bsearch', help='use bin search to find depth', action='store_true')
    args = parser.parse_args()

    if args.bsearch and args.all:
        for game in all_games:
            if game[0] <5 or game[1] < 5:
                continue
            args.board = game
            tryValues(args)
        sys.exit(0)

        
    if args.all:
        play_all(args)
        sys.exit(0)
        
    if args.bsearch:
        tryValues(args)
        sys.exit(0)



    if args.delete and args.compile:
        raise Exception('You can\'t delete and compile at the same time')

    if args.delete:
        remove_all_class()
        sys.exit(0)

    if args.compile:
        compile_all_java()
        sys.exit(0)

    command = make_command(args)
    print(f"executing: {command}")
    os.system(command)

all_games = [
    (3, 3, 3),
    (4, 3, 3),
    (4, 4, 3),
    (4, 4, 4),
    (5, 4, 4),
    (5, 5, 4),
    (5, 5, 5),
    (6, 4, 4),
    (6, 5, 4),
    (6, 6, 4),
    (6, 6, 5),
    (6, 6, 6),
    (7, 4, 4),
    (7, 5, 4),
    (7, 6, 4),
    (7, 7, 4),
    (7, 5, 5),
    (7, 6, 5),
    (7, 7, 5),
    (7, 7, 6),
    (7, 7, 7),
    (8, 8, 4),
    (10, 10, 5),
    (50, 50, 10),
    (70, 70, 10),
]
def writeValueToBigBoard(val,numeroDiMosse):
    with open('mnkgame/time/DepthValue.java', 'w') as file:
        file.write("package mnkgame.time;")
        file.write("public class DepthValue {")
        file.write("public static final int Depth = " + str(val) + ";")
        file.write("public static final int NumeroDiMosse= " + str(numeroDiMosse) + ";")
        file.write("}")
        file.close()

def tryToExecute(command):
    out = subprocess.run(command.split(), capture_output=True).stdout.decode().strip().split(os.linesep)
    res = Output(format_output(out[0]))
    return res.error == 0
        

def tryValues(args):
    with open('./log.txt', 'a') as file:
        print(f"{args.board=}", file=file)
        numeroDiMosse = 10000
        massimo = 3
        while(numeroDiMosse<10**8):
            temp = searchTheResult(args,numeroDiMosse,massimo)
            if temp< massimo :
                print(f"con {numeroDiMosse} il computer non riesce più a eseguire abbastanza operazioni", file=file)
                file.flush()
                break
            massimo = temp  
            print(f"{massimo=}, {numeroDiMosse=}", file=file)
            numeroDiMosse*=10
            file.flush()



def searchTheResult(args,numeroMosse,depthVecchia):
    # pdb.set_trace()
    hasError = False
    while not hasError:
        writeValueToBigBoard(depthVecchia, numeroMosse)
        compile_all_java()
        command = make_command(args)
        if not tryToExecute(command):
            hasError = True
        else:
            depthVecchia+=1
    return depthVecchia


def get_src_dir():
    return os.path.join(os.getcwd(), "mnkgame")


def remove_all_class():
    """
    Rimuove tutti i file .class
    
    old:
    source = get_src_dir()
    for file in os.listdir(source):
        if file.endswith(".class"):
            os.remove(os.path.join("mnkgame", file))
    """
    os.system("make clean")

def compile_all_java():
    """
    Compila tutti i file .java
    NON MI WORKA SU WINDOWS BOH
    """
    """
    source = get_src_dir()
    for file in os.listdir(source):
        if file.endswith(".java"):
            os.system(os.path.join("mnkgame", file))
    """
    os.system("make compile")
    

def name_to_classname(name):
    """
    Converte un nome di file in un nome del file
    """
    if name == 'random':
        return 'mnkgame.RandomPlayer'
    elif name == 'qrandom':
        return 'mnkgame.QuasiRandomPlayer'
    elif name == 'iterative':
        return 'mnkgame.IterativeDeepeningPlayer'
    elif name == 'minimax':
        return 'mnkgame.MinimaxPlayer'
    elif name == 'boardminimax':
        return 'mnkgame.BoardMinimaxPlayer'
    elif name == 'euristic':
        return 'mnkgame.simpleheuristic.MinimaxPlayer'
    elif name == 'euristicarray':
        return 'mnkgame.simpleheuristic.MinimaxPlayerArray'
    elif name == 'mics':
        return 'mnkgame.mics.MicsPlayer'
    elif name == 'doublemics':
        return 'mnkgame.mics.MicsDoubleCheckPlayer'
    elif name == 'bigiterative':
        return 'mnkgame.bigheuristics.IterativePlayer'
    elif name == 'bigiterative2':
        return 'mnkgame.bigheuristics.IterativePlayerV2'
    elif name == 'mcts':
        return 'mnkgame.montecarlo.Player'
    elif name == 'time':
        return 'mnkgame.time.LastPlayer'
    elif name == 'time2':
        return 'mnkgame.time.LastPlayer2'
    elif name == 'debug':
        return 'mnkgame.debugPlayer.DebugPlayer'
    elif name == 'markcello':
        return 'MarkcelloPlayer.LastPlayer'
    
    

    # seguenti sono file di altre persone, quindi bisogna scaricarli e impostarli per provarli
    elif name == 'notxia':
        return 'mnkgame.github.notxia.OurPlayer'
    elif name == 'campemanu':
        return 'subroutine.GroupPlayer'
    elif name == 'negamax':
        return 'BottargaPlayer.PlayerNegamax.Player'
    elif name == 'bmoveorder':
        return 'BottargaPlayer.PlayerMoveOrder.Player'
    elif name == 'pigna':
        return 'mnkgame.Player'

def make_command(args):
    if len(args.board) != 3:
        raise Exception('Invalid board size should be 3')

    player1 = name_to_classname(args.player1)
    player2 = name_to_classname(args.player2)
    if args.human:
        return f"java -cp build mnkgame.MNKGame {args.board[0]} {args.board[1]} {args.board[2]} {player1 if player1 is not None else ''} {player2 if player2 is not None else ''}"
    else:
        verbose = "-v" if args.verbose else ""
        return f"java -cp build mnkgame.MNKPlayerTester {args.board[0]} {args.board[1]} {args.board[2]} {player1} {player2} -r {args.rounds} -t {args.time} {verbose}"


# BEGIN FORMAT OUTPUT ZONE :D

class Output:
    def __init__(self, output_tuple: tuple[int]):
        if len(output_tuple) != 5:
            raise Exception('Invalid output tuple')

        self.score = output_tuple[0]
        self.won = output_tuple[1]
        self.lost = output_tuple[2]
        self.draw = output_tuple[3]
        self.error = output_tuple[4]

    def __add__(self, other):
        return Output((self.score + other.score, self.won + other.won, self.lost + other.lost, self.draw + other.draw, self.error + other.error))

    def __str__(self):
        return f"score: {self.score}, won: {self.won}, lost: {self.lost}, draw: {self.draw}, error: {self.error}"

def format_output(string: str):
    """
    Formatta l'output della partita
    """
    from re import sub
    # replace initial string
    string = sub(r".*?Score: ", "(", string)
    string = string.replace(" Won: ", ", ")
    string = string.replace(" Lost: ", ", ")
    string = string.replace(" Draw: ", ", ")
    string = string.replace(" Error: ", ", ")
    string += ')'
    return eval(string)  # should return tuple of 4

def play_all(args):
    """
    Esegue tutte le partite simulando un test del prof.
    """


    # overwrite existings args, so that is default
    args.rounds = 1
    args.time = 10 
    args.verbose = False

    player1_result = Output((0, 0, 0, 0, 0))
    player2_result = Output((0, 0, 0, 0, 0))

    print(f"simulating prof. play between {args.player1} and {args.player2}")
    for game in all_games:
        print("playing on the board:", game)
        args.board = game
        command = make_command(args)

        # splitta per \r\n on win e \n on linux, ritorna l'output del comando eseguito nel sottoprocesso
        out = subprocess.run(command.split(), capture_output=True).stdout.decode().strip().split(os.linesep)

        player1_result += Output(format_output(out[0]))
        player2_result += Output(format_output(out[1]))
        print(player1_result)
        print(player2_result)

        # swap players
        args.player1, args.player2 = args.player2, args.player1
        command = make_command(args)
        out = subprocess.run(command.split(), capture_output=True).stdout.decode().strip().split(os.linesep)

        player1_result += Output(format_output(out[1]))
        player2_result += Output(format_output(out[0]))
        print(player1_result)
        print(player2_result)

        args.player1, args.player2 = args.player2, args.player1

    print(f"player 1 final score: {player1_result}")
    print(f"player 2 final score: {player2_result}")

if __name__ == "__main__":
    main()