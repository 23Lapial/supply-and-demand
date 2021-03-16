import random
import time


class Stock:
    def __init__(self):
        self.price = 10.0
        self.l2_data = [0.50]
        self.history = [50.0]
        self.momentum = 0
        self.volume = 0

    def return_sentiment(self):
        return sum(self.l2_data[-10:]) / 10  # len(self.l2_data)

    def return_average(self):
        return sum(self.history[-5:]) / 5  # len(self.history)

    def change_price(self):

        print(f'{self.return_sentiment():.2f}')

        if self.return_sentiment() >= .44:
            self.price += 0.01
        else:
            self.price -= 0.01

        self.history.append(self.price)

        print(f'{self.price:.2f}')


class AutoTrader:
    def __init__(self, is_smart):
        self.is_smart = is_smart
        self.positions = 0
        self.buying_power = random.randint(23, 435)
        self.trades_executed = 0
        self.trade_delay = random.randint(1, 33)

    def submit_buy_order(self, stock, qty):
        if self.buying_power <= stock.price * qty:
            return -1

        self.buying_power -= stock.price * qty

        self.positions += qty

        self.trades_executed += 1

        [stock.l2_data.append(1) for _ in range(int(qty // 2))]

    def submit_sell_order(self, stock, qty):
        if self.positions <= 0:
            return -1

        self.buying_power += stock.price * qty

        self.positions -= qty

        [stock.l2_data.append(0) for _ in range(int(qty // 2))]

    def think(self, stock):

        sentiment = stock.return_sentiment()
        average = stock.return_average()

        if stock.price <= average and sentiment >= .33 and self.trade_delay <= 0:
            self.submit_buy_order(stock=stock, qty=(0.33 * self.buying_power) // stock.price)
            self.trade_delay = random.randint(1, 13)
        else:
            self.submit_sell_order(stock=stock, qty=self.positions // 2)

        return 0

    def __repr__(self):
        return f'Trader({self.trades_executed:.2f}, {self.positions:.2f}, {self.buying_power:.2f}, {self.is_smart})'


def main():
    stock = Stock()

    traders = [
        AutoTrader(is_smart=False),
        AutoTrader(is_smart=True),
        AutoTrader(is_smart=True)
    ]

    while True:
        time.sleep(0.1)
        stock.change_price()

        for trader in traders:

            if trader.is_smart:
                trader.think(stock=stock)
                # print(trader)
            else:
                if random.choice([True, False]):
                    trader.submit_buy_order(stock=stock, qty=(0.33 * trader.buying_power) // stock.price)
                else:
                    trader.submit_sell_order(stock=stock, qty=trader.positions // 2)

            print(trader)

            trader.trade_delay -= 1


#            if trader.evaluate_stock(stock) >= .5:
#                trader.submit_buy_order(stock, 1)
#            else:
#                trader.submit_sell_order(stock, 1)


if __name__ == "__main__":
    main()
