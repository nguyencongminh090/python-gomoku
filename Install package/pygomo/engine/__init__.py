class Engine:
    def __init__(self, engine_name):
        import subprocess
        self.__engine_name = engine_name
        self.__engine = subprocess.Popen(engine_name, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       bufsize=1, universal_newlines=True)
        self.__is_running = True
        self.protocol = __Protocol(self.__engine)

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
            for i in findProcessIdByName(self.__engine_name):
                _proc = psutil.Process(i)
                _proc.terminate()
            self.__is_running = False
        except:
            pass

    def is_running(self):
        return self.__is_running

    def __str__(self):
        return f'<Engine {self.__engine_name}>'


class ReadOutput:
    def __init__(self, message):
        self.message = message.lower()

    def depth(self):
        try:
            output = self.message.split()[self.message.split().index('depth') + 1]
            return output
        except:
            return None
        
    def ev(self):
        try:
            output = self.message.split()[self.message.split().index('ev') + 1]
            return output
        except:
            return None

    def pv(self, is_Kata=False):
        try:
            output = self.message.split('pv')[1]
            return output.strip()
        except:
            return None

    def __str__(self):
        return f'ReadOutput(depth={self.depth()}, ev={self.ev()}, pv={self.pv()})'

    def __repr__(self):
        return f'ReadOutput(depth={self.depth()}, ev={self.ev()}, pv={self.pv()})'


class __Protocol:
    def __init__(self, engine):
        self.__engine = engine
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
        self.__engine.stdin.write(command + '\n')

    # Receive output
    def receive(self, stdout=True, stderr=False):
        if stdout:
            return self.__engine.stdout.readline().strip()
        elif stderr:
            return self.__engine.stderr.readline().strip()

    def about(self):
        # Get info about engine
        self.send('ABOUT')
        info = self.receive()
        return info

    def set_info(self, info=''):
        for i in self.info_dict:
            if i in info:
                self.send('INFO', i, info[i])
            else:
                self.send('INFO', i, self.info_dict[i])
        pass

    def is_ready(self, board_size=15):
        self.send('start', board_size)
        valid = self.receive()
        return valid.upper() == 'OK'

    def accept_restart(self):
        self.send('restart')
        valid = self.receive()
        return valid.upper() == 'OK'

    def put_move(self, move, info=False):
        self.send('turn', move)
        return self.get_move(info)

    def play_first_move(self, info=False):
        self.send('begin')
        return self.get_move(info)

    def set_board(self, lst: list, info=False):
        self.send('board')
        for i in range(len(lst)):
            k = '1' if len(lst) % 2 == i % 2 else '2'
            self.send(lst[i] + ',' + k)
        self.send('done')
        return self.get_move(info)

    def get_move(self, info=False):
        if info:
            lst = []
        while True:
            text = self.receive().upper()
            if 'MESSAGE' not in text and 'DEBUG' not in text and ',' in text:
                return (text) if not info else (text, lst)
            if info:
                txt = text.lower()
                if 'message' in txt:
                    lst.append(ReadOutput(txt))

    def takeback(self, move):
        self.send('takeback', move)

    def exit(self):
        # Exit engine
        self.send('END')
