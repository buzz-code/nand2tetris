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

// Put your code here.

// screen_end
@8192
D=A
@SCREEN
D=D+A
@screen_end
M=D


(LOOP)
	@KBD
	D=M
	@WHITE
	D;JEQ
	
	(BLACK)
		@color
		M=-1
		@CONT
		0;JMP
		
	(WHITE)
		@color
		M=0
		
	(CONT)
		// position = SCREEN[0]
		@SCREEN
		D=A
		@position
		M=D
		(LOOP2)
			// SCREEN[position] = color
			@color
			D=M
			@position
			A=M
			M=D
			// position = position + 1
			@position
			MD=M+1
			// if position < screen_end goto LOOP2
			@screen_end
			A=M
			D=A-D
			@LOOP2
			D;JGT

	// infinite loop
	@LOOP
	0;JMP
	
(END)