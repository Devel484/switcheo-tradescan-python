from typing import Union, List, Optional
from tradescan.utils import Request


class PublicClient(object):
    """
    This class allows the user to interact with the TradeScan API including information
    available with validators, tokens, delegators, addresses, and blockchain stats.
    """

    def __init__(self, node_ip: Union[None, str], node_port: Union[None, int] = 5001, uri: Union[None, str] = None):
        """
        Create a public client using IP:Port or URI format.

        Example::
            public_client = PublicClient("127.0.0.1", 5001)

            # or use uri method

            public_client = PublicClient(uri="https://tradehub-api-server.network/")

        :param node_ip: ip address off a tradehub node.
        :param node_port: prt off a tradehub node, default 5001.
        :param uri: URI address off tradehub node.
        """
        if node_ip and uri:
            raise ValueError("Use IP [+Port] or URI, not both!")

        if node_ip and not node_port:
            raise ValueError("Port has to be set if an IP address is provided!")

        self.api_url: str = uri or f"http://{node_ip}:{node_port}"
        self.request: Request = Request(api_url=self.api_url, timeout=30)
        # self.validators = self.get_validator_public_nodes()
        # self.transaction_types = self.get_transaction_types()
        self.tokens: List[dict] = self.get_token_list()


    # def get_address_rewards(self, address):
    #     if address is not None and isinstance(address, str):
    #         return self.request.get(path = '/distribution/delegators/' + address + '/rewards')

    # def get_address_staking(self, address):
    #     if address is not None and isinstance(address, str):
    #         return self.request.get(path = '/staking/delegators/' + address + '/delegations')

    def get_account(self, swth_address: str) -> dict:
        """
        Request account information about swth wallet.

        Example::

            # wallet behind Devel And Co validator
            public_client.get_account("swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl")

        The expected return result for this function is as follows::

            {
              "height": "6102489",
              "result": {
                "type": "cosmos-sdk/Account",
                "value": {
                  "address": "swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl",
                  "coins": [
                    {
                      "denom": "cel1",
                      "amount": "7"
                    },
                    {
                      "denom": "eth1",
                      "amount": "64752601707981"
                    },
                    {
                      "denom": "nex1",
                      "amount": "12289"
                    },
                    {
                      "denom": "nneo2",
                      "amount": "31555"
                    },
                    {
                      "denom": "swth",
                      "amount": "4113439708"
                    },
                    {
                      "denom": "usdc1",
                      "amount": "45376"
                    },
                    {
                      "denom": "wbtc1",
                      "amount": "29"
                    }
                  ],
                  "public_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "AtCcJkRx1VhzZkOV06yrxKMZ9IvdRxqv5S4gJSQI/aCB"
                  },
                  "account_number": "1756",
                  "sequence": "55"
                }
              }
            }

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: json response
        """
        api_params = {
            "account": swth_address,
        }
        return self.request.get(path='/get_account', params=api_params)

    def get_address(self, username: str) -> str:
        """
        Request swth1 tradehub address which is represented by a username.
        Example::

            public_client.get_address("devel484")

        The expected return result for this function is as follows::

            "swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz"

        .. warning:: This endpoint returns only a string if address is found. If no address is found an exception with status code 404 will be raised.

        :param username: Username is lower case
        :return: swth1 address if found
        """
        api_params = {
            "username": username
        }
        return self.request.get(path='/get_address', params=api_params)

    def get_all_validators(self) -> List[dict]:
        """
        Get all validators. This includes active, unbonding and unbonded validators.

        Example::

            public_client.get_all_validators()

        The expected return result for this function is as follows::

            [
                {
                "OperatorAddress":"swthvaloper1vwges9p847l9csj8ehrlgzajhmt4fcq4dmg8x0",
                "ConsPubKey":"swthvalconspub1zcjduepqcufdssqqfycjwz2srp42tytrs7gtdkkry9cpspea3zqsjzqd2tps73pr63",
                "Jailed":false,
                "Status":2,
                "Tokens":"22414566.55131922",
                "DelegatorShares":"22414566.55131922",
                "Description":{
                    "moniker":"Devel \u0026 Co",
                    "identity":"c572aef1818379c38996878357c321398165fcf0",
                    "website":"https://gitlab.com/switcheo-utils",
                    "security_contact":"",
                    "details":"'Devel' @Devel484 25Y (GER) and 'Coco' @colino87 33Y (FR) are two developers from the Switcheo community who have joined forces to develop awesome applications and tools to support the Switcheo Ecosystem. Stay tuned. Telegram: @DevelAndCo"},
                    "UnbondingHeight":0,
                    "UnbondingCompletionTime":"1970-01-01T00:00:00Z",
                    "Commission":{
                        "commission_rates":{
                            "rate":"0.004200000000000000",
                            "max_rate":"0.200000000000000000",
                            "max_change_rate":"0.010000000000000000"
                        },
                        "update_time":"2020-11-27T20:25:33.45991154Z"
                    },
                    "MinSelfDelegation":"1",
                    "ConsAddress":"swthvalcons1pqnlj0na6k8u9y27j3elrx584mt3380dal0j9s",
                    "ConsAddressByte":"0827F93E7DD58FC2915E9473F19A87AED7189DED",
                    "WalletAddress":"swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl",
                    "BondStatus":"bonded"
                },
                ...
            ]

        .. warning:: The response from this endpoint uses different types off name conventions! For example 'UpperCamelCase' and 'snake_case'.
        :return: list with validators
        """
        return self.request.get(path='/get_all_validators')

    def get_balance(self, swth_address: str) -> dict:
        """
        Get balance which includes available, in open orders and open positions.

        Example::

            # wallet behind Devel And Co validator
            public_client.get_balance("swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl")

        The expected return result for this function is as follows::

            {
                "cel1":{
                    "available":"0.0007",
                    "order":"0",
                    "position":"0",
                    "denom":"cel1"
                },
                "eth1":{
                    "available":"0.000064752601707981",
                    "order":"0",
                    "position":"0",
                    "denom":"eth1"
                },
                "nex1":{
                    "available":"0.00012289",
                    "order":"0",
                    "position":"0",
                    "denom":"nex1"
                },
                "nneo2":{
                    "available":"0.00031555",
                    "order":"0",
                    "position":"0",
                    "denom":"nneo2"
                },
                "swth":{
                    "available":"41.13439708",
                    "order":"0",
                    "position":"0",
                    "denom":"swth"
                },
                "usdc1":{
                    "available":"0.045376",
                    "order":"0",
                    "position":"0",
                    "denom":"usdc1"
                },
                "wbtc1":{
                    "available":"0.00000029",
                    "order":"0",
                    "position":"0",
                    "denom":"wbtc1"
                }
            }

        .. note::
            Only non zero balances are returned. Values are already in human readable version.

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: dict with currently holding tokens.
        """
        api_params = {
            "account": swth_address
        }
        return self.request.get(path='/get_balance', params=api_params)

    def get_block_time(self) -> str:
        """
        Get the block time in format HH:MM:SS.ZZZZZZ

        Example::

            public_client.get_block_time()

        The expected return result for this function is as follows::

            "00:00:02.190211"

        .. warning:: This endpoint returns only a string.

        :return: block time as string
        """
        return self.request.get(path='/get_block_time')

    def get_blocks(self, before_id: Optional[int] = None, after_id: Optional[int] = None, order_by: Optional[str] = None, swth_valcons: Optional[str] = None, limit: Optional[int] = None) -> List[dict]:
        """
        Get latest blocks or request specific blocks.

        Example::

            public_client.get_blocks()

        The expected return result for this function is as follows::

            [
                {
                    "block_height":"6103923",
                    "time":"2021-01-09T14:15:53.071509+01:00",
                    "count":"1",
                    "proposer_address":"swthvalcons17m2ueqqqt8u0jz4rv5kvk4kg0teel4sckytjlc"
                },
                {
                    "block_height":"6103922",
                    "time":"2021-01-09T14:15:50.824548+01:00",
                    "count":"0",
                    "proposer_address":"swthvalcons1zecfdrf22f6syz8xj4vn8jsvsalxdhwl9tlflk"
                },
                ...
            ]

        .. warning:: This endpoint is not well documented in official documents. The parameters are NOT required.

        :param before_id: Before block height(exclusive)
        :param after_id: After block height(exclusive)
        :param order_by: Not specified yet
        :param swth_valcons: Switcheo tradehub validator consensus starting with 'swthvalcons1' on mainnet and 'tswthvalcons1' on testnet.
        :param limit: Limit the responded result. Values greater than 200 have no effect and a maximum off 200 results are returned.
        :return: List with found blocks matching the requested parameters. Can be empty list []
        """
        api_params = {
            "before_id": before_id,
            "after_id": after_id,
            "order_by": order_by,
            "proposer": swth_valcons,
            "limit": limit
        }

        return self.request.get(path='/get_blocks', params=api_params)

    def get_candlesticks(self, market: str, granularity: int, from_epoch: int, to_epoch: int) -> List[dict]:
        """
        Get candlesticks for a market.

        Example::

            public_client.get_candlesticks("swth_eth1", 5, 1610203000, 1610203090)

        The expected return result for this function is as follows::
            [
                {
                    "id":38648,
                    "market":"swth_eth1",
                    "time":"2021-01-09T15:35:00+01:00",
                    "resolution":5,
                    "open":"0.0000212",
                    "close":"0.0000212",
                    "high":"0.0000212",
                    "low":"0.0000212",
                    "volume":"2100",
                    "quote_volume":"0.04452"
                }
            ]


        .. warning::
            This endpoint is not well documented in official documents.

            The example market swth_eth does not exist on mainnet. The correct market ticker is 'swth_eth1'.
            See get_markets() for correct tickers.

            If any off the required parameters is not provided or incorrect the server responses with 500 status codes.

            Responses are marked as 'plain' and not as 'text/json'.

            This endpoint returns numbers as string(ex. "volume":"2100") or integer(ex. "resolution":5)


        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :param granularity: Candlestick period in minutes, possible values are: 1, 5, 30, 60, 360 or 1440.
        :param from_epoch: Start of time range for data in epoch seconds.
        :param to_epoch: End of time range for data in epoch seconds.
        :return: List with candles as dict
        """
        if granularity not in [1, 5, 30, 60, 360, 1440]:
            raise ValueError(f"Granularity/Resolution has to be on off the following values: 1, 5, 30, 60, 360 or 1440")

        api_params = {
            "market": market,
            "resolution": granularity,
            "from": from_epoch,
            "to": to_epoch
        }
        return self.request.get(path='/candlesticks', params=api_params)

    def get_delegation_rewards(self, swth_address: str) -> dict:
        """
        Request delegation rewards made by a tradehub wallet.

        Example::

            # wallet behind Devel And Co validator
            public_client.get_delegation_rewards("swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl")

        The expected return result for this function is as follows::

            {
              "height": "6104998",
              "result": {
                "rewards": [
                  {
                    "validator_address": "swthvaloper1vwges9p847l9csj8ehrlgzajhmt4fcq4dmg8x0",
                    "reward": [
                      {
                        "denom": "swth",
                        "amount": "7928468882.342780820000000000"
                      },
                      ...
                    ]
                  },
                  ...
                ],
                "total": [
                  {
                    "denom": "cel1",
                    "amount": "0.032116540000000000"
                  },
                  ...
                ]
              }
            }

        .. warning::
            Only non zero balances are returned. Values are NOT in human readable version even the values contain a
            decimal separator.

        .. note::
            This endpoint does not include unclaimed commissions off a validator. If a validator wallet is requested
            only the rewards earned by delegation are returned.

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: return dict with generated unclaimed rewards.
        """
        api_params = {
            "account": swth_address,
        }
        return self.request.get(path='/get_delegation_rewards', params=api_params)

    def get_external_transfers(self, swth_address: str) -> List[dict]:
        """
        Get external transfers(withdraws or deposits) from other blockchains.

        Example::

            # wallet Devel
            public_client.get_delegation_rewards("swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz")

        The expected return result for this function is as follows::

            [
                {
                    "address":"swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz",
                    "amount":"0.9826",
                    "block_height":5937838,
                    "blockchain":"eth",
                    "contract_hash":"9a016ce184a22dbf6c17daa59eb7d3140dbd1c54",
                    "denom":"eth1",
                    "fee_address":"swth1prv0t8j8tqcdngdmjlt59pwy6dxxmtqgycy2h7",
                    "fee_amount":"0.0174",
                    "id":"12853",
                    "status":"success",
                    "symbol":"ETH",
                    "timestamp":1609839309,
                    "token_name":"Ethereum",
                    "transaction_hash":"",
                    "transfer_type":"deposit"
                },
                ...
            ]

        .. warning::
            This endpoint returns numbers as string(ex. "id":"12853") or integer(ex. "timestamp":1609839309)

        .. note::
            This endpoint return amounts in human readable format.

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: List with external transfers
        """
        api_params = {
            "account": swth_address
        }
        return self.request.get(path='/get_external_transfers', params=api_params)

    def get_insurance_fund_balance(self):
        # TODO result currently []
        return self.request.get(path='/get_insurance_balance')

    def get_leverage(self, swth_address: str, market: str):
        # TODO result currently not available
        api_params = {
            "account": swth_address,
            "market": market
        }
        return self.request.get(path='/get_leverage', params=api_params)

    def get_liquidations(self, before_id: int, after_id: int, order_by: str, limit: int):
        # TODO result currently not available
        api_params = {
            "before_id": before_id,
            "after_id": after_id,
            "order_by": order_by,
            "limit": limit
        }
        return self.request.get(path='/get_liquidations', params=api_params)

    def get_market(self, market: str) -> dict:
        """
        Get information about a market.

        Example::
            public_client.get_market("swth_eth1")

        The expected return result for this function is as follows::

           {
                "type":"",
                "name":"swth_eth1",
                "display_name":"SWTH_ETH",
                "description":"SWTH/ETH Spot Market",
                "market_type":"spot",
                "base":"swth",
                "base_name":"Switcheo",
                "base_precision":8,
                "quote":"eth1",
                "quote_name":"Ethereum",
                "quote_precision":18,
                "lot_size":"1",
                "tick_size":"0.0000001",
                "min_quantity":"200",
                "maker_fee":"-0.0005",
                "taker_fee":"0.0025",
                "risk_step_size":"0",
                "initial_margin_base":"1",
                "initial_margin_step":"0",
                "maintenance_margin_ratio":"0",
                "max_liquidation_order_ticket":"0",
                "max_liquidation_order_duration":0,
                "impact_size":"0",
                "mark_price_band":0,
                "last_price_protected_band":0,
                "index_oracle_id":"",
                "expiry_time":"1970-01-01T01:00:00+01:00",
                "is_active":true,
                "is_settled":false,
                "closed_block_height":0,
                "created_block_height":0
            }

        .. warning::
            This endpoint is not well documented in official documents.

            The example market swth_eth does not exist on mainnet. The correct market ticker is 'swth_eth1'.
            See get_markets() for correct tickers.

            This endpoint returns numbers as string(eg. "lot_size":"1") or integer(eg. "base_precision":8)

            This endpoint returns the same dict structure even the market does not exist with default values!

        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :return:
        """
        api_params = {
            "market": market,
        }
        return self.request.get(path='/get_market', params=api_params)

    def get_market_stats(self, market: Optional[str] = None) -> List[dict]:
        """
        Get statistics about one or all markets.

        Example::
            public_client.get_market_stats()

        The expected return result for this function is as follows::

            [
                {
                    "day_high":"0.0000215",
                    "day_low":"0.000021",
                    "day_open":"0.0000211",
                    "day_close":"0.0000212",
                    "day_volume":"436030",
                    "day_quote_volume":"9.2787298",
                    "index_price":"0",
                    "mark_price":"0",
                    "last_price":"212000",
                    "market":"swth_eth1",
                    "market_type":"spot",
                    "open_interest":"0"
                }
                ...
            ]

        .. warning::
            Values are in human readable format except field: "last_price":"212000" which is: 0.0000212

        .. note::
            This endpoint does not include unclaimed commissions off a validator. If a validator wallet is requested
            only the rewards earned by delegation are returned.

        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :return: List with market stats as dict
        """
        api_params = {
            "market": market
        }
        return self.request.get(path='/get_market_stats', params=api_params)

    def get_markets(self, market_type: Optional[str] = None, is_active: Optional[bool] = None, is_settled: Optional[bool] = None) -> List[dict]:
        """
        Get all markets or filter markets.

        Example::

            public_client.get_markets()

        The expected return result for this function is as follows::

            [
                {
                    "type":"",
                    "name":"swth_eth1",
                    "display_name":"SWTH_ETH",
                    "description":"SWTH/ETH Spot Market",
                    "market_type":"spot",
                    "base":"swth",
                    "base_name":"Switcheo",
                    "base_precision":8,
                    "quote":"eth1",
                    "quote_name":"Ethereum",
                    "quote_precision":18,
                    "lot_size":"1",
                    "tick_size":"0.0000001",
                    "min_quantity":"200",
                    "maker_fee":"-0.0005",
                    "taker_fee":"0.0025",
                    "risk_step_size":"0",
                    "initial_margin_base":"1",
                    "initial_margin_step":"0",
                    "maintenance_margin_ratio":"0",
                    "max_liquidation_order_ticket":"0",
                    "max_liquidation_order_duration":0,
                    "impact_size":"0",
                    "mark_price_band":0,
                    "last_price_protected_band":0,
                    "index_oracle_id":"",
                    "expiry_time":"1970-01-01T01:00:00+01:00",
                    "is_active":true,
                    "is_settled":false,
                    "closed_block_height":0,
                    "created_block_height":0
                },
                ...
            ]

        .. warning::
            This endpoint returns numbers as string(eg. "lot_size":"1") or integer(eg. "base_precision":8)

        :param market_type: type of the market can be 'futures' or 'spot'
        :param is_active: if only active markets should be returned
        :param is_settled: if only settled markets should be returned
        :return: List with returned market stats as dict
        """

        if market_type not in ['futures', 'spot']:
            raise ValueError(f"Parameter 'market_type' only can be 'futures' or 'spot'. Got {market_type} instead.")

        api_params = {
            "market_type": market_type,
            "is_active": is_active,
            "is_settled": is_settled
        }

        return self.request.get(path='/get_markets', params=api_params)

    def get_oracle_result(self, oracle_id: str):
        # TODO no results yet available
        api_params = {
            "id": oracle_id
        }
        return self.request.get(path='/get_oracle_result', params=api_params)

    def get_oracle_results(self):
        # TODO no results yet available
        return self.request.get(path='/get_oracle_results')

    def get_orderbook(self, market: str, limit: Optional[int] = None):
        """
        Get the orderbook from a market.

        Example::

            public_client.get_orderbook("swth_eth1")

        The expected return result for this function is as follows::

            {
                "asks": [
                    {
                        "price":"0.0000214",
                        "quantity":"49863"
                    },
                    {
                        "price":"0.0000215",
                        "quantity":"49446"
                    },
                    ...
                ],
                "bids": [
                    {
                        "price":"0.0000212",
                        "quantity":"50248"
                    },
                    {
                        "price":"0.0000211",
                        "quantity":"50295"
                    },
                    ...
                ]
            }

         .. warning::
            This endpoint returns an empty 'asks' and 'bids' list if the market is not known.

        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :param limit: Number off returned orders per side(asks, bids).
        :return: Orderbook as 'asks' and 'bids' list
        """
        api_params = {
            "market": market,
            "limit": limit
        }
        return self.request.get(path='/get_orderbook', params=api_params)

    def get_order(self, order_id: str) -> dict:
        """
        Get a specific order by id.

        Example::

            public_client.get_order("4F54D2AE0D793F833806109B4278335BF3D392D4096B682B9A27AF9F8A8BCA58")

        The expected return result for this function is as follows:

            {
                "order_id":"4F54D2AE0D793F833806109B4278335BF3D392D4096B682B9A27AF9F8A8BCA58",
                "block_height":6117321,
                "triggered_block_height":0,
                "address":"swth1wmcj8gmz4tszy5v8c0d9lxnmguqcdkw22275w5",
                "market":"eth1_usdc1",
                "side":"buy",
                "price":"1255.68",
                "quantity":"0.01",
                "available":"0.01",
                "filled":"0",
                "order_status":"open",
                "order_type":"limit",
                "initiator":"amm",
                "time_in_force":"gtc",
                "stop_price":"0",
                "trigger_type":"",
                "allocated_margin_denom":"usdc1",
                "allocated_margin_amount":"0",
                "is_liquidation":false,
                "is_post_only":false,
                "is_reduce_only":false,
                "type":"",
                "block_created_at":"2021-01-09T22:13:34.711571+01:00",
                "username":"",
                "id":"990817"
            }

        :param order_id: Order identified by id
        :return: Order as dict
        """
        api_params = {
            "order_id": order_id
        }
        return self.request.get(path='/get_order', params=api_params)

    def get_orders(self, swth_address: Optional[str] = None, before_id: Optional[int] = None,
                   after_id: Optional[int] = None, market: Optional[str] = None, order_type: Optional[str] = None,
                   initiator: Optional[str] = None, order_status: Optional[str] = None, limit: Optional[int] = None) -> List[dict]:
        """
        Request last orders or filter them.

        Example::

            public_client.get_orders()

        The expected return result for this function is as follows::

            [
                {
                    "order_id":"4F54D2AE0D793F833806109B4278335BF3D392D4096B682B9A27AF9F8A8BCA58",
                    "block_height":6117321,
                    "triggered_block_height":0,
                    "address":"swth1wmcj8gmz4tszy5v8c0d9lxnmguqcdkw22275w5",
                    "market":"eth1_usdc1",
                    "side":"buy",
                    "price":"1255.68",
                    "quantity":"0.01",
                    "available":"0.01",
                    "filled":"0",
                    "order_status":"open",
                    "order_type":"limit",
                    "initiator":"amm",
                    "time_in_force":"gtc",
                    "stop_price":"0",
                    "trigger_type":"",
                    "allocated_margin_denom":"usdc1",
                    "allocated_margin_amount":"0",
                    "is_liquidation":false,
                    "is_post_only":false,
                    "is_reduce_only":false,
                    "type":"",
                    "block_created_at":"2021-01-09T22:13:34.711571+01:00",
                    "username":"",
                    "id":"990817"
                },
                ...
            ]

        .. warning::
            This endpoint is not well documented in official documents.
            Parameter account is NOT required! It is possible to give more parameters, known ones are documented here.

            This endpoint returns numbers as string(eg. "id":"990817") or integer(eg. "block_height":6117321)

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :param before_id: return orders before id(exclusive)
        :param after_id: return orders after id(exclusive)
        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :param order_type: Return specific orders, allowed values: 'limit', 'market', 'stop-market' or 'stop-limit'
        :param initiator: Filter by user oder automated market maker order, allowed values: 'user' or 'amm'
        :param order_status: Filter by order status, allowed values: 'open' or 'closed'
        :param limit: Limit response, values above 200 have no effect
        :return: List off orders as dict
        """
        api_params = {
            "account": swth_address,
            "before_id": before_id,
            "after_id": after_id,
            "market": market,
            "order_type": order_type,
            "initiator": initiator,
            "order_status": order_status,
            "limit": limit
        }
        return self.request.get(path='/get_orders', params=api_params)

    def get_position(self, swth_address: str, market: str):
        # TODO responses currently not available
        api_params = {
            "account": swth_address,
            "market": market
        }
        return self.request.get(path='/get_position', params=api_params)

    def get_positions(self, swth_address: str):
        # TODO responses currently not available
        api_params = {
            "account": swth_address
        }
        return self.request.get(path='/get_positions', params=api_params)

    def get_positions_sorted_by_pnl(self, market):
        # TODO responses currently not available
        api_params = {
            "market": market
        }
        return self.request.get(path='/get_positions_sorted_by_pnl', params=api_params)

    def get_positions_sorted_by_risk(self, market):
        # TODO responses currently not available
        api_params = {
            "market": market
        }
        return self.request.get(path='/get_positions_sorted_by_risk', params=api_params)

    def get_positions_sorted_by_size(self, market):
        # TODO responses currently not available
        api_params = {
            "market": market
        }
        return self.request.get(path='/get_positions_sorted_by_size', params=api_params)

    def get_prices(self, market: Optional[str]) -> dict:
        """
        Get prices off a market.

        Example::

            public_client.get_prices("swth_eth1")

        The expected return result for this function is as follows::

            {
                "last":"207000",
                "index":"0",
                "fair":"0",
                "mark":"0",
                "mark_avg":"0",
                "settlement":"0",
                "fair_index_delta_avg":"0",
                "market":"",
                "marking_strategy":"",
                "index_updated_at":"0001-01-01T00:00:00Z",
                "last_updated_at":"2021-01-09T22:50:59.068526+01:00",
                "block_height":0
            }

        .. warning::
            This endpoint is not well documented in official documents.
            Parameter 'market' is NOT required, but strongly recommended. The return result has an empty 'market' field.

            This endpoint returns amounts which are NOT human readable values. Consider 'base_precision' and
            'quote_precision' to calculate a multiplication factor = 10 ^ ('base_precision' - 'quote_precision')

            This endpoint returns numbers as string(eg. "last":"207000") or integer(eg. "block_height":0)

        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :return: Prices as dict
        """
        api_params = {
            "market": market
        }
        return self.request.get(path='/get_prices', params=api_params)

    def get_profile(self, swth_address: str) -> dict:
        """
        Get profile from a tradehub wallet.

        Example::

            public_client.get_profile("swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz")

        The expected return result for this function is as follows::

            {
                "address":"swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz",
                "last_seen_block":"6036318",
                "last_seen_time":"2021-01-07T21:47:14.593249+01:00",
                "twitter":"",
                "username":"devel484"
            }


        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: Profile as dict
        """
        api_params = {
            "account": swth_address
        }
        return self.request.get(path='/get_profile', params=api_params)

    def get_rich_list(self, token: str):
        '''
            This does not appear to be working.
        '''
        api_params = {
            "token": token
        }
        return self.request.get(path='/get_rich_list', params=api_params)

    def get_status(self) -> dict:
        """
        Return cosmos RPC status endpoint.

        Example::

            public_client.get_status()

        The expected return result for this function is as follows::

            {
              "jsonrpc": "2.0",
              "id": -1,
              "result": {
                "node_info": {
                  "protocol_version": {
                    "p2p": "7",
                    "block": "10",
                    "app": "0"
                  },
                  "id": "f4cee80e4dec5a686139cb82729118e15f7ce19c",
                  "listen_addr": "tcp://0.0.0.0:26656",
                  "network": "switcheo-tradehub-1",
                  "version": "0.33.7",
                  "channels": "4020212223303800",
                  "moniker": "Devel Sentry Node 2",
                  "other": {
                    "tx_index": "on",
                    "rpc_address": "tcp://0.0.0.0:26659"
                  }
                },
                "sync_info": {
                  "latest_block_hash": "4A2C89C105D7864AA74C9DE4752AF5B59E96045EBAF984C69DD447C4524EC36F",
                  "latest_app_hash": "773651392EEDBFF6AEE088F76E7D75F2932B4D9F74CA27D568F706ADFC12B174",
                  "latest_block_height": "6119142",
                  "latest_block_time": "2021-01-09T22:18:52.722611018Z",
                  "earliest_block_hash": "B4AF1F3D3D3FD5795BDDB7A6A2E6CA4E34D06338505D6EC46DD8F99E72ADCDAB",
                  "earliest_app_hash": "",
                  "earliest_block_height": "1",
                  "earliest_block_time": "2020-08-14T07:32:27.856700491Z",
                  "catching_up": false
                },
                "validator_info": {
                  "address": "DCB03C204B7F94765B4ADCE1D8BEE88AA43AE811",
                  "pub_key": {
                    "type": "tendermint/PubKeyEd25519",
                    "value": "1GmDSymN6jTqQlZA2KeyzqknIncGMMrwnnas/DWGNOI="
                  },
                  "voting_power": "0"
                }
              }
            }

        :return: Status as dict
        """
        return self.request.get(path='/get_status')

    def get_transaction(self, hash):
        api_params = {}
        api_params["hash"] = hash
        return self.request.get(path = '/get_transaction', params = api_params)

    def get_transaction_types(self):
        return self.request.get(path = '/get_transaction_types')

    def get_transactions(self, swth_address: Optional[str] = None, msg_type: Optional[str] = None,
                         height: Optional[int] = None, start_block: Optional[int] = None,
                         end_block: Optional[int] = None, before_id: Optional[int] = None,
                         after_id: Optional[int] = None, order_by: Optional[str] = None,
                         limit: Optional[int] = None) -> List[dict]:
        """
        Get latest transactions or filter them.

        Example::

            public_client.get_transactions()

        The expected return result for this function is as follows::

            [
                {
                    "id":"322811",
                    "hash":"9742B27016F08484D8FADFD361C34563F3FDA92A36A8DD3B844A2F86E3552451",
                    "address":"swth1xkahzn8ymps6xdu6feulutawu42fkyqz5fgvhx",
                    "username":"",
                    "msg_type":"create_order",
                    "msg":"{\"market\":\"eth1_usdc1\",\"side\":\"buy\",\"quantity\":\"0.019\",\"type\":\"limit\",\"price\":\"1283.98\",\"is_post_only\":false,\"is_reduce_only\":false,\"originator\":\"swth1xkahzn8ymps6xdu6feulutawu42fkyqz5fgvhx\"}",
                    "code":"0",
                    "gas_used":"140666",
                    "gas_limit":"100000000000",
                    "memo":"",
                    "height":"6119373",
                    "block_time":"2021-01-09T23:27:10.247711+01:00"
                },
                ...
            ]

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :param msg_type: filter by msg_type, allowed values can be fetch with 'get_transaction_types'
        :param height: get order at a specific height
        :param start_block: get orders after block(exclusive)
        :param end_block: get orders before block(exclusive)
        :param before_id: get orders before id(exclusive)
        :param after_id: get orders after id(exclusive)
        :param order_by: TODO no official documentation
        :param limit: limit the responded result, values above 200 have no effect
        :return: List with transactions as dict
        """
        api_params = {
            "address": swth_address,
            "msg_type": msg_type,
            "height": height,
            "start_block": start_block,
            "end_block": end_block,
            "before_id": before_id,
            "after_id": after_id,
            "order_by": order_by,
            "limit": limit
        }
        return self.request.get(path='/get_transactions', params=api_params)

    def get_token(self, token):
        '''
        This endpoint does not exist on the TradeHub nodes but it does exist in TradeScan.
        This has benn built to mimic what TradeScan returns.
        '''
        if token is not None and token.lower() in self.tokens:
            for get_token in self.get_tokens():
                if get_token["denom"] == token.lower():
                    return get_token

    def get_token_list(self):
        token_list = []
        tokens = self.get_tokens()
        for token in tokens:
            token_list.append(token["denom"])
        return token_list

    def get_tokens(self):
        return self.request.get(path = '/get_tokens')

    def get_top_r_profits(self, market, limit):
        api_params = {}
        api_params["market"] = market
        api_params["limit"] = limit
        return self.request.get(path = '/get_top_r_profits', params = api_params)

    def get_total_balances(self):
        '''
            This doesn't appear to be working.
        '''
        return self.request.get(path = '/get_total_balances')

    def get_trades(self, market, before_id, after_id, order_by, limit):
        api_params = {}
        api_params["market"] = market
        api_params["before_id"] = before_id
        api_params["after_id"] = after_id
        api_params["order_by"] = order_by
        api_params["limit"] = limit
        return self.request.get(path = '/get_trades', params = api_params)

    def get_trades_by_account(self, before_id, after_id, order_by, limit):
        '''
            This appears to be dead.
        '''
        api_params = {}
        api_params["before_id"] = before_id
        api_params["after_id"] = after_id
        api_params["order_by"] = order_by
        api_params["limit"] = limit
        return self.request.get(path = '/get_trades_by_account', params = api_params)

    def get_username_check(self, username):
        api_params = {}
        api_params["username"] = username
        return self.request.get(path = '/username_check', params = api_params)
