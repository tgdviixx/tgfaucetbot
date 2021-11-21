import datetime
import os
import sqlite3

sl_create_table = """
CREATE TABLE memberfaucet (userid text, date numeric, claim text, symbol text, qty real, filled numeric)
"""
sl_determine_f = "SELECT userid, claim, date FROM memberfaucet WHERE claim=? or userid=?;"
sl_start_f = "INSERT INTO memberfaucet VALUES (?,?,?,?,?,0);"
sl_start_sample = "INSERT INTO memberfaucet VALUES ('oko','87348798','0x839283','BTC',100,0);"
sl_update_filled = "UPDATE memberfaucet SET filled=1 WHERE claim=?;"
sl_again_f = "UPDATE memberfaucet SET filled=0, date=? WHERE claim=?;"


class TokenKeeperX:
    def __init__(self, root: str, symbol_token: str, amount: float, _delta: datetime.timedelta):
        self.pending = {}
        _file_db_source = os.path.join(root, "deploy_history", "faucet.db")
        self.con = sqlite3.connect(_file_db_source)
        self.cur = self.con.cursor()
        self.symbol = symbol_token
        self.giveaway = amount
        self.delta = _delta

    def flow(self, userID: str, haha_address: str) -> bool:
        if haha_address in self.pending and self.pending[haha_address] is True:
            return False
        x = datetime.datetime.now()
        checkpoint = x - self.delta
        rows = self.cur.execute(sl_determine_f, (haha_address, userID), ).fetchall()
        print(f"🎌 selected {haha_address} found: {len(rows)}")
        print(checkpoint.timestamp())
        print(x.timestamp())

        if len(rows) > 0:
            for (userid, claim, date) in rows:
                if float(date) < float(checkpoint.timestamp()):
                    if userID is not userid:
                        print("your user Id is different then before..")
                        return False

                    if claim is not haha_address:
                        print("you have claimed with different address..")
                        return False

                    self.cur.execute(sl_again_f, (x.timestamp(), haha_address), )
                    self.pending[haha_address] = True
                    self.ok()
                    return True
                else:
                    print("not now")
                    return False
        else:
            print("first time claim yes")
            self.cur.execute(
                sl_start_f,
                (userID, x.timestamp(), haha_address, self.symbol, self.giveaway),
            )
            self.pending[haha_address] = True
            self.ok()
            return True

    def ok(self) -> "TokenKeeperX":
        self.con.commit()
        return self

    def faucet_done(self, haha_address: str):
        if haha_address in self.pending and self.pending[haha_address] is True:
            self.pending[haha_address] = False
            self.cur.execute(sl_update_filled, (haha_address,), )
        else:
            print(f"too fast.. {haha_address}")

    def sampleNewTable(self):
        # Create table
        self.cur.execute(sl_create_table)

    def insertDataSample(self):
        # Insert a row of data
        self.cur.execute(sl_start_sample)

    def done(self):
        # Save (commit) the changes
        self.con.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()

    @property
    def GiveAmountWei(self) -> int:
        return self.giveaway * 10 ** 18

    @property
    def GiveAmount(self) -> float:
        return self.giveaway


class OKTFaucet(TokenKeeperX):
    def __init__(self, root: str):
        delta = datetime.timedelta(hours=24, minutes=0, seconds=0)
        super().__init__(root, "OKT", 0.1, delta)


class RSCFaucet(TokenKeeperX):
    def __init__(self, root: str):
        delta = datetime.timedelta(hours=0, minutes=2, seconds=0)
        super().__init__(root, "RSC", 0.1, delta)


ROOT = os.path.join(os.path.dirname(__file__))


def create_schema():
    okf = OKTFaucet(ROOT)
    okf.sampleNewTable()
    okf.insertDataSample()
    okf.done()


def oncedrop():
    okf = OKTFaucet(ROOT)
    okf.flow("aux", "0x734897283479278797879")
