from socketserver import BaseRequestHandler, TCPServer
import DefinedInformation
import GlobalStates
import MessageController


class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('[NW]: connection from:', self.client_address)
        while True:

            msg = self.request.recv(16384) #8192
            MessageController.ValidateMessage(msg)
            if not msg:
                break
            if (GlobalStates.sendMessage):
                self.request.send(bytes(GlobalStates.messageToSend.fullMessage))
                GlobalStates.sendMessage = False

def Start():
    server = TCPServer(('', DefinedInformation.TCPPort), EchoHandler)
    server.serve_forever()

def RequestToSend(message):
    GlobalStates.messageToSend = message
    GlobalStates.sendMessage = True
    print('[NM]: Sent Request (' + str(message.data) + ')')
        
