# MIPS ASSEMBLY CODE TO FIND GCD OF 2 NUMBERS USING STEIN ALGORITHM

.data
msg1: .asciiz "Enter the first number: "
msg2: .asciiz "Enter the second number: "
finalMsg: .asciiz "The GCD of the two numbers you entered is: "
newline: .asciiz "\n"

.text
main: 
     #Taking the input
     li $v0, 4
     la $a0, msg1
     syscall
     li $v0, 5
     syscall
     add $s0, $v0, $0
     
     li $v0, 4
     la $a0, msg2
     syscall
     li $v0, 5
     syscall
     add $s1, $v0, $0
     
     #The 2 numbers entered are our arguments
     add $a2, $s0, $0    # $a2 = a
     add $a3, $s1, $0    # $a3 = b
     
     
     #Calling the GCD function
     jal gcd
     add $s2, $v0, $0
     
     #Printing the GCD of the 2 numbers
     li $v0, 4
     la $a0, finalMsg
     syscall 
     li $v0, 1
     add $a0, $s2, $0
     syscall
     
     #Exit
     li $v0, 10
     syscall
     
gcd:
     beq $a2, $0, returnSecond      # if(a==0) return b;
     beq $a3, $0, returnFirst      # if(b==0) return a;
     
     li $t0, 0                  # k=0
for_loop: 
         andi $t1, $a2, 1
         andi $t2, $a3, 1
         or $t3, $t1, $t2
         bne $t3, $0, whileLoop1
         srl $a2, $a2, 1        # a>>=1
         srl $a3, $a3, 1        # b>>=1
         addi $t0, $t0, 1       # k++
         j for_loop

whileLoop1: 
           andi $t3, $a2, 1         # a&1
           bne $t3, $0, whileLoop2  # if a&1 != 0 we exit
           srl $a2, $a2, 1          # a>>=1
           j whileLoop1

whileLoop2:
           andi $t3, $a3, 1         # b&1
           bne $t3, $0, compare     # if b&1 != 0, we exit the loop
           srl $a3, $a3, 1          # b>>=1
           j whileLoop2
           
compare: 
        slt $t3, $a3, $a2           # check if b < a
        beq $t3, $0, subtract       # if b >= a, we just do the subtraction
        # Else we do the swap
        add $t4, $a2, $0
        add $a2, $a3, $0
        add $a3, $t4, $0

subtract: 
         sub $a3, $a3, $a2          # b-=a
         bne $a3, $0, whileLoop2    # if b!=0, we continue the iterations
         
         sllv $v0, $a2, $t0         # a<<k
         # returning our answer
         jr $ra

returnFirst: add $v0, $a2, $0
          jr $ra
returnSecond: add $v0, $a3, $0
          jr $ra
