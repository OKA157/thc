from phe import paillier
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

sys.path.append(parent_dir)
import COLORS.color as color
import voteFunctions.TimeRecorder as stopWatch


def generate_key_pair():
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key

def encrypt(public_key, plaintext):
    ciphertext = public_key.encrypt(plaintext)
    return ciphertext

def decrypt(private_key, ciphertext):
    plaintext = private_key.decrypt(ciphertext)
    return plaintext

def test(num1, num2):
    color.print_colored_text(""" 
                             ################################# 
                             # PAILLIER ENCRYPTION ALGORYTHM #
                             #################################\n\n""","bright_yellow")
    color.print_colored_text("First Operand: ","white")
    color.print_colored_text(num1,"bright_red")
    color.print_colored_text("\nSecond Operand: ","white")
    color.print_colored_text(f"{num2}\n","bright_red")

    public_key, private_key = generate_key_pair()

    color.print_colored_text(f'''
          MANUAL:
          _______

          The operation are the following:
          Operation 1:  
          {num1} + {num2} = {num1+num2}
          Operation 2:  
          {num1} + {num1+num2} = {num1+num2+num1}
                    .
                    .
                    .
          Operation n:  
          {num1} + Operation n-1 result =  Operation n result
           ''', "bright_cyan")
    

    ciphertext_num1 = encrypt(public_key, num1)
    ciphertext_num2 = encrypt(public_key, num2)

    num_operations = 20
    for i in range(num_operations):
        result_ciphertext = ciphertext_num1 + ciphertext_num2

        decrypted_result = decrypt(private_key, result_ciphertext)
        color.print_colored_text(f"\nIteration {i+1}: ", "orange")
        print(f"\n\n{ciphertext_num1} + {ciphertext_num2} = {result_ciphertext}\n\nDecrypted Sum: {decrypted_result}")
        
        ciphertext_num1 = result_ciphertext

if __name__ == "__main__":
    test(7, 11)
