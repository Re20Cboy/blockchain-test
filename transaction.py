import json
from typing import List, Dict
import toolbox
import blocks

class TX:
    def __init__(self, tID=0, v=0, oID=0, rID=0):
        self.tx_ID = tID
        self.val = v
        self.owner_ID = oID
        self.acb_high = 0
        self.recv_ID = rID
        self.prf_str = ""

    def __init__(self, tx: 'TX'):
        self.tx_ID = tx.tx_ID
        self.val = tx.val
        self.owner_ID = tx.owner_ID
        self.recv_ID = tx.recv_ID
        self.acb_high = tx.acb_high
        self.prf_str = tx.prf_str

    def __init__(self, tx_str):
        flag = True
        from_ = 0
        to = tx_str.find(",")
        if to == -1:
            flag = False
        self.tx_ID = int(tx_str[from_:to])
        from_ = to + 1
        to = tx_str.find(",", from_)
        if to == -1:
            flag = False
        self.val = int(tx_str[from_:to])
        from_ = to + 1
        to = tx_str.find(",", from_)
        if to == -1:
            flag = False
        self.owner_ID = int(tx_str[from_:to])
        from_ = to + 1
        to = tx_str.find(",", from_)
        if to == -1:
            flag = False
        self.acb_high = int(tx_str[from_:to])
        from_ = to + 1
        to = tx_str.find(";", from_)
        if to == -1:
            flag = False
        self.recv_ID = int(tx_str[from_:to])
        if to != len(tx_str) - 1 or not flag:
            print("tx type Error")
            print(tx_str)

    def duo(self, tx: 'TX') -> 'TX':
        return TX(tx)

    def tx_to_str(self) -> str:
        tx_str = str(self.tx_ID) + ","
        tx_str += str(self.val) + ","
        tx_str += str(self.owner_ID) + ","
        tx_str += str(self.acb_high) + ","
        tx_str += str(self.recv_ID) + ";"
        tx_str += self.prf_str
        return tx_str

    def check(self, tx_str):
        flag = True
        from_ = 0
        to = tx_str.find(",")
        if to == -1:
            flag = False
        from_ = to + 1
        to = tx_str.find(",", from_)
        if to == -1:
            flag = False
        from_ = to + 1
        to = tx_str.find(",", from_)
        if to == -1:
            flag = False
        from_ = to + 1
        to = tx_str.find(",", from_)
        if to == -1:
            flag = False
        from_ = to + 1
        to = tx_str.find(";", from_)
        if to == -1:
            flag = False
        if to != len(tx_str) - 1 or not flag:
            print("tx type Error")
            print(tx_str)
            toolbox.recordError(toolbox.error_type.tx_type)
        return flag

class Prf:
    def __init__(self, iID: int, v: int, high: int = 0):
        self.init_ID = iID
        self.val = v
        self.init_high = high
        self.tx_cnt = 0
        self.txs_vec = []
        self.txs_h = []

    def __init__(self, prf_str: str):
        prf_list = prf_str.split(";")
        self.init_ID, self.val, self.init_high = map(int, prf_list[0].split(","))
        self.tx_cnt = len(prf_list) - 1
        self.txs_vec = []
        self.txs_h = []
        for i in range(self.tx_cnt):
            tx_list = prf_list[i].split(",")
            tx = TX(int(tx_list[0]), int(tx_list[1]), int(tx_list[2]), int(tx_list[4]))
            tx.acb_high = int(tx_list[3])
            tx.prf_str = prf_list[i+1]
            self.txs_vec.append([tx])
            self.txs_h.append(tx.acb_high)

    def __init__(self, str):
        self.tx_cnt = 0
        self.txs_vec = []
        self.txs_h = []
        self.val = 0
        from_ = 0
        to = str.find_first_of(",", from_)
        vec_sz = int(str[from_:to])
        self.txs_vec.resize(vec_sz)
        self.txs_h.resize(vec_sz)
        from_ = to + 1
        to = str.find_first_of(",", from_)
        self.init_ID = int(str[from_:to])
        from_ = to + 1
        to = str.find_first_of(",", from_)
        self.init_high = int(str[from_:to])
        from_ = to + 1
        to = str.find_first_of(";", from_)
        self.val = int(str[from_:to])
        from_ = to + 1
        for i in range(vec_sz):
            seg = str.find_first_of("/", from_)
            while from_ < seg:
                to = str.find_first_of(";", from_)
                t = TX(str[from_:1 + to - from_])
                self.txs_vec[i].append(t)
                from_ = to + 1
                self.tx_cnt += 1
            from_ = seg + 1
            to = str.find_first_of("|", from_)
            h = int(str[from_:to])
            self.txs_h[i] = h
            from_ = to + 1

    def prf_to_str(self):
        prf_str = ""
        sz = len(self.txs_vec)
        prf_str = str(sz)
        prf_str += ","
        prf_str += str(self.init_ID)
        prf_str += ","
        prf_str += str(self.init_high)
        prf_str += ","
        prf_str += str(self.val)
        prf_str += ";"
        for i in range(sz):
            for j in range(len(self.txs_vec[i])):
                prf_str += self.txs_vec[i][j].tx_to_str()
            prf_str += "/"
            prf_str += str(self.txs_h[i])
            prf_str += "|"
        prf_str += "-"
        prf_str += str(self.tx_cnt)
        if prf_str == "":
            toolbox.recordError(toolbox.error_type.empty_prf)
        return prf_str

    def addtxs(self, pb_chain):
        if not pb_chain:
            return
        last_high = 0
        if self.txs_vec:
            idx = len(self.txs_vec) - 1
            last_high = self.txs_h[idx]
        pb_idx = len(pb_chain) - 1
        flag = True
        while flag:
            b_ptr = pb_chain[pb_idx]
            if b_ptr.height < last_high or pb_idx == 0:
                if b_ptr.height < last_high:
                    pb_idx += 1
                while pb_idx < len(pb_chain):
                    v = []
                    for it in b_ptr.txs:
                        tx = TX(it)
                        v.append(tx)
                    if not v:
                        pb_idx += 1
                        continue
                    self.txs_h.append(b_ptr.height)
                    self.txs_vec.append(v)
                    pb_idx += 1
                break
            pb_idx = 0 if pb_idx == 0 else pb_idx - 1
        self.tx_cnt = self.tx_in_prf()
        return

    def addtxs(self, pb_chain, nodeID):
        if not pb_chain:
            return
        last_high = 0
        if self.txs_vec:
            idx = len(self.txs_vec) - 1
            last_high = self.txs_h[idx]
        pb_idx = len(pb_chain) - 1
        flag = True
        while flag:
            key = pb_chain[pb_idx]
            value = PBDB.Get(leveldb.ReadOptions(), key)
            b_ptr = blocks.pc_block(value)
            if b_ptr.height < last_high or pb_idx == 0:
                if b_ptr.height < last_high:
                    pb_idx += 1
                while pb_idx < len(pb_chain):
                    key = pb_chain[pb_idx]
                    value = PBDB.Get(leveldb.ReadOptions(), key)
                    b_ptr = blocks.pc_block(value)
                    v = []
                    for it in b_ptr.txs:
                        tx = TX(it)
                        v.append(tx)
                    if not v:
                        pb_idx += 1
                        continue
                    self.txs_h.append(b_ptr.height)
                    self.txs_vec.append(v)
                    pb_idx += 1
                break
            pb_idx = 0 if pb_idx == 0 else pb_idx - 1
        self.tx_cnt = self.tx_in_prf()
        return

    def afterCC(self, to):
        if not self.txs_vec:
            return 0
        idx = len(self.txs_vec) - 1
        while idx > 0:
            h = self.txs_h[idx]
            if h < to:
                self.txs_vec = self.txs_vec[idx - 1:]
                self.txs_h = self.txs_h[idx - 1:]
                self.tx_cnt = self.tx_in_prf()
                if not self.txs_vec or self.txs_h[0] > to:
                    toolbox.recordError(toolbox.error_type.after_cc)
                return idx
            idx -= 1
        self.tx_cnt = self.tx_in_prf()
        return idx

    def tx_in_prf(self):
        cnt = 0
        for x in self.txs_vec:
            cnt += len(x)
        return cnt


class Inf:
    def __init__(self, oID: int, a: str):
        self.owner_ID = oID
        self.txs = []
        self.prfs = []
        self.abs = a

    def __init__(self, oID: int, a: str, prf_str: str):
        self.owner_ID = oID
        self.txs = []
        self.prfs = [Prf(prf_str)]
        self.abs = a

    def add_prf(self, prf_str: str):
        self.prfs.append(Prf(prf_str))

    def add_tx(self, tx: 'TX'):
        self.txs.append(tx)

