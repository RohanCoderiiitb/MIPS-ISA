# MIPS ASSEMBLY PROGRAM FOR ITERATIVE BINARY SEARCH ALGORITHM

.data
msg1: .asciiz "Number of elements you want to enter: \n"
msg2: .asciiz "Enter numbers in ascending order:\n"
msg3: .asciiz "Enter the value to search: \n"
msg4: .asciiz "Element not found\n"
msg5: .asciiz "Element has been found at index: "

.align 2
nums: .space 4000  # Reserving space for 1000 integers(4 bytes)

.text
main: # Taking the inputs
      li $v0, 4
      la $a0, msg1
      syscall
      li $v0, 5
      syscall
      add $a1, $v0, $0
      
      li $v0, 4    # Printing message before taking numbers
      la $a0, msg2
      syscall
      
      # Filling the array with numbers 
      la $s1, nums                        # Storing the base address of the array nums
      li $t0, 0                   # int i=0
read: 
     slt $t1, $t0, $a1
     beq $t1, $0, read_done
     li $v0, 5
     syscall
     sll $t2, $t0, 2                      # i*4(offset)
     add $t3, $s1, $t2                    # Address of nums[i]
     sw $v0, 0($t3)                       # Store the number in the location
     addi $t0, $t0, 1                     # i++
     j read
     
read_done:
          # Taking input for the value to look for
          li $v0, 4
          la $a0, msg3
          syscall
          li $v0, 5
          syscall
          add $a2, $v0, $0
          add $a3, $s1, $0
          
          # $a1 = no. of elements, #a2 = value to search for, $a3 = base address of our array
          
          # Calling the binary search function
          jal binarySearch
          add $s2, $v0, $0
          
          # Printing the final result
          li $t0, -1
          beq $v0, $t0, notFound
          li $v0, 4
          la $a0, msg5
          syscall
          li $v0, 1
          add $a0, $s2, $0
          syscall

          # Exit 
          li $v0, 10 
          syscall
          
binarySearch: 
             li $s0, 0              # int low = 0
             addi $s1, $a1, -1
             add $s1, $s1, $0       # int high = n-1
whileLoop:
          #bgt $s0, $s1, endLoop  
          
          slt $t6, $s1, $s0
          bne $t6, $0, endLoop

          add $s2, $s0, $s1
          srl $s2, $s2, 1           # mid = (low + high)/2
          sll $s3, $s2, 2           # 4*mid
          add $t2, $a3, $s3         # base address + 4*mid
          lw $t3, 0($t2)            # getting the nums[mid]
          beq $t3, $a2, returnIdx   # if nums[mid]==val we have to return mid
          slt $t4, $t3, $a2         
          beq $t4, $0, searchLeft   # if nums[mid]>val
          j searchRight             # if nums[mid]<val
          
searchRight: 
            addi $s0, $s2, 1        # low = mid+1
            j whileLoop
             
searchLeft:     
            addi $s1, $s2, -1       # high = mid-1
            j whileLoop

returnIdx: add $v0, $s2, $0
           jr $ra
           
endLoop: 
        li $v0, -1
        jr $ra
    
notFound:
         li $v0, 4
         la $a0, msg4
         syscall  
         
         # Exit 
         li $v0, 10
         syscall
