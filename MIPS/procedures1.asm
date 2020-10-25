.data
	message: .asciiz "Hola mundo.\nMi nombre es Ivan"

.text

	.main:
		jal saludar
		li $v0,10
		syscall
	
	saludar:
		li $v0, 4
		la $a0, message
		syscall
		jr $ra