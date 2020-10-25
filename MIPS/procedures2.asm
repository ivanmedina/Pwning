.data

.text

	.main:
		addi $a1,$zero,100
		addi $a2,$zero,150
		
		jal sumar
		
		li $v0,1
		addi $a0, $v1, 0
		syscall
		
		li $v0,10
		syscall
	
	sumar:
		add $v1, $a1,$a2
		jr $ra