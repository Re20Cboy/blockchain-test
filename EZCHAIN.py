import EZBLCOK

class EzChain:
    def __init__(self):
        self.chain = []
        self.add_genesis_block()

    def add_new_block(self, newblock:EZBLCOK.Blcok):
        self.chain.append(newblock)

    #添加创世块
    def add_genesis_block(self):
        GenesisBlock = EZBLCOK.Blcok()
        GenesisBlock.Height = 1
        GenesisBlock.ID = 1
        GenesisBlock.CP = None
        GenesisBlock.TxnCons = None
        GenesisBlock.AddMiner = 'Re20CBoy'
        GenesisBlock.PoWPrf = '0000000'
        GenesisBlock.PreHash = None
        GenesisBlock.Sig = 'u cannot redo.'
        self.chain.append(GenesisBlock)

    def get_height(self):
        return len(self.chain)

#本地存储的临时的完整交易信息的链，即，白皮书中的LocalChain
class LocalChain:
    def __init__(self):
        self.chain = []

    def add_new_block(self, newblock:EZBLCOK.TmpBlock):
        self.chain += newblock

    def get_height(self):
        return len(self.chain)