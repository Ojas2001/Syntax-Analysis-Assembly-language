	START 	100
A 	DC 	01
	LOAD 	A
	LOAD 	C
	ADD 	='5'
	ADD 	   D
 	ORIGIN 	A+4
	SUB 	='10'
	ADD 	L
	LTORG
		='5'
		='10'
L 	ADD 	='5'
	ADD 	B
B 	DS 	1
C 	EQU 	B 
D 	DS 	1
	END
