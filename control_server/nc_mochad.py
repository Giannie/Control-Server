import socket

class nc:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.messages = []

    def send(self, content):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.hostname, self.port)
        s.sendall(b"%s\n" % content)
        s.shutdown(socket.SHUT_WR)

        buff = ""

        while True:
            data = s.recv(1024)
            if data == "":
                break
            buff = "%s%s" % (buff, data)
        s.close()
        if len(self.messages >= 100):
            self.messages = self.messages[1:]
        self.mesages.append(buff)

class x10:
    def __init__(self, nci):
        self.nc = nci

    def on(self, dev):
        s = "pl " + dev.lower() + " on"
        self.nc.send(s)

    def off(self, dev):
        s = "pl " + dev.lower() + " off"
        self.nc.send(s)
