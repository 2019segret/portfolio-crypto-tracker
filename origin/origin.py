# Loading initial investment in a class in case you want to add features.
class Origin_wallet():
    def __init__(self, origin_wallet):
        self.wallet = origin_wallet["values"]
        self.quantity = origin_wallet["quantity"]

    def update(self):
        raise NotImplementedError