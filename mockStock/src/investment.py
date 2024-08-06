class MockInvestment:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.portfolio = {}

    def buy(self, symbol, price, quantity):
        total_cost = price * quantity
        if self.balance >= total_cost:
            self.balance -= total_cost
            if symbol in self.portfolio:
                self.portfolio[symbol] += quantity
            else:
                self.portfolio[symbol] = quantity
            return f'Bought {quantity} shares of {symbol} at {price}'
        else:
            return 'Insufficient funds'

    def sell(self, symbol, price, quantity):
        if symbol in self.portfolio and self.portfolio[symbol] >= quantity:
            self.portfolio[symbol] -= quantity
            total_sale = price * quantity
            self.balance += total_sale
            return f'Sold {quantity} shares of {symbol} at {price}'
        else:
            return 'Not enough shares to sell'

    def show_portfolio(self):
        return self.portfolio, self.balance
