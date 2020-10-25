.data
	miMensaje: .asciiz "HOLA MUNDO\n"
	miCaracter: .byte 'I'
	miEntero: .word 23
	miFloat: .float 3.14
	miDouble: .double 7.202
	miZero: .double 0

.text
 	li $v0, 4
 	la $a0, miMensaje
 	syscall
  	li $v0, 4
 	la $a0, miCaracter
 	syscall
   	li $v0, 1
 	lw $a0, miEntero
 	syscall
    	li $v0, 2
 	lwc1 $f12, miFloat
 	syscall
 	ldc1 $f2, miDouble
 	ldc1 $f0, miZero
 	li $v0, 3
 	add.d $f12, $f2,$f0
 	syscall
 
