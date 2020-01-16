""" IRC Conroller  """
import socket
import time


class IrcController():
    """description of class"""
    def __init__(self, server: str, port: int, pingwait: int = 3000):
        # Populate values
        self._server: str = server
        self._port: int = port
        self._pingWait: int = pingwait
        self._pingString: str = ""
        self._lastPing: time = time.time()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self)->None:
        """

        Connect to IRC server
        """
        try:
            # Create new socket and connect
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self._socket.connect((self._server, self._port))

            return
        except Exception as error:
            raise Exception(error)

    def disconnect(self)->None:
        """ diconnnect """
        self._socket.close()

    def send(self, data: str)->None:
        """ send"""
        try:
            self._socket.setblocking(True)
            if not data.endswith("\r\n"):
                data += "\r\n"
            self._socket.send(data.encode())
            
            return 
        except Exception as error:
            raise Exception(error)

    def receive(self)->str:
        """  receive """

        data: str = ""
        # keep alive ping
        self._ping()
        while True:
            try:
                # disable sockets error supression to maintian local event loop
                self._socket.setblocking(False)
                # Check for received data and handle any data
                data += self._socket.recv(4096).decode()
                if data.startswith("PING"):
                    self._pong(data)
            except WindowsError as error:
                # Socket.recev buffer is empty return data
                if error.errno == 10035:
                    if len(data) > 0:
                        return data

    def _ping(self)->None:
        """ _ping  """
        try:
            if time.time() - self._lastPing > self._pingWait:
                self._lastPing = time.time()
                self.send("PING")
        except Exception as error:
            raise Exception(error)

    def _pong(self, data: str)->None:
        """ _ping  """
        try:
            self._lastPing = time.time()
            self.send(data.replace("PING", "PONG"))
            return
        except Exception as error:
            raise Exception(error)
