import sys


char = ''
token = ""


class UnknownTokenException(Exception):
    pass


class Processor:
    index = -1
    string = ""
    reserveDict = {
        'BEGIN': 'Begin',
        'END': 'End',
        'FOR': 'For',
        # 'do': 4,
        'IF': 'If',
        'THEN': 'Then',
        'ELSE': 'Else'
    }
    # 标识符: 8,
    # INT: 9,
    symbolDict = {
        ':': 10,
        '+': 11,
        '*': 12,
        ',': 13,
        '(': 14,
        ')': 15,
        ':=': 16
    }

    def init(self):
        global char
        char = ""
        global token
        token = ""
        self.index = -1

    def isEOF(self):
        return  self.index>=self.string.__len__()

    def load_string(self, str):
        self.string = str

    def getchar(self):
        global char
        self.index = self.index + 1
        if self.isEOF():
            return
        else:
            char = self.string[self.index]
            return char

    def isbc(self):
        if(char == ' ' or char == '\n' or char == '\r' or char == '\t'):
            return True
        return False

    def getnbc(self):
        self.getchar()
        while(not self.isEOF() and self.isbc()):
            self.getchar()

    def cat(self):
        global token
        token += char

    def isletter(self):
        return char.isalpha()

    def isdigit(self):
        return char.isdigit()

    def ungetch(self):
        self.index -= 1

    def reserve(self):
        if(self.reserveDict.__contains__(token)):
            return True
        else:
            return False

    def atoi(self):
        return int(token)

    def error(self):
        self.index = self.string.__len__()
        return "Unknown"

    def outputToIdent(self, string):
        return "Ident("+string+")"

    def outputToInt(self, num):
        return "Int("+str(num)+")"

    def process(self):
        global token
        token = ""
        self.getnbc()
        if self.isEOF():
            return
        elif self.isletter():
            while self.isletter() or self.isdigit():
                self.cat()
                if not self.getchar():
                    break
            self.ungetch()
            if self.reserve():
                return self.reserveDict[token]
            else:
                return self.outputToIdent(token)
        elif self.isdigit():
            while self.isdigit():
                self.cat()
                if not self.getchar():
                    break
            self.ungetch()
            # return ('INTSY', self.atoi())
            return self.outputToInt(self.atoi())
        else:
            if char == '+':
                return "Plus"
            elif char == '*':
                return "Star"
            elif char == ',':
                return "Comma"
            elif char == '(':
                return "LParenthesis"
            elif char == ')':
                return "RParenthesis"
            elif char == ':':
                self.getchar()
                if char == '=':
                    return "Assign"
                else:
                    self.ungetch()
                    return "Colon"
            else:
                return self.error()


def main():
    # print("Start analysing...")
    file = open(sys.argv[1], 'r')
    # word_to_process = input("Please input the program\n")

    p = Processor()
    word_to_process = file.readline()
    try:
        while word_to_process:
            p.init()
            p.load_string(word_to_process)
            while not p.isEOF():
                result = p.process()
                if result == "Unknown":
                    raise UnknownTokenException
                elif result:
                    print(result)
            word_to_process = file.readline()
    except UnknownTokenException:
        pass



if __name__ == '__main__':
    main()
