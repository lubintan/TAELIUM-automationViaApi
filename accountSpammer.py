import requests, csv, datetime, time, random



MASTER_FILE = 'masterAccounts.csv'
TEST_FILE = 'testAccounts.csv'
MORE_FILE = 'moreAccounts20k.csv'
INITIAL_BALANCE = '360000' + '00000000'
INITIAL_BALANCE = '500' + '00000000'

TOTAL_NXT_BAL = 99889898673081900
PORT = '52112'
TOTAL_TAELS_ALLOC = int(1e9 * 1e8 * 0.1)

AMOUNT = '270000'


def sendMoney(recipient, amount, password,publicKey):
    URL = "http://localhost:"+PORT+"/nxt?" +\
      'requestType=sendMoney&' +\
      'secretPhrase=' + password +'&'+\
      'recipient=' + recipient + '&' +\
      'amountNQT=' + amount + '&' +\
      'feeNQT=10000&' +\
      'deadline=60&recipientPublicKey=' + publicKey


    # print URL
    # print recipient

    # abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef1234
    # f04f7dcfb90cbadf59b9b8dc81f52b395ee2cb0dd54cc586b4e72f8234d16c47

    r = requests.post(url=URL)

    data = r.json()

    for each in data:
        print each, data[each]

def sendMoneyNoPubKey(recipient, amount, password):
    URL = "http://localhost:" + PORT + "/nxt?" + \
          'requestType=sendMoney&' + \
          'secretPhrase=' + password + '&' + \
          'recipient=' + recipient + '&' + \
          'amountNQT=' + amount + '&' + \
          'feeNQT=10000&' + 'deadline=60'

    r = requests.post(url=URL)

    data = r.json()

    for each in data:
        print each, data[each]

def getRS(acctNum):
    URL = 'http://localhost:'+PORT+'/nxt?' +\
    'requestType=rsConvert&' +\
    'account=' + acctNum

    # print URL

    r = requests.post(url=URL)

    data = r.json()

    return data['accountRS']

def readCSV(inputFile):

    accountsList = []

    with open(inputFile, 'rb') as f:
        reader = csv.reader(f)

        for row in reader:
            phrase = row[0].strip()
            accountRS = row[1].strip()
            accountNum = row[2].strip()
            publicKey = row[3].strip()

            accountsList.append([phrase,accountRS,accountNum,publicKey])

    return accountsList

def createGenesisJson():
    genesisAccounts = readCSV(MASTER_FILE)
    testAccounts = readCSV(TEST_FILE)
    moreAccounts = readCSV(MORE_FILE)
    nxtAccounts = readNxtAcctBalCSV("nxtSnapshotAcctBal.csv")
    nxtPubKeys = readNxtPubKeys()

    totalBal = 0

    with open("genesisAccounts_200kPlus.json","w+") as genesisAccountFile:
        genesisAccountFile.write('{"balances":{\n')

        for eachAccount in moreAccounts:
            thisLine = '"TAEL-'+ eachAccount[1] + '":"' + INITIAL_BALANCE + '",\n'
            genesisAccountFile.write(thisLine)

            totalBal += int(INITIAL_BALANCE)

        for eachAccount in testAccounts:
            thisLine = '"TAEL-'+ eachAccount[1] + '":"' + INITIAL_BALANCE + '",\n'
            genesisAccountFile.write(thisLine)

            totalBal += int(INITIAL_BALANCE)

        for eachAccount in genesisAccounts:
            thisLine = '"TAEL-'+ eachAccount[1] + '":"' + INITIAL_BALANCE + '",\n'
            genesisAccountFile.write(thisLine)

            totalBal += int(INITIAL_BALANCE)

        for eachAccount in nxtAccounts:
            thisLine = '"' + eachAccount[0] + '":"' + eachAccount[1]+ '",\n'
            genesisAccountFile.write(thisLine)

            totalBal += int(eachAccount[1])

        genesisAccountFile.write('},"publicKeys":[\n')

        for eachAccount in genesisAccounts:
            thisLine = '"' + eachAccount[3] + '",\n'
            genesisAccountFile.write(thisLine)

        for pubKey in nxtPubKeys:
            thisLine = '"' + pubKey + '",\n'
            genesisAccountFile.write(thisLine)

        genesisAccountFile.write(']}\n')


        print
        print 'TOTAL BAL:', totalBal
        print 'DIFFERENCE:', int(int(int(1e8) * int(1e9))-totalBal)

        print 'TOTAL TAELS:', totalBal/(1e8)
        print 'Diff Taels:', (int(int(1e8) * int(1e9))-totalBal)/1e8





def main():

    masterAccounts = readCSV(MASTER_FILE)

    count = 0

    for each in masterAccounts:
        print "['" + "TAEL-" + each[1] + "', '" + each[0] + "'],"

    #     count+=1
    #     print
    #     for el in each:
    #         print el, '\t',
    #
    # print "\nCount: ", count

def readNxtAccounts():

    nxtAcctAndBal = []

    counter = 0

    with open("genesisAccountsNxtAt1834461.json", "rb") as f:
    # with open('nxtSnapshotAt1834461.csv')
        reader=csv.reader(f)


        for each in reader:
            for y in each:
                splitY = y.split(':')
                addrNum = splitY[0].strip()
                balance = splitY[1].strip()

                # rsAccount = None
                rsAccount = getRS(addrNum)
                counter += 1

                if ((counter%100)==0):
                    print "AccountRS getting at numero:",counter

                nxtAcctAndBal.append([str(rsAccount), str(int(balance)*TOTAL_TAELS_ALLOC/TOTAL_NXT_BAL)])

    print 'Done reading file and getting AccountRSes.'


    counter = 0
    with open("nxtSnapshotAcctBal.csv", "w+") as f:

        for each in nxtAcctAndBal:
            f.write(each[0] +','+each[1] + '\n')

            counter+=1
            if ((counter%100==0)):
                print 'line count at:',counter


    sum = 0
    for each in nxtAcctAndBal:
        sum+= each[1]

    print "TOTAL:", sum
    print "TOTAL TAELS:", sum/1e8


    print len(nxtAcctAndBal)


def readNxtPubKeys():

    pubKeyList =[]

    with open("nxtPubKeys.txt", "rb") as f:
        reader = csv.reader(f)


        for each in reader:

            if each[0] != 'null':
                pubKeyList.append(each[0])
                # print each[0]


    # print "Length: ", len(pubKeyList)

    return pubKeyList

def readNxtAcctBalCSV(inputFile):

    accountsList = []

    with open(inputFile, 'rb') as f:
        reader = csv.reader(f)

        for row in reader:
            accountRS = row[0].strip()
            bal = row[1].strip()

            accountsList.append([accountRS,bal])

    return accountsList

def getAccountBalance(account):

    URL = 'http://localhost:'+PORT+'/nxt?' +\
    'requestType=getBalance&' +\
    'account=' + account

    r = requests.post(url=URL)
    data = r.json()

    #
    # for each in data:
    #     print each, data[each]

    return data['balanceNQT']


def spamTest():
    testAccts = readCSV(TEST_FILE)

    masterAccts = readCSV(MASTER_FILE)


    jose = masterAccts[7]

    counter = 0

    for pogba in testAccts:
        sendMoney('TAEL-'+pogba[1], AMOUNT, jose[0], pogba[3])
        counter += 1


        time.sleep(12)

        if counter%100 == 0:
            print 'total sent count:', counter


    print
    print 'Completed Sending. Verifying Accounts...'





def spamVerify():
    testAccts = readCSV(TEST_FILE)

    counter = 0

    for pogba in testAccts:
        bal = getAccountBalance('TAEL-'+pogba[1])

        if (bal == AMOUNT) or (bal==(2*AMOUNT)):
            counter += 1
            print 'passed'
        else:
            print 'bal:', bal
            print 'expected:', AMOUNT

        if counter % 5 == 0:
            print 'total verified count:', counter
            print
            print
            time.sleep(1)

def startForging(password):
    URL = "http://localhost:" + PORT + "/nxt?" + \
          'requestType=startForging&' + \
          'secretPhrase=' + password

    r = requests.post(url=URL)
    data = r.json()

    for each in data:
        print each, data[each]

def stopForging(password):
    URL = "http://localhost:" + PORT + "/nxt?" + \
          'requestType=stopForging&' + \
          'secretPhrase=' + password

    r = requests.post(url=URL)
    data = r.json()

    for each in data:
        print each, data[each]


def onOffForgers():

    startForgers(None)
    masterAccts = readCSV(MASTER_FILE)

    forgerList = masterAccts[0:7]
    amount = '330000000'

    senders = masterAccts[0:2]
    recipients = masterAccts[10:20]

    forgerTarget = None

    while (True):
        sleepTime = random.randint(10,120*60)
        print 'sleeping for', sleepTime, 'seconds'
        time.sleep(sleepTime)

        if (random.randint(0,1) == 0) and (forgerTarget==None):
            forgerTarget = forgerList[random.randint(0,6)][0]
            startForging(forgerTarget)

        elif forgerTarget!=None:
            stopForging(forgerTarget)
            forgerTarget = None

        else:
            stopForging(forgerList[random.randint(0,6)][0])

        time.sleep(2)

        sender = senders[random.randint(0, len(senders) - 1)]
        recipient = recipients[random.randint(0, len(recipients) - 1)]

        print 'Sending Money', sender[1], 'to', recipient[1], 'amount:', amount

        sendMoneyNoPubKey('TAEL-' + recipient[1], amount, sender[0])

        time.sleep(2)


        # print 'Number:', counter
        # print

def startForgers(inputFile):

    if inputFile==None:
        inputFile = MASTER_FILE

    masterAccts = readCSV(inputFile)

    forgerList = masterAccts[4:8]

    counter = 0
    for each in forgerList:

        startForging(each[0])
        counter += 1

        print 'Number:', counter
        print


def stopForgers(inputFile):

    if inputFile==None:
        inputFile = MASTER_FILE

    masterAccts = readCSV(MASTER_FILE)

    forgerList = masterAccts[0:2000]

    counter = 0
    for each in forgerList:

        stopForging(each[0])
        counter += 1

        print 'Number:', counter
        print



def startOldForgers():
    oldForgers = ['password1','password2','password3','password4','password5','password6','password7','password8','password9','password10']
    oldForgers += ['password11','password12','password13','password14','password15','password16','password17','password18','password19','password20',]

    for each in oldForgers:
        startForging(each)

def startOldMasterForgers():
    startForgers("oldMasterAccounts.csv")

def sendMoneyAround():
    masterAccts = readCSV(MASTER_FILE)

    senders = masterAccts[0]
    recipients = masterAccts[1]

    wait = [1,2,3,4,5]

    amount = '330000000'

    while (True):
        sender = senders[random.randint(0,len(senders)-1)]
        recipient = recipients[random.randint(0,len(recipients)-1)]

        print 'Sending Money', sender[1], 'to', recipient[1], 'amount:', amount

        sendMoneyNoPubKey('TAEL-'+recipient[1],amount,sender[0])

        time.sleep(wait[random.randint(0, len(wait)-1)])


if __name__ == '__main__':
    # main()
    # createGenesisJson()
    # readNxtAccounts()
    # readNxtPubKeys()
    # readNxtPubKeys()
    # spamTest()
    # spamVerify()
    # startForgers(None)
    # # startOldForgers()
    # # startOldMasterForgers()
    # spamTest()

    # stopForgers(None)
    # startForgers(None)
    # spamTest()
    # onOffForgers()


    # sendMoneyAround()

    #1534032000000

    targetMillis = (1533970080000 + 20000)/1000

    while (True):
        time.sleep(2)

        current = time.time()

        print "current: ", current
        print "target: ", targetMillis

        if (current > targetMillis):
            onOffForgers()
