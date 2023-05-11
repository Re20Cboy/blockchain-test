import crypt

class pc_block:
    def __init__(self, str):
        from_ = 0
        to = str.find("$", from_)
        self.height = int(str[from_:to])

        from_ = to + 1
        pos = str.find("$", from_)
        while from_ < pos:
            to = str.find('\t', from_)
            self.txs.append(str[from_:to])
            from_ = to + 1
        from_ = pos + 1
        pos = str.find("$", from_)
        while from_ < pos:
            to = str.find('\t', from_)
            self.prfs.append(str[from_:to])
            from_ = to + 1
        if pos + 1 < len(str):
            self.txs_abstract = str[pos + 1:]

    def __del__(self):
        del self.txs[:]
        del self.prfs[:]
        self.txs_abstract = ""

    def block_2_str(self):
        str = f"{self.height}$"
        for s in self.txs:
            str += f"{s}\t"
        str += "$"
        for s in self.prfs:
            str += f"{s}\t"
        str += "$"
        str += self.txs_abstract
        return str

class ac_block:
    def __init__(self, height, ID, prev_ID, node_ID, time):
        self.height = height
        self.ID = ID
        self.prev_ID = prev_ID
        self.node_ID = node_ID
        self.time = time
        self.state = 0
        self.prev = None
        self.node_filter = {}
        self.A_vec = []

    def block_2_str(self):
        ab_str = str(self.ID) + ','
        ab_str += str(self.height) + ','
        ab_str += str(self.prev_ID) + ','
        ab_str += str(self.node_ID) + ','
        ab_str += str(self.time) + "$"
        for a in self.A_vec:
            ab_str += a + "$"
        return ab_str

    @staticmethod
    def str_2_block(str):
        h = 0
        id = 0
        prev_id = 0
        node_id = 0
        t = 0.0
        from_ = 0
        to = str.find(',', from_)
        id = int(str[from_:to])
        from_ = to + 1
        to = str.find(',', from_)
        h = int(str[from_:to])
        from_ = to + 1
        to = str.find(',', from_)
        prev_id = int(str[from_:to])
        from_ = to + 1
        to = str.find(',', from_)
        node_id = int(str[from_:to])
        from_ = to + 1
        to = str.find("$", from_)
        t = float(str[from_:to])
        ret = ac_block(h, id, prev_id, node_id, t)
        from_ = to + 1
        while from_ < len(str):
            to = str.find("$", from_)
            ret.A_vec.append(str[from_:to])
            from_ = to + 1
        return ret

    @staticmethod
    def record():
        return

class cc_block:
    def __init__(self, height, ID, prev_ID, node_ID, acb_height, block_epoch, time, txn_cnt):
        self.height = height
        self.ID = ID
        self.prev_ID = prev_ID
        self.node_ID = node_ID
        self.acb_height = acb_height
        self.block_epoch = block_epoch
        self.time = time
        self.txn_cnt = txn_cnt
        self.fail_txn = []
        self.fail_txs = {}

    def block_2_str(self):
        cc_str = str(self.ID) + ','
        cc_str += str(self.height) + ','
        cc_str += str(self.prev_ID) + ','
        cc_str += str(self.node_ID) + ','
        cc_str += str(self.acb_height) + ','
        cc_str += str(self.block_epoch) + ','
        cc_str += str(self.time) + ','
        cc_str += str(self.txn_cnt) + '$'
        for it in self.fail_txs:
            cc_str += it + ','
            cc_str += str(self.fail_txs[it]) + '$'
        for it_1 in self.fail_txn:
            cc_str += '%'
            for it_2 in it_1:
                cc_str += it_2
        return cc_str

    def Clear(self):
        self.fail_txn.clear()
        self.fail_txs.clear()

    @staticmethod
    def str_2_block(str):
        h, nID, a_h = 0, 0, 0
        t, b_epoch, t_cnt, val = 0.0, 0, 0, 0
        pID, ID = 0, 0
        from_ = 0
        to = str.find(',', from_)
        ID = int(str[from_:to])

        from_ = to + 1
        to = str.find(',', from_)
        h = int(str[from_:to])

        from_ = to + 1
        to = str.find(',', from_)
        pID = int(str[from_:to])

        from_ = to + 1
        to = str.find(',', from_)
        nID = int(str[from_:to])

        from_ = to + 1
        to = str.find(',', from_)
        a_h = int(str[from_:to])

        from_ = to + 1
        to = str.find(',', from_)
        b_epoch = int(str[from_:to])

        from_ = to + 1
        to = str.find(',', from_)
        t = float(str[from_:to])

        from_ = to + 1
        to = str.find('$', from_)
        t_cnt = int(str[from_:to])

        cc = cc_block(h, ID, pID, nID, a_h, b_epoch, t, t_cnt)

        from_ = to + 1
        to = str.find('$', from_)
        pos = str.find('%')
        s = ''
        if pos == -1:
            pos = len(str)
        while from_ < pos:
            to = str.find(',', from_)
            s = str[from_:to]
            from_ = to + 1
            to = str.find('$', from_)
            val = int(str[from_:to])
            cc.fail_txs[s] = val
            from_ = to + 1
        while pos < len(str):
            from_ = pos + 1
            pos = str.find('%', pos + 1)
            if pos == -1:
                pos = len(str)
            vec = []
            while from_ < pos:
                to = str.find('$', from_) + 1
                s = str[from_:to]
                vec.append(s)
                from_ = to
            cc.fail_txn.append(vec)
        return cc

#交易集
class INF:
    def __init__(self, node_ID):
        self.node_ID = node_ID
        self.tx_prf_vec = []
        self.abs = ""
        self.height = 0

    def getTxAbs(self, str):
        from_idx = str.find("$") + 1
        to_idx = str.rfind("$") + 1
        str = str[from_idx:to_idx]
        txs_str = ""
        to_idx = str.find('\t', from_idx)
        while to_idx != -1:
            txs_str += str[from_idx:to_idx]
            from_idx = to_idx + 1
            to_idx = str.find('\t', from_idx)
        txs_str = cryptography.Cryptography.GetHash(txs_str.encode(), len(txs_str))
        return txs_str

    def getTxAbs(self):
        txs_str = ""
        for s in self.tx_prf_vec:
            to_idx = s.find(';')
            txs_str += s[:to_idx+1]
        txs_str = cryptography.Cryptography.GetHash(txs_str.encode(), len(txs_str))
        return txs_str

    def inf_to_str(self):
        str = str(self.node_ID) + ','
        str += str(len(self.tx_prf_vec)) + "$"
        for s in self.tx_prf_vec:
            str += s
        str += self.abs + ','
        str += str(self.height)
        return str

    @staticmethod
    def str_2_inf(str):
        from_idx = 0
        to_idx = str.find(',', from_idx)
        node_ID = int(str[from_idx:to_idx])
        ret = INF(node_ID)

        from_idx = to_idx + 1
        to_idx = str.find("$", from_idx)
        sz = int(str[from_idx:to_idx])

        for i in range(sz):
            from_idx = to_idx + 1
            to_idx = str.find("$", from_idx) + 1
            ret.tx_prf_vec.append(str[from_idx:to_idx])
        if from_idx < len(str):
            to_idx = str.find(',', from_idx)
            ret.abs = str[from_idx:to_idx]
            from_idx = to_idx + 1
        if from_idx < len(str):
            ret.height = int(str[from_idx:])
        return ret

#回执
class receipt:
    def __init__(self, sID, rID, h):
        self.sendID = sID
        self.recvID = rID
        self.height = h
        self.tx_idx = 0
        self.txs = []
        self.tx = ""
        self.prf = ""

    def __del__(self):
        self.txs = []

    def receipt_to_str(self):
        str = f"{self.sendID},"
        str += f"{self.recvID},"
        str += f"{self.height},"
        str += f"{self.tx_idx}$"
        for t in self.txs:
            str += f"{t}$"
        str += f"{self.tx}\t{self.prf}"
        return str

    @staticmethod
    def str_to_receipt(str):
        _from = 0
        _to = str.find(',', _from)
        sID = int(str[_from:_to])
        _from = _to + 1
        _to = str.find(',', _from)
        rID = int(str[_from:_to])
        _from = _to + 1
        _to = str.find(',', _from)
        h = int(str[_from:_to])
        _from = _to + 1
        _to = str.find("$", _from)
        idx = int(str[_from:_to])
        ret = receipt(sID, rID, h)
        _from = _to + 1
        _to = str.find("$", _from)
        while _to != -1:
            ret.txs.append(str[_from:_to])
            _from = _to + 1
            _to = str.find("$", _from)
        _to = str.rfind("$")
        _from = _to + 1
        _to = str.rfind('\t')
        ret.tx = str[_from:_to]
        ret.prf = str[_to + 1:]
        return ret

class sigclass:
    def __init__(self, cID, sign, recv, time, k):
        self.ccb_ID = cID
        self.sign_Node = sign
        self.recv_Node = recv
        self.time_Stamp = time
        self.kind = k

    def sig_to_str(self):
        s_str = str(self.ccb_ID) + ','
        s_str += str(self.sign_Node) + ','
        s_str += str(self.recv_Node) + ','
        s_str += str(self.time_Stamp) + ','
        s_str += str(self.kind)
        return s_str

    @staticmethod
    def str_to_sig(str):
        _from = 0
        _to = str.find(',', _from)
        cID = int(str[_from:_to])

        _from = _to + 1
        to = str.find(',', _from)
        sign = int(str[_from:_to])

        _from = _to + 1
        _to = str.find(',', _from)
        recv = int(str[_from:_to])

        _from = _to + 1
        _to = str.find(',', _from)
        time = float(str[_from:_to])

        _from = _to + 1
        k = int(str[_from:])
        return sigclass(cID, sign, recv, time, k)

class sigclass2:
    def __init__(self):
        self.ccb_id = 0

class staticticStruct:
    def __init__(self):
        self.time = 0
        self.CCPT = 0
        self.ACC_storage = 0
        self.CCC_storage = 0
        self.PBC_storage = 0
