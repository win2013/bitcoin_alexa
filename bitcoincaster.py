####
#
#     ASK/FALSK APi for using Alexa to interface with an mBot Device
#     By: Dr. Edwin A Hernandez   edwinhm@eglacorp.com
#     (C) 2018   - EGLA COMMUNICATIONS  - All rights reserved
#
#######################@

from random    import randint
from flask     import Flask, render_template, g
from flask_ask import Ask, statement, question, session
import logging
from btcprice import BTCPricing
from PredictedPrice import PredictedPrice

b_Scheduled = False

app      = Flask(__name__)
ask      = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

_author__     = "Edwin Hernandez, PhD"
__copyright__  = "Copyright 2018, Edwin Hernandez LLC"
__version__    = "0.1"

@ask.launch
def new_game():
    welcome_msg = render_template('welcome_msg')
    return question(welcome_msg)

def to_currency(s):
    if s.lower() not in ['dollars', 'euros']:
        raise Exception("must be dollars or euros")
    return "eur" if s == 'euros' else "usd"


@ask.intent("NoIntent")
def choose_from_no_options():
         global b_Scheduled
         scheule_msg_not = ""
         if (not b_Scheduled):
             schedule_msg_not = render_template("not_scheduled")
         choose_msg = render_template("instructions") + schedule_msg_not
         return question(choose_msg)

@ask.intent("YesIntent")
def choose_from_opotions():
        schedule_msg =""
        global b_Scheduled
        if (b_Scheduled):
            schedule_msg = render_template("scheduled")
            b_Scheduled = False;
        choose_msg = render_template("instructions") + schedule_msg
        return question(choose_msg)

@ask.intent("PriceIntent", convert={'currency': to_currency})
def last_price_bitcoin(currency):
        BTCP = BTCPricing()
        price = BTCP.getPricing(currency)
        return question('The last price {}'.format(price))

@ask.intent("ComissionIntent", convert={"currency" : to_currency})
def price_commisison_currency(currency):
        print "Commision in Currency " + currency
        pred = PredictedPrice(currency)
        if (currency=="usd"):
            currency="Dollars"
        else:
            currency="Euros"
        value_low, value_med, value_high = pred.getPredictedFee(inSatosh=False)
        data = {'low':  value_low, 'med': value_med, 'high': value_high}
        return question ("The cost of this transactuon to execute in less than 20 minutes at %s %s,  in half an hour at %s %s  and at least one hour at %s %s, what else can I do for you? " %
                          (data['low'], currency, data['med'], currency, data['high'], currency) )

@ask.intent("ComissionSatoshiIntent")
def price_commisison_currency(currency):
        pred = PredictedPrice("usd")
        value_low, value_med, value_high = pred.getPredictedFee(inSatosh=True)
        data = {'low':  value_low, 'med': value_med, 'high': value_high}
        return question ("The cost of thius transactuon is fast %(low)s satoshis for 20 minutes, or %(med)s for half and hour, and if you want to wait spend %(high)s satoshis for one hour, what else can I do for you?" % data)

@ask.intent("BestTimeIntent")
def price_commisison_currency(currency):
        pred = PredictedPrice("usd")
        best_time = pred.getBestTime()
        b_Scheduled=True
        return question ("The best time to schedule your transactiuon is at %s, would you like me to schedule it? " % best_time)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
def answer(first, second, third):
    winning_numbers = session.attributes['numbers']
    if [first, second, third] == winning_numbers:
        msg = render_template('win')
    else:
        msg = render_template('lose')
    return question(msg)


if __name__ == '__main__':
    print "Loading PriceCaster Intent for Alexa / Echo"
    #initMBot();
    app.run(debug=True, use_reloader=False)
    #g.bot.close()
