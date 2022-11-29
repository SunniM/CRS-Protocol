'''Contains methods to build and parse CRSP messages'''
def parseMessage(message):
    """
    Parses message according to CRSP

    args: 
        message (str) : CRSP message to be parsed
    returns:
        yy (str) : message type
        q (str) : q value (whether there are more portions of a single message)
        payload (str) : payload of the message

    """
    message = message.decode()
    yy = message[0:2]
    q = message[2]
    
    payload = ''
    
    if(len(message) > 3):
        payload = message[3:]

    return yy, q, payload

def build_Message(yy, q, payload):
    """
    Builds message according to CRSP

    args: 
        yy (str) : message type
        q (str) : q value (whether there are more portions of a single message)
        payload (str) : payload of the message

    returns:
        message (str) : constructed CRSP message

    """

    message = yy + q + payload 
    return message.encode()