from math import sqrt

import src.chain.pojos

class PoolFee:
    def __init__(self,inFee=0,outFee=0):
        self.inFee= inFee
        self.outFee= outFee

class Pool:
    def __init__(self, tokenA: src.chain.pojos.Token, tokenB: src.chain.pojos.Token,
                 commission: float= 0.002, feeA: PoolFee=PoolFee(), feeB: PoolFee=PoolFee()):
        self.tokenA = tokenA
        self.tokenB = tokenB
        self.reserveA = 0
        self.reserveB = 0
        self.totalLiquidity = 0
        self.commission= commission
        self.feeA= feeA
        self.feeB= feeB

    def __str__(self):
        return f"{self.reserveA/self.reserveB:.4f}/{self.reserveB/self.reserveA:.4f} {self.tokenA.symbol}({self.reserveA:.2f})-{self.tokenB.symbol}({self.reserveB:.2f}) {self.totalLiquidity:.2f}"

    def getSymbol(self):
        return self.tokenA.symbol + "-" + self.tokenB.symbol

    def getAB(self):
        return self.reserveA/self.reserveB

    def getSwapValueAfterFees(self,AtoB):
        inFee= self.feeA if AtoB else self.feeB
        outFee= self.feeB if AtoB else self.feeA
        price= self.reserveB/self.reserveA if AtoB else self.reserveA/self.reserveB
        return (1-self.commission)*(1-inFee.inFee)*price*(1-outFee.outFee)

    def swap(self, fromToken: str, amount: float):
        X = self.reserveA * self.reserveB
        inAmount= amount*(1-self.commission)
        if fromToken == self.tokenA.symbol:
            inAmount*= (1-self.feeA.inFee)
            swapOut = self.reserveB - X / (self.reserveA + inAmount)
            self.reserveA += inAmount
            self.reserveB -= swapOut
            swapOut *= (1-self.feeB.outFee)
        else:
            inAmount*= (1-self.feeB.inFee)
            swapOut = self.reserveA - X / (self.reserveB + inAmount)
            self.reserveB += inAmount
            self.reserveA -= swapOut
            swapOut *= (1-self.feeA.outFee)
        return swapOut

    def addLiquidity(self, amountA: float, amountB: float):
        if self.totalLiquidity == 0:
            self.reserveA = amountA
            self.reserveB = amountB
            self.totalLiquidity = sqrt(amountA * amountB)
            return self.totalLiquidity
        else:
            tokenFromA = amountA / self.reserveA
            tokenFromB = amountB / self.reserveB
            result = min(tokenFromA, tokenFromB) * self.totalLiquidity
            self.totalLiquidity += result
            self.reserveA += amountA
            self.reserveB += amountB
            return result

    def removeLiquidity(self, amount:float):
        remA= self.reserveA*amount/self.totalLiquidity
        remB= self.reserveB*amount/self.totalLiquidity
        self.totalLiquidity-= amount
        return {self.tokenA.symbol:remA,self.tokenB.symbol:remB}
