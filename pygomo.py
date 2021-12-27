import subprocess
from Game import *


class Engine:
    def __init__(self, engine_name):
        self.engine_name = engine_name
        self.engine = subprocess.Popen(engine_name, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       bufsize=1, universal_newlines=True)
        self.is_running = True
        self.protocol = Protocol(self.engine)

    # Kill process of engine
    def kill_engine(self):
        import psutil

        def findProcessIdByName(_processName):
            """
            Get a list of all the PIDs of a all the running process whose name contains
            the given string _processName
            """
            listOfProcessObjects = []
            # Iterate over the all the running process
            for process in psutil.process_iter():
                try:
                    pinfo = process.as_dict(attrs=['pid', 'name', 'create_time'])
                    # Check if process name contains the given name string.
                    if _processName.lower() in pinfo['name'].lower():
                        listOfProcessObjects.append(pinfo['pid'])
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            return listOfProcessObjects

        try:
            for i in findProcessIdByName(self.engine_name):
                _proc = psutil.Process(i)
                _proc.terminate()
            self.is_running = False
        except:
            pass

    def __str__(self):
        return f'<Engine {self.engine_name}>'


class Protocol:
    def __init__(self, engine):
        self.engine = engine
        # You can add more option
        self.info_dict = {
            'timeout_match': 0,
            'timeout_turn': 0,
            'game_type': 0,
            'rule': 1,
            'time_left': 0,
            'max_memory': 0,
        }

    def __str__(self):
        return '<class Protocol'

    # Send input to engine
    def send(self, *command):
        command = ' '.join([str(i) for i in command]).upper()
        self.engine.stdin.write(command + '\n')

    # Receive output
    def receive(self, stdout=True, stderr=False):
        if stdout:
            return self.engine.stdout.readline().strip()
        elif stderr:
            return self.engine.stderr.readline().strip()

    def about(self):
        # Get info about engine
        self.send('ABOUT')
        info = self.receive()
        return info

    def set_info(self, info=''):
        if not info:
            info = self.info_dict
        for i in info:
            self.send('INFO', i, info[i])
        pass

    def is_ready(self, board_size=15):
        self.send('start', board_size)
        valid = self.receive()
        return valid.upper() == 'OK'

    def accept_restart(self):
        self.send('restart')
        valid = self.receive()
        return valid.upper() == 'OK'

    def put_move(self, move):
        self.send('turn', move)
        return self.get_move()

    def play_first_move(self):
        self.send('begin')
        return self.get_move()

    def board(self, lst):
        self.send('board')
        for i in range(len(lst)):
            k = '1' if len(lst) % 2 == i % 2 else '2'
            self.send(lst[i] + ',' + k)
        self.send('done')
        return self.get_move()

    def get_move(self):
        while True:
            text = self.receive()
            if 'MESSAGE' not in text and 'DEBUG' not in text and ',' in text:
                return text

    def exit(self):
        # Exit engine
        self.send('END')


# Example
def main():
    engine = Engine('embryo.exe')
    about = engine.protocol.about()
    engine.protocol.info_dict['timeout_turn'] = 0
    engine.protocol.info_dict['timeout_match'] = 10000
    engine.protocol.info_dict['time_left'] = 10000
    engine.protocol.set_info()
    if not engine.protocol.is_ready():
        engine.protocol.exit()
        engine.kill_engine()
        return
    # Case 1
    # move = engine.protocol.put_move('7,7')
    # Case 2
    # move = engine.protocol.play_first_move()
    # Case 3
    move = engine.protocol.board(['7,7', '9,4', '5,2', '6,0'])
    print(move)
    engine.protocol.exit()
    engine.kill_engine()

    game = Game(['7, 7'])
    print(game.is_win())
    print(engine)
    print(about)
    return


if __name__ == '__main__':
    main()
