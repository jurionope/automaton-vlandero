class ValidationExeption(Exception):
    pass


class Automaton():
    def __init__(self, config_file):
        self.config_file = config_file
        self.Sigma = []
        self.States = []
        self.Transitions = []
        self.mat = []
        self.State_dict = {}
        self.Word_dict = {}
        self.Final_states = []
        self.Start_state = ''
        self.isDFA = True

        with open(self.config_file, 'r') as fin:
            self.graph_creation(fin.read())

    def graph_creation(self, input_str):

        def void_function(*args, **kwargs):
            pass

        if not self.validate_input(input_str, void_function):
            raise ValidationExeption

        self.mat = [[0] * (len(self.Word_dict.keys())+1) for _ in range(len(self.States)+1)]
        for t in self.Transitions: 
            if self.mat[self.State_dict[t[0]]][self.Word_dict[t[1]]] != 0:
                self.isDFA = False
            self.mat[self.State_dict[t[0]]][self.Word_dict[t[1]]] = self.State_dict[t[2]]
        # print(self.mat)
        if not self.isDFA:
            self.createNFA()
        return True

    def validate_input(self, input_str, print=print):
        # print(input_str)
        input_str = [line for line in input_str.split('\n') if line and not line.startswith('#')]
        lineNum = 0

        if not input_str[lineNum].startswith('Sigma'):
            return False
        lineNum += 1
        cnt = 1
        while input_str[lineNum] != 'End':
            if(lineNum == len(input_str)):
                return False
            if len(input_str[lineNum].split()) > 1:
                return False
            self.Sigma.append(input_str[lineNum].strip())
            self.Word_dict[input_str[lineNum].strip()] = cnt
            cnt += 1
            lineNum += 1

        lineNum += 1
        print(f"Sigma: {self.Sigma}")
        if not input_str[lineNum].startswith('States'):
            return False
        lineNum += 1
        cnt = 1
        while input_str[lineNum] != 'End':
            if(lineNum == len(input_str)):
                return False

            s = [x.strip() for x in input_str[lineNum].split(',')]
            if len(s) > 2:
                return False
            if len(s) == 2:
                try:
                    if s[1] not in "FS":
                        return False
                except:
                    return False
                if s[1] == 'F':
                    self.Final_states.append(s[0])
                if s[1] == 'S':
                    if self.Start_state != '':
                        return False
                    self.Start_state = s[0]
            self.States.append(s[0])
            self.State_dict[s[0]] = cnt
            cnt += 1
            lineNum += 1
        lineNum += 1
        print(f"States: {self.States}")

        if not input_str[lineNum].startswith('Transitions'):
            return False
        lineNum += 1
        while input_str[lineNum] != 'End':
            if(lineNum == len(input_str)):
                return False
            try:
                stateX, wordY, stateZ = [
                    x.strip() for x in input_str[lineNum].split(',')]
            except:
                return False
            if stateX not in self.States or wordY not in self.Sigma or stateZ not in self.States:
                return False
            self.Transitions.append((stateX, wordY, stateZ))
            lineNum += 1
        print(f"Transitions: {self.Transitions}")
        return True

    def print_details(self):
        print("\nStates:")
        for key, value in self.State_dict.items():
            print(f"{key} -> {value}")
        print("\nWords:")
        for key, value in self.Word_dict.items():
            print(f"{key} -> {value}")
        print(self.mat)
        

    def createNFA(self):
        self.mat = [[[] for _ in range (len(self.Word_dict.keys())+2)] for _ in range(len(self.States)+1)]
        for t in self.Transitions:
            self.mat[self.State_dict[t[0]]][self.Word_dict[t[1]]].append(self.State_dict[t[2]])

def main():
    try:
        a = Automaton('file.txt')
        print('OK')
    except ValidationExeption:
        print('Not OK')
        return
    #a.print_details()


if __name__ == "__main__":
    main()
