

import json
import urllib2
from CostPerTransaction import CostPerTransaction

_author__     = "Edwin Hernandez, PhD"
__copyright__  = "Copyright 2018, Edwin Hernandez LLC"
__version__    = "0.1"

#{ "fastestFee": 40, "halfHourFee": 20, "hourFee": 10 }'

class PredictedPrice(object):
      url="https://bitcoinfees.earn.com/api/v1/fees/recommended"
      currency="usd"

      def __init__(self, currency):
          print "PredictedPrice.... "
          self.currency=currency
          self.cpt_fastest = 0
          self.cpt_halfhour = 0
          self.cpt_hourfee = 0

      def getBestTime(self):
          return "22:15:00"

      def getPredictedFee(self, inSatosh=False):
          print self.url
          hdr = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                  'Accept-Encoding': 'none',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Connection': 'keep-alive' }
          req = urllib2.Request(self.url, headers=hdr)
          page = urllib2.urlopen(req)
          json_data = json.load(page)
          print json_data["fastestFee"]
          #print self.currency
          AVG_BYTES=1000
          if (not inSatosh):
             self.cpt_fastest = CostPerTransaction(json_data["fastestFee"], self.currency).getTransactionValue();
             self.cpt_halfhour = CostPerTransaction(json_data["halfHourFee"], self.currency).getTransactionValue()
             self.cpt_hourfee  = CostPerTransaction(json_data["hourFee"], self.currency).getTransactionValue()
             return self.cpt_fastest*AVG_BYTES, self.cpt_halfhour*AVG_BYTES, self.cpt_hourfee*AVG_BYTES
          else:
             return json_data["fastestFee"], json_data["halfHourFee"], json_data["hourFee"]



if __name__ == '__main__':
     # currencies = ["usd", "eur"]
      p_usd=PredictedPrice("usd")
      print p_usd.getPredictedFee(inSatosh=True)
      p_eur=PredictedPrice("eur")
      print p_eur.getPredictedFee();
