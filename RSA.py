from random import randint as rd
import random
import math
import string

class RSA:
    def __init__(self):
        self.p = self.generate_prime()
        self.q = self.generate_prime()
        self.compute_key()

    def generate_prime(self):
        # Generate a random prime number
        while True:
            num = rd(50, 100)
            if self.is_prime(num):
                return num

    def is_prime(self, n):
        # Check if a number is prime
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def compute_key(self):
        self.n = self.p * self.q
        self.lcm = math.lcm(self.p - 1, self.q - 1)
        self.e = self.generate_public_key()
        self.d = self.generate_private_key()

    def generate_public_key(self):
        # Generate a random public key
        while True:
            e = rd(2, self.lcm - 1)
            if math.gcd(e, self.lcm) == 1:
                return e

    def generate_private_key(self):
        # Compute the private key using the Extended Euclidean Algorithm
        a, b = self.e, self.lcm
        x, y = 0, 1
        while a != 0:
            q, b, a = b // a, a, b % a
            x, y = y - q * x, x
        if y < 0:
            y += self.lcm
        return y

    def get_public_key(self):
        return self.n, self.e

    def get_private_key(self):
        return self.d

class Cipher:
    def __init__(self):
        self.rsas = []  # List of RSA instances
        self.encryption_alpha = []  # List to store encryption alphabets
        self.public_keys = []  # List to store public keys
        self.private_keys = []  # List to store private keys

        print("inside object", self.public_keys, self.private_keys)
    
    def addRSA(self, rsa_new):
        self.rsas.append(rsa_new)
        self.public_keys.append(rsa_new.get_public_key())
        self.private_keys.append(rsa_new.get_private_key())
        self.encryption_alpha.append(self.generate_key()) 
        print("inside object", self.public_keys, self.private_keys)
        return rsa_new


    def generate_key(self):
        # Generate a random key for the substitution cipher
        alphabet = list(string.printable)
        rand = list(range(0,99)) 
        random.shuffle(rand)
        key = [alphabet[i] for i in rand]
        #key = [alphabet[i] for i in key_indices]
        return ''.join(key)
    
    def encrypt(self, message, private_key):
        alphabet = list(string.printable) # ASCII characters
        if private_key in self.private_keys:
            private_key_index = self.private_keys.index(private_key)
            encrypted_message = [self.encryption_alpha[private_key_index][alphabet.index(char)] for char in message]
            return ''.join(encrypted_message)
        else:
            print("Private key not valid")


        
    def decrypt(self, message, public_key):
        alphabet = list(string.printable) # ASCII characters
        if public_key in self.public_keys:
            public_key_index = self.public_keys.index(public_key)
            decrypted_message = [alphabet[self.encryption_alpha[public_key_index].index(char)] for char in message]
            return ''.join(decrypted_message)
        else:
            print("Public key not valid")

        


    
if __name__ == "__main__":
    # Steph generates RSA keys
    steph_cipher = Cipher()
    steph_rsa = RSA()
    steph_rsacipher = steph_cipher.addRSA(steph_rsa)  # Call addRSA method to initialize RSA keys
    steph_public_key = steph_rsacipher.get_public_key()
    steph_private_key = steph_rsacipher.get_private_key()
    print("STEPH PRIVATE, PUBLIC:", steph_private_key, steph_public_key)

    # Silu generates RSA keys
    #silu_cipher = Cipher()
    silu_cipher = Cipher()
    silu_rsa = RSA()
    silu_rsacipher = silu_cipher.addRSA(silu_rsa)  # Call addRSA method to initialize RSA keys
    silu_public_key = silu_rsacipher.get_public_key()
    silu_private_key = silu_rsacipher.get_private_key()
    print("SILU PRIVATE, PUBLIC:", silu_private_key, silu_public_key)

    # Steph sends a message to Silu
    message = "Hello Silu!!"
    encrypted_message = steph_cipher.encrypt(message,steph_private_key) 
    decrypted_message = steph_cipher.decrypt(encrypted_message,steph_public_key)

    # Silu receives and decrypts the message using her private key

    print("Original message:", message)
    print("Encrypted message:", encrypted_message)
    print("Decoded message:", decrypted_message)
