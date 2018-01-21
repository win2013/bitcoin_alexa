

import json
import urllib2

_author__     = "Edwin Hernandez, PhD"
__copyright__  = "Copyright 2018, Edwin Hernandez LLC"
__version__    = "0.1"

class BTCPricing(object):

    currencies= ["usd", "eur"]
    coins     = ["btc", "ltc", "eth"]

    url="https://www.bitstamp.net/api/v2/ticker/"

    def BTCPricing(self):
        print "Pricing for Currencies and Coins"

    def getPricing(self, currency, coin="btc", which="last"):
        if (currency in self.currencies):
            print "OK Currrency"
        else:
            currency="usd"

        if (coin in self.coins):
            print "OK Coin"
        else:
            coin = "btc"
        response = urllib2.urlopen(self.url+coin+currency)
        json_data = json.load(response)
        return json_data[which]


if __name__ == '__main__':
      currencis=["usd", "eur"];
      BTCp = BTCPricing();
      print "Last price..."
      print "BTC to USD "+ BTCp.getPricing("usd")
      print "BTC to EUR "+ BTCp.getPricing("eur")
      print "LTC to USD "+ BTCp.getPricing("usd", "ltc")
      print "LTC to EUR "+ BTCp.getPricing("eur", "ltc")
      print "ETH to USD "+ BTCp.getPricing("usd", "eth")
      print "ETH to EUR "+ BTCp.getPricing("eur", "eth")
