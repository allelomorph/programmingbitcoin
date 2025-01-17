#!/usr/bin/python3
"""`test_tx` - Unit test module for tx.py

Part of an educational mockup of Bitcoin Core; adapted from original
repository developed by Jimmy Song, et al:

    https://github.com/jimmysong/programmingbitcoin

for his book Programming Bitcoin, O'Reilly Media Inc, March 2019.

"""

from unittest import TestCase
from unittest import main
from io import BytesIO

from tx import (
    TxFetcher,
    Tx,
)


class SongTestTx(TestCase):
    """Song's unit tests for tx module methods.

    """
    cache_file = '../tx.cache'

    @classmethod
    def setUpClass(cls):
        # TBD: why are the cache files not used in Song's unit tests? Is this
        #   utilized in later chapters?
        TxFetcher.load_cache(cls.cache_file)

    def test_parse_version(self):
        raw_tx = bytes.fromhex(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303'
            'c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746f'
            'a5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f5'
            '6100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f'
            '89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef010000'
            '00001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800'
            '000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac1943'
            '0600'
        )
        stream = BytesIO(raw_tx)
        tx = Tx.deserialize(stream)
        self.assertEqual(tx.version, 1)

    def test_parse_inputs(self):
        raw_tx = bytes.fromhex(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303'
            'c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746f'
            'a5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f5'
            '6100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f'
            '89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef010000'
            '00001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800'
            '000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac1943'
            '0600')
        stream = BytesIO(raw_tx)
        tx = Tx.deserialize(stream)
        self.assertEqual(len(tx.tx_ins), 1)
        want = bytes.fromhex(
            'd1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81')
        self.assertEqual(type(tx.tx_ins[0].prev_tx), type(want))
        self.assertEqual(tx.tx_ins[0].prev_tx, want)
        self.assertEqual(tx.tx_ins[0].prev_index, 0)
        want = bytes.fromhex(
            '6b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf213'
            '20b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c319'
            '67743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd'
            '94bdd531d2e213bf016b278a')
        self.assertEqual(tx.tx_ins[0].script_sig.serialize(), want)
        self.assertEqual(tx.tx_ins[0].sequence, 0xfffffffe)

    def test_parse_outputs(self):
        raw_tx = bytes.fromhex(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303'
            'c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746f'
            'a5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f5'
            '6100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f'
            '89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef010000'
            '00001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800'
            '000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac1943'
            '0600')
        stream = BytesIO(raw_tx)
        tx = Tx.deserialize(stream)
        self.assertEqual(len(tx.tx_outs), 2)
        want = 32454049
        self.assertEqual(tx.tx_outs[0].amount, want)
        want = bytes.fromhex(
            '1976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac')
        self.assertEqual(tx.tx_outs[0].script_pubkey.serialize(), want)
        want = 10011545
        self.assertEqual(tx.tx_outs[1].amount, want)
        want = bytes.fromhex(
            '1976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac')
        self.assertEqual(tx.tx_outs[1].script_pubkey.serialize(), want)

    def test_parse_locktime(self):
        raw_tx = bytes.fromhex(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303'
            'c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746f'
            'a5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f5'
            '6100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f'
            '89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef010000'
            '00001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800'
            '000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac1943'
            '0600')
        stream = BytesIO(raw_tx)
        tx = Tx.deserialize(stream)
        self.assertEqual(tx.locktime, 410393)

    def test_fee(self):
        raw_tx = bytes.fromhex(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303'
            'c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746f'
            'a5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f5'
            '6100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f'
            '89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef010000'
            '00001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800'
            '000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac1943'
            '0600')
        stream = BytesIO(raw_tx)
        tx = Tx.deserialize(stream)
        self.assertEqual(tx.fee(), 40000)
        raw_tx = bytes.fromhex(
            '010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e148a1fc61'
            'c6ed7a069e010000006a47304402204585bcdef85e6b1c6af5c2669d4830ff86'
            'e42dd205c0e089bc2a821657e951c002201024a10366077f87d6bce1f7100ad8'
            'cfa8a064b39d4e8fe4ea13a7b71aa8180f012102f0da57e85eec2934a82a585e'
            'a337ce2f4998b50ae699dd79f5880e253dafafb7feffffffeb8f51f4038dc17e'
            '6313cf831d4f02281c2a468bde0fafd37f1bf882729e7fd3000000006a473044'
            '02207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc2'
            '6125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae36490'
            '71c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6'
            'a19b43c15a2937feffffff567bf40595119d1bb8a3037c356efd56170b64cbcc'
            '160fb028fa10704b45d775000000006a47304402204c7c7818424c7f7911da6c'
            'ddc59655a70af1cb5eaf17c69dadbfc74ffa0b662f02207599e08bc8023693ad'
            '4e9527dc42c34210f7a7d1d1ddfc8492b654a11e7620a0012102158b46fbdff6'
            '5d0172b7989aec8850aa0dae49abfb84c81ae6e5b251a58ace5cfeffffffd63a'
            '5e6c16e620f86f375925b21cabaf736c779f88fd04dcad51d26690f7f3450100'
            '00006a47304402200633ea0d3314bea0d95b3cd8dadb2ef79ea8331ffe1e61f7'
            '62c0f6daea0fabde022029f23b3e9c30f080446150b23852028751635dcee2be'
            '669c2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e563ff2722eb4c'
            'ff0ad6006e86ee20dfe7520d55feffffff0251430f00000000001976a914ab0c'
            '0b2e98b1ab6dbf67d4750b0a56244948a87988ac005a6202000000001976a914'
            '3c82d7df364eb6c75be8c80df2b3eda8db57397088ac46430600')
        stream = BytesIO(raw_tx)
        tx = Tx.deserialize(stream)
        self.assertEqual(tx.fee(), 140500)
