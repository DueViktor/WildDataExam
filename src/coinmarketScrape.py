# https://github.com/guptarohit/cryptoCMD

from cryptocmd import CmcScraper

def scrape_it(coin_name:str):
    # initialise scraper without time interval
    scraper = CmcScraper(coin_name)

    # Pandas dataFrame for the same data
    df = scraper.get_dataframe()

    df.to_csv(f'data/coinmarket-{coin_name}.csv')

if __name__ == '__main__':
    coins = ['BTC','XRP','ETC','SOL','DOT'] 
    for coin in coins:
        print(f'Scraping {coin}')
        scrape_it(coin_name=coin)