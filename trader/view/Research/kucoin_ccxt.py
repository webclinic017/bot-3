from ccxt.base.exchange import Exchange
import hashlib
import math
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import AccountSuspended
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce
from ccxt.base.precise import Precise


class kucoin(Exchange):

    def describe(self):
        return self.deep_extend(super(kucoin, self).describe(), {
            'id': 'kucoin',
            'name': 'KuCoin',
            'countries': ['SC'],
            'rateLimit': 334,
            'version': 'v2',
            'certified': False,
            'pro': True,
            'comment': 'Platform 2.0',
            'has': {
                'CORS': False,
                'cancelAllOrders': True,
                'cancelOrder': True,
                'createDepositAddress': True,
                'createOrder': True,
                'fetchAccounts': True,
                'fetchBalance': True,
                'fetchClosedOrders': True,
                'fetchCurrencies': True,
                'fetchDepositAddress': True,
                'fetchDeposits': True,
                'fetchFundingFee': True,
                'fetchLedger': True,
                'fetchMarkets': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchStatus': True,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTime': True,
                'fetchTrades': True,
                'fetchWithdrawals': True,
                'withdraw': True,
                'transfer': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/87295558-132aaf80-c50e-11ea-9801-a2fb0c57c799.jpg',
                'referral': 'https://www.kucoin.com/?rcode=E5wkqe',
                'api': {
                    'public': 'https://openapi-v2.kucoin.com',
                    'private': 'https://openapi-v2.kucoin.com',
                    'futuresPrivate': 'https://api-futures.kucoin.com',
                    'futuresPublic': 'https://api-futures.kucoin.com',
                },
                'test': {
                    'public': 'https://openapi-sandbox.kucoin.com',
                    'private': 'https://openapi-sandbox.kucoin.com',
                    'futuresPrivate': 'https://api-sandbox-futures.kucoin.com',
                    'futuresPublic': 'https://api-sandbox-futures.kucoin.com',
                },
                'www': 'https://www.kucoin.com',
                'doc': [
                    'https://docs.kucoin.com',
                ],
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'password': True,
            },
            'api': {
                'public': {
                    'get': [
                        'timestamp',
                        'status',
                        'symbols',
                        'markets',
                        'market/allTickers',
                        'market/orderbook/level{level}_{limit}',
                        'market/orderbook/level2_20',
                        'market/orderbook/level2_100',
                        'market/histories',
                        'market/candles',
                        'market/stats',
                        'currencies',
                        'currencies/{currency}',
                        'prices',
                        'mark-price/{symbol}/current',
                        'margin/config',
                    ],
                    'post': [
                        'bullet-public',
                    ],
                },
                'private': {
                    'get': [
                        'market/orderbook/level{level}',
                        'market/orderbook/level2',
                        'market/orderbook/level3',
                        'accounts',
                        'accounts/{accountId}',
                        'accounts/{accountId}/ledgers',
                        'accounts/{accountId}/holds',
                        'accounts/transferable',
                        'sub/user',
                        'sub-accounts',
                        'sub-accounts/{subUserId}',
                        'deposit-addresses',
                        'deposits',
                        'hist-deposits',
                        'hist-orders',
                        'hist-withdrawals',
                        'withdrawals',
                        'withdrawals/quotas',
                        'orders',
                        'order/client-order/{clientOid}',
                        'orders/{orderId}',
                        'limit/orders',
                        'fills',
                        'limit/fills',
                        'margin/account',
                        'margin/borrow',
                        'margin/borrow/outstanding',
                        'margin/borrow/borrow/repaid',
                        'margin/lend/active',
                        'margin/lend/done',
                        'margin/lend/trade/unsettled',
                        'margin/lend/trade/settled',
                        'margin/lend/assets',
                        'margin/market',
                        'margin/trade/last',
                        'stop-order/{orderId}',
                        'stop-order',
                        'stop-order/queryOrderByClientOid',
                    ],
                    'post': [
                        'accounts',
                        'accounts/inner-transfer',
                        'accounts/sub-transfer',
                        'deposit-addresses',
                        'withdrawals',
                        'orders',
                        'orders/multi',
                        'margin/borrow',
                        'margin/order',
                        'margin/repay/all',
                        'margin/repay/single',
                        'margin/lend',
                        'margin/toggle-auto-lend',
                        'bullet-private',
                        'stop-order',
                    ],
                    'delete': [
                        'withdrawals/{withdrawalId}',
                        'orders',
                        'orders/client-order/{clientOid}',
                        'orders/{orderId}',
                        'margin/lend/{orderId}',
                        'stop-order/cancelOrderByClientOid',
                        'stop-order/{orderId}',
                        'stop-order/cancel',
                    ],
                },
                'futuresPublic': {
                    'get': [
                        'contracts/active',
                        'contracts/{symbol}',
                        'ticker',
                        'level2/snapshot',
                        'level2/depth20',
                        'level2/depth100',
                        'level2/message/query',
                        'level3/message/query',  # deprecated，level3/snapshot is suggested
                        'level3/snapshot',  # v2
                        'trade/history',
                        'interest/query',
                        'index/query',
                        'mark-price/{symbol}/current',
                        'premium/query',
                        'funding-rate/{symbol}/current',
                        'timestamp',
                        'status',
                        'kline/query',
                    ],
                    'post': [
                        'bullet-public',
                    ],
                },
                'futuresPrivate': {
                    'get': [
                        'account-overview',
                        'transaction-history',
                        'deposit-address',
                        'deposit-list',
                        'withdrawals/quotas',
                        'withdrawal-list',
                        'transfer-list',
                        'orders',
                        'stopOrders',
                        'recentDoneOrders',
                        'orders/{order-id}',  # ?clientOid={client-order-id}  # get order by orderId
                        'orders/byClientOid',  # ?clientOid=eresc138b21023a909e5ad59  # get order by clientOid
                        'fills',
                        'recentFills',
                        'openOrderStatistics',
                        'position',
                        'positions',
                        'funding-history',
                    ],
                    'post': [
                        'withdrawals',
                        'transfer-out',  # v2
                        'orders',
                        'position/margin/auto-deposit-status',
                        'position/margin/deposit-margin',
                        'bullet-private',
                    ],
                    'delete': [
                        'withdrawals/{withdrawalId}',
                        'cancel/transfer-out',
                        'orders/{order-id}',
                        'orders',
                        'stopOrders',
                    ],
                },
            },
            'timeframes': {
                '1m': '1min',
                '3m': '3min',
                '5m': '5min',
                '15m': '15min',
                '30m': '30min',
                '1h': '1hour',
                '2h': '2hour',
                '4h': '4hour',
                '6h': '6hour',
                '8h': '8hour',
                '12h': '12hour',
                '1d': '1day',
                '1w': '1week',
            },
            'exceptions': {
                'exact': {
                    'order not exist': OrderNotFound,
                    'order not exist.': OrderNotFound,  # duplicated error temporarily
                    'order_not_exist': OrderNotFound,  # {"code":"order_not_exist","msg":"order_not_exist"} ¯\_(ツ)_/¯
                    'order_not_exist_or_not_allow_to_cancel': InvalidOrder,
                    # {"code":"400100","msg":"order_not_exist_or_not_allow_to_cancel"}
                    'Order size below the minimum requirement.': InvalidOrder,
                    # {"code":"400100","msg":"Order size below the minimum requirement."}
                    'The withdrawal amount is below the minimum requirement.': ExchangeError,
                    # {"code":"400100","msg":"The withdrawal amount is below the minimum requirement."}
                    'Unsuccessful! Exceeded the max. funds out-transfer limit': InsufficientFunds,
                    # {"code":"200000","msg":"Unsuccessful! Exceeded the max. funds out-transfer limit"}
                    '400': BadRequest,
                    '401': AuthenticationError,
                    '403': NotSupported,
                    '404': NotSupported,
                    '405': NotSupported,
                    '429': RateLimitExceeded,
                    '500': ExchangeNotAvailable,
                    # Internal Server Error -- We had a problem with our server. Try again later.
                    '503': ExchangeNotAvailable,
                    '101030': PermissionDenied,  # {"code":"101030","msg":"You haven't yet enabled the margin trading"}
                    '200004': InsufficientFunds,
                    '230003': InsufficientFunds,  # {"code":"230003","msg":"Balance insufficient!"}
                    '260100': InsufficientFunds,  # {"code":"260100","msg":"account.noBalance"}
                    '300000': InvalidOrder,
                    '400000': BadSymbol,
                    '400001': AuthenticationError,
                    '400002': InvalidNonce,
                    '400003': AuthenticationError,
                    '400004': AuthenticationError,
                    '400005': AuthenticationError,
                    '400006': AuthenticationError,
                    '400007': AuthenticationError,
                    '400008': NotSupported,
                    '400100': BadRequest,
                    '411100': AccountSuspended,
                    '415000': BadRequest,  # {"code":"415000","msg":"Unsupported Media Type"}
                    '500000': ExchangeError,
                },
                'broad': {
                    'Exceeded the access frequency': RateLimitExceeded,
                    'require more permission': PermissionDenied,
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.001,
                    'maker': 0.001,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {},
                    'deposit': {},
                },
            },
            'commonCurrencies': {
                'HOT': 'HOTNOW',
                'EDGE': 'DADI',  # https://github.com/ccxt/ccxt/issues/5756
                'WAX': 'WAXP',
                'TRY': 'Trias',
                'VAI': 'VAIOT',
            },
            'options': {
                'version': 'v1',
                'symbolSeparator': '-',
                'fetchMyTradesMethod': 'private_get_fills',
                'fetchBalance': 'trade',
                # endpoint versions
                'versions': {
                    'public': {
                        'GET': {
                            'status': 'v1',
                            'market/orderbook/level2_20': 'v1',
                            'market/orderbook/level2_100': 'v1',
                            'market/orderbook/level{level}_{limit}': 'v1',
                        },
                    },
                    'private': {
                        'GET': {
                            'market/orderbook/level2': 'v3',
                            'market/orderbook/level3': 'v3',
                            'market/orderbook/level{level}': 'v3',
                        },
                        'POST': {
                            'accounts/inner-transfer': 'v2',
                            'accounts/sub-transfer': 'v2',
                        },
                    },
                    'futuresPrivate': {
                        'GET': {
                            'account-overview': 'v1',
                            'positions': 'v1',
                        },
                        'POST': {
                            'transfer-out': 'v2',
                        },
                    },
                    'futuresPublic': {
                        'GET': {
                            'level3/snapshot': 'v2',
                        },
                    },
                },
                'accountsByType': {
                    'trade': 'trade',
                    'trading': 'trade',
                    'spot': 'trade',
                    'margin': 'margin',
                    'main': 'main',
                    'funding': 'main',
                    'futures': 'contract',
                    'contract': 'contract',
                    'pool': 'pool',
                    'pool-x': 'pool',
                },
            },
        })

    def nonce(self):
        return self.milliseconds()

    def load_time_difference(self, params={}):
        response = self.publicGetTimestamp(params)
        after = self.milliseconds()
        kucoinTime = self.safe_integer(response, 'data')
        self.options['timeDifference'] = int(after - kucoinTime)
        return self.options['timeDifference']

    def fetch_time(self, params={}):
        response = self.publicGetTimestamp(params)
        #
        #     {
        #         "code":"200000",
        #         "msg":"success",
        #         "data":1546837113087
        #     }
        #
        return self.safe_integer(response, 'data')

    def fetch_status(self, params={}):
        response = self.publicGetStatus(params)
        #
        #     {
        #         "code":"200000",
        #         "data":{
        #             "msg":"",
        #             "status":"open"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        status = self.safe_value(data, 'status')
        if status is not None:
            status = 'ok' if (status == 'open') else 'maintenance'
            self.status = self.extend(self.status, {
                'status': status,
                'updated': self.milliseconds(),
            })
        return self.status

    def fetch_markets(self, params={}):
        response = self.publicGetSymbols(params)
        #
        #     {
        #         quoteCurrency: 'BTC',
        #         symbol: 'KCS-BTC',
        #         quoteMaxSize: '9999999',
        #         quoteIncrement: '0.000001',
        #         baseMinSize: '0.01',
        #         quoteMinSize: '0.00001',
        #         enableTrading: True,
        #         priceIncrement: '0.00000001',
        #         name: 'KCS-BTC',
        #         baseIncrement: '0.01',
        #         baseMaxSize: '9999999',
        #         baseCurrency: 'KCS'
        #     }
        #
        data = response['data']
        result = []
        for i in range(0, len(data)):
            market = data[i]
            id = self.safe_string(market, 'symbol')
            baseId, quoteId = id.split('-')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            active = self.safe_value(market, 'enableTrading')
            baseMaxSize = self.safe_number(market, 'baseMaxSize')
            baseMinSizeString = self.safe_string(market, 'baseMinSize')
            quoteMaxSizeString = self.safe_string(market, 'quoteMaxSize')
            baseMinSize = self.parse_number(baseMinSizeString)
            quoteMaxSize = self.parse_number(quoteMaxSizeString)
            quoteMinSize = self.safe_number(market, 'quoteMinSize')
            # quoteIncrement = self.safe_number(market, 'quoteIncrement')
            precision = {
                'amount': self.precision_from_string(self.safe_string(market, 'baseIncrement')),
                'price': self.precision_from_string(self.safe_string(market, 'priceIncrement')),
            }
            limits = {
                'amount': {
                    'min': baseMinSize,
                    'max': baseMaxSize,
                },
                'price': {
                    'min': self.safe_number(market, 'priceIncrement'),
                    'max': self.parse_number(Precise.string_div(quoteMaxSizeString, baseMinSizeString)),
                },
                'cost': {
                    'min': quoteMinSize,
                    'max': quoteMaxSize,
                },
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'baseId': baseId,
                'quoteId': quoteId,
                'base': base,
                'quote': quote,
                'active': active,
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def fetch_currencies(self, params={}):
        response = self.publicGetCurrencies(params)
        #
        #     {
        #         "currency": "OMG",
        #         "name": "OMG",
        #         "fullName": "OmiseGO",
        #         "precision": 8,
        #         "confirms": 12,
        #         "withdrawalMinSize": "4",
        #         "withdrawalMinFee": "1.25",
        #         "isWithdrawEnabled": False,
        #         "isDepositEnabled": False,
        #         "isMarginEnabled": False,
        #         "isDebitEnabled": False
        #     }
        #
        data = self.safe_value(response, 'data', [])
        result = {}
        for i in range(0, len(data)):
            entry = data[i]
            id = self.safe_string(entry, 'currency')
            name = self.safe_string(entry, 'fullName')
            code = self.safe_currency_code(id)
            precision = self.safe_integer(entry, 'precision')
            isWithdrawEnabled = self.safe_value(entry, 'isWithdrawEnabled', False)
            isDepositEnabled = self.safe_value(entry, 'isDepositEnabled', False)
            fee = self.safe_number(entry, 'withdrawalMinFee')
            active = (isWithdrawEnabled and isDepositEnabled)
            result[code] = {
                'id': id,
                'name': name,
                'code': code,
                'precision': precision,
                'info': entry,
                'active': active,
                'fee': fee,
                'limits': self.limits,
            }
        return result

    def fetch_accounts(self, params={}):
        response = self.privateGetAccounts(params)
        #
        #     {
        #         code: "200000",
        #         data: [
        #             {
        #                 balance: "0.00009788",
        #                 available: "0.00009788",
        #                 holds: "0",
        #                 currency: "BTC",
        #                 id: "5c6a4fd399a1d81c4f9cc4d0",
        #                 type: "trade"
        #             },
        #             {
        #                 balance: "0.00000001",
        #                 available: "0.00000001",
        #                 holds: "0",
        #                 currency: "ETH",
        #                 id: "5c6a49ec99a1d819392e8e9f",
        #                 type: "trade"
        #             }
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data')
        result = []
        for i in range(0, len(data)):
            account = data[i]
            accountId = self.safe_string(account, 'id')
            currencyId = self.safe_string(account, 'currency')
            code = self.safe_currency_code(currencyId)
            type = self.safe_string(account, 'type')  # main or trade
            result.append({
                'id': accountId,
                'type': type,
                'currency': code,
                'info': account,
            })
        return result

    def fetch_funding_fee(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
        }
        response = self.privateGetWithdrawalsQuotas(self.extend(request, params))
        data = response['data']
        withdrawFees = {}
        withdrawFees[code] = self.safe_number(data, 'withdrawMinFee')
        return {
            'info': response,
            'withdraw': withdrawFees,
            'deposit': {},
        }

    def parse_ticker(self, ticker, market=None):
        #
        #     {
        #         symbol: "ETH-BTC",
        #         high: "0.019518",
        #         vol: "7997.82836194",
        #         last: "0.019329",
        #         low: "0.019",
        #         buy: "0.019329",
        #         sell: "0.01933",
        #         changePrice: "-0.000139",
        #         time:  1580553706304,
        #         averagePrice: "0.01926386",
        #         changeRate: "-0.0071",
        #         volValue: "154.40791568183474"
        #     }
        #
        #     {
        #         "trading": True,
        #         "symbol": "KCS-BTC",
        #         "buy": 0.00011,
        #         "sell": 0.00012,
        #         "sort": 100,
        #         "volValue": 3.13851792584,   #total
        #         "baseCurrency": "KCS",
        #         "market": "BTC",
        #         "quoteCurrency": "BTC",
        #         "symbolCode": "KCS-BTC",
        #         "datetime": 1548388122031,
        #         "high": 0.00013,
        #         "vol": 27514.34842,
        #         "low": 0.0001,
        #         "changePrice": -1.0e-5,
        #         "changeRate": -0.0769,
        #         "lastTradedPrice": 0.00012,
        #         "board": 0,
        #         "mark": 0
        #     }
        #
        percentage = self.safe_number(ticker, 'changeRate')
        if percentage is not None:
            percentage = percentage * 100
        last = self.safe_number_2(ticker, 'last', 'lastTradedPrice')
        marketId = self.safe_string(ticker, 'symbol')
        symbol = self.safe_symbol(marketId, market, '-')
        baseVolume = self.safe_number(ticker, 'vol')
        quoteVolume = self.safe_number(ticker, 'volValue')
        vwap = self.vwap(baseVolume, quoteVolume)
        timestamp = self.safe_integer_2(ticker, 'time', 'datetime')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_number(ticker, 'high'),
            'low': self.safe_number(ticker, 'low'),
            'bid': self.safe_number(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_number(ticker, 'sell'),
            'askVolume': None,
            'vwap': vwap,
            'open': self.safe_number(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_number(ticker, 'changePrice'),
            'percentage': percentage,
            'average': self.safe_number(ticker, 'averagePrice'),
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.publicGetMarketAllTickers(params)
        #
        #     {
        #         "code": "200000",
        #         "data": {
        #             "date": 1550661940645,
        #             "ticker": [
        #                 'buy': '0.00001168',
        #                 'changePrice': '-0.00000018',
        #                 'changeRate': '-0.0151',
        #                 'datetime': 1550661146316,
        #                 'high': '0.0000123',
        #                 'last': '0.00001169',
        #                 'low': '0.00001159',
        #                 'sell': '0.00001182',
        #                 'symbol': 'LOOM-BTC',
        #                 'vol': '44399.5669'
        #             },
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data', {})
        tickers = self.safe_value(data, 'ticker', [])
        result = {}
        for i in range(0, len(tickers)):
            ticker = self.parse_ticker(tickers[i])
            symbol = self.safe_string(ticker, 'symbol')
            if symbol is not None:
                result[symbol] = ticker
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        response = self.publicGetMarketStats(self.extend(request, params))
        #
        #     {
        #         "code": "200000",
        #         "data": {
        #             'buy': '0.00001168',
        #             'changePrice': '-0.00000018',
        #             'changeRate': '-0.0151',
        #             'datetime': 1550661146316,
        #             'high': '0.0000123',
        #             'last': '0.00001169',
        #             'low': '0.00001159',
        #             'sell': '0.00001182',
        #             'symbol': 'LOOM-BTC',
        #             'vol': '44399.5669'
        #         },
        #     }
        #
        return self.parse_ticker(response['data'], market)

    def parse_ohlcv(self, ohlcv, market=None):
        #
        #     [
        #         "1545904980",             # Start time of the candle cycle
        #         "0.058",                  # opening price
        #         "0.049",                  # closing price
        #         "0.058",                  # highest price
        #         "0.049",                  # lowest price
        #         "0.018",                  # base volume
        #         "0.000945",               # quote volume
        #     ]
        #
        return [
            self.safe_timestamp(ohlcv, 0),
            self.safe_number(ohlcv, 1),
            self.safe_number(ohlcv, 3),
            self.safe_number(ohlcv, 4),
            self.safe_number(ohlcv, 2),
            self.safe_number(ohlcv, 5),
        ]

    def fetch_ohlcv(self, symbol, timeframe='15m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        marketId = market['id']
        request = {
            'symbol': marketId,
            'type': self.timeframes[timeframe],
        }
        duration = self.parse_timeframe(timeframe) * 1000
        endAt = self.milliseconds()  # required param
        if since is not None:
            request['startAt'] = int(int(math.floor(since / 1000)))
            if limit is None:
                # https://docs.kucoin.com/#get-klines
                # https://docs.kucoin.com/#details
                # For each query, the system would return at most 1500 pieces of data.
                # To obtain more data, please page the data by time.
                limit = self.safe_integer(self.options, 'fetchOHLCVLimit', 1500)
            endAt = self.sum(since, limit * duration)
        elif limit is not None:
            since = endAt - limit * duration
            request['startAt'] = int(int(math.floor(since / 1000)))
        request['endAt'] = int(int(math.floor(endAt / 1000)))
        response = self.publicGetMarketCandles(self.extend(request, params))
        #
        #     {
        #         "code":"200000",
        #         "data":[
        #             ["1591517700","0.025078","0.025069","0.025084","0.025064","18.9883256","0.4761861079404"],
        #             ["1591516800","0.025089","0.025079","0.025089","0.02506","99.4716622","2.494143499081"],
        #             ["1591515900","0.025079","0.02509","0.025091","0.025068","59.83701271","1.50060885172798"],
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    def create_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id']}
        response = self.privatePostDepositAddresses(self.extend(request, params))
        # BCH {"code":"200000","data":{"address":"bitcoincash:qza3m4nj9rx7l9r0cdadfqxts6f92shvhvr5ls4q7z","memo":""}}
        # BTC {"code":"200000","data":{"address":"36SjucKqQpQSvsak9A7h6qzFjrVXpRNZhE","memo":""}}
        data = self.safe_value(response, 'data', {})
        address = self.safe_string(data, 'address')
        # BCH/BSV is returned with a "bitcoincash:" prefix, which we cut off here and only keep the address
        if address is not None:
            address = address.replace('bitcoincash:', '')
        tag = self.safe_string(data, 'memo')
        if code != 'NIM':
            # contains spaces
            self.check_address(address)
        return {
            'info': response,
            'currency': code,
            'address': address,
            'tag': tag,
        }

    def fetch_deposit_address(self, code, params={}):
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
            # for USDT - OMNI, ERC20, TRC20, default is ERC20
            # for BTC - Native, Segwit, TRC20, the parameters are bech32, btc, trx, default is Native
            # 'chain': 'ERC20',  # optional
        }
        response = self.privateGetDepositAddresses(self.extend(request, params))
        # BCH {"code":"200000","data":{"address":"bitcoincash:qza3m4nj9rx7l9r0cdadfqxts6f92shvhvr5ls4q7z","memo":""}}
        # BTC {"code":"200000","data":{"address":"36SjucKqQpQSvsak9A7h6qzFjrVXpRNZhE","memo":""}}
        data = self.safe_value(response, 'data', {})
        address = self.safe_string(data, 'address')
        tag = self.safe_string(data, 'memo')
        if code != 'NIM':
            # contains spaces
            self.check_address(address)
        return {
            'info': response,
            'currency': code,
            'address': address,
            'tag': tag,
        }

    def fetch_l3_order_book(self, symbol, limit=None, params={}):
        return self.fetch_order_book(symbol, limit, {'level': 3})

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        marketId = self.market_id(symbol)
        level = self.safe_integer(params, 'level', 2)
        request = {'symbol': marketId, 'level': level}
        method = 'privateGetMarketOrderbookLevelLevel'
        if level == 2:
            if limit is not None:
                if (limit == 20) or (limit == 100):
                    request['limit'] = limit
                    method = 'publicGetMarketOrderbookLevelLevelLimit'
                else:
                    raise ExchangeError(self.id + ' fetchOrderBook limit argument must be None, 20 or 100')
        response = getattr(self, method)(self.extend(request, params))
        #
        # 'market/orderbook/level2'
        # 'market/orderbook/level2_20'
        # 'market/orderbook/level2_100'
        #
        #     {
        #         "code":"200000",
        #         "data":{
        #             "sequence":"1583235112106",
        #             "asks":[
        #                 # ...
        #                 ["0.023197","12.5067468"],
        #                 ["0.023194","1.8"],
        #                 ["0.023191","8.1069672"]
        #             ],
        #             "bids":[
        #                 ["0.02319","1.6000002"],
        #                 ["0.023189","2.2842325"],
        #             ],
        #             "time":1586584067274
        #         }
        #     }
        #
        # 'market/orderbook/level3'
        #
        #     {
        #         "code":"200000",
        #         "data":{
        #             "sequence":"1583731857120",
        #             "asks":[
        #                 # id, price, size, timestamp in nanoseconds
        #                 ["5e915f8acd26670009675300","6925.7","0.2","1586585482194286069"],
        #                 ["5e915f8ace35a200090bba48","6925.7","0.001","1586585482229569826"],
        #                 ["5e915f8a8857740009ca7d33","6926","0.00001819","1586585482149148621"],
        #             ],
        #             "bids":[
        #                 ["5e915f8acca406000ac88194","6925.6","0.05","1586585482384384842"],
        #                 ["5e915f93cd26670009676075","6925.6","0.08","1586585491334914600"],
        #                 ["5e915f906aa6e200099b49f6","6925.4","0.2","1586585488941126340"],
        #             ],
        #             "time":1586585492487
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        timestamp = self.safe_integer(data, 'time')
        orderbook = self.parse_order_book(data, symbol, timestamp, 'bids', 'asks', level - 2, level - 1)
        orderbook['nonce'] = self.safe_integer(data, 'sequence')
        return orderbook

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        marketId = self.market_id(symbol)
        # required param, cannot be used twice
        clientOrderId = self.safe_string_2(params, 'clientOid', 'clientOrderId', self.uuid())
        params = self.omit(params, ['clientOid', 'clientOrderId'])
        request = {
            'clientOid': clientOrderId,
            'side': side,
            'symbol': marketId,
            'type': type,  # limit or market
            # 'remark': '',  # optional remark for the order, length cannot exceed 100 utf8 characters
            # 'stp': '',  # self trade prevention, CN, CO, CB or DC
            # To improve the system performance and to accelerate order placing and processing, KuCoin has added a new interface for margin orders
            # The current one will no longer accept margin orders by May 1st, 2021(UTC)
            # At the time, KuCoin will notify users via the announcement, please pay attention to it
            # 'tradeType': 'TRADE',  # TRADE, MARGIN_TRADE  # not used with margin orders
            # limit orders ---------------------------------------------------
            # 'timeInForce': 'GTC',  # GTC, GTT, IOC, or FOK(default is GTC), limit orders only
            # 'cancelAfter': long,  # cancel after n seconds, requires timeInForce to be GTT
            # 'postOnly': False,  # Post only flag, invalid when timeInForce is IOC or FOK
            # 'hidden': False,  # Order will not be displayed in the order book
            # 'iceberg': False,  # Only a portion of the order is displayed in the order book
            # 'visibleSize': self.amount_to_precision(symbol, visibleSize),  # The maximum visible size of an iceberg order
            # market orders --------------------------------------------------
            # 'size': self.amount_to_precision(symbol, amount),  # Amount in base currency
            # 'funds': self.cost_to_precision(symbol, cost),  # Amount of quote currency to use
            # stop orders ----------------------------------------------------
            # 'stop': 'loss',  # loss or entry, the default is loss, requires stopPrice
            # 'stopPrice': self.price_to_precision(symbol, amount),  # need to be defined if stop is specified
            # margin orders --------------------------------------------------
            # 'marginMode': 'cross',  # cross(cross mode) and isolated(isolated mode), set to cross by default, the isolated mode will be released soon, stay tuned
            # 'autoBorrow': False,  # The system will first borrow you funds at the optimal interest rate and then place an order for you
        }
        quoteAmount = self.safe_number_2(params, 'cost', 'funds')
        amountString = None
        costString = None
        if type == 'market':
            if quoteAmount is not None:
                params = self.omit(params, ['cost', 'funds'])
                # kucoin uses base precision even for quote values
                costString = self.amount_to_precision(symbol, quoteAmount)
                request['funds'] = costString
            else:
                amountString = self.amount_to_precision(symbol, amount)
                request['size'] = self.amount_to_precision(symbol, amount)
        else:
            amountString = self.amount_to_precision(symbol, amount)
            request['size'] = amountString
            request['price'] = self.price_to_precision(symbol, price)
        response = self.privatePostOrders(self.extend(request, params))
        #
        #     {
        #         code: '200000',
        #         data: {
        #             "orderId": "5bd6e9286d99522a52e458de"
        #         }
        #    }
        #
        data = self.safe_value(response, 'data', {})
        timestamp = self.milliseconds()
        id = self.safe_string(data, 'orderId')
        order = {
            'id': id,
            'clientOrderId': clientOrderId,
            'info': data,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': self.parse_number(amountString),
            'cost': self.parse_number(costString),
            'average': None,
            'filled': None,
            'remaining': None,
            'status': None,
            'fee': None,
            'trades': None,
        }
        return order

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {}
        clientOrderId = self.safe_string_2(params, 'clientOid', 'clientOrderId')
        method = 'privateDeleteOrdersOrderId'
        if clientOrderId is not None:
            request['clientOid'] = clientOrderId
            method = 'privateDeleteOrdersClientOrderClientOid'
        else:
            request['orderId'] = id
        params = self.omit(params, ['clientOid', 'clientOrderId'])
        return getattr(self, method)(self.extend(request, params))

    def cancel_all_orders(self, symbol=None, params={}):
        self.load_markets()
        request = {
            # 'symbol': market['id'],
            # 'tradeType': 'TRADE',  # default is to cancel the spot trading order
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        return self.privateDeleteOrders(self.extend(request, params))

    def fetch_orders_by_status(self, status, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {
            'status': status,
        }
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if since is not None:
            request['startAt'] = since
        if limit is not None:
            request['pageSize'] = limit
        response = self.privateGetOrders(self.extend(request, params))
        #
        #     {
        #         code: '200000',
        #         data: {
        #             "currentPage": 1,
        #             "pageSize": 1,
        #             "totalNum": 153408,
        #             "totalPage": 153408,
        #             "items": [
        #                 {
        #                     "id": "5c35c02703aa673ceec2a168",   #orderid
        #                     "symbol": "BTC-USDT",   #symbol
        #                     "opType": "DEAL",      # operation type,deal is pending order,cancel is cancel order
        #                     "type": "limit",       # order type,e.g. limit,markrt,stop_limit.
        #                     "side": "buy",         # transaction direction,include buy and sell
        #                     "price": "10",         # order price
        #                     "size": "2",           # order quantity
        #                     "funds": "0",          # order funds
        #                     "dealFunds": "0.166",  # deal funds
        #                     "dealSize": "2",       # deal quantity
        #                     "fee": "0",            # fee
        #                     "feeCurrency": "USDT",  # charge fee currency
        #                     "stp": "",             # self trade prevention,include CN,CO,DC,CB
        #                     "stop": "",            # stop type
        #                     "stopTriggered": False,  # stop order is triggered
        #                     "stopPrice": "0",      # stop price
        #                     "timeInForce": "GTC",  # time InForce,include GTC,GTT,IOC,FOK
        #                     "postOnly": False,     # postOnly
        #                     "hidden": False,       # hidden order
        #                     "iceberg": False,      # iceberg order
        #                     "visibleSize": "0",    # display quantity for iceberg order
        #                     "cancelAfter": 0,      # cancel orders time，requires timeInForce to be GTT
        #                     "channel": "IOS",      # order source
        #                     "clientOid": "",       # user-entered order unique mark
        #                     "remark": "",          # remark
        #                     "tags": "",            # tag order source
        #                     "isActive": False,     # status before unfilled or uncancelled
        #                     "cancelExist": False,   # order cancellation transaction record
        #                     "createdAt": 1547026471000  # time
        #                 },
        #             ]
        #         }
        #    }
        responseData = self.safe_value(response, 'data', {})
        orders = self.safe_value(responseData, 'items', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status('done', symbol, since, limit, params)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return self.fetch_orders_by_status('active', symbol, since, limit, params)

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {}
        clientOrderId = self.safe_string_2(params, 'clientOid', 'clientOrderId')
        method = 'privateGetOrdersOrderId'
        if clientOrderId is not None:
            request['clientOid'] = clientOrderId
            method = 'privateGetOrdersClientOrderClientOid'
        else:
            # a special case for None ids
            # otherwise a wrong endpoint for all orders will be triggered
            # https://github.com/ccxt/ccxt/issues/7234
            if id is None:
                raise InvalidOrder(self.id + ' fetchOrder() requires an order id')
            request['orderId'] = id
        params = self.omit(params, ['clientOid', 'clientOrderId'])
        response = getattr(self, method)(self.extend(request, params))
        market = None
        if symbol is not None:
            market = self.market(symbol)
        responseData = self.safe_value(response, 'data')
        return self.parse_order(responseData, market)

    def parse_order(self, order, market=None):
        #
        # fetchOpenOrders, fetchClosedOrders
        #
        #     {
        #         "id": "5c35c02703aa673ceec2a168",   #orderid
        #         "symbol": "BTC-USDT",   #symbol
        #         "opType": "DEAL",      # operation type,deal is pending order,cancel is cancel order
        #         "type": "limit",       # order type,e.g. limit,markrt,stop_limit.
        #         "side": "buy",         # transaction direction,include buy and sell
        #         "price": "10",         # order price
        #         "size": "2",           # order quantity
        #         "funds": "0",          # order funds
        #         "dealFunds": "0.166",  # deal funds
        #         "dealSize": "2",       # deal quantity
        #         "fee": "0",            # fee
        #         "feeCurrency": "USDT",  # charge fee currency
        #         "stp": "",             # self trade prevention,include CN,CO,DC,CB
        #         "stop": "",            # stop type
        #         "stopTriggered": False,  # stop order is triggered
        #         "stopPrice": "0",      # stop price
        #         "timeInForce": "GTC",  # time InForce,include GTC,GTT,IOC,FOK
        #         "postOnly": False,     # postOnly
        #         "hidden": False,       # hidden order
        #         "iceberg": False,      # iceberg order
        #         "visibleSize": "0",    # display quantity for iceberg order
        #         "cancelAfter": 0,      # cancel orders time，requires timeInForce to be GTT
        #         "channel": "IOS",      # order source
        #         "clientOid": "",       # user-entered order unique mark
        #         "remark": "",          # remark
        #         "tags": "",            # tag order source
        #         "isActive": False,     # status before unfilled or uncancelled
        #         "cancelExist": False,   # order cancellation transaction record
        #         "createdAt": 1547026471000  # time
        #     }
        #
        marketId = self.safe_string(order, 'symbol')
        symbol = self.safe_symbol(marketId, market, '-')
        orderId = self.safe_string(order, 'id')
        type = self.safe_string(order, 'type')
        timestamp = self.safe_integer(order, 'createdAt')
        datetime = self.iso8601(timestamp)
        price = self.safe_number(order, 'price')
        if price == 0.0:
            # market orders
            price = None
        side = self.safe_string(order, 'side')
        feeCurrencyId = self.safe_string(order, 'feeCurrency')
        feeCurrency = self.safe_currency_code(feeCurrencyId)
        feeCost = self.safe_number(order, 'fee')
        amount = self.safe_number(order, 'size')
        filled = self.safe_number(order, 'dealSize')
        cost = self.safe_number(order, 'dealFunds')
        # bool
        isActive = self.safe_value(order, 'isActive', False)
        cancelExist = self.safe_value(order, 'cancelExist', False)
        status = 'open' if isActive else 'closed'
        status = 'canceled' if cancelExist else status
        fee = {
            'currency': feeCurrency,
            'cost': feeCost,
        }
        clientOrderId = self.safe_string(order, 'clientOid')
        timeInForce = self.safe_string(order, 'timeInForce')
        stopPrice = self.safe_number(order, 'stopPrice')
        postOnly = self.safe_value(order, 'postOnly')
        return self.safe_order({
            'id': orderId,
            'clientOrderId': clientOrderId,
            'symbol': symbol,
            'type': type,
            'timeInForce': timeInForce,
            'postOnly': postOnly,
            'side': side,
            'amount': amount,
            'price': price,
            'stopPrice': stopPrice,
            'cost': cost,
            'filled': filled,
            'remaining': None,
            'timestamp': timestamp,
            'datetime': datetime,
            'fee': fee,
            'status': status,
            'info': order,
            'lastTradeTimestamp': None,
            'average': None,
            'trades': None,
        })

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if limit is not None:
            request['pageSize'] = limit
        method = self.options['fetchMyTradesMethod']
        parseResponseData = False
        if method == 'private_get_fills':
            # does not return trades earlier than 2019-02-18T00:00:00Z
            if since is not None:
                # only returns trades up to one week after the since param
                request['startAt'] = since
        elif method == 'private_get_limit_fills':
            # does not return trades earlier than 2019-02-18T00:00:00Z
            # takes no params
            # only returns first 1000 trades(not only "in the last 24 hours" as stated in the docs)
            parseResponseData = True
        elif method == 'private_get_hist_orders':
            # despite that self endpoint is called `HistOrders`
            # it returns historical trades instead of orders
            # returns trades earlier than 2019-02-18T00:00:00Z only
            if since is not None:
                request['startAt'] = int(since / 1000)
        else:
            raise ExchangeError(self.id + ' invalid fetchClosedOrder method')
        response = getattr(self, method)(self.extend(request, params))
        #
        #     {
        #         "currentPage": 1,
        #         "pageSize": 50,
        #         "totalNum": 1,
        #         "totalPage": 1,
        #         "items": [
        #             {
        #                 "symbol":"BTC-USDT",       # symbol
        #                 "tradeId":"5c35c02709e4f67d5266954e",        # trade id
        #                 "orderId":"5c35c02703aa673ceec2a168",        # order id
        #                 "counterOrderId":"5c1ab46003aa676e487fa8e3",  # counter order id
        #                 "side":"buy",              # transaction direction,include buy and sell
        #                 "liquidity":"taker",       # include taker and maker
        #                 "forceTaker":true,         # forced to become taker
        #                 "price":"0.083",           # order price
        #                 "size":"0.8424304",        # order quantity
        #                 "funds":"0.0699217232",    # order funds
        #                 "fee":"0",                 # fee
        #                 "feeRate":"0",             # fee rate
        #                 "feeCurrency":"USDT",      # charge fee currency
        #                 "stop":"",                 # stop type
        #                 "type":"limit",            # order type, e.g. limit, market, stop_limit.
        #                 "createdAt":1547026472000  # time
        #             },
        #             #------------------------------------------------------
        #             # v1(historical) trade response structure
        #             {
        #                 "symbol": "SNOV-ETH",
        #                 "dealPrice": "0.0000246",
        #                 "dealValue": "0.018942",
        #                 "amount": "770",
        #                 "fee": "0.00001137",
        #                 "side": "sell",
        #                 "createdAt": 1540080199
        #                 "id":"5c4d389e4c8c60413f78e2e5",
        #             }
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data', {})
        trades = None
        if parseResponseData:
            trades = data
        else:
            trades = self.safe_value(data, 'items', [])
        return self.parse_trades(trades, market, since, limit)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        if since is not None:
            request['startAt'] = int(math.floor(since / 1000))
        if limit is not None:
            request['pageSize'] = limit
        response = self.publicGetMarketHistories(self.extend(request, params))
        #
        #     {
        #         "code": "200000",
        #         "data": [
        #             {
        #                 "sequence": "1548764654235",
        #                 "side": "sell",
        #                 "size":"0.6841354",
        #                 "price":"0.03202",
        #                 "time":1548848575203567174
        #             }
        #         ]
        #     }
        #
        trades = self.safe_value(response, 'data', [])
        return self.parse_trades(trades, market, since, limit)

    def parse_trade(self, trade, market=None):
        #
        # fetchTrades(public)
        #
        #     {
        #         "sequence": "1548764654235",
        #         "side": "sell",
        #         "size":"0.6841354",
        #         "price":"0.03202",
        #         "time":1548848575203567174
        #     }
        #
        #     {
        #         sequence: '1568787654360',
        #         symbol: 'BTC-USDT',
        #         side: 'buy',
        #         size: '0.00536577',
        #         price: '9345',
        #         takerOrderId: '5e356c4a9f1a790008f8d921',
        #         time: '1580559434436443257',
        #         type: 'match',
        #         makerOrderId: '5e356bffedf0010008fa5d7f',
        #         tradeId: '5e356c4aeefabd62c62a1ece'
        #     }
        #
        # fetchMyTrades(private) v2
        #
        #     {
        #         "symbol":"BTC-USDT",
        #         "tradeId":"5c35c02709e4f67d5266954e",
        #         "orderId":"5c35c02703aa673ceec2a168",
        #         "counterOrderId":"5c1ab46003aa676e487fa8e3",
        #         "side":"buy",
        #         "liquidity":"taker",
        #         "forceTaker":true,
        #         "price":"0.083",
        #         "size":"0.8424304",
        #         "funds":"0.0699217232",
        #         "fee":"0",
        #         "feeRate":"0",
        #         "feeCurrency":"USDT",
        #         "stop":"",
        #         "type":"limit",
        #         "createdAt":1547026472000
        #     }
        #
        # fetchMyTrades v2 alternative format since 2019-05-21 https://github.com/ccxt/ccxt/pull/5162
        #
        #     {
        #         symbol: "OPEN-BTC",
        #         forceTaker:  False,
        #         orderId: "5ce36420054b4663b1fff2c9",
        #         fee: "0",
        #         feeCurrency: "",
        #         type: "",
        #         feeRate: "0",
        #         createdAt: 1558417615000,
        #         size: "12.8206",
        #         stop: "",
        #         price: "0",
        #         funds: "0",
        #         tradeId: "5ce390cf6e0db23b861c6e80"
        #     }
        #
        # fetchMyTrades(private) v1(historical)
        #
        #     {
        #         "symbol": "SNOV-ETH",
        #         "dealPrice": "0.0000246",
        #         "dealValue": "0.018942",
        #         "amount": "770",
        #         "fee": "0.00001137",
        #         "side": "sell",
        #         "createdAt": 1540080199
        #         "id":"5c4d389e4c8c60413f78e2e5",
        #     }
        #
        marketId = self.safe_string(trade, 'symbol')
        symbol = self.safe_symbol(marketId, market, '-')
        id = self.safe_string_2(trade, 'tradeId', 'id')
        orderId = self.safe_string(trade, 'orderId')
        takerOrMaker = self.safe_string(trade, 'liquidity')
        timestamp = self.safe_integer(trade, 'time')
        if timestamp is not None:
            timestamp = int(timestamp / 1000000)
        else:
            timestamp = self.safe_integer(trade, 'createdAt')
            # if it's a historical v1 trade, the exchange returns timestamp in seconds
            if ('dealValue' in trade) and (timestamp is not None):
                timestamp = timestamp * 1000
        priceString = self.safe_string_2(trade, 'price', 'dealPrice')
        amountString = self.safe_string_2(trade, 'size', 'amount')
        price = self.parse_number(priceString)
        amount = self.parse_number(amountString)
        side = self.safe_string(trade, 'side')
        fee = None
        feeCost = self.safe_number(trade, 'fee')
        if feeCost is not None:
            feeCurrencyId = self.safe_string(trade, 'feeCurrency')
            feeCurrency = self.safe_currency_code(feeCurrencyId)
            if feeCurrency is None:
                if market is not None:
                    feeCurrency = market['quote'] if (side == 'sell') else market['base']
            fee = {
                'cost': feeCost,
                'currency': feeCurrency,
                'rate': self.safe_number(trade, 'feeRate'),
            }
        type = self.safe_string(trade, 'type')
        if type == 'match':
            type = None
        cost = self.safe_number_2(trade, 'funds', 'dealValue')
        if cost is None:
            cost = self.parse_number(Precise.string_mul(priceString, amountString))
        return {
            'info': trade,
            'id': id,
            'order': orderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'takerOrMaker': takerOrMaker,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': fee,
        }

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.load_markets()
        self.check_address(address)
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
            'address': address,
            'amount': amount,
            # 'memo': tag,
            # 'isInner': False,  # internal transfer or external withdrawal
            # 'remark': 'optional',
            # 'chain': 'OMNI',  # 'ERC20', 'TRC20', default is ERC20
        }
        if tag is not None:
            request['memo'] = tag
        response = self.privatePostWithdrawals(self.extend(request, params))
        #
        # https://github.com/ccxt/ccxt/issues/5558
        #
        #     {
        #         "code":  200000,
        #         "data": {
        #             "withdrawalId":  "abcdefghijklmnopqrstuvwxyz"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        return {
            'id': self.safe_string(data, 'withdrawalId'),
            'info': response,
        }

    def parse_transaction_status(self, status):
        statuses = {
            'SUCCESS': 'ok',
            'PROCESSING': 'ok',
            'FAILURE': 'failed',
        }
        return self.safe_string(statuses, status)

    def parse_transaction(self, transaction, currency=None):
        #
        # fetchDeposits
        #
        #     {
        #         "address": "0x5f047b29041bcfdbf0e4478cdfa753a336ba6989",
        #         "memo": "5c247c8a03aa677cea2a251d",
        #         "amount": 1,
        #         "fee": 0.0001,
        #         "currency": "KCS",
        #         "isInner": False,
        #         "walletTxId": "5bbb57386d99522d9f954c5a@test004",
        #         "status": "SUCCESS",
        #         "createdAt": 1544178843000,
        #         "updatedAt": 1544178891000
        #         "remark":"foobar"
        #     }
        #
        # fetchWithdrawals
        #
        #     {
        #         "id": "5c2dc64e03aa675aa263f1ac",
        #         "address": "0x5bedb060b8eb8d823e2414d82acce78d38be7fe9",
        #         "memo": "",
        #         "currency": "ETH",
        #         "amount": 1.0000000,
        #         "fee": 0.0100000,
        #         "walletTxId": "3e2414d82acce78d38be7fe9",
        #         "isInner": False,
        #         "status": "FAILURE",
        #         "createdAt": 1546503758000,
        #         "updatedAt": 1546504603000
        #         "remark":"foobar"
        #     }
        #
        currencyId = self.safe_string(transaction, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        address = self.safe_string(transaction, 'address')
        amount = self.safe_number(transaction, 'amount')
        txid = self.safe_string(transaction, 'walletTxId')
        if txid is not None:
            txidParts = txid.split('@')
            numTxidParts = len(txidParts)
            if numTxidParts > 1:
                if address is None:
                    if len(txidParts[1]) > 1:
                        address = txidParts[1]
            txid = txidParts[0]
        type = 'withdrawal' if (txid is None) else 'deposit'
        rawStatus = self.safe_string(transaction, 'status')
        status = self.parse_transaction_status(rawStatus)
        fee = None
        feeCost = self.safe_number(transaction, 'fee')
        if feeCost is not None:
            rate = None
            if amount is not None:
                rate = feeCost / amount
            fee = {
                'cost': feeCost,
                'rate': rate,
                'currency': code,
            }
        tag = self.safe_string(transaction, 'memo')
        timestamp = self.safe_integer_2(transaction, 'createdAt', 'createAt')
        id = self.safe_string(transaction, 'id')
        updated = self.safe_integer(transaction, 'updatedAt')
        isV1 = not ('createdAt' in transaction)
        # if it's a v1 structure
        if isV1:
            type = 'withdrawal' if ('address' in transaction) else 'deposit'
            if timestamp is not None:
                timestamp = timestamp * 1000
            if updated is not None:
                updated = updated * 1000
        comment = self.safe_string(transaction, 'remark')
        return {
            'id': id,
            'info': transaction,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'address': address,
            'addressTo': address,
            'addressFrom': None,
            'tag': tag,
            'tagTo': tag,
            'tagFrom': None,
            'currency': code,
            'amount': amount,
            'txid': txid,
            'type': type,
            'status': status,
            'comment': comment,
            'fee': fee,
            'updated': updated,
        }

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        if limit is not None:
            request['pageSize'] = limit
        method = 'privateGetDeposits'
        if since is not None:
            # if since is earlier than 2019-02-18T00:00:00Z
            if since < 1550448000000:
                request['startAt'] = int(since / 1000)
                method = 'privateGetHistDeposits'
            else:
                request['startAt'] = since
        response = getattr(self, method)(self.extend(request, params))
        #
        #     {
        #         code: '200000',
        #         data: {
        #             "currentPage": 1,
        #             "pageSize": 5,
        #             "totalNum": 2,
        #             "totalPage": 1,
        #             "items": [
        #                 #--------------------------------------------------
        #                 # version 2 deposit response structure
        #                 {
        #                     "address": "0x5f047b29041bcfdbf0e4478cdfa753a336ba6989",
        #                     "memo": "5c247c8a03aa677cea2a251d",
        #                     "amount": 1,
        #                     "fee": 0.0001,
        #                     "currency": "KCS",
        #                     "isInner": False,
        #                     "walletTxId": "5bbb57386d99522d9f954c5a@test004",
        #                     "status": "SUCCESS",
        #                     "createdAt": 1544178843000,
        #                     "updatedAt": 1544178891000
        #                     "remark":"foobar"
        #                 },
        #                 #--------------------------------------------------
        #                 # version 1(historical) deposit response structure
        #                 {
        #                     "currency": "BTC",
        #                     "createAt": 1528536998,
        #                     "amount": "0.03266638",
        #                     "walletTxId": "55c643bc2c68d6f17266383ac1be9e454038864b929ae7cee0bc408cc5c869e8@12ffGWmMMD1zA1WbFm7Ho3JZ1w6NYXjpFk@234",
        #                     "isInner": False,
        #                     "status": "SUCCESS",
        #                 }
        #             ]
        #         }
        #     }
        #
        responseData = response['data']['items']
        return self.parse_transactions(responseData, currency, since, limit, {'type': 'deposit'})

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        self.load_markets()
        request = {}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        if limit is not None:
            request['pageSize'] = limit
        method = 'privateGetWithdrawals'
        if since is not None:
            # if since is earlier than 2019-02-18T00:00:00Z
            if since < 1550448000000:
                request['startAt'] = int(since / 1000)
                method = 'privateGetHistWithdrawals'
            else:
                request['startAt'] = since
        response = getattr(self, method)(self.extend(request, params))
        #
        #     {
        #         code: '200000',
        #         data: {
        #             "currentPage": 1,
        #             "pageSize": 5,
        #             "totalNum": 2,
        #             "totalPage": 1,
        #             "items": [
        #                 #--------------------------------------------------
        #                 # version 2 withdrawal response structure
        #                 {
        #                     "id": "5c2dc64e03aa675aa263f1ac",
        #                     "address": "0x5bedb060b8eb8d823e2414d82acce78d38be7fe9",
        #                     "memo": "",
        #                     "currency": "ETH",
        #                     "amount": 1.0000000,
        #                     "fee": 0.0100000,
        #                     "walletTxId": "3e2414d82acce78d38be7fe9",
        #                     "isInner": False,
        #                     "status": "FAILURE",
        #                     "createdAt": 1546503758000,
        #                     "updatedAt": 1546504603000
        #                 },
        #                 #--------------------------------------------------
        #                 # version 1(historical) withdrawal response structure
        #                 {
        #                     "currency": "BTC",
        #                     "createAt": 1526723468,
        #                     "amount": "0.534",
        #                     "address": "33xW37ZSW4tQvg443Pc7NLCAs167Yc2XUV",
        #                     "walletTxId": "aeacea864c020acf58e51606169240e96774838dcd4f7ce48acf38e3651323f4",
        #                     "isInner": False,
        #                     "status": "SUCCESS"
        #                 }
        #             ]
        #         }
        #     }
        #
        responseData = response['data']['items']
        return self.parse_transactions(responseData, currency, since, limit, {'type': 'withdrawal'})

    def fetch_balance(self, params={}):
        self.load_markets()
        defaultType = self.safe_string_2(self.options, 'fetchBalance', 'defaultType', 'trade')
        requestedType = self.safe_string(params, 'type', defaultType)
        accountsByType = self.safe_value(self.options, 'accountsByType')
        type = self.safe_string(accountsByType, requestedType)
        if type is None:
            keys = list(accountsByType.keys())
            raise ExchangeError(self.id + ' type must be one of ' + ', '.join(keys))
        params = self.omit(params, 'type')
        if (type == 'contract') or (type == 'futures'):
            # futures api requires a futures apiKey
            # only fetches one balance at a time
            # by default it will only fetch the BTC balance of the futures account
            # you can send 'currency' in params to fetch other currencies
            # fetchBalance({'type': 'futures', 'currency': 'USDT'})
            response = self.futuresPrivateGetAccountOverview(params)
            #
            #     {
            #         code: '200000',
            #         data: {
            #             accountEquity: 0.00005,
            #             unrealisedPNL: 0,
            #             marginBalance: 0.00005,
            #             positionMargin: 0,
            #             orderMargin: 0,
            #             frozenFunds: 0,
            #             availableBalance: 0.00005,
            #             currency: 'XBT'
            #         }
            #     }
            #
            result = {
                'info': response,
                'timestamp': None,
                'datetime': None,
            }
            data = self.safe_value(response, 'data')
            currencyId = self.safe_string(data, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(data, 'availableBalance')
            account['total'] = self.safe_string(data, 'accountEquity')
            result[code] = account
            return self.parse_balance(result)
        else:
            request = {
                'type': type,
            }
            response = self.privateGetAccounts(self.extend(request, params))
            #
            #     {
            #         "code":"200000",
            #         "data":[
            #             {"balance":"0.00009788","available":"0.00009788","holds":"0","currency":"BTC","id":"5c6a4fd399a1d81c4f9cc4d0","type":"trade"},
            #             {"balance":"3.41060034","available":"3.41060034","holds":"0","currency":"SOUL","id":"5c6a4d5d99a1d8182d37046d","type":"trade"},
            #             {"balance":"0.01562641","available":"0.01562641","holds":"0","currency":"NEO","id":"5c6a4f1199a1d8165a99edb1","type":"trade"},
            #         ]
            #     }
            #
            data = self.safe_value(response, 'data', [])
            result = {
                'info': response,
                'timestamp': None,
                'datetime': None,
            }
            for i in range(0, len(data)):
                balance = data[i]
                balanceType = self.safe_string(balance, 'type')
                if balanceType == type:
                    currencyId = self.safe_string(balance, 'currency')
                    code = self.safe_currency_code(currencyId)
                    account = self.account()
                    account['total'] = self.safe_string(balance, 'balance')
                    account['free'] = self.safe_string(balance, 'available')
                    account['used'] = self.safe_string(balance, 'holds')
                    result[code] = account
            return self.parse_balance(result)

    def transfer(self, code, amount, fromAccount, toAccount, params={}):
        self.load_markets()
        currency = self.currency(code)
        requestedAmount = self.currency_to_precision(code, amount)
        accountsById = self.safe_value(self.options, 'accountsByType', {})
        fromId = self.safe_string(accountsById, fromAccount)
        if fromId is None:
            keys = list(accountsById.keys())
            raise ExchangeError(self.id + ' fromAccount must be one of ' + ', '.join(keys))
        toId = self.safe_string(accountsById, toAccount)
        if toId is None:
            keys = list(accountsById.keys())
            raise ExchangeError(self.id + ' toAccount must be one of ' + ', '.join(keys))
        if fromId == 'contract':
            if toId != 'main':
                raise ExchangeError(self.id + ' only supports transferring from futures account to main account')
            request = {
                'currency': currency['id'],
                'amount': requestedAmount,
            }
            if not ('bizNo' in params):
                # it doesn't like more than 24 characters
                request['bizNo'] = self.uuid22()
            response = self.futuresPrivatePostTransferOut(self.extend(request, params))
            #
            #     {
            #         code: '200000',
            #         data: {
            #             applyId: '605a87217dff1500063d485d',
            #             bizNo: 'bcd6e5e1291f4905af84dc',
            #             payAccountType: 'CONTRACT',
            #             payTag: 'DEFAULT',
            #             remark: '',
            #             recAccountType: 'MAIN',
            #             recTag: 'DEFAULT',
            #             recRemark: '',
            #             recSystem: 'KUCOIN',
            #             status: 'PROCESSING',
            #             currency: 'XBT',
            #             amount: '0.00001',
            #             fee: '0',
            #             sn: '573688685663948',
            #             reason: '',
            #             createdAt: 1616545569000,
            #             updatedAt: 1616545569000
            #         }
            #     }
            #
            data = self.safe_value(response, 'data')
            timestamp = self.safe_integer(data, 'createdAt')
            id = self.safe_string(data, 'applyId')
            currencyId = self.safe_string(data, 'currency')
            code = self.safe_currency_code(currencyId)
            amount = self.safe_number(data, 'amount')
            rawStatus = self.safe_string(data, 'status')
            status = None
            if rawStatus == 'PROCESSING':
                status = 'pending'
            return {
                'info': response,
                'currency': code,
                'timestamp': timestamp,
                'datetime': self.iso8601(timestamp),
                'amount': amount,
                'fromAccount': fromId,
                'toAccount': toId,
                'id': id,
                'status': status,
            }
        else:
            request = {
                'currency': currency['id'],
                'from': fromId,
                'to': toId,
                'amount': requestedAmount,
            }
            if not ('clientOid' in params):
                request['clientOid'] = self.uuid()
            response = self.privatePostAccountsInnerTransfer(self.extend(request, params))
            # {code: '200000', data: {orderId: '605a6211e657f00006ad0ad6'}}
            data = self.safe_value(response, 'data')
            id = self.safe_string(data, 'orderId')
            return {
                'info': response,
                'id': id,
                'timestamp': None,
                'datetime': None,
                'currency': code,
                'amount': requestedAmount,
                'fromAccount': fromId,
                'toAccount': toId,
                'status': None,
            }

    def fetch_ledger(self, code=None, since=None, limit=None, params={}):
        if code is None:
            raise ArgumentsRequired(self.id + ' fetchLedger() requires a code param')
        self.load_markets()
        self.load_accounts()
        currency = self.currency(code)
        accountId = self.safe_string(params, 'accountId')
        if accountId is None:
            for i in range(0, len(self.accounts)):
                account = self.accounts[i]
                if account['currency'] == code and account['type'] == 'main':
                    accountId = account['id']
                    break
        if accountId is None:
            raise ExchangeError(self.id + ' ' + code + 'main account is not loaded in loadAccounts')
        request = {
            'accountId': accountId,
        }
        if since is not None:
            request['startAt'] = int(math.floor(since / 1000))
        response = self.privateGetAccountsAccountIdLedgers(self.extend(request, params))
        #
        #     {
        #         code: '200000',
        #         data: {
        #             totalNum: 1,
        #             totalPage: 1,
        #             pageSize: 50,
        #             currentPage: 1,
        #             items: [
        #                 {
        #                     createdAt: 1561897880000,
        #                     amount: '0.0111123',
        #                     bizType: 'Exchange',
        #                     balance: '0.13224427',
        #                     fee: '0.0000111',
        #                     context: '{"symbol":"KCS-ETH","orderId":"5d18ab98c788c6426188296f","tradeId":"5d18ab9818996813f539a806"}',
        #                     currency: 'ETH',
        #                     direction: 'out'
        #                 }
        #             ]
        #         }
        #     }
        #
        items = response['data']['items']
        return self.parse_ledger(items, currency, since, limit)

    def parse_ledger_entry(self, item, currency=None):
        #
        # trade
        #
        #     {
        #         createdAt: 1561897880000,
        #         amount: '0.0111123',
        #         bizType: 'Exchange',
        #         balance: '0.13224427',
        #         fee: '0.0000111',
        #         context: '{"symbol":"KCS-ETH","orderId":"5d18ab98c788c6426188296f","tradeId":"5d18ab9818996813f539a806"}',
        #         currency: 'ETH',
        #         direction: 'out'
        #     }
        #
        # withdrawal
        #
        #     {
        #         createdAt: 1561900264000,
        #         amount: '0.14333217',
        #         bizType: 'Withdrawal',
        #         balance: '0',
        #         fee: '0.01',
        #         context: '{"orderId":"5d18b4e687111437cf1c48b9","txId":"0x1d136ee065c5c4c5caa293faa90d43e213c953d7cdd575c89ed0b54eb87228b8"}',
        #         currency: 'ETH',
        #         direction: 'out'
        #     }
        #
        currencyId = self.safe_string(item, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        fee = {
            'cost': self.safe_number(item, 'fee'),
            'code': code,
        }
        amount = self.safe_number(item, 'amount')
        after = self.safe_number(item, 'balance')
        direction = self.safe_string(item, 'direction')
        before = None
        if after is not None and amount is not None:
            difference = amount if (direction == 'out') else -amount
            before = self.sum(after, difference)
        timestamp = self.safe_integer(item, 'createdAt')
        type = self.parse_ledger_entry_type(self.safe_string(item, 'bizType'))
        contextString = self.safe_string(item, 'context')
        id = None
        referenceId = None
        if self.is_json_encoded_object(contextString):
            context = self.parse_json(contextString)
            id = self.safe_string(context, 'orderId')
            if type == 'trade':
                referenceId = self.safe_string(context, 'tradeId')
            elif type == 'transaction':
                referenceId = self.safe_string(context, 'txId')
        return {
            'id': id,
            'currency': code,
            'account': None,
            'referenceAccount': None,
            'referenceId': referenceId,
            'status': None,
            'amount': amount,
            'before': before,
            'after': after,
            'fee': fee,
            'direction': direction,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'type': type,
            'info': item,
        }

    def parse_ledger_entry_type(self, type):
        types = {
            'Exchange': 'trade',
            'Withdrawal': 'transaction',
            'Deposit': 'transaction',
            'Transfer': 'transfer',
        }
        return self.safe_string(types, type, type)

    def fetch_positions(self, symbols=None, params={}):
        response = self.futuresPrivateGetPositions(params)
        #
        #     {
        #         code: '200000',
        #         data: [
        #             {
        #                 id: '605a9772a229ab0006408258',
        #                 symbol: 'XBTUSDTM',
        #                 autoDeposit: False,
        #                 maintMarginReq: 0.005,
        #                 riskLimit: 200,
        #                 realLeverage: 0,
        #                 crossMode: False,
        #                 delevPercentage: 0,
        #                 currentTimestamp: 1616549746099,
        #                 currentQty: 0,
        #                 currentCost: 0,
        #                 currentComm: 0,
        #                 unrealisedCost: 0,
        #                 realisedGrossCost: 0,
        #                 realisedCost: 0,
        #                 isOpen: False,
        #                 markPrice: 54371.92,
        #                 markValue: 0,
        #                 posCost: 0,
        #                 posCross: 0,
        #                 posInit: 0,
        #                 posComm: 0,
        #                 posLoss: 0,
        #                 posMargin: 0,
        #                 posMaint: 0,
        #                 maintMargin: 0,
        #                 realisedGrossPnl: 0,
        #                 realisedPnl: 0,
        #                 unrealisedPnl: 0,
        #                 unrealisedPnlPcnt: 0,
        #                 unrealisedRoePcnt: 0,
        #                 avgEntryPrice: 0,
        #                 liquidationPrice: 0,
        #                 bankruptPrice: 0,
        #                 settleCurrency: 'USDT',
        #                 isInverse: False
        #             },
        #             {
        #                 id: '605a9772026ac900066550df',
        #                 symbol: 'XBTUSDM',
        #                 autoDeposit: False,
        #                 maintMarginReq: 0.005,
        #                 riskLimit: 200,
        #                 realLeverage: 0,
        #                 crossMode: False,
        #                 delevPercentage: 0,
        #                 currentTimestamp: 1616549746110,
        #                 currentQty: 0,
        #                 currentCost: 0,
        #                 currentComm: 0,
        #                 unrealisedCost: 0,
        #                 realisedGrossCost: 0,
        #                 realisedCost: 0,
        #                 isOpen: False,
        #                 markPrice: 54354.76,
        #                 markValue: 0,
        #                 posCost: 0,
        #                 posCross: 0,
        #                 posInit: 0,
        #                 posComm: 0,
        #                 posLoss: 0,
        #                 posMargin: 0,
        #                 posMaint: 0,
        #                 maintMargin: 0,
        #                 realisedGrossPnl: 0,
        #                 realisedPnl: 0,
        #                 unrealisedPnl: 0,
        #                 unrealisedPnlPcnt: 0,
        #                 unrealisedRoePcnt: 0,
        #                 avgEntryPrice: 0,
        #                 liquidationPrice: 0,
        #                 bankruptPrice: 0,
        #                 settleCurrency: 'XBT',
        #                 isInverse: True
        #             }
        #         ]
        #     }
        #
        return self.safe_value(response, 'data', response)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        #
        # the v2 URL is https://openapi-v2.kucoin.com/api/v1/endpoint
        #                                †                 ↑
        #
        versions = self.safe_value(self.options, 'versions', {})
        apiVersions = self.safe_value(versions, api, {})
        methodVersions = self.safe_value(apiVersions, method, {})
        defaultVersion = self.safe_string(methodVersions, path, self.options['version'])
        version = self.safe_string(params, 'version', defaultVersion)
        params = self.omit(params, 'version')
        endpoint = '/api/' + version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        endpart = ''
        headers = headers if (headers is not None) else {}
        if query:
            if (method == 'GET') or (method == 'DELETE'):
                endpoint += '?' + self.urlencode(query)
            else:
                body = self.json(query)
                endpart = body
                headers['Content-Type'] = 'application/json'
        url = self.urls['api'][api] + endpoint
        if (api == 'private') or (api == 'futuresPrivate'):
            self.check_required_credentials()
            timestamp = str(self.nonce())
            headers = self.extend({
                'KC-API-KEY-VERSION': '2',
                'KC-API-KEY': self.apiKey,
                'KC-API-TIMESTAMP': timestamp,
            }, headers)
            apiKeyVersion = self.safe_string(headers, 'KC-API-KEY-VERSION')
            if apiKeyVersion == '2':
                passphrase = self.hmac(self.encode(self.password), self.encode(self.secret), hashlib.sha256, 'base64')
                headers['KC-API-PASSPHRASE'] = passphrase
            else:
                headers['KC-API-PASSPHRASE'] = self.password
            payload = timestamp + method + endpoint + endpart
            signature = self.hmac(self.encode(payload), self.encode(self.secret), hashlib.sha256, 'base64')
            headers['KC-API-SIGN'] = signature
            partner = self.safe_value(self.options, 'partner', {})
            partnerId = self.safe_string(partner, 'id')
            partnerSecret = self.safe_string(partner, 'secret')
            if (partnerId is not None) and (partnerSecret is not None):
                partnerPayload = timestamp + partnerId + self.apiKey
                partnerSignature = self.hmac(self.encode(partnerPayload), self.encode(partnerSecret), hashlib.sha256,
                                             'base64')
                headers['KC-API-PARTNER-SIGN'] = partnerSignature
                headers['KC-API-PARTNER'] = partnerId
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if not response:
            self.throw_broadly_matched_exception(self.exceptions['broad'], body, body)
            return
        #
        # bad
        #     {"code": "400100", "msg": "validation.createOrder.clientOidIsRequired"}
        # good
        #     {code: '200000', data: {...}}
        #
        errorCode = self.safe_string(response, 'code')
        message = self.safe_string(response, 'msg', '')
        self.throw_exactly_matched_exception(self.exceptions['exact'], message, self.id + ' ' + message)
        self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, self.id + ' ' + message)

