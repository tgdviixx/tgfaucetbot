# !/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.
from eth_abi import exceptions
from moody import Config
from moody.contracttool import ContractTool
from moody.m.erc20 import Ori20
from web3 import exceptions as w3exceptions, Web3

from codec.faucetcore import TokenKeeperX
from key import private_key, LISTDE


class BulkHeart:
    def __init__(self, root_path: str, perm: list, opt: dict = None):
        self._options = opt
        self.lines = ""
        self.lines_vb = ""
        self._rootpath = root_path
        self._developer = perm[0]
        self._ContractBusExpress = None
        self._ContractLTOKEN = None
        self._bulkhandler = None
        self._p = None
        self._is_acc_new = True
        self._erc20_address = ""

    def isPaidVersion(self) -> bool:
        collect_fee = True
        if self._options is not None and "collect_fee" in self._options:
            if not self._options["collect_fee"]:
                collect_fee = False
        return collect_fee

    def tgTextLogger(self, content_line: str):
        self.lines = self.lines + "\n" + content_line

    def loggerLine(self, content_line: str):
        if self._bulkhandler is None:
            return
        self._bulkhandler.appendLogLine(content_line)

    def initExpress(self, chat_id: int = 0):
        self._p = ContractTool(self.Connect(), self._rootpath, LISTDE, [])
        self._p.withPOA().Auth(private_key)
        self._p.connect(self._rootpath, "x")
        self._p.OverrideGasConfig(6000000, 1059100000)
        self._p.OverrideChainConfig(10 ** 18, 6)

        if self._erc20_address != "":
            self._ContractLTOKEN = Ori20(self._p, self._erc20_address)
            self._ContractLTOKEN.CallDebug(True).CallContractFee(100000000000000000).EnforceTxReceipt(True)

    def check_address(self, h: str) -> bool:
        return Web3.isAddress(h)

    def give_eth(self, to: str, amount: float) -> bool:
        try:
            h = self._p.Transfer(to, amount)
            if h != "":
                return True
            else:
                return False
        except ValueError as ve:
            return False

    def tgFlushLines(self) -> str:
        dat = self.lines
        self.lines = ""
        return dat

    """
    
    All the ERC20 processing in here
    """

    def check_balance_sufficient(self, amount_required: int, wallet_address: str) -> bool:
        bal = self._ContractLTOKEN.balance_of(wallet_address)
        return bal >= amount_required

    def check_balance_gas(self, wallet: str, required_amount: int) -> bool:
        return self._p.w3.eth.get_balance(wallet) > required_amount

    def check_token(self, _text: str) -> any:
        try:
            test_token = Ori20(self._p, _text).CallDebug(False).EnforceTxReceipt(False)
            try:
                tsym = test_token.symbol()
            except ValueError:
                return False
            try:
                tname = test_token.name()
            except ValueError:
                return False
            try:
                decimal = test_token.decimals()
            except ValueError:
                return False

        except w3exceptions.BadFunctionCallOutput:
            return False
        except exceptions.InsufficientDataBytes:
            return False
        except ValueError:
            return False

        return [tname, tsym, decimal]

    """def GetFaucetSystem(self) -> OKTFaucet:
        return OKTFaucet(self._rootpath)"""

    def GetFaucetSystem(self) -> TokenKeeperX:
        pass

    def Connect(self) -> Config:
        pass
