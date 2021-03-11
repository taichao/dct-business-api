### `sub_user_update` 用户级信息实时更新

**重点说明 这类信息为保证最终触达，在不明确客户方收到的情况下，会反复重试,目前间隔10S，直至成功。请务必处理好数据重复问题！！！**

暂时包含两类信息
#### 账户更新信息

```
{
   "accountUpdate": {
      "balanceDataList": [
         {
            "asset": "BTC",
            "available": 6.0E-7,
            "freezing": 0
         },
         {
            "asset": "BNB",
            "available": 0,
            "freezing": 0
         },
         {
            "asset": "USDT",
            "available": 88.31624,
            "freezing": 90
         }
      ],
      "lastUpdateTime": 1614767178971
   },
   "eventType": "ACCOUNT_UPDATE",
   "streamType": "USER",
   "transactionType": "SPOT",
   "exchange": "BINANCE"
}
```

#### 订单状态变化

若是executionType=TRADE，平台会同步存储数据， 通过`rest_api get_order_trades`可查询到


重点关注字段如下

- executionType ‘TRADE’为成交
- orderStatus 当前订单最新状态
- lastFilledAmount 本次成交金额
- lastFilledQty 本次成交数量
- lastFilledPrice 本次成交价格

```
{
   "eventType": "ORDER_UPDATE",
   "orderUpdate": {
      "commissionAmount": 0,
      "cumulativeFilledAmount": 0,
      "cumulativeFilledQty": 0,
      "exchange": "BINANCE",
      "executionType": "CANCELED",
      "icebergOrderQty": 0,
      "isForward": true,
      "isInOrderBook": false,
      "isPendingOrder": false,
      "lastFilledAmount": 0,
      "lastFilledPrice": 0,
      "lastFilledQty": 0,
      "orderId": 5072583352,
      "orderListId": -1,
      "orderStatus": "CANCELED",
      "orderTradeTime": 1614767178971,
      "origQty": 0.001,
      "price": 30000,
      "quoteOrderQty": 0,
      "rejectReason": "NONE",
      "side": "BUY",
      "stopPrice": 0,
      "symbol": "BTCUSDT",
      "tradeId": -1,
      "type": "LIMIT"
   },
   "streamType": "USER",
   "transactionType": "SPOT",
   "exchange": "BINANCE"
}
```