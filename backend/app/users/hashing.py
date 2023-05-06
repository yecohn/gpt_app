from passlib.context import CryptContext


class Hash:
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def bcrypt(cls, password: str):
        return cls.pwd_ctx.hash(password)

        
    def verify(hashed_password, plain_password):
        return Hash.pwd_ctx.verify(plain_password, hashed_password)
