import datetime
import os
import sqlite3

from typing import Tuple

sl_create_table = """
CREATE TABLE {} (userid text, date numeric, claim text, symbol text, qty real, filled numeric);
"""
sl_determine_f = "SELECT userid, claim, date FROM {} WHERE claim=? or userid=?;"
sl_determine_u = "SELECT userid, claim, qty, filled FROM {} WHERE userid=?;"
sl_start_f = "INSERT INTO {} VALUES (?,?,?,?,?,0);"
sl_start_sample = "INSERT INTO {} VALUES ('@oko','87348798','0x839283','BTC',100,0);"
sl_update_filled = "UPDATE {} SET filled=1 WHERE claim=?;"
sl_again_f = "UPDATE {} SET filled=0, date=? WHERE claim=?;"
sl_amount_yul = "SELECT sum(qty) as total FROM {};"


class AirdropTable:
    def __init__(self, root: str, symbol_token: str, tablename: str):
        self.pending = {}
        self.table_name = tablename
        _file_db_source = os.path.join(root, "deploy_history", "faucet.db")
        self.con = sqlite3.connect(_file_db_source)
        self.cur = self.con.cursor()
        self.symbol = symbol_token

    def scan_sync_line(self, username: str, address: str, amount: int) -> bool:
        rows = self.cur.execute(sl_determine_f.format(self.table_name), (address, username), ).fetchall()
        x = datetime.datetime.now()
        if len(rows) > 0:
            print("Already in the book")
            return False
        else:
            self.cur.execute(sl_start_f.format(self.table_name), (username, int(x.timestamp()), address, self.symbol, amount))
            return True

    def check_claim_ready(self, username: str) -> Tuple[bool, str, str, int]:
        """
        :param username:
        :return: success or not, failure reason, claim wallet address, amount of token to receive
        """
        result = self.cur.execute(sl_determine_u.format(self.table_name), (username,)).fetchone()
        if result is None:
            return (False, "You did not participate this campaign", "", 0)
        else:
            (userid, claim, qty, filled) = result
            if int(filled) == 0:
                return (True, "You have token {} to be received".format(qty), claim, qty)
            else:
                return (False, "You have claimed the airdrop already", "", 0)

    def sum_airdrop(self):
        result = self.cur.execute(sl_amount_yul.format(self.table_name))
        print(result)

    def confirm_claim(self, claim_address: str):
        self.cur.execute(sl_update_filled.format(self.table_name), (claim_address,))
        self.ok()

    def ok(self) -> "AirdropTable":
        self.con.commit()
        return self

    def sampleNewTable(self):
        # Create table
        self.cur.execute(sl_create_table.format(self.table_name))

    def insertDataSample(self):
        # Insert a row of data
        self.cur.execute(sl_start_sample.format(self.table_name))

    def done(self):
        # Save (commit) the changes
        self.con.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.con.close()


class BLRCV1(AirdropTable):
    def __init__(self, root: str):
        super().__init__(root, "BLRC", "balincerairdropevent1")


def create_schema(fromroot: str):
    okf = BLRCV1(fromroot)
    okf.sampleNewTable()
    okf.insertDataSample()
    okf.done()


def oncedrop(fromroot: str):
    okf = BLRCV1(fromroot)
    okf.scan_sync_line("aux", "0x734897283479278797879", 99820938409180982390)
