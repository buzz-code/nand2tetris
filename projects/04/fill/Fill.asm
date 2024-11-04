// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(START)

// if KBD != 0, flag = -1, else flag = 0
@flag
M=-1

@KBD
D=M
@INIT_END
D;JNE

@flag
M=0
(INIT_END)

// address = end of screen
@8191
D=A
@address
M=D

(LOOP)
// SCREEN[address] = flag
@address
D=M
@SCREEN
D=D+A
@realAddress
M=D
@flag
D=M
@realAddress
A=M
M=D

// address = address - 1
@address
M=M-1

// if address >= 0 loop
@address
D=M
@LOOP
D;JGE


@START
0;JMP