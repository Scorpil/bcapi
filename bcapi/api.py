import requests

from bcapi.resources import Block, Tx, TxOut, Address, MultiAddress


class DataApi(object):

    base_url = "http://blockchain.info/"

    @staticmethod
    def block(block):
        raw_json = DataApi.request('rawblock', block)
        return Block(raw_json)

    @staticmethod
    def tx(tx):
        raw_json = DataApi.request('rawtx', tx)
        return Tx(raw_json)

    @staticmethod
    def chart_data(chart_type, **kwargs):
        kwargs.setdefault('format', 'json')
        return DataApi.request('charts', chart_type, **kwargs)['values']

    @staticmethod
    def block_height(height, **kwargs):
        kwargs.setdefault('format', 'json')
        raw_json = DataApi.request('block-height', height, **kwargs)
        return [Block(raw_block) for raw_block in raw_json['blocks']]

    @staticmethod
    def address(address, **kwargs):
        if isinstance(address, Address):
            address = address.address
        raw_json = DataApi.request('rawaddr', address, **kwargs)
        return Address(raw_json)

    @staticmethod
    def multi_address(adresses, **kwargs):
        kwargs['active'] = '|'.join(adresses)
        raw_json = DataApi.request('multiaddr', **kwargs)
        return MultiAddress(raw_json)

    @staticmethod
    def unspent(addresses):
        if isinstance(adresses, list):
            addresses = '|'.join(adresses)
        raw_json = DataApi.request('unspent', active=addresses)
        return [TxOut(tx_out) for tx_out in raw_json['unspent_outputs']]

    @staticmethod
    def latest_block():
        block_hash = DataApi.request('latestblock')['hash']
        raw_json = DataApi.request('rawblock', block_hash)
        return Block(raw_json)

    @staticmethod
    def unconfirmed_txs(**kwargs):
        kwargs.setdefault('format', 'json')
        raw_json = DataApi.request('unconfirmed-transactions', **kwargs)
        return [Tx(raw_tx) for raw_tx in raw_json['txs']]

    @staticmethod
    def request(*args, **kwargs):
        url = DataApi.base_url + '/'.join(tuple(map(str, args)))
        response = requests.get(url, params=kwargs)
        response.raise_for_status()
        return response.json()
