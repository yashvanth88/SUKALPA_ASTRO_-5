from Crypto.Random import get_random_bytes

# Generate a random 256-bit key
secret_key = get_random_bytes(32)

print(f"{secret_key}")

# Write the key to a file (in binary mode)
with open("secretKey.txt", 'wb') as file:
    file.write(secret_key)
