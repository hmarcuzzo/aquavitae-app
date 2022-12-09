import binascii
import json

from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from cryptography.fernet import Fernet

from config import ENCRYPT_KEY
from src.modules.blockchain.server_wallet import PRIVATE_KEY


class BlockchainUtils:
    @staticmethod
    def encrypt_data(data: dict) -> bytes:
        cipher = Fernet(ENCRYPT_KEY)

        body_bytes = json.dumps(data, indent=2).encode("utf-8")
        return cipher.encrypt(body_bytes)

    @staticmethod
    def sign(transaction_data: bytes) -> str:
        hash_object = SHA256.new(transaction_data)
        signature = pkcs1_15.new(PRIVATE_KEY).sign(hash_object)
        return binascii.hexlify(signature).decode("utf-8")
