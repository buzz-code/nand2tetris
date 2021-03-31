from enum import Enum
import re
import sys


class CommandType(Enum):
    A_COMMAND = 'A_COMMAND'
    C_COMMAND = 'C_COMMAND'
    L_COMMAND = 'L_COMMAND'


class Parser:
    def __init__(self, filePath: str):
        with open(filePath, 'r') as f:
            self.lines = f.readlines() + ['']
        self.pc = 0
        self.advance()

    def hasMoreCommands(self) -> bool:
        return self.pc < len(self.lines)

    def advance(self) -> None:
        self.currentInstruction = re.sub(
            r'(\s)|(\/\/.*)', '', self.lines[self.pc])
        self.pc += 1
        if self.currentInstruction == '' and self.hasMoreCommands():
            self.advance()

    def commandType(self) -> CommandType:
        if self.currentInstruction[0] == '@':
            return CommandType.A_COMMAND
        elif self.currentInstruction[0] == '(':
            return CommandType.L_COMMAND
        else:
            return CommandType.C_COMMAND

    def symbol(self) -> str:
        return re.sub(r'[\)\(\@]', '', self.currentInstruction)

    def dest(self) -> str:
        return re.sub(r'=.*|^[^=]*$', '', self.currentInstruction)

    def comp(self) -> str:
        return re.sub(r'(.*=)|(;.*)', '', self.currentInstruction)

    def jump(self) -> str:
        return re.sub(r'.*;|^[^;]*$', '', self.currentInstruction)


class Code:
    def __init__(self):
        self.destDict = {
            '': '000',
            'M': '001',
            'D': '010',
            'MD': '011',
            'A': '100',
            'AM': '101',
            'AD': '110',
            'AMD': '111',
        }
        self.compDict = {
            '0': '0101010',
            '1': '0111111',
            '-1': '0111010',
            'D': '0001100',
            'A': '0110000',
            'M': '1110000',
            '!D': '0001101',
            '!A': '0110001',
            '!M': '1110001',
            '-D': '0001111',
            '-A': '0110011',
            '-M': '1110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'M+1': '1110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'M-1': '1110010',
            'D+A': '0000010',
            'D+M': '1000010',
            'D-A': '0010011',
            'D-M': '1010011',
            'A-D': '0000111',
            'M-D': '1000111',
            'D&A': '0000000',
            'D&M': '1000000',
            'D|A': '0010101',
            'D|M': '1010101',
        }
        self.jumpDict = {
            '': '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }

    def dest(self, value: str) -> str:
        return self.destDict[value]

    def comp(self, value: str) -> str:
        return self.compDict[value]

    def jump(self, value: str) -> str:
        return self.jumpDict[value]


class SymbolTable:
    def __init__(self):
        self.symbolTable = {
            'SP': 0x00000,
            'LCL': 0x0001,
            'ARG': 0x0002,
            'THIS': 0x0003,
            'THAT': 0x0004,
            'R0': 0x0000,
            'R1': 0x0001,
            'R2': 0x0002,
            'R3': 0x0003,
            'R4': 0x0004,
            'R5': 0x0005,
            'R6': 0x0006,
            'R7': 0x0007,
            'R8': 0x0008,
            'R9': 0x0009,
            'R10': 0x000a,
            'R11': 0x000b,
            'R12': 0x000c,
            'R13': 0x000d,
            'R14': 0x000e,
            'R15': 0x000f,
            'SCREEN': 0x4000,
            'KBD': 0x6000,
        }

    def addEntry(self, symbol: str, address: int) -> None:
        self.symbolTable[symbol] = address

    def contains(self, symbol: str) -> bool:
        return symbol in self.symbolTable

    def GetAddress(self, symbol: str) -> int:
        return self.symbolTable[symbol]


class HackAssembler:
    def __init__(self, filePath: str):
        self.symbolTable = SymbolTable()
        self.code = Code()
        self.initialPass(filePath)
        self.processFile(filePath)

    def initialPass(self, filePath: str) -> None:
        parser = Parser(filePath)
        counter = 0
        while parser.hasMoreCommands():
            commandType = parser.commandType()
            if commandType == CommandType.L_COMMAND:
                self.symbolTable.addEntry(parser.symbol(), counter)
            else:
                counter += 1
            parser.advance()

    def processFile(self, filePath: str) -> None:
        self.parser = Parser(filePath)
        self.n = 16
        fileHackPath = filePath.split('.asm')[0] + '.hack'
        with open(fileHackPath, 'w') as f:
            while self.parser.hasMoreCommands():
                line = self.processLine()
                if line != None:
                    f.write(line + '\n')
                self.parser.advance()

    def processLine(self) -> str:
        commandType = self.parser.commandType()
        if commandType == CommandType.C_COMMAND:
            return '111' + self.code.comp(self.parser.comp()) + self.code.dest(self.parser.dest()) + self.code.jump(self.parser.jump())
        elif commandType == CommandType.L_COMMAND:
            return None
        elif commandType == CommandType.A_COMMAND:
            symbol = self.parser.symbol()
            if symbol.isdigit():
                address = int(symbol)
            else:
                if not self.symbolTable.contains(symbol):
                    self.symbolTable.addEntry(symbol, self.n)
                    self.n += 1
                address = self.symbolTable.GetAddress(symbol)
            return '0' + format(address, '015b')


if __name__ == '__main__':
    HackAssembler(sys.argv[1])
