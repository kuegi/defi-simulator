from ..chain.Pool import Pool, PoolFee
from ..chain.pojos import Token, Wallet
from .simulation import Simulation
from ..chain.transactions.CompositeSwap import SwapPath
from ..chain.transactions.liquidity import AddLiquidity
from ..strategies.BBB import BBBStrategy
from ..strategies.DUSDBuy import DUSDBuyStrategy
from ..strategies.DUSDLoop import DUSDLoopArbStrategy
from ..strategies.DUSDSell import DUSDSellStrategy
from ..strategies.cexArbStrat import cexArbStrat, ArbPair
from ..strategies.oracleStrat import OracleFromLambda


class BBBEffectSimulation(Simulation):

    def __init__(self,sellsPerDay,buysPerDay,ratioToDFI,BBBDFIPerDay):
        super().__init__()
        self.sellsPerDay= sellsPerDay
        self.buysPerDay=buysPerDay
        self.ratioToDFI= ratioToDFI
        self.BBBDFIPerDay= BBBDFIPerDay

    def initChain(self):
        #tokens
        self.chain.addToken(Token("DFI"))
        self.chain.addToken(Token("BTC"))
        self.chain.addToken(Token("ETH"))
        self.chain.addToken(Token("USDT"))
        self.chain.addToken(Token("USDC"))
        self.chain.addToken(Token("DUSD"))

        # pools
        self.chain.addPool(Pool(self.chain.tokens["DUSD"],self.chain.tokens["DFI"],feeA=PoolFee(inFee=0.3)))
        usdtdfi= self.chain.addPool(Pool(self.chain.tokens["USDT"],self.chain.tokens["DFI"]))
        usdcdfi= self.chain.addPool(Pool(self.chain.tokens["USDC"],self.chain.tokens["DFI"]))
        btcdfi= self.chain.addPool(Pool(self.chain.tokens["BTC"],self.chain.tokens["DFI"]))
        ethdfi= self.chain.addPool(Pool(self.chain.tokens["ETH"],self.chain.tokens["DFI"]))

        self.chain.addPool(Pool(self.chain.tokens["USDT"],self.chain.tokens["DUSD"],feeB=PoolFee(inFee=0.3)))
        self.chain.addPool(Pool(self.chain.tokens["USDC"],self.chain.tokens["DUSD"],feeB=PoolFee(inFee=0.3)))

        # wallets
        self.chain.addWallet(Wallet("initialFunds",None))
        self.chain.wallets["initialFunds"].balances["DFI"] = 100e6
        self.chain.wallets["initialFunds"].balances["BTC"] = 100e6
        self.chain.wallets["initialFunds"].balances["ETH"] = 100e6
        self.chain.wallets["initialFunds"].balances["DUSD"] = 100e6
        self.chain.wallets["initialFunds"].balances["USDT"] = 100e6
        self.chain.wallets["initialFunds"].balances["USDC"] = 100e6

        self.chain.oracles["BTCUSD"]= 27044
        self.chain.oracles["ETHUSD"]= 1910
        #self.chain.addWallet(Wallet("BTCOracle",OracleFromLambda(lambda id,chain: 28000 if id == "BTCUSD" else None)))

        self.chain.addWallet(Wallet("CexArb",cexArbStrat(0.01,1000,
                                                         [
                                                             ArbPair("BTCUSD",SwapPath([usdcdfi,btcdfi],"USDC","BTC")),
                                                             ArbPair("BTCUSD",
                                                                     SwapPath([usdtdfi, btcdfi], "USDT", "BTC")),
                                                             ArbPair("ETHUSD",SwapPath([usdcdfi,ethdfi],"USDC","ETH")),
                                                             ArbPair("ETHUSD",
                                                                     SwapPath([usdtdfi, ethdfi], "USDT", "ETH"))
                                                         ])))
        self.chain.wallets["CexArb"].balances["BTC"] = 100e6
        self.chain.wallets["CexArb"].balances["ETH"] = 100e6
        self.chain.wallets["CexArb"].balances["USDT"] = 100e6
        self.chain.wallets["CexArb"].balances["USDC"] = 100e6

        if self.BBBDFIPerDay > 0:
            self.chain.addWallet(Wallet("BBB",BBBStrategy(self.BBBDFIPerDay)))
            self.chain.wallets["BBB"].balances["DFI"] = 100e6

        self.chain.addWallet(Wallet("DUSDLoopArb",DUSDLoopArbStrategy(1000)))
        self.chain.wallets["DUSDLoopArb"].balances["DUSD"] = 10000

        self.chain.addWallet(Wallet("DUSDBuyer",DUSDBuyStrategy(self.buysPerDay/24,120)))
        self.chain.wallets["DUSDBuyer"].balances["USDT"] = 100e6
        self.chain.wallets["DUSDBuyer"].balances["USDC"] = 100e6

        #add DUSDSeller

        self.chain.addWallet(Wallet("DUSDSeller",DUSDSellStrategy(self.sellsPerDay/24,120,self.ratioToDFI)))
        self.chain.wallets["DUSDSeller"].balances["DUSD"] = 100e6

        # initial liquidity
        self.chain.addToMempool([AddLiquidity(owner="initialFunds",balances={"DFI":12.21e6,"DUSD":11.41e6})])
        self.chain.addToMempool([AddLiquidity(owner="initialFunds",balances={"DFI":95685998,"BTC":1234})])
        self.chain.addToMempool([AddLiquidity(owner="initialFunds",balances={"DFI":24433133,"ETH":4458})])

        self.chain.addToMempool([AddLiquidity(owner="initialFunds",balances={"USDT":1.972e6,"DUSD":5.663e6})])
        self.chain.addToMempool([AddLiquidity(owner="initialFunds",balances={"USDC":891e3,"DUSD":2.569e6})])

        self.chain.addToMempool([AddLiquidity(owner="initialFunds",balances={"USDT":1.718e6,"DFI":4.964e6})])
        self.chain.addToMempool([AddLiquidity(owner="initialFunds",balances={"USDC":1.589e6,"DFI":4.556e6})])

        self.run(1) #initial step



