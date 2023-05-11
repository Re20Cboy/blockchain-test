import os
import random
#import leveldb
from typing import List, Tuple

NODENUM = 0
MNUM = 0
EPOCHT = 0.0
N_V = 0
TXRATE = 0.0
USECC = False
ABS_SZ = 0.0
TX_SZ = 0.0
CCB_SZ = 0.0
MSG_ID = 0
VAL_CNT = 0
TX_CNT = 0
TX_SEND_CNT = 0
ABS_CNT = 0
simulationTime = 0
currentSimulationTime = 0.0
delay = 0.0
CCPT = 0
ACC_storage = 0.0
CCC_storage = 0.0
PBC_storage = 0.0
RECORD_INTERVAL = 0.0
TXDB = None
PRFDB = None
PBDB = None
INFDB = None
statistic_file = ""
statistic_folder = ""

INF_POOL = {"size": 0, "head": None, "tail": None}
ACC = {"size": 0, "head": None, "tail": None}
CCC = {"size": 0, "head": None, "tail": None}

class tx_cc:
    @staticmethod
    def add(cnt: List[int], x: int = 1) -> int:
        cnt[0] += x
        return cnt[0]

    @staticmethod
    def CCPT(cnt: List[int], tx_cnt: int) -> int:
        return cnt[0] // tx_cnt

    @staticmethod
    def sub(cnt: List[int], x: int) -> int:
        cnt[0] -= x
        return cnt[0]

class TX_P_VAL:
    def __init__(self):
        self.tx_num = []

    def get_mean(self, node_num: int) -> float:
        return sum(self.tx_num) / node_num

class simEvent:
    def __init__(self, node, t, msgP):
        self.time = t
        self.nodeID = node
        self.msgP = msgP

    def getTime(self):
        return self.time

    def getNodeID(self):
        return self.nodeID

    def getMsg(self):
        return self.msgP

class simulation:
    def __init__(self, simTime: float, n: int, M: int, T: float, nV: int, k: float, u: bool):
        self.command = ""
        self.currentSimulationTime = 0.0
        self.simulationTime = simTime
        self.nodeNum = n
        self.mNum = M
        self.epochT = T
        self.n_V = nV
        self.txRate = k
        self.useCC = u
        self.nodeLst = []
        self.eList = []
        self.sta = None

    def showParameter(self):
        print("Simulation Time: ", self.simulationTime)
        print("Node Number: ", self.nodeNum)
        print("M Number: ", self.mNum)
        print("Epoch Time: ", self.epochT)
        print("Value Number: ", self.n_V)
        print("Transaction Rate: ", self.txRate)
        print("Use CC: ", self.useCC)

    def changeParameter(self, idx: int) -> int:
        return 0

    def setSimulationTime(self, s: str) -> int:
        self.simulationTime = float(s)
        return 0

    def setnodeNum(self, s: str) -> int:
        self.nodeNum = int(s)
        return 0

    def setmNum(self, s: str) -> int:
        self.mNum = int(s)
        return 0

    def setepochT(self, s: str) -> int:
        self.epochT = float(s)
        return 0

    def setn_V(self, s: str) -> int:
        self.n_V = int(s)
        return 0

    def settxRate(self, s: str) -> int:
        self.txRate = float(s)
        return 0

    def setuseCC(self, s: str) -> int:
        self.useCC = bool(s)
        return 0

msg_type = {
    "hello": 0,
    "gen_TX": 1,
    "hash": 2,
    "acb": 3,
    "inf_for_pack": 4,
    "T_timer": 5,
    "g1": 6,
    "g2": 7,
    "g3": 9,
    "g4": 10,
    "t_msg_type": 11,
    "Inf_pack_fail": 12,
    "ccb_1": 13,
    "ccb_2": 14,
    "ccb_3": 15,
    "ccb_4": 16,
    "ccb_5": 17,
    "sig": 18,
    "light_Inf": 19,
    "space": 20
}

error_type = {
    "tx_type": -1,
    "prf_type": -2,
    "recv_node": -3,
    "init_high": -4,
    "empty_prf": -5,
    "double_spent": -6,
    "prf_incomplete": -7,
    "cross_CC": -8,
    "wrong_owner": -9,
    "inf_empty": -10,
    "inf_abs": -11,
    "acc_height": -12,
    "not_spend": -13,
    "acc_begin": -14,
    "after_cc": -15
}

def random(a: float, b: float) -> float:
    return random.uniform(a, b)

def poisson(Lamda: float) -> float:
    return random.expovariate(Lamda)

def randomExponential(lambda_: float) -> float:
    return random.expovariate(lambda_)

def intuniform(a: int, b: int) -> int:
    return random.randint(a, b)

def recordScalar(c: str, time: float) -> int:
    return 0

def recordError(type_: int) -> int:
    return 0

def stringToLPCWSTR(orig: str) -> str:
    return orig

def FindOrCreateDirectory(name):
    if os.path.isdir(name):
        return True
    try:
        os.makedirs(name)
    except OSError:
        print("Failed to create directory")
        return False
    return True

def stringToLPCWSTR(c: str) -> str:
    return c

def recordError(type):
    name = "Error record.csv"
    if FindOrCreateDirectory(statistic_folder):
        name = statistic_folder + "\\" + name
    file = open(name, "a")
    file.write(str(type) + "\n")
    file.close()
    return 0