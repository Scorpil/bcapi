**bcapi** - [BlockChain.info](http://blockchain.info/) API wrapper.

**This is tool is under heavy development. Use at your own risk.**

## Api classes

### bcapi.DataApi

Wrapper for [Data API](https://blockchain.info/api/blockchain_api):

  * **block(block_id)**: Get block info. __block_id__ may be block hash or block index
  * **tx(tx_id)**: Get transaction info. __tx_id__ may be transaction hash or transaction index
  * **block_height(height)**: Get list of blocks at the specified height.
  * **address(address)**: Get address info.
  * **multi_address(addresses)**: Get multiple adresses info.
  * **unspent(addresses)**: Get unspent outputs.
  * **latest_block()**: Get latest block.
  * **unconfirmed_txs()**: Get currently unconfirmed transactions.


### bcapi.StatsApi

Wrapper for [Stats API](https://blockchain.info/api/charts_api):

  * __charts(chart_type, **kwargs)__: Returns json values corresponding to the data seen on the requested chart.
  * __stats(**kwargs)__: Returns a JSON object containing the statistics seen on the stats page.

Pass URL parameters as keyword arguments. For example, data for [this chart](https://blockchain.info/charts/transaction-fees?timespan=30days&showDataPoints=false&daysAverageString=1&show_header=true&scale=0&address=) can be retrieved like this:

    import bcapi
	data = bcapi.StatsApi.charts('transaction-fees',
	                             timespan='30days',
				                 showDataPoints=False,
						         daysAverageString=1,
								 show_header=True,
								 scale=0,
								 address=None)


### bcapi.ExchangeApi

Wrapper for [Exchange Rates API](https://blockchain.info/api/exchange_rates_api):

  * **ticker()**: Returns BTC market price.
  * **tobtc(currency, value)**: Convert value in the provided currency to btc.


### bcapi.QueryApi

Wrapper for [Simple Query API](https://blockchain.info/q):

  * **difficulty()**: Current difficulty target as a decimal number.
  * **blockcount()**: Current block height in the longest chain.
  * **latesthash()**: Hash of the latest block.
  * **bcperblock()**: Current block reward in BTC.
  * **totalbc()**: Total Bitcoins in circulation (delayed by upto 1 hour).
  * **probability()**: Probability of finding a valid block each hash attempt.
  * **hashestowin()**: Average number of hash attempts needed to solve a block.
  * **nextretarget()**: Block height of the next difficulty retarget.
  * **avgtxsize()**: Average transaction size for the past 1000 blocks.
  * **avgtxvalue()**: Average transaction value for the past 1000 blocks.
  * **avgtxnumber()**: Average number of transactions per block (100 Default).
  * **interval()**: Average time between blocks in seconds.
  * **eta()**: Estimated time until the next block (in seconds).


## Resources

  * **bcapi.resources.Block**: represents block in BlockChain
    * **Block.tx**: block transactions
	* **Block.prev_block**: previous block
  * **bcapi.resources.Tx**: represents transaction
    * **Tx.inputs**: transaction inputs
	* **Tx.out**: transaction outputs
  * **bcapi.resources.TxIn**: represents transaction input
  * **bcapi.resources.TxOut**: represents transaction output
  * **bcapi.resources.Address**: represents BitCoin address
    * **Address.txs**: address transactions
