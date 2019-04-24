
import socket, time, logging
logging.basicConfig(level=logging.INFO)

class LANconnect:

    def __init__(self,side,ip,myip=None,port=5005):
        '''
        Creates a LANconnect object which holds a socket object

        side specifies the type of socket and should equal either "client" or "server" 
        '''
        if not side in ["client","server"]:
            raise ValueError('side can only equal "client" or "server"')
        self.side = side
        if myip == None:
            myip = socket.gethostbyname(socket.gethostname()) 
            # on some computers this raises an exception, in that case myip has to be specified
        self.myip = myip
        self.ip = ip
        self.port = port
        if self.side == "client":
            self.connect()
        if self.side == "server":
            self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            attempts = 0
            while attempts < 3:
                try:
                    self.serv.bind((myip,port))
                except OSError:
                    logging.warn('Waiting for socket to close')
                    attempts += 1
                        
                    time.sleep(60)
                else:
                    break
            else:
                raise OSError("Socket failed "+ attempts +" times, giving up")

            self.serv.listen(1)
            logging.info('Done binding server socket')
            logging.info('Waiting for connection')
            (self.s, self.p) = self.serv.accept()
            self.serv.close()
            self.testConnection()

    def testConnection(self):
        logging.info("Connected: "+str(self.s))
        logging.info("Testing connection")
        id_msg = self.side
        id_msg = id_msg.encode()
        self.s.send(id_msg)
        resp = self.s.recv(10)
        resp = resp.decode()
        if self.side == "server":
            notSide = "client"
        else:
            notSide = "server"
        if resp != notSide:
            raise ValueError('Expected "' + notSide + '", got "' + resp + '"')
        else:
            logging.info('Setup Done, Connection good')

    def send(self,data):
        self.s.send(data)

    def receive(self,length):
        return self.s.recv(length)

    def cleanup(self):
        self.s.close()
