.data
	number1: .word 10
	number2: .word 5
	number3: .word 20
	number4: .word 8

.text 

	#SUMA
	lw $t0, number1($zero)
	lw $t1, number2($zero)
	add $t2, $t0, $t1
	
	li $v0,1
	add $a0, $zero, $t2
	syscall
	
	#RESTA
	lw $s0, number3
	lw $s1, number4
	
	sub $t0,$s0,$s1
	
	li $v0, 1
	move $a0,$t0
	syscall
	
	#MULTIPLICACION MUL
	addi $s0,$zero,10
	addi $s1,$zero,4
	
	mul $t0,$s0,$s1	
	
	li $v0, 1
	add $a0,$zero,$t0
	syscall
	
	#MULTIPLICAION MULT
	addi $t0,$zero,2000
	addi $t1,$zero,10
	
	mult $t0,$t1
	mflo $s0
	li $v0, 1
	add $a0,$zero,$s0
	syscall
	
	#MULTIPLICACION SLL
	addi $s0,$zero,4
	sll, $t0, $s0, 3
	li $v0,1
	add $a0,$zero,$t0
	syscall
	
	#DIVISION 1
	addi $t0,$zero,30
	addi $t1,$zero,5
	
	div $s0, $t0, $t1
	
	li $v0, 1
	add $a0,$zero,$s0
	syscall
	
	#DIVISON 2 (PRINT REMAINDER)
	addi $t0,$zero,30
	addi $t1,$zero,8
	
	div $t0, $t1
	mflo $s0
	mfhi $s1
	li $v0,1
	add $a0,$zero,$s1
	syscall