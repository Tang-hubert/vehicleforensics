import falcon
import os

# Generate a public and private key pair
private_key, public_key = falcon.keygen()

print(private_key)
# Load the file to be signed
with open('target.txt', 'rb') as file:
    file_data = file.read()

# Sign the file data using the private key
signature = falcon.sign(private_key, file_data)

# Save the signature to a file
with open('signature.txt', 'w') as file:
    file.write(signature)

# Verify the signature
with open('signature.txt', 'r') as file:
    signature = file.read()

verified = falcon.verify(public_key, file_data, signature)

if verified:
    print('Signature is valid!')
else:
    print('Signature is not valid.')