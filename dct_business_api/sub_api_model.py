class UserEventModel:
    def __init__(self, event):
        self.exchange = event.get("exchange")
        self.stream_type = event.get("streamType")
        self.transaction_type = event.get("transactionType")
        self.event_type = event.get("eventType")
        self.data = event.get("data")
        if not self.data:
            raise Exception('data is None')


class OrderCreatedModel(UserEventModel):
    def __init__(self, event):
        super(OrderCreatedModel, self).__init__(event)
        self.order_id = self.data.get("orderId")
        self.status = self.data.get('status')


class OrderCanceledModel(UserEventModel):
    def __init__(self, event):
        super(OrderCanceledModel, self).__init__(event)
        self.order_id = self.data.get("orderId")
        self.status = self.data.get('status')
        self.remark = self.data.get('remark')
        self.tradeTime = self.data.get('tradeTime')
        self.price = self.data.get('price')


class OrderCreateFailedModel(UserEventModel):
    def __init__(self, event):
        super(OrderCreateFailedModel, self).__init__(event)
        self.order_id = self.data.get("orderId")


class OrderFilledModel(UserEventModel):
    def __init__(self, event):
        super(OrderFilledModel, self).__init__(event)
        self.order_id = self.data.get('orderId')
        # True = 已完全成交 False = 未完全成交
        self.is_end = self.data.get('isEnd')
        self.status = self.data.get('status')

        # 暂时忽略
        self.is_forward = self.data.get('isForward')
        self.trade_id = self.data.get('tradeId')
        self.filled_qty = self.data.get('filledQty')
        self.filled_price = self.data.get('filledPrice')
        self.filled_amount = self.data.get('filledAmount')
        self.cumulative_filled_qty = self.data.get('cumulativeFilledQty')
        self.cumulative_filled_amount = self.data.get('cumulativeFilledAmount')
        self.commission_asset = self.data.get('commissionAsset')
        self.commission_amount = self.data.get('commissionAmount')


class AccountUpdateModel(UserEventModel):
    def __init__(self, event):
        super(AccountUpdateModel, self).__init__(event)
        self.balance_list = self.data.get('balanceDataList')
        if self.balance_list:
            self.balance_dict = dict((item['asset'], item) for item in self.balance_list)

    def get(self, asset):
        self.balance_dict.get(asset)
