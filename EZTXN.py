import json
from typing import List, Dict

import crypt
import toolbox
import EZBLCOK
import EZGLOBAL

class TxnIn:
    def __init__(self, pretxntid, txnid, blockheight, presender=None):
        self.PerTxnId = pretxntid #此TxnIn关联的前置输出的交易id
        self.TxnId = txnid #此TxnIn隶属于的交易Txn的id
        self.BlockHeight = blockheight #此TxnIn关联的前置输出所隶属于的区块高度
        self.PreSender = presender #此TxnIn输入交易的发起者，即，快速找到此token的上一任持有者

class TxnOut:
    def __init__(self, addrecipient, amount, txnoutid, txnid):
        self.AddRecipient = addrecipient #交易token接收方的地址
        self.Amount = amount #此交易输出转移的token金额
        self.TxnOutId = txnoutid #此TxnOut的id
        self.TxnId = txnid #此TxnOut隶属于的交易Txn的id

class Txn:
    def __init__(self):
        self.TxnIns = [] #此交易包含的所有输入
        self.TxnOuts = [] #此交易包含的所有输出
        self.TxnId = None #此交易的id
        self.Sender = None #此交易的发起方
        self.Sig = None #此交易发起方对此交易的签名

    def __init__(self, txnins:List[TxnIn], txnouts:List[TxnOut], txnid, sender, sig):
        self.TxnIns = txnins
        self.TxnOuts = txnouts
        self.TxnId = txnid
        self.Sender = sender
        self.Sig = sig

#生成TxnCon中的Sig内容
def getTxnConSig(txns:List[Txn]):
    return Sig(Abs(txns)) #伪代码，还没改！！！！！！！


#交易详情，包含多笔交易，但不包含交易的证明
class TxnCom:
    def __init__(self):
        self.Txns = []
        self.Sig = None
        self.Sender = None
        self.BlockHeight = None #记录此完整交易最后被提交到哪个区块上，此区块的Height是多少。在提交验证阶段不需要填写此成员

    def __init__(self, txns: List[Txn], sig, sender):
        self.Txns = txns
        self.Sig = sig
        self.Sender = sender
        self.BlockHeight = None

#发起方提交的此信息最终被上链共识（con=consensus）的部分（只包含签名的交易集摘要），即，TxnCom的摘要签名集
class TxnCon:
    def __init__(self):
        self.Sig = None
        self.Sender = None

    def __init__(self, sig, sender):
        self.Sig = sig
        self.Sender = sender

#交易的证明，注意不是token的证明，TxnProof只针对某个token在两个持有者之间的流转路径的记录
class TxnProof:
    def __init__(self):
        self.TxnPrfs = List[TxnCom]
        self.CPHeight = None

    def __init__(self, txnprfs: List[TxnCom], cpheight):
        self.TxnPrfs = txnprfs
        self.CPHeight = cpheight #若包含checkpoint则此项为checkpoint的ID，否则为None

#token证明的树状节点结构
class PrfTree:
    def __init__(self):
        self.value = None
        self.childID = None #用来记录此节点是其父节点的第几个孩子节点，便于检索
        self.children = []

    def __init__(self, childid, value: TxnProof):
        self.value = value
        self.childID = childid
        self.children = []

#单笔交易详情+此交易的证明
class TxnInf:
    def __init__(self):
        self.Txn = Txn()
        self.Prf = PrfTree()

    def __init__(self, txn: Txn, prftree: PrfTree):
        self.Txn = txn
        self.Prf = prftree

#TxnInf的集合，即，真正提交给miner和交易接收方的信息集合。
class TxnInfs:
    def __init__(self, infs: List[TxnInf], sender):
        self.Infs = infs
        self.Sender = sender

#交易池
class TxnPool:
    def __init__(self):
        self.TxnComs = [] #节点打包的完整交易信息汇聚形成的交易池

    def add_txn_com(self):
        #向交易池中添加完整交易
        return

    def delete_txn_com(self):
        #从交易池中删除完整交易
        return

    def get_block(self):
        #生成打包的块
        return

#根据TxnID找到对应的TxnInf
def get_txninf_via_txnid(txnid)->TxnInf:
    txninf = TxnInf()
    return txninf

#根据交易发起者信息和EZchain上的某个块（信标）找到此交易发起者在此块中的具体交易集合信息，并返回。
def get_sender_txncom_in_block(sender, block:EZBLCOK.Blcok)->TxnCom:
    for item in block.TxnCons:
        if item.Sender is sender:
            for item2 in EZGLOBAL.EZLocalChain[block.height].TxnComs: #遍历本地链中对应的块找到指定sender的存储在本地的交易集合
                if item2.sender is sender:
                    tmptxncom = item2
                    return tmptxncom

#通过txnid找到对应的完整交易信息
def get_txncom_via_txnid(txnid) ->TxnCom:
    txncom = TxnCom(TxnProof())
    return txncom

#递归遍历proof树，并筛选删除已被checkpoint标记的部分
def filter_prftree(node, condition, latestcpheight): #筛选条件为是否到达最新的checkpoint，condition为筛选条件：checkpoint对应的EZblock的高度
    for child in node.children:
        if child.value.TxnPrfs[-1].BlockHeight <= condition: #若此token流转的过程均比（固使用TxnPrfs[-1]，即，最新的证据进行筛选）筛选条件（checkpoint）更早，那么此证明则无需再提交。
            del node.children[child.childID] #已被checkpoint覆盖，则删除此孩子节点
        elif child.value.TxnPrfs[0].BlockHeight <= condition:
            child.value.TxnPrfs.CPHeight = latestcpheight
        filter_prftree(node = child, condition = condition, latestcpheight = latestcpheight)

#获取指定交易txn的proof
def get_prf(txn:Txn):
    sender = txn.Sender
    latestcpezheight = EZBLCOK.get_latest_cp_ezheight()
    latestcpheight = EZBLCOK.get_latest_cp_height()
    prftree = PrfTree()

    for item in txn.TxnIns: #遍历此（即将发布的）交易中需要用到的所有输入token
        tmpprftree = PrfTree()
        tmpprf = []
        flag_meet_cp_or_gb = False
        for item2 in reversed(EZGLOBAL.EZchain.chain[item.BlockHeight:-1]): #遍历当前此token持有者至上任持有者之间的此token流转经历
            tmpprf.append(get_sender_txncom_in_block(sender, item2))
            if EZBLCOK.meet_cp_or_gb(block=item2): #记录此流转过程中有没有遇到checkpoint
                flag_meet_cp_or_gb = True
        if not flag_meet_cp_or_gb: #没有遇到checkpoint：
            tmpprftree.value = TxnProof(tmpprf, None)
            tmpprftree.children = get_txninf_via_txnid(txnid=item.Txnid).Prf #还需将此前持有者提交的proof一同加入新的proof中
        else: #遇到checkpoint：
            tmpprftree.value = TxnProof(tmpprf, latestcpheight)
        prftree.children.append(tmpprftree) #将此token到当前（now）时间节点为止的所有证据作为孩子节点插入交易证明树中

    filter_prftree(prftree, latestcpezheight, latestcpheight) #根据最新的checkpoint信息裁剪此证明树。
    return prftree

###############################验证函数簇###############################

#验证交易输入的格式合法性
def verify_txnin_format(txnin:TxnIn, txn:Txn) -> bool:
    #验证txnin的所有参数的格式正确性
    if not isinstance(txnin.TxnId, str):
        return False
    if not isinstance(txnin.BlockHeight, int):
        return False
    if not isinstance(txnin.PerTxnId, str):
        return False
    if not isinstance(txnin.PreSender, str):
        return False
    #验证txnin关联的前置交易所在区块的高度没有超过最新的区块高度
    if txnin.BlockHeight > EZGLOBAL.EZchain.get_height():
        return False
    #验证txnin的txnid是其所属txn的id
    if txnin.TxnId is not txn.TxnId:
        return False
    #验证txnin的sender是否能在对应的区块中找到其上链的txncon
    flag_find_sender = False
    # 遍历输入交易的所在的区块的所有TxnCon
    for item in EZGLOBAL.EZchain.chain[txnin.BlockHeight].TxnCons:
        #如果存在一个（且应当仅有一个）TxnCon的sender是输入交易中的presender则说明找到了对应的交易集
        if item.Sender is txnin.PreSender:
            flag_find_sender = True
    if not flag_find_sender: #若没找到对应的sender交易集，那么说明此txnin是非法的
        return False
    # txnin.PerTxnId暂时无法检测，因为EZchain上只能索引到摘要信息，此处只是格式检测，真正的检测则会推迟到正式验证函数
    return True

#验证交易输出的格式合法性
def verify_txnout_format(txnout:TxnOut, receiver, amount, txn) -> bool:
    #验证txnout的所有参数的格式正确性
    if not isinstance(txnout.AddRecipient, str):
        return False
    if not isinstance(txnout.TxnId, str):
        return False
    if not isinstance(txnout.TxnOutId, str):
        return False
    if not isinstance(txnout.Amount, float):
        return False
    #检测token接收者是否正确
    if txnout.AddRecipient is not receiver:
        return False
    #验证txnout的txnid是其所属txn的id
    if txnout.TxnId is not txn.TxnId:
        return False
    #检测交易转移的token数量是否正确
    if txnout.Amount is not amount:
        return False
    #txnout.TxnOutId暂时无需检测，因为其暂时还没有实质性的用途。

#检验单笔交易的格式合法性
def verify_txn_format(sender, receiver, amount, txn: Txn) -> bool:
    # 检测txn是否是Txn格式
    if not isinstance(txn, Txn):
        return False

    # 检查交易id是否存在且格式合法
    if not isinstance(txn.TxnId, str):
        return False
    elif txn.TxnId is not crypt.sha256(txn.TxnIns + txn.TxnOuts): #这种+号的使用是否合法？
        return False

    # 检测TxnIns中的所有输入token是否存在且格式合法
    if not (isinstance(txn.TxnIns, list) and all(isinstance(item, TxnIn) for item in txn.TxnIns)):
        return False
    else:
        for item in txn.TxnIns:
            if not verify_txnin_format(item, txn):
                return False

    # 检测TxnOuts中的所有输出是否存在且格式合法
    if not (isinstance(txn.TxnOuts, list) and all(isinstance(item, TxnOut) for item in txn.TxnOuts)):
        return False
    else:
        for item in txn.TxnOuts:
            if not verify_txnout_format(item, receiver, amount, txn):
                return False

    # 检测签名是否为bytes类型
    if not isinstance(txn.Sig, bytes):
        return False

    # 检测发送者(即，sender地址，十六进制字符串)是否为合法类型
    if not isinstance(txn.Sender, str):
        return False

    # 如果所有检查都通过，则返回True
    return True

#验证提交的交易集合的合法性，可以被交易接收方或miner调用,sender是需要验证的交易的发送方，receiver是需要验证的交易的接收方，amount是需要验证的交易的金额，txninfs是需要验证的交易所在的TxnInfs集。
def verify_txninfs_format(sender, receiver, amount, txninfs:TxnInfs):
    if not isinstance(txninfs, TxnInfs):
        return False
    if txninfs.Sender is not sender:
        return False
    if not all(isinstance(item, TxnInf) for item in txninfs.Infs):
        return False
    #检测此txninfs集合中所有交易是否符合格式规范
    if not all(verify_txn_format(sender, receiver, amount, item.Txn) for item in txninfs.Infs):
        return False

    return True

#验证提交的交易集合的合法性，可以被交易接收方或miner调用,其中参数index是要验证的交易在TxnInfs中的索引（方便快速索引）,sender是需要验证的交易的发送方，receiver是需要验证的交易的接收方，amount是需要验证的交易的金额，txninfs是需要验证的交易所在的TxnInfs集。
def verify_txninfs(sender, receiver, amount, txninfs:TxnInfs, index):
    #验证txninfs的格式的合法性
    if not verify_txninfs_format(sender, receiver, amount, txninfs):
        return False
    #验证交易的逻辑合法性（即，不存在双花）
    txninfs.Infs[index].Txn #需要验证的交易
    txninfs.Infs[index].Txn.TxnIns[0].PerTxnId #需要验证的交易的第一个TxnIn关联的PerTxnId
    #验证思路：遍历检测sender在持有此token的生命周期中所有此sender交易的所有TxnIn中的PerTxnId是否和txninfs.Infs[index].Txn.TxnIns[0].PerTxnId相同，若相同则说明存在双花。
    #首先验证prf中的内容是否和EZchain中的摘要信息全部对应，且无错误。
    for item in reversed(EZGLOBAL.EZchain.chain):
        for item2 in item.TxnCons:
            item2.Sig =
