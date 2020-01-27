""" IRC Conroller 

    .. codeauthor:: Eli Reid <EliR@EliReid.com>
"""
import socket
import time

class IrcController():
    """ IRC Conroller

        :param server: address to IRC server
        :type server: str

        :param port: IRC server port
        :type port: int

        :param pingwait: keep alive delay 
        :type ping: int
    """
    def __init__(self, server: str, port: int, pingwait: int = 300)->None:
        # Populate values
        self._server: str = server
        self._port: int = port
        self._pingWait: int = pingwait
        self._lastPing: time = time.time()
        self._connected: bool = False
        self._socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self)->None:
        """ IrcController.connect - Creates new socket & Opens connection to IRC server  
        
            :return: None
            :rtype: None
        """
        try:
            # Create new socket and connect
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self._server, self._port))
            self._connected =True
            print(f"Connected to {self._server}:{self._port}!")
        except socket.error as error:
            self.disconnect(error)
            
    def disconnect(self, reason)->None:
        """ IrcController.disconnect - Closes sockets & Disconects from IRC server 
        
            :return: None
            :rtype: None
        """
        self._socket.close()
        print(f"Disconneted! {reason}")
        self._connected = False

    def send(self, data: str)->None:
        """ IrcController.send - sends to server 
            
            :param data: string to be sent to IRC server
            :type event: str

            :return: None
            :rtype: None
        """
        try:
            data = f"{data}\r\n" if not data.endswith("\r\n") else data
            self._socket.sendall(data.encode())
        except socket.error as error:
            self.disconnect(error)

    def receive(self)->str:
        """ IrcController.receive - Receives all data from socket buffer 
        
            :return: data 
            :rtype: str
        """
        data: str = ""
        self._ping()
        while self._connected:
            self._socket.setblocking(False)
            try:
                # Should be ready to read
                data += self._socket.recv(4096).decode()
                if data.startswith("PING"):
                    self._pong(data)
            except BlockingIOError:
                self._socket.setblocking(True)
                break
            except socket.error as error:
                self.disconnect(error)
        return data if len(data) > 0 else None 

    def isConnected(self)->bool:
        """ IrcController.isConnected - Gets status of server connection
            
            :return: self._connected
            :rtype: bool
        """
        return True if self._connected else False

    def _ping(self)->None:
        """ IrcController._ping - sends keep alive ping if pingwait timer runs out  
        
            :return: None
            :rtypr: None
        """
        try:
            if time.time() - self._lastPing > self._pingWait:
                self._lastPing = time.time()
                self.send("PING")
        except socket.error as error:
            self.disconnect(error)

    def _pong(self, data: str)->None:
        """ IrcController._pong - replies to server ping 

            :return: None
            :rtypr: None   
        """
        try:
            self._lastPing = time.time()
            self.send(data.replace("PING", "PONG"))
        except socket.error as error:
            self.disconnect(error)