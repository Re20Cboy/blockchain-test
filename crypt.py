import ecdsa
import hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

#mdctx类用于计算消息摘要
class md_ctx:
    def __init__(self):
        self.ctx_ = hashlib.sha256()

    def update(self, v):
        self.ctx_.update(v)

    def get(self):
        return self.ctx_.digest()

#md类用于获取消息摘要算法的实例
class md:
    def __init__(self, md_name):
        self.md_ = hashlib.new(md_name)

    def create_ctx(self):
        c = md_ctx()
        c.ctx_ = self.md_.copy()
        return c

    def __bool__(self):
        if self.md_:
            return True
        return False

    @staticmethod
    def from_name(md_name):
        return md(md_name)

#eckey类用于生成和管理椭圆曲线加密算法的密钥对
class ec_key:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.curve = ec.SECP256K1() #curve 是一个变量，它的作用是指定椭圆曲线加密算法中使用的曲线类型。在这个代码中，curve 的值是 ec.SECP256K1()，表示使用的是 secp256k1 曲线。secp256k1 曲线是一种椭圆曲线，被广泛用于比特币和其他加密货币的公钥加密和数字签名。

    def generate_key(self):
        private_key = ec.generate_private_key(self.curve, default_backend()) #default_backend() 函数是用于获取加密算法的默认后端的函数。在这个代码中，它被用于获取默认的加密算法后端，以便在生成密钥对时使用。
        self.private_key = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
        self.public_key = private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def get_private_key(self):
        return self.private_key.decode() #decode() 函数是用于将字节串解码为字符串的函数。函数返回的是字节串，因此需要使用 decode() 函数将其解码为字符串。

    def get_public_key(self):
        return self.public_key.decode()

#函数 load_public_key_from_hex是用于从十六进制字符串中加载公钥的函数。具体来说，它将输入的十六进制字符串转换为字节串
    def load_public_key_from_hex(self, hex):
        public_key_bytes = bytes.fromhex(hex)
        public_key = ec.EllipticCurvePublicKey.from_encoded_point(self.curve, public_key_bytes)
        self.public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def load_private_key_from_hex(self, hex):
        private_key_bytes = bytes.fromhex(hex)
        private_key = ec.derive_private_key(int.from_bytes(private_key_bytes, byteorder='big'), self.curve, default_backend())
        self.private_key = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
        self.public_key = private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    def sign(self, data):
        private_key = serialization.load_pem_private_key(self.private_key.encode(), password=None, backend=default_backend())
        signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
        return signature

    def verify(self, data, signature):
        public_key = serialization.load_pem_public_key(self.public_key.encode(), backend=default_backend())
        try:
            public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False


def sha256(data) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def generate_private_key():
    return ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

def get_address(priv_key):
    pub_key = priv_key.get_verifying_key()
    return pub_key.to_string().hex()

def sign(priv_key, data):
    signature = priv_key.sign(data.encode())
    return signature.hex()

def verify(addr, data, signature):
    pub_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(addr), curve=ecdsa.SECP256k1)
    return pub_key.verify(bytes.fromhex(signature), data.encode())

