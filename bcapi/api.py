import requests

from bcapi.resources import Block, Tx, TxOut, Address, MultiAddress
from utils import ClassProperty


class BaseApi(object):
    base_url = "http://blockchain.info/"

    @staticmethod
    def _request(*args, **kwargs):
        """
        Make request where:
            base url is BaseApi.base_url
            args are url sections (e.g. arg1/arg2/arg3)
            kwargs are url parameters (e.g. key1=val1&key2=val2)
        """
        url = DataApi.base_url + '/'.join(tuple(map(str, args)))
        response = requests.get(url, params=kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    def json_request(*args, **kwargs):
        """Default JSON request handling."""
        response = BaseApi._request(*args, **kwargs)
        return response.json()

    @staticmethod
    def typed_request(conv_type, *args, **kwargs):
        """Request typed plaintext data."""
        response = BaseApi._request(*args, **kwargs)
        return conv_type(response.text)


class DataApi(BaseApi):
    """
    Data API wrapper.
    https://blockchain.info/api/blockchain_api
    """

    @staticmethod
    def block(block_hash):
        raw_json = DataApi.json_request('rawblock', block)
        return Block(raw_json)

    @staticmethod
    def tx(tx):
        raw_json = DataApi.json_request('rawtx', tx)
        return Tx(raw_json)

    @staticmethod
    def block_height(height, **kwargs):
        kwargs.setdefault('format', 'json')
        raw_json = DataApi.json_request('block-height', height, **kwargs)
        return [Block(raw_block) for raw_block in raw_json['blocks']]

    @staticmethod
    def address(address, **kwargs):
        if isinstance(address, Address):
            address = address.address
        raw_json = DataApi.json_request('rawaddr', address, **kwargs)
        return Address(raw_json)

    @staticmethod
    def multi_address(adresses, **kwargs):
        kwargs['active'] = '|'.join(adresses)
        raw_json = DataApi.json_request('multiaddr', **kwargs)
        return MultiAddress(raw_json)

    @staticmethod
    def unspent(addresses):
        if isinstance(adresses, list):
            addresses = '|'.join(adresses)
        raw_json = DataApi.json_request('unspent', active=addresses)
        return [TxOut(tx_out) for tx_out in raw_json['unspent_outputs']]

    @staticmethod
    def latest_block():
        block_hash = DataApi.json_request('latestblock')['hash']
        raw_json = DataApi.json_request('rawblock', block_hash)
        return Block(raw_json)

    @staticmethod
    def unconfirmed_txs(**kwargs):
        kwargs.setdefault('format', 'json')
        raw_json = DataApi.json_request('unconfirmed-transactions', **kwargs)
        return [Tx(raw_tx) for raw_tx in raw_json['txs']]


class StatsApi(BaseApi):
    """
    Charts & Statistics API wrapper.
    https://blockchain.info/api/charts_api
    """

    @staticmethod
    def charts(chart_type, **kwargs):
        kwargs.setdefault('format', 'json')
        return DataApi.json_request('charts', chart_type, **kwargs)['values']

    @staticmethod
    def stats(**kwargs):
        kwargs.setdefault('format', 'json')
        return DataApi.json_request('stats', **kwargs)


class ExchangeApi(BaseApi):
    """
    Exchange Rates API wrapper.
    https://blockchain.info/api/exchange_rates_api
    """

    @staticmethod
    def ticker():
        return ExchangeApi.json_request('ticker')

    @staticmethod
    def tobtc(currency, value):
        return ExchangeApi.json_request('tobtc', currency=currency, value=value)


class QueryApi(BaseApi):
    """
    Simple Query API wrapper.
    https://blockchain.info/q
    """

    @ClassProperty
    @staticmethod
    def difficulty():
        """Current difficulty target as a decimal number."""
        return QueryApi.typed_request(float, 'q', 'getdifficulty')

    @ClassProperty
    @staticmethod
    def blockcount():
        """Current block height in the longest chain."""
        return QueryApi.typed_request(int, 'q', 'getblockcount')

    @ClassProperty
    @staticmethod
    def latesthash():
        """Current block height in the longest chain."""
        return QueryApi.typed_request(str, 'q', 'latesthash')

    @ClassProperty
    @staticmethod
    def bcperblock():
        """Current block reward in BTC."""
        satoshi = QueryApi.typed_request(int, 'q', 'bcperblock')
        return int(round(satoshi / 100000000))

    @ClassProperty
    @staticmethod
    def totalbc():
        """Total Bitcoins in circulation (delayed by upto 1 hour)."""
        return QueryApi.typed_request(int, 'q', 'totalbc')

    @ClassProperty
    @staticmethod
    def probability():
        """Probability of finding a valid block each hash attempt."""
        return QueryApi.typed_request(float, 'q', 'probability')

    @ClassProperty
    @staticmethod
    def hashestowin():
        """Average number of hash attempts needed to solve a block."""
        return QueryApi.typed_request(int, 'q', 'hashestowin')

    @ClassProperty
    @staticmethod
    def nextretarget():
        """Block height of the next difficulty retarget"""
        return QueryApi.typed_request(int, 'q', 'nextretarget')

    @ClassProperty
    @staticmethod
    def avgtxsize():
        """
        Average transaction size for the past 1000 blocks.
        Change the number of blocks by passing an integer
        as the second argument e.g. avgtxsize/2000.
        """
        return QueryApi.typed_request(int, 'q', 'avgtxsize')

    @ClassProperty
    @staticmethod
    def avgtxvalue():
        """Average transaction value (1000 Default)."""
        return QueryApi.typed_request(int, 'q', 'avgtxsize')

    @ClassProperty
    @staticmethod
    def avgtxnumber():
        """Average number of transactions per block (100 Default)."""
        return QueryApi.typed_request(int, 'q', 'avgtxnumber')

    @ClassProperty
    @staticmethod
    def interval():
        """Average time between blocks in seconds."""
        return QueryApi.typed_request(float, 'q', 'interval')

    @ClassProperty
    @staticmethod
    def eta():
        """Estimated time until the next block (in seconds)."""
        return QueryApi.typed_request(float, 'q', 'eta')
