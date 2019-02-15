import sys
import json
import os.path


def envVarToFullPath(path):
    if path[0] == "$":
        return os.environ[path[1:]]
    return path


HISTORY_PATH = envVarToFullPath('$desktop') + '/history.json'


class HistoryLog:
    def __init__(self):
        if os.path.isfile(HISTORY_PATH):
            self.from_json()
        else:
            self.history = [os.path.curdir]
            self.current = 0

    def store(self):
        open(HISTORY_PATH, 'w+').write(self.to_json())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                              sort_keys=True, indent=4)

    def from_json(self):
        a = json.load(open(HISTORY_PATH, 'r'))
        self.history = a['history']
        self.current = a['current']




if __name__ == "__main__":

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('2 OR 3 ARGUMENTS!')
        exit(1)

    hl = HistoryLog()

    if sys.argv[1] == 'd':

        if len(sys.argv) != 3:
            print('third argument should be the path to the directory you want to change to')
            exit(1)

        # if there are records ahead of current
            # destroy all records that are ahead of current
        # write argv[3] to history (after current)
        # cd argv[3]

        if len(hl.history) - 1 > hl.current:
            hl.history = hl.history[:hl.current]
        hl.history.append(envVarToFullPath(sys.argv[2]))
        hl.current += 1
        hl.store()
        print(envVarToFullPath(sys.argv[2])) #chdir

    elif sys.argv[1] == 'b':

        # if current has a before
            # set before to be current
        # else
            # print you reached the end of history

        # cd to current

        if hl.current > 0:
            hl.current -= 1
            hl.store()
            print(hl.history[hl.current]) #chdir
        else:
            print('You reached the end of history')

    elif sys.argv[1] == 'f':

        # if current has a next
            # set next to be current
            # change directory to current
        # else
            # print there is no future

        if hl.current < len(hl.history) - 1:
            hl.current += 1
            hl.store()
            print(hl.history[hl.current]) #chdir
        else:
            print('there is no future')

    elif sys.argv[1] == 'c':

        # delete the file
        os.remove(HISTORY_PATH)

