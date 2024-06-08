# CSEN233 Extra Credit #2: Knapsack Encryption
# Chirag Radhakrishna (cradhakrishna@scu.edu)
# Divya Shetty (dshetty2@scu.edu)

# Implementation of encryption and decryption using the knapsack algorithm

import logging
import argparse
from random import randint
import math
import socket
import json


logger = logging.getLogger(__name__)


def create_logger():
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("knapsack_shettydivya.log")
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(fh_formatter)

    ch_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(ch_formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)


def gen_coprime(modulus):
    coprime = randint(1, modulus - 1)
    while math.gcd(modulus, coprime) != 1:
        coprime = randint(1, modulus - 1)

    return coprime


def gen_private_key(num_elems):
    # super-increasing sequence of length num_elems
    seq = []

    for i in range(num_elems):
        prev_total = sum(seq)
        # randomly increase the next int (max limit of 10)
        next_elem = prev_total + randint(1, 10)
        seq.append(next_elem)

    return seq


def gen_public_key(seq, mod, mult):
    key = [(mult * elem) % mod for elem in seq]
    return key


def encrypt(msg, public_key):
    encrypted_seq = []
    for i in range(len(msg)):
        encrypted_seq.append(int(msg[i]) * public_key[i])

    return sum(encrypted_seq)

# helper method to find (g, a, b) where (xa + yb = gcd(x, y)
# logic from wikibooks
def _gcd(x, y):
    if x == 0:
        return y, 0, 1
    else:
        gcd, a, b = _gcd((y % x), x)
        return gcd, b - (y // x) * a, a


# helper method to calculate the modular multiplicative inverse
def _mod_mult_inverse(mult, mod):
    gcd, a, b = _gcd(mult, mod)
    if gcd != 1:
        return None
    return a % mod

    
def decrypt(cipher, private_key, mod, mult):
    # modular inverse of mult % mod
    mod_inv = _mod_mult_inverse(mult, mod)
    if not mod_inv:
        raise Exception('Cannot decrypt. No modular multiplicative inverse exists')

    cipher_prime = (cipher * mod_inv) % mod
    indices = []

    # locate bit positions to be '1'
    for i in range(len(private_key) - 1, -1, -1):
        if private_key[i] <= cipher_prime:
            cipher_prime -= private_key[i]
            indices.append(i+1)

    # directly use index values to "flip bit" in a string of 0s
    decrypted = sum([2**(len(private_key)-index) for index in indices])
    
    # convert to bit format
    return format(decrypted, f'0{len(private_key)}b')


def exchange(host=None, port=None):
    user_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # send public key to provided host:port, decrypt returning msg
        if args.host and args.port:
            logger.info("You will be SHARING your key")
            logger.info('Generating private and public key...')
            num = int(input("Number of elements for private key sequence: "))
            private = gen_private_key(num)
            modulus = sum(private) + randint(1, 50)
            multiplier = gen_coprime(modulus)
            public = gen_public_key(private, modulus, multiplier)
            logger.debug(f'Private key: {private}, Public key: {public}, '
                         f'Modulus: {modulus}, Multiplier: {multiplier}')

            # convert public key to json string for simpler sending
            public_json = json.dumps(public)
            logger.info(f'Sending public key to ({args.host}, {args.port})')
            user_socket.sendto(public_json.encode('utf-8'), (args.host, args.port))

            # receive and decrypt msg
            cipher_bytes, addr = user_socket.recvfrom(2048)
            cipher = int(cipher_bytes.decode('utf-8'))
            logger.info(f'Received encrypted message: {cipher}')

            final_msg = decrypt(cipher, private, modulus, multiplier)
            logger.info(f'Decrypted message: {final_msg}')

        # wait for public key, encrypt a message
        else:
            bind_to_local(user_socket)
            logger.info("You will be RECEIVING a key")
            
            # load received public key -> list format
            other_public_json, addr = user_socket.recvfrom(2048)
            other_public = json.loads(other_public_json.decode('utf-8'))
            logger.debug(f'Other public key: {other_public}')
            
            message = input(f'Enter binary message of {len(other_public)} bits: ')
            while (len(message) != len(other_public)):
                message = input(f'Incorrect length. Try again: ')
            logger.debug(f'Confirm message is: {message}')

            # encrypt and send msg
            encrypted_msg = encrypt(message, other_public)
            logger.info(f'Encrypted message: {encrypted_msg}')

            encrypted_msg_json = json.dumps(encrypted_msg)
            user_socket.sendto(encrypted_msg_json.encode('utf-8'), addr)
            logger.info(f'Sent encrypted message to {addr}')
    except Exception as e:
        logger.error(e)
    finally:
        user_socket.close()

        
def bind_to_local(user_socket):
    localhost = socket.gethostname()
    user_socket.bind((localhost, 0))
    host = user_socket.getsockname()[0]
    port = user_socket.getsockname()[1]
    logger.info(f'Connect at ({host}, {port})')


if __name__ == "__main__":
    create_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--host', action='store', help="connection ip")
    parser.add_argument('-p', '--port', type=int, help="connection port")

    args = parser.parse_args()

    exchange(args.host, args.port)
