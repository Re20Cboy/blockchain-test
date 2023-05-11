
class wallet:
    def __init__(self):
        pass

    def __init__(self, rhs):
        self.priv_key_ = rhs.priv_key_
        self.name_ = rhs.name_

    def __bool__(self):
        if not self.priv_key_.get():
            return False
        return True

    def get_balance(self, cache: icache[unspent_txout]) -> coin:
        address = self.get_address()
        view = cache.view()
        balance = 0
        for tx in view:
            if address == tx.address:
                balance += tx.amount
        return balance

    def get(self) -> ecdsa_key:
        return self.priv_key_

    def get_address(self) -> ecdsa_address:
        return crypt.get_address(self.priv_key_)

    def as_debug_string(self) -> str:
        return f"{self.get_name()}: addr[{self.get_address().get()}]"

    def to_file(self, path: str):
        pass

    @staticmethod
    def from_file(path: str) -> wallet:
        w = wallet()
        return w

    @staticmethod
    def from_priv_key_str(name: str, priv_str: ecdsa_key) -> wallet:
        w = wallet()
        w.set_name(name)
        w.priv_key_ = priv_str
        return w

    @staticmethod
    def from_on_the_fly(name: str) -> wallet:
        w = wallet()
        w.set_name(name)
        w.priv_key_ = crypt.generate_private_key()
        return w

    def get_name(self) -> str:
        return self.name_

    def set_name(self, name: str):
        self.name_ = name
