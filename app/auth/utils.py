import secrets
import bcrypt


def hashpwd(password: str) -> str:
    """Get bcrypt hash of password"""
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt()).decode()


def checkpwd(password: str, bcrypt_hash: str) -> bool:
    """Check bcrypt password hash"""
    return bcrypt.checkpw(str.encode(password), str.encode(bcrypt_hash))


def new_token():
    """Genereate new random token"""
    return secrets.token_urlsafe(32)
