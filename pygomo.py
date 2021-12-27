import subprocess


class Engine:
    def __init__(self, engine_name):
        self.engine_name = engine_name
        self.engine = subprocess.Popen(engine_name, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       bufsize=1, universal_newlines=True)
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
        except:
            pass


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

    # Send input to engine
    def send(self, *command):
        command = ' '.join([str(i) for i in command]).upper()
        print(command)
        self.engine.stdin.write(command + '\n')

    # Receive output
    def receive(self, stdout=True, stderr=False):
        if stdout:
            return self.engine.stdout.readline()
        elif stderr:
            return self.engine.stderr.readline()

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

    def start_game(self):
        self.send('start')
        valid = self.receive().upper() == 'OK'
        return valid

    def put_move(self, move):
        self.send('turn', move)

    def exit(self):
        # Exit engine
        self.send('END')


# Example
def main():
    engine = Engine('embryo.exe')
    about = engine.protocol.about()
    engine.protocol.set_info()
    engine.protocol.exit()
    engine.kill_engine()
    print(about)
    return


if __name__ == '__main__':
    main()
