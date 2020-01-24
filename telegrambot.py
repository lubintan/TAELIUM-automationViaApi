#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging, csv, requests, time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

START, PUBKEY, ADDR_ENTRY = range(3)

ID_FILE = 'telegram_ids'
HEX_CHARACTERS = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

EIGHT_ZEROES = 100000000.0
TAELS_PER_ETH = 7800
FEE = 0.001
FEE_HAEDS = 100000
PORT = 'insert port number'
AMOUNT = 100000000000
PHRASE = 'insert phrase here'

def sendMoney(recipient, amount, password, publicKey):
    # api-endpoint
    URL = "http://localhost:"+PORT+"/nxt?" +\
      'requestType=sendMoney&' +\
      'secretPhrase=' + password +'&'+\
      'recipient=' + recipient + '&' +\
      'amountNQT=' + str(amount) + '&' +\
      'feeNQT=100000&' +\
      'deadline=60&' +\
        'recipientPublicKey=' + publicKey


    # sending get request and saving the response as response object
    r = requests.post(url=URL)

    # extracting data in json format
    data = r.json()

    # for each in data:
    #     print each, data[each]

    if 'errorDescription' in data:
        # print data['errorDescription']

        return False, data['errorDescription']

    return True, data['transaction']

def getBalance(account):
    URL = "http://localhost:"+PORT+"/nxt?" +\
    'requestType=getBalance&' +\
    'account='+account

    # sending get request and saving the response as response object
    r = requests.post(url=URL)

    # extracting data in json format
    data = r.json()

    return data['balanceNQT']


def check_duplicate_csv(filename, id):
    idList = []

    with open(filename + '.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            idList.append(row[0])

    print idList

    if str(id) in idList:
        return True

    return False


def append_to_csv(fileName, data):
    with open(fileName + '.csv', 'ab') as f:
        writer = csv.writer(f)
        writer.writerow([data])

def start(bot, update):
    update.message.reply_text(
        'Welcome to the Taelium Test Net Tap!\n'
        'Please enter your Taelium Test Net address in the following format:\n'
        'TAEL-XXXX-XXXX-XXXX-XXXXX')

    return ADDR_ENTRY


def addr_entry(bot, update, user_data):



    user = update.message.from_user
    input = update.message.text
    input = input.strip().upper()

    user_data['address'] = input

    print
    print 'entering address:'
    print user.id
    print input




    # address check
    if not ((len(input) == 25) and (input[4] == '-') and (input[9] == '-') and (input[14] == '-') and (
        input[19] == '-') and (input[0:4]=='TAEL')):
        update.message.reply_text(
            'Please check that you entered your address correctly. \n'
            '\nIf the problem persists, please contact the Taelium channel admin @delvol.\n')
        update.message.reply_text(
            'Please enter your Taelium Test Net address in the following format:\n'
            'TAEL-XXXX-XXXX-XXXX-XXXXX')
        return ADDR_ENTRY

    if check_duplicate_csv(ID_FILE, user.id):  # true means got duplicate
        update.message.reply_text(
            'Our records indicate that you have already received Taels from the tap. \n'
            'Please use those Taels to fund your other accounts. \n'
            'If you need more Taels, please contact the Taelium channel admin @delvol.\n'
            'Thank you for being a part of Taelium!\n')
        # update.message.reply_text(
        #     'Please enter your Taelium Test Net address in the following format:\n'
        #     'TAEL-XXXX-XXXX-XXXX-XXXXX')

        return ConversationHandler.END

    update.message.reply_text(
        'Please enter your public key.\n')

    return PUBKEY




def pubkey(bot, update, user_data):

    address = user_data['address']

    user = update.message.from_user
    input = update.message.text
    input = input.strip().lower()
    publicKey = input

    print
    print 'entering public key:'
    print user.id
    print input

    if (len(input) != 64):
        ##### DANGER WRONG PUBLIC KEY! #####
        update.message.reply_text(
            'Please check that you have entered your public key correctly. \n'
            '\nIf the problem persists, please contact the Taelium channel admin @delvol.\n')
        update.message.reply_text(
            'Please enter your Taelium Test Net address in the following format:\n'
            'TAEL-XXXX-XXXX-XXXX-XXXXX')
        return ADDR_ENTRY

    for eachChar in input:
        if (not (eachChar in HEX_CHARACTERS)):
            update.message.reply_text(
                'Please check that you have entered your public key correctly. \n'
                '\nIf the problem persists, please contact the Taelium channel admin @delvol.\n')
            update.message.reply_text(
                'Please enter your Taelium Test Net address in the following format:\n'
                'TAEL-XXXX-XXXX-XXXX-XXXXX')
            return ADDR_ENTRY

    ################
    # Send section #
    ################

    update.message.reply_text(
        'Processing transaction..\n')

    beforeAmount = int(getBalance(address))
    status, details = sendMoney(address, AMOUNT, PHRASE, publicKey)

    if status==False:
        update.message.reply_text(
            'There was a problem with your transaction. \n'
            'Error Message: ' + details +'\n'
            '\nPlease try again.\n')
        update.message.reply_text(
            'Please enter your Taelium Test Net address in the following format:\n'
            'TAEL-XXXX-XXXX-XXXX-XXXXX')
        return ADDR_ENTRY





    append_to_csv(ID_FILE, user.id)

    update.message.reply_text(
        'Please wait for the transaction to be confirmed.\n(This may take several minutes.)\n')

    time.sleep(10)
    afterAmount = int(getBalance(address))

    while ((afterAmount - beforeAmount) < AMOUNT):
        time.sleep(5)
        afterAmount = int(getBalance(address))

    update.message.reply_text(
        'Transaction successful.\n'
        'Transaction ID: ' + details + '\n'
        'Recipient: ' + address + '\n'
        'Amount: 1000 Taels\n\n'
        'Thank you for using Taelium. For any questions or feedback, please '
        'contact the Taelium channel admin at t.me/delvol or visit the Taelium website '
        'at Taelium.com.\n'
    )

    return ConversationHandler.END





# def cancel(bot, update):
#     user = update.message.from_user
#     logger.info("User %s canceled the conversation.", user.first_name)
#     update.message.reply_text('Bye! I hope we can talk again some day.',
#                               reply_markup=ReplyKeyboardRemove())
#
#     return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("copy paste bot token here")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            START: [MessageHandler(Filters.text, start, pass_user_data=True)],
            ADDR_ENTRY: [MessageHandler(Filters.text, addr_entry, pass_user_data=True)],
            PUBKEY: [MessageHandler(Filters.text, pubkey,pass_user_data=True)],




        },

        fallbacks=[CommandHandler('start', start)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()



