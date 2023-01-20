import src.chain.pojos


class Pool:
    def __init__(self, tokenA: src.chain.pojos.Token, tokenB: src.chain.pojos.Token):
        self.tokenA = tokenA
        self.tokenB = tokenB
        self.reserveA = 0
        self.reserveB = 0
        self.totalLiquidity = 0

    def getSymbol(self):
        return self.tokenA.symbol + "-" + self.tokenB.symbol

    def swap(self, fromToken: str, amount: float):
        return 0  # TODO: implement

    def addLiquidity(self, amountA: float, amountB: float):
        if self.totalLiquidity == 0:
            self.reserveA = amountA
            self.reserveB = amountB
            self.totalLiquidity = amountA * amountB
            return self.totalLiquidity
        else:
            tokenFromA = amountA / self.reserveA
            tokenFromB = amountB / self.reserveB
            result = min(tokenFromA, tokenFromB) * self.totalLiquidity
            self.totalLiquidity += result
            self.reserveA += amountA
            self.reserveB += amountB
            return result
