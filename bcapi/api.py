import requests
from utils import lazyproperty


class Resource(object):
    def __init__(self, raw_json):
        self.raw_json = raw_json

    def __getattr__(self, name):
        return self.raw_json[name]


class Block(Resource):
    @lazyproperty
    def tx(self):
        return [Tx(raw_t, block=self) for raw_t in self.raw_json['tx']]

    def __repr__(self):
        return "<Block: %s>" % self.hash


class Tx(Resource):
    def __init__(self, raw_json, block=None):
        super(Tx, self).__init__(raw_json)
        self.block = block

    @lazyproperty
    def inputs(self):
        if self.raw_json['inputs'] and self.raw_json['inputs'][0]:
            return [TxIn(inputs, tx=self) for inputs in self.raw_json['inputs']]
        return None

    @lazyproperty
    def out(self):
        if self.raw_json['out'] and self.raw_json['out'][0]:
            return [TxOut(out, tx=self) for out in self.raw_json['out']]
        return None

    def __repr__(self):
        return "<Tx: %s>" % self.hash


class TxIO(Resource):
    def __init__(self, raw_json, tx):
        super(TxIO, self).__init__(raw_json)
        self.tx = tx


class TxIn(TxIO):
    def __repr__(self):
        return "<Tx Input: %.5f BTC from %s>" % (self.value / float(100000000), self.addr)


class TxOut(TxIO):
    def __repr__(self):
        return "<Tx Output: %.5f BTC to %s>" % (self.value / float(100000000), self.addr)


class Api(object):

    base_url = "http://blockchain.info/"

    @staticmethod
    def latest_block():
        block_hash = Api.request('latestblock')['hash']
        raw_json = Api.request('rawblock', block_hash)
        return Block(raw_json)

    @staticmethod
    def get_block(block):
        raw_json = Api.request('rawblock', block)
        return Block(raw_json)

    @staticmethod
    def get_tx(tx):
        raw_json = Api.request('rawtx', tx)
        return Tx(raw_json)

    @staticmethod
    def request(*args, **kwargs):
        url = Api.base_url + '/'.join(tuple(map(str, args)))
        response = requests.get(url, params=kwargs)
        response.raise_for_status()
        return response.json()
