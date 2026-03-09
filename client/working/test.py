from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt(plaintext: bytes):
    # Generate RSA keys (temporary for now)
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import os

def encrypt(plaintext: bytes):
    # 🔐 Load EXISTING public key
    with open("keys/public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Generate per-file AES key
    aes_key = AESGCM.generate_key(bit_length=256)
    iv = os.urandom(12)

    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(iv, plaintext, None)

    # Encrypt AES key with RSA
    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext, encrypted_aes_key, iv




import requests
import base64

def postfile(username, password, file_bytes):
    BASE_URL = "http://127.0.0.1:8000"

    # Login
    login_res = requests.post(
        f"{BASE_URL}/api/token/",
        json={"username": username, "password": password}
    )
    access_token = login_res.json()["access"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # 🔐 Encrypt file
    ciphertext, encrypted_aes_key, iv = encrypt(file_bytes)

    files = {
        "file": ("intermediate/encrypted.bin", ciphertext)
    }

    data = {
        "encrypted_key": base64.b64encode(encrypted_aes_key).decode(),
        "iv": base64.b64encode(iv).decode(),
        "original_filename": "newfile.txt",
        "size": len(ciphertext)
    }

    upload_res = requests.post(
        f"{BASE_URL}/api/files/upload/",
        headers=headers,
        files=files,
        data=data
    )

    print(upload_res.status_code)
    print(upload_res.json())



import requests
import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64


def getfile(username , password ,id):
    BASE_URL = "http://127.0.0.1:8000"


    login_payload = {
        "username": username,
        "password": password
    }

    login_res = requests.post(
        f"{BASE_URL}/api/token/",
        json=login_payload
    )

    tokens = login_res.json()
    access_token = tokens["access"]

   
    headers = {
        "Authorization": f"Bearer {access_token}"
    }




    meta_res = requests.get(
        f"{BASE_URL}/api/files/{id}/meta/",
        headers=headers
    )

    meta = meta_res.json()

    
    encrypted_aes_key = base64.b64decode(meta["encrypted_key"])
    iv = base64.b64decode(meta["iv"])

    print("encrypted_aes_key type:", type(encrypted_aes_key))
    print("encrypted_aes_key length:", len(encrypted_aes_key))
    print("iv length:", len(iv))








    get_res = requests.get(
        f"{BASE_URL}/api/files/{id}/download",
        headers=headers,
        stream= True
    )

    print(get_res.status_code)
    print(get_res.headers)

    with open("intermediate/encrypted.bin", "wb") as f:
        for chunk in get_res.iter_content(8192):
            f.write(chunk)



    

    # Load private key
    with open("keys/private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    # Read encrypted file
    with open("intermediate/encrypted.bin", "rb") as f:
        ciphertext = f.read()

    # RSA decrypt AES key
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # AES decrypt file
    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(iv, ciphertext, None)

    # Save decrypted file
    with open("intermediate/decrypted_test.txt", "wb") as f:
        f.write(plaintext)

    print("✅ Decryption successful")