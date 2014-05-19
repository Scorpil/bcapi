import requests
import unittest

from mock import patch, Mock

from bcapi import DataApi
from bcapi.resources import Block, Tx


block_json = {
                "hash":"0000000000000000098674acf363d04a51e84e8ef19168189505322b32cfc4f9",
                "ver":2,
                "prev_block":"00000000000000005f688971690511fe5f1b4c73308c49ec547205e8c429af08",
                "mrkl_root":"e040be9aa8ba3be4378025978c9619de24f2c7a0664ff1fd559eb91e7d23b6b5",
                "time":1400241612,
                "bits":410792019,
                "fee":1355000,
                "nonce":1531794105,
                "n_tx":1,
                "size":47787,
                "block_index":405536,
                "main_chain":True,
                "height":301031,
                "received_time":1400241612,
                "relayed_by":"46.105.121.159",
                "tx":[{
                    "time":1400241612,
                    "inputs":[{}],
                    "vout_sz":1,
                    "relayed_by":"46.105.121.159",
                    "hash":"e64011a748f5660fbef90f01df1ad0cf06ec66090e71389b16698524efc2d3f5",
                    "vin_sz":1,
                    "tx_index":56595646,
                    "ver":1,
                    "out":[{
                            "addr_tag":"ghash.io",
                            "n":0,
                            "value":2501355000,
                            "addr":"1CjPR7Z5ZSyWk6WtXvSFgkptmpoi4UM9BC",
                            "tx_index":56595646,
                            "spent":True,
                            "type":0,
                            "script":"76a91480ad90d403581fa3bf46086a91b2d9d4125db6c188ac",
                            "addr_tag_link":"https:\/\/www.ghash.io\/"}],
                    "size":157},
                    ]
                }

fake_block_response = Mock()
fake_block_response.json.return_value = block_json


class TestDataApi(unittest.TestCase):
    """
    Testing BlockChain Data Api.
    This test is just performing all the requests,
    so be careful no to abuse api restrictions.
    """

    def assertBlockEqual(self, block):
        self.assertIsInstance(block, Block)
        self.assertEqual(block.hash, block_json['hash'])

        # checking number of transaction: declared vs real
        self.assertEqual(block.n_tx, block_json['n_tx'])
        self.assertEqual(len(block.tx), block_json['n_tx'])

        self.assertTxEqual(block.tx[0])

    def assertTxEqual(self, tx):
        json_tx = block_json['tx'][0]
        self.assertIsInstance(tx, Tx)
        self.assertEqual(tx.hash, json_tx['hash'])

    @patch.object(requests, 'get', return_value=fake_block_response)
    def test_block_hash(self, get):
        """Get block by hash"""
        url = DataApi.base_url + '%s/%s' % ('rawblock', block_json['hash'])
        block = DataApi.block(block_json['hash'])
        get.assert_called_once_with(url, params={})
        self.assertBlockEqual(block)

    @patch.object(requests, 'get', return_value=fake_block_response)
    def test_block_index(self, get):
        """Get block by index"""
        url = DataApi.base_url + '%s/%s' % ('rawblock', block_json['block_index'])
        block = DataApi.block(block_json['block_index'])
        get.assert_called_once_with(url, params={})
        self.assertBlockEqual(block)

    def test_tx_hash(self):
        """Get transaction by hash"""
        tx = DataApi.tx(block_json['tx'][0]['hash'])
        self.assertTxEqual(tx)

    def test_tx_index(self):
        """Get transaction by index"""
        tx = DataApi.tx(block_json['tx'][0]['tx_index'])
        self.assertTxEqual(tx)

    def test_block_height(self):
        """Get blocks by height"""
        block_list = DataApi.block_height(block_json['height'])
        self.assertBlockEqual(block_list[0])

    def test_chart_data(self):
        """Get chart data"""
        chart_data = DataApi.chart_data('market-cap')
        self.assertIsInstance(chart_data, list)
        self.assertTrue(isinstance(chart_data[0]['x'], int) or isinstance(chart_data[0]['x'], float))
        self.assertTrue(isinstance(chart_data[0]['y'], int) or isinstance(chart_data[0]['y'], float))

    def test_latest_block(self):
        """Get latest block"""
        block = DataApi.latest_block()
        self.assertIsInstance(block, Block)
