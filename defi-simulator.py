# A simulator to predict defi markets
from src.chain.Pool import Pool
from src.chain.blockchain import BlockChain
from src.chain.pojos import Token, Wallet, Block
from src.chain.transactions.AccountToAccount import AccountToAccount

chain = BlockChain()

# init chain
#tokens
chain.addToken(Token("DFI"))
chain.addToken(Token("DUSD"))
# pools
chain.addPool(Pool(chain.tokens["DUSD"],chain.tokens["DFI"]))

# wallets
chain.addWallet(Wallet("wallet1",None))
chain.wallets["wallet1"].balances["DFI"] = 1000
chain.wallets["wallet1"].balances["DUSD"] = 10000

chain.addWallet(Wallet("wallet2",None))
chain.wallets["wallet2"].balances["DFI"] = 1

chain.addToMempool([AccountToAccount("wallet1","wallet2",{"DFI":100,"DUSD":50})])

chain.addBlock(Block(prev=None,txs=[])) # genesis block

def doStep():
    block = chain.blockFromMempool()
    chain.addBlock(block)
    for wallet in chain.wallets.values():
        txs = wallet.strategy.createTxs(chain)
        chain.addToMempool(txs)
