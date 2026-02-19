"""Credential encryption and decryption utilities"""

import os
import json
from pathlib import Path
from typing import Dict, Optional
from cryptography.fernet import Fernet
from loguru import logger


class CredentialManager:
    """Manages encrypted credential storage"""

    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize credential manager.
        
        Args:
            encryption_key: Base64-encoded Fernet key. If None, reads from ENCRYPTION_KEY env var.
        """
        if encryption_key is None:
            encryption_key = os.getenv("ENCRYPTION_KEY")
        
        if not encryption_key:
            raise ValueError(
                "ENCRYPTION_KEY not found. Set ENCRYPTION_KEY environment variable or pass it explicitly.\n"
                "Generate one with: python -c \"from cryptography.fernet import Fernet; "
                "print(Fernet.generate_key().decode())\""
            )
        
        try:
            self.cipher_suite = Fernet(encryption_key.encode() if isinstance(encryption_key, str) else encryption_key)
            self.encryption_key = encryption_key
        except Exception as e:
            raise ValueError(f"Invalid ENCRYPTION_KEY format: {str(e)}")

        self.creds_file = Path("config/encrypted_creds.json")

    @staticmethod
    def generate_key() -> str:
        """Generate a new encryption key"""
        return Fernet.generate_key().decode()

    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext string"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        encrypted = self.cipher_suite.encrypt(plaintext)
        return encrypted.decode()

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt ciphertext string"""
        if isinstance(ciphertext, str):
            ciphertext = ciphertext.encode()
        decrypted = self.cipher_suite.decrypt(ciphertext)
        return decrypted.decode()

    def save_credentials(self, credentials: Dict[str, str]) -> None:
        """Save credentials to encrypted file"""
        try:
            # Ensure directory exists
            self.creds_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Encrypt all credential values
            encrypted_creds = {}
            for key, value in credentials.items():
                encrypted_creds[key] = self.encrypt(value)
            
            # Save to file
            with open(self.creds_file, "w") as f:
                json.dump(encrypted_creds, f, indent=2)
            
            logger.info(f"✓ Credentials saved to {self.creds_file}")
        except Exception as e:
            logger.error(f"✗ Failed to save credentials: {str(e)}")
            raise

    def load_credentials(self) -> Dict[str, str]:
        """Load and decrypt credentials from file"""
        if not self.creds_file.exists():
            logger.warning(f"Credentials file not found at {self.creds_file}")
            return {}
        
        try:
            with open(self.creds_file, "r") as f:
                encrypted_creds = json.load(f)
            
            # Decrypt all values
            decrypted_creds = {}
            for key, encrypted_value in encrypted_creds.items():
                decrypted_creds[key] = self.decrypt(encrypted_value)
            
            return decrypted_creds
        except Exception as e:
            logger.error(f"✗ Failed to load credentials: {str(e)}")
            return {}

    def get_credential(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a specific credential"""
        creds = self.load_credentials()
        return creds.get(key, default)

    def update_credential(self, key: str, value: str) -> None:
        """Update a single credential"""
        creds = self.load_credentials()
        creds[key] = value
        self.save_credentials(creds)

    def delete_credential(self, key: str) -> None:
        """Delete a specific credential"""
        creds = self.load_credentials()
        if key in creds:
            del creds[key]
            self.save_credentials(creds)
            logger.info(f"✓ Credential '{key}' deleted")
        else:
            logger.warning(f"Credential '{key}' not found")


def init_credentials() -> CredentialManager:
    """Initialize credential manager from environment"""
    try:
        return CredentialManager()
    except ValueError as e:
        logger.error(f"✗ Credential manager initialization failed: {str(e)}")
        raise


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "generate-key":
        key = CredentialManager.generate_key()
        print(f"Generated encryption key:\n{key}")
        print("\nAdd this to your .env file as:")
        print(f"ENCRYPTION_KEY={key}")
    else:
        print("Usage: python -m src.utils.credentials generate-key")
