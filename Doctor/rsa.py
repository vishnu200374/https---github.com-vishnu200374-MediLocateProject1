# views.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_message(message, public_key):
    public_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message.encode())
    return base64.b64encode(encrypted_message)

def decrypt_message(encrypted_message, private_key):
    private_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message.decode()

# Example usage in a Django view
from django.http import HttpResponse

def rsa_example(request):
    private_key, public_key = generate_keys()
    message = "Hello, RSA!"

    encrypted_message = encrypt_message(message, public_key)
    decrypted_message = decrypt_message(encrypted_message, private_key)

    response = f"Original Message: {message}<br>"
    response += f"Encrypted Message: {encrypted_message}<br>"
    response += f"Decrypted Message: {decrypted_message}"

    return HttpResponse(response)
