from chat_utils import *
import json
from RSA import RSA

class ClientSM:
    def __init__(self, s,cipher):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.cipher = cipher
        self.rsa = RSA()
        self.cipher.addRSA(self.rsa)
        self.peer_publickey = ''

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me
    
    def send_rsa(self):
        msg = json.dumps({"action": "send rsa", "rsa_public_key": self.rsa.get_public_key(), "encryption_alpha" : self.cipher.encryption_alpha[self.cipher.private_keys.index(self.rsa.get_private_key())]})
    
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["results"] == "success":
            self.out_msg += 'Succesfully shared key to '+ self.peer + ' ' + '\n' 
            
            return (True)
        return (False)
    
    # def receive_rsa(self, peer_msg):
    #     # Receive and process RSA public key from the server
    #     if "rsa_public_key" in peer_msg:
    #         rsa_public_key = peer_msg["rsa_public_key"]
    #         self.cipher.addRSA(rsa_public_key)

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        print(response)
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            self.send_rsa()
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''
        self.peer_publickey = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                elif peer_msg["action"] == "recieve rsa":
                    self.peer_publickey = peer_msg["rsa_public_key"]
                    self.cipher.encryption_alpha.append(peer_msg["encryption_alpha"])
                    self.cipher.public_keys.append(self.peer_publickey)
                    self.cipher.private_keys.append(1)
                    self.out_msg += 'Recieved rsa public key from '+ self.peer + '\n'
                    self.send_rsa()
                    self.state = S_CHATTING
        
                    
        


#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                
                encrypted_message = self.cipher.encrypt(my_msg,self.rsa.get_private_key())
                print("private key", self.rsa.get_private_key())
                print("cipher private key",self.cipher.private_keys)
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":encrypted_message}))


                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
                
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                elif peer_msg["action"] == "recieve rsa":
                    self.peer_publickey = peer_msg["rsa_public_key"]
                    self.cipher.encryption_alpha.append(peer_msg["encryption_alpha"])
                    self.cipher.public_keys.append(self.peer_publickey)
                    self.cipher.private_keys.append(1)
                    self.out_msg += 'Recieved rsa public key from' + self.peer + '\n'
                else:
                    print("ppk", self.peer_publickey)
                    print("cipher keys", self.cipher.public_keys)
                    decrypted_message = self.cipher.decrypt(peer_msg["message"],self.peer_publickey)
                    print("decrypted message", decrypted_message)
                    self.out_msg += peer_msg["from"] + ": " + decrypted_message

                    


            # Display the menu again
            # if self.state == S_LOGGEDIN:
            #     self.out_msg += menu
    
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
