## create_order
### request
- timeInForce GTC 默认先传这个
- type 默认传LIMIT 暂时只测试了LIMIT
- symbol 交易对
- quantity 数量
- price 价格

### response
#### success demo

```
{
    "code": "success",
    "data": {
        "orderId": 1369914333810663426,
        "userId": 1,
        "accountId": 4,
        "otherId": 5183210539,
        "exchange": "BINANCE",
        "transactionType": "SPOT",
        "symbol": "BTC-USDT",
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": 0.0004000000,
        "quoteOrderQty": null,
        "price": 54100.0000000000,
        "stopPrice": null,
        "icebergQty": null,
        "status": "NEW",
        "transactTime": 1615448003929,
        "transactTimeDt": "2021-03-11 07:33:24",
        "executedQty": 0E-10,
        "cummulativeQuoteQty": 0E-10
    },
    "extra": null,
    "message": "交易成功"
}
```
- status 
```
NEW,
    PARTIALLY_FILLED,
    FILLED,
    CANCELED,
    PENDING_CANCEL,
    REJECTED,
    EXPIRED,
    ERROR,
    API_ERROR,
    NOSENT
```
- executedQty 交易所执行数量 如交易对BTC-USDT 的BTC数量
- cummulativeQuoteQty 交易所执行金额 如交易对BTC-USDT 的USDT金额

#### error
- platform_api_business_error 调用交易所api错误，理论上同参数不应该重试
- runtime_error 平台服务器未知异常
- param_error

## get_order
### response
#### success
```
{
    "code": "success",
    "data": {
        "orderId": 1358206112343699458,
        "userId": 1,
        "accountId": 4,
        "otherId": 4688226574,
        "exchange": "BINANCE",
        "transactionType": "SPOT",
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": 0.0010000000,
        "quoteOrderQty": null,
        "price": 39137.0000000000,
        "stopPrice": null,
        "icebergQty": null,
        "status": "FILLED",
        "transactTime": 1612656546594,
        "transactTimeDt": "2021-02-07 00:09:07",
        "executedQty": 0.0010000000,
        "cummulativeQuoteQty": 39.1070600000
    },
    "extra": null,
    "message": "交易成功"
}
```
#### error 订单不存在
```
{
    "code": "param_error",
    "data": null,
    "extra": null,
    "message": "no order found"
}
```

## cancel_order
### response 
#### success
取消成功，同时返回订单最新信息

```
{
    "code": "success",
    "data": {
        "orderId": 1369936141041541122,
        "userId": 1,
        "accountId": 4,
        "otherId": 5184082719,
        "exchange": "BINANCE",
        "transactionType": "SPOT",
        "symbol": "BTC-USDT",
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": 0.0004000000,
        "quoteOrderQty": null,
        "price": 45000.0000000000,
        "stopPrice": null,
        "icebergQty": null,
        "status": "CANCELED",
        "transactTime": 1615453203574,
        "transactTimeDt": "2021-03-11 09:00:04",
        "executedQty": 0E-10,
        "cummulativeQuoteQty": 0E-10
    },
    "extra": null,
    "message": "交易成功"
}
```
####  `order_delete_not_supported`
对不支持的订单返回此错误，同时返回订单最新信息
```
{
    "code": "order_delete_not_supported",
    "data": {
        "orderId": 1369936141041541122,
        "userId": 1,
        "accountId": 4,
        "otherId": 5184082719,
        "exchange": "BINANCE",
        "transactionType": "SPOT",
        "symbol": "BTC-USDT",
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": 0.0004000000,
        "quoteOrderQty": null,
        "price": 45000.0000000000,
        "stopPrice": null,
        "icebergQty": null,
        "status": "CANCELED",
        "transactTime": 1615453203574,
        "transactTimeDt": "2021-03-11 09:00:04",
        "executedQty": 0E-10,
        "cummulativeQuoteQty": 0E-10
    },
    "extra": "delete_already_end_of_status",
    "message": "当前状态不支持取消"
}
```

## get_order
```
{
    "code": "success",
    "data": {
        "orderId": 1369936141041541122,
        "userId": 1,
        "accountId": 4,
        "otherId": 5184082719,
        "exchange": "BINANCE",
        "transactionType": "SPOT",
        "symbol": "BTC-USDT",
        "side": "BUY",
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": 0.0004000000,
        "quoteOrderQty": null,
        "price": 45000.0000000000,
        "stopPrice": null,
        "icebergQty": null,
        "status": "CANCELED",
        "transactTime": 1615453203574,
        "transactTimeDt": "2021-03-11 09:00:04",
        "executedQty": 0E-10,
        "cummulativeQuoteQty": 0E-10
    },
    "extra": null,
    "message": "交易成功"
}
```

## `get_order_trades`
### success with data
- tradeId 交易所id
- symbol 交易所symbol 这个没做特殊转化，具体判断以order信息位置

```
{
    "code": "success",
    "data": [
        {
            "id": 1358243351740235777,
            "orderId": 1358206112343699458,
            "tradeId": 622409774,
            "symbol": "BTCUSDT",
            "price": 39107.0600000000,
            "qty": 0.0010000000,
            "quoteQty": 39.1070600000,
            "commission": 0.0000010000,
            "commissionAsset": "BTC",
            "time": "2021-02-07 00:09:07",
            "isBuyer": "true",
            "isMaker": "false",
            "isBestMatch": "true"
        }
    ],
    "extra": null,
    "message": "交易成功"
}
```
### success without data

```
{
    "code": "success",
    "data": [],
    "extra": null,
    "message": "交易成功"
}
```