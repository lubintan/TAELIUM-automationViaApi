# importing the requests library
import requests, csv, datetime, time

'''
http://localhost:7876/nxt?
  requestType=sendMoney&
  secretPhrase=IWontTellYou&
  recipient=NXT-4VNQ-RWZC-4WWQ-GVM8S&
  amountNQT=100000000&
  feeNQT=100000000&
  deadline=60
'''

ACCOUNTS = [['TAEL-VXVQ-APCC-UHDD-7A3ZX','password1'],
        ['TAEL-PGDQ-XR6X-2EAS-9H2KM','password2'],
          ['TAEL-D6PA-3TCG-AXGA-BVHW4','password3'],
          ['TAEL-Y4LF-K6UK-AT74-CT6JS','password4'],
          ['TAEL-J4YD-K25L-6AAS-E6Y9C','password5'],
          ['TAEL-D8XY-HTU7-QWM5-2YHMZ','password6'],
          ['TAEL-PQMA-6CS2-XU9J-AWZY7','password7'],
          ['TAEL-N7LT-FNZN-A9QJ-GPXMA','password8'],
          ['TAEL-KXHS-8A7R-5FF5-5PFS6','password9'],
            ['TAEL-DLMP-5UTD-LDQQ-8929X', 'password10'],
            ['TAEL-7WM6-25HQ-PWRD-6JYL5', 'password11'],
            ['TAEL-2F46-CUYL-GEQ9-HAV4S', 'password12'],
            ['TAEL-MVSV-VJT9-ZF66-BD69Q', 'password13'],
            ['TAEL-YB5W-5BC5-Y8BR-FSAHE', 'password14'],
            ['TAEL-6J4A-KQPT-WKUU-8UCVZ', 'password15'],
            ['TAEL-KXFC-KDK9-9QZZ-F62B6', 'password16'],
            ['TAEL-YPYD-HL88-3MAB-BBZ5Y', 'password17'],
            ['TAEL-PHRR-B6MS-K68F-B787N', 'password18'],
            ['TAEL-C2KW-R47L-UL46-FP4V4', 'password19'],
            ['TAEL-GG8F-KX2Y-EKJH-B5R7A', 'password20'],
            ['TAEL-CSA4-ZUHN-RFZ3-G2GXB','password90']]

RED_QUEEN = '44333'
ALPHA = '43255'
DEFAULT = '43250'
PORT = '44333'
def getLatestBlock():
    '''
    http://localhost:7876/nxt?
  requestType=getBlockchainStatus
    :return:
    '''

    URL = 'http://localhost:'+PORT+'/nxt?' +\
  'requestType=getBlockchainStatus'

    r = requests.post(url=URL)
    data = r.json()
    blockId = data['lastBlock']
    print 'Latest Block:', blockId

    URL = 'http://localhost:'+PORT+'/nxt?' + \
          'requestType=getBlock&block=' + blockId

    r = requests.post(url=URL)
    data = r.json()
    height = data['height']
    print 'Height:', height

def getPublicKey(accountId):
    '''
    http://localhost:7876/nxt?
      requestType=getAccountPublicKey&
      account=NXT-L6FM-89WK-VK8P-FCRBB

    '''
    URL = 'http://localhost:'+PORT+'/nxt?' + 'requestType=getAccountPublicKey&account=' + accountId
    r = requests.post(url=URL)
    data = r.json()

    print data['publicKey']

def getTxInfo(txId):
    #now check if tx went through
    '''
    http: // localhost:7876 / nxt?
    requestType = getTransaction &
    transaction = 15200507403046301754
    '''

    try:
        URL = 'http://localhost:'+PORT+'/nxt?' +\
      'requestType=getTransaction&' +\
      'transaction=' + txId

        r = requests.post(url=URL)
        data = r.json()

        return data['block'], data['blockTimestamp'],data['height']
    except Exception,e:
        print str(e)
        return None, None, None

def getAccountBalance(account):

    URL = 'http://localhost:'+PORT+'/nxt?' +\
    'requestType=getAccount&' +\
    'account=' + account

    r = requests.post(url=URL)
    data = r.json()

    for each in data:
        print each, data[each]

def sendMoney(recipient, amount, password):
    URL = "http://localhost:"+PORT+"/nxt?" +\
      'requestType=sendMoney&' +\
      'secretPhrase=' + password +'&'+\
      'recipient=' + recipient + '&' +\
      'amountNQT=' + amount + '&' +\
      'feeNQT=10000&' +\
      'deadline=60&recipientPublicKey=fc7d966d995eec3d130720a9883a89adb6c21713b9c6702fe7f196da93697a40'

    # abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef1234
    # f04f7dcfb90cbadf59b9b8dc81f52b395ee2cb0dd54cc586b4e72f8234d16c47

    r = requests.post(url=URL)

    data = r.json()

    for each in data:
        print each, data[each]

def startForging(password):
    URL = "http://localhost:"+PORT+"/nxt?" +\
      'requestType=startForging&' +\
      'secretPhrase=' + password

    r = requests.post(url=URL)
    data = r.json()

    for each in data:
        print each, data[each]

def stopForging(password):
    URL = "http://localhost:"+PORT+"/nxt?" +\
      'requestType=stopForging&' +\
      'secretPhrase=' + password

    r = requests.post(url=URL)
    data = r.json()

    for each in data:
        print each, data[each]

def getForging(password):
    URL = "http://localhost:"+PORT+"/nxt?" + \
          'requestType=getForging&' + \
          'secretPhrase=' + password

    r = requests.post(url=URL)
    data = r.json()

    return data

def getForgers():
    for account in ACCOUNTS:
        data = getForging(account[1])

        try:
            data['hitTime']
            print account[0], 'is forging.'
        except:
            print account[0], 'is NOT forging.'



if __name__ == '__main__':

    # fn = raw_input('0 - startForging, 1 - stopForging, 2 - getForgers, 3 - sendMoney, 4 - getAcctBalance, 5 - getLatestBlock, 6 - forgeAll, 7 - getPublicKey\n')

    fn = '8'

    if (fn=='0'):
        account = raw_input('Enter Acct #: (1-20)\n')
        startForging(ACCOUNTS[int(account)-1][1])

    elif (fn=='1'):
        account = raw_input('Enter Acct #: (1-10)\n')
        stopForging(ACCOUNTS[int(account)-1][1])

    elif (fn=='2'):
        getForgers()

    elif (fn=='3'):
        recipient,amount,sender = raw_input('recipient amount sender:').split()
        sendMoney(recipient=ACCOUNTS[int(recipient)-1][0], amount=amount, password=ACCOUNTS[int(sender)-1][1])

    elif (fn=='4'):
        account = raw_input('Enter Acct #: (1-10)\n')
        getAccountBalance(ACCOUNTS[int(account)-1][0])
    elif (fn=='5'):
        getLatestBlock()
    elif (fn=='6'):
        for eachAcct in ACCOUNTS:
            startForging(eachAcct[1])
    elif (fn=='7'):
        accoundId = raw_input("please enter account ID.")
        getPublicKey(accoundId)
    elif(fn=='8'):
        print 'sending..'
        # recipient, amount, sender = raw_input('recipient amount sender:').split()
        sendMoney(recipient='TAEL-HFHX-BW39-DTRT-4S8UN', amount='70000000', password=ACCOUNTS[1][1])
