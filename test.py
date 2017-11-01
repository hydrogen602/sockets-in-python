#
# How to use:
# LANconnect() <- starts connection,
#            - note that the server side must be started first
#
# .send(msg) <- sends a msg, this must be in bytes
# .receive(length) <- receives msg, length is the length of msg
#
# .cleanup() <- use at the end of code to close sockets

import socket, time, logging
logging.basicConfig(level=logging.INFO)

class LANconnect:

    def __init__(self,side,ip,myip=None,port=5002):
        if not side in ["client","server"]:
            raise ValueError('side can only equal "client" or "server"')
        self.side = side
        if myip == None:
            myip = socket.gethostbyname(socket.gethostname()) # on some computers this raises an exception, in that case myip has to be specified
        self.myip = myip
        self.ip = ip
        self.version = "1.0"
        self.port = port
        if self.side == "client":
            self.connect()
        if self.side == "server":
            self.serv = socket.socket()
            i = 5
            while True:
                try:
                    self.serv.bind((myip,port))
                except OSError:
                    logging.warn('Waiting for socket to close')
                    i -= 1
                    if i <= 0:
                        raise OSError("Socket failed "+i+" times, giving up")
                    time.sleep(60)
                else:
                    break
            self.serv.listen(1)
            logging.info('Done binding server socket')
            logging.info('Waiting for connection')
            (self.s, self.p) = self.serv.accept()
            self.serv.close()
            self.testConnection()

    def __repr__(self):
        return "<LANconnect, side="+side+", ip="+ip+", myip="+myip+">"
            
    def connect(self):
        if self.side == "server":
            logging.warn("Client only function. This is the server side")
        else:
            self.s = socket.socket()
            i = 5
            while True:
                try:
                    self.s.connect((self.ip,self.port))
                except ConnectionRefusedError:
                    logging.warn("Connection Refused")
                    time.sleep(1)
                    i -= 1
                    if i <= 0:
                        raise ConnectionRefusedError("Server port may not be open")
                except OSError:
                    logging.warn("Issues "+str(i))
                    time.sleep(1)
                    i -= 1
                    if i <= 0:
                        raise OSError("Your code has issues")
                        break
                else:
                    break
            logging.info("Connected: "+str(self.s))
            logging.info("Testing connection")
            self.testConnection()

    def testConnection(self):
        logging.info("Connected: "+str(self.s))
        logging.info("Testing connection")
        id_msg = self.side + " " + self.version
        id_msg = id_msg.encode()
        self.s.send(id_msg)
        resp = self.s.recv(10)
        resp = resp.decode()
        if self.side == "server":
            notSide = "client"
        else:
            notSide = "server"
        if resp != notSide + " " + self.version:
            raise ValueError('Expected "'+notSide + " " + self.version + '", got "'+resp+'"')
        else:
            logging.info('Setup Done, Connection good')

    def send(self,data):
        self.s.send(data)

    def receive(self,length):
        return self.s.recv(length)

    def cleanup(self):
        self.s.close()
        
