##from engine import Engine
##from game import Game
from pygomo import *

# Example
def main():
    engine = Engine('embryo.exe')
    about = engine.protocol.about()
    engine.protocol.set_info({
        'timeout_turn': 0,
        'timeout_match': 0,
        'time_left': 10000
        })
    if not engine.protocol.is_ready():
        engine.protocol.exit()
        engine.kill_engine()
        return
    # Case 1
    # move = engine.protocol.put_move('7,7')
    # Case 2
    # move = engine.protocol.play_first_move()
    # Case 3
    # output = engine.protocol.set_board(['7,7', '9,4', '5,2', '6,0'], info=True)
    # move = output[0]
    # info = output[1]
    # print(move)
    # print(info)
    # print(info[0].ev())
    # Case 4
    move = engine.protocol.set_board(['7,7', '9,4', '5,2', '6,0'])
    print(move)
    engine.protocol.exit()
    engine.kill_engine()
    print(engine.is_running())

    game = Game(['7, 7'])
    print(game.is_win())
    print(engine)
    print(about)
    return


if __name__ == '__main__':
    main()
