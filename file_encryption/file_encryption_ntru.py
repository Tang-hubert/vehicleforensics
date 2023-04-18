from ntru import NTRU
import os

# Define the parameters for NTRU
N = 503
p = 3
q = 64

# Generate a public and private key pair
public_key, private_key = NTRU.generate_key_pair(N, p, q)

# Load the file to be encrypted
with open('target.txt', 'rb') as file:
    file_data = file.read()

# Encrypt the file data using the public key
encrypted_data = NTRU.encrypt(public_key, file_data)

# Save the encrypted data to a file
with open('encrypted_file.bin', 'wb') as file:
    file.write(encrypted_data)

# Save the private key to a file
with open('private_key.txt', 'w') as file:
    file.write(private_key)

# To decrypt the file, load the encrypted data and private key
with open('encrypted_file.bin', 'rb') as file:
    encrypted_data = file.read()

with open('private_key.txt', 'r') as file:
    private_key = file.read()

# Decrypt the encrypted data using the private key
decrypted_data = NTRU.decrypt(private_key, encrypted_data)

# Save the decrypted data to a file
with open('decrypted_file.txt', 'wb') as file:
    file.write(decrypted_data)
    