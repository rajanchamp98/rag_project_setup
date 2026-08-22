from pwdlib import PasswordHash

password_hash=PasswordHash.recommended()


def hash_passowrd(password:str)->str:
    hash=password_hash.hash(password)
    return hash

def verify_password(password:str,hash_value)->bool:
    return password_hash.verify(password,hash_value)

