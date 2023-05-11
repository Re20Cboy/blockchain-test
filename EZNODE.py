import crypt
import EZCHAIN

class node:
    def __init__(self, nodeid):
        self.KeyPair = crypt.ec_key()
        self.NodeID = nodeid
        self.KeyPair.generate_key()
        self.EZchain = EZCHAIN.EzChain()

    #获取公钥
    def get_public_key(self):
        return self.KeyPair.get_public_key()

    #获取私钥
    def get_private_key(self):
        return self.KeyPair.get_private_key()

    #对数据data签名
    def sign_data(self, data) -> bytes:
        return self.KeyPair.sign(data=data)

    #自己对签名进行验证
    def verify_sign(self, data, signature) -> bool:
        return self.KeyPair.verify(data, signature)
