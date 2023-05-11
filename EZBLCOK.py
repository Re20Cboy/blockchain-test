import crypt
import EZTXN
from typing import List

class Blcok:
    def __init__(self, txncons:List[EZTXN.TxnCon]):
        self.ID = None #区块ID
        self.Height = None #区块高度
        self.TxnCons = txncons #区块中的交易集合
        self.PoWPrf = None #PoW证明
        self.PreHash = None #前个块的哈希索引
        self.AddMiner = None #出块者的地址
        self.CP = None #挂栽的checkpoint
        self.Sig = None #出块者对此块的数字签名

    def __init__(self, blockid = 0, height=0, txncons=[], powprf=None, prehash=None, addminer=None, cp=None, sig=None):
        self.ID = blockid  # 区块ID
        self.Height = height #区块高度
        self.TxnCons = txncons #区块中的交易集合
        self.PoWPrf = powprf #PoW证明
        self.PreHash = prehash #前个块的哈希索引
        self.AddMiner = addminer #出块者的地址
        self.CP = cp #挂栽的checkpoint
        self.Sig = sig #出块者对此块的数字签名

#checkpoint检查点
class CP:
    def __init__(self):
        #self.ID = None  # 区块ID
        self.Height = None  # 区块高度
        self.EZHeight = None #此checkpoint对应的EZblock的高度
        self.IllegalTxnList = [] #checkpoint中的非法交易集合
        self.BeginHeight = None #checkpoint开始的EZblock高度
        self.EndHeight = None #checkpoint结束的EZblock高度

    def __init__(self, height, ezheight, itl, bh, eh):
        #self.ID = blockid  # 区块ID
        self.Height = height  # 区块高度
        self.EZHeight = ezheight
        self.IllegalTxnList = itl
        self.BeginHeight = bh
        self.EndHeight = eh

#LocalChain中的块的结构
class TmpBlock:
    def __init__(self, height, txncoms:List[EZTXN.TxnCom]):
        self.Height = height #区块高度
        self.TxnComs = txncoms

#通过id找到区块
def get_block_via_id(id)->Blcok:
    block = Blcok()
    return block

# 检测是否遇到checkpoint或者遇到创世块
def meet_cp_or_gb(block:Blcok) -> bool:
    return False

#返回最新的checkpoint对应的EZblock的高度
def get_latest_cp_ezheight():
    latestcpezheight = None
    return latestcpezheight

#返回最新的checkpoint的高度
def get_latest_cp_height():
    latestcpheight = None
    return latestcpheight