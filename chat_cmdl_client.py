
from chat_client_class import *
from RSA import Cipher

def main():
    import argparse
    cipher = Cipher()
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()

    client = Client(args)
    client.run_chat(cipher)

main()
