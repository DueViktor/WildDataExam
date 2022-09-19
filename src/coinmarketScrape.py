# https://github.com/guptarohit/cryptoCMD

from cryptocmd import CmcScraper

def scrape_it(coin_name:str):
    # initialise scraper without time interval
    scraper = CmcScraper("XRP")

    # # export the data as csv file, you can also pass optional `name` parameter
    # scraper.export("csv", name="xrp_all_time")

    # Pandas dataFrame for the same data
    df = scraper.get_dataframe()

    df.to_csv(f'data/coinmarket-{coin_name}.csv')

if __name__ == '__main__':
    coins = ['Bitcoin','XRP','Ethereum','Solana','Polkadot'] 
    for coin in coins:
        scrape_it(coin_name=coin)