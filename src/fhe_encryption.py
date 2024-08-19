import crypten
import torch
from logger import Logger

class OptimismFHEEncryption:
    def __init__(self, precision=1e-6):
        crypten.init()
        self.logger = Logger()
        self.precision = precision
        self.logger.log("Initializing FHE Encryption with precision {}".format(precision))

    def encrypt_data(self, data):
        try:
            self.logger.log("Encrypting data: {}".format(data))
            encrypted_data = crypten.cryptensor(torch.tensor([data]), precision=self.precision)
            self.logger.log("Data encrypted successfully.")
            return encrypted_data
        except Exception as e:
            self.logger.log_error("Encryption failed: {}".format(e))
            return None

    def decrypt_data(self, encrypted_data):
        try:
            self.logger.log("Decrypting data...")
            decrypted_data = encrypted_data.get_plain_text()
            self.logger.log("Data decrypted successfully: {}".format(decrypted_data.item()))
            return decrypted_data.item()
        except Exception as e:
            self.logger.log_error("Decryption failed: {}".format(e))
            return None