# CSEN 233 Extra Credit 2
# Knapsack Encryption
#
# Members: Chirag Radhakrishna SCU ID: 07700009612 (cradhakrishna@scu.edu) &
#          Divya Shetty SCU ID: (dshetty2@scu.edu)
#---------------------------------------------------------------------------

import math
import json
import socket
import struct
import random
import argparse
import logging

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s -%(message)s', filename = "csen233ec2RadhakrishnaChirag.logs", filemode = "w")
logger = logging.getLogger(__name__)

"""
Function that generates a super-increasing sequence of n values. This n value is provided via user input.
The super-increasing sequence is used as the private key.
"""

def super_increasing_sequence(n): # Private Key.
    knapsack = []
    total = 0
    for i in range(1, n+1):
        next_element = random.randint(total + 1, 2*total + 1)
        knapsack.append(next_element)
        total = total + next_element
    return knapsack

"""
Generate a random integer q.
The value of q must be greater than the sum of elements in the super-increasing sequence.
"""

def generate_q(private_key_sequence): # q value.
    sums = 0
    for i in private_key_sequence:
        sums = sums + i
    q = sums + random.randint(1,500)
    return q

"""
Function that generates value r.
r is co-prime to q, gcd(r, q) = 1.
"""

def generate_r(q): # r value (r is co-prime to q).
    r = random.randint(2, q - 1)
    while math.gcd(q, r) != 1:
        r = random.randint(2, q-1)
    return r

"""
Function that generates the public key.
The public key is a non-super increasing sequence. It is obtained from the private key sequence, q and r.
"""

def public_key(private_key, q, r): # Public key
    pb_key = []
    for i in range(len(private_key)):
        item = (private_key[i] * r) % q
        pb_key.append(item)
    return pb_key

"""
Encrypting the plaintext using the public key.
Cipher text is a product of public key sequence and plaintext bits.
"""
def encrypt_f(message, public_key): # Encryption
    sums = 0
    for i in range(len(public_key)):
        sums += (public_key[i] * int(message[i]))
    return sums

"""
Decrypting the ciphertext using the private key.
"""
# Find r inverse using Extended-Euclidean Algorithm-
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b%a, a)
        return gcd, y - (b//a) * x, x

def inverse(r, q):
    gcd, x, y = extended_gcd(r, q)
    if gcd !=1:
        return None
    else:
        return x%q

def decrypt_f(cipher, private_key, r_inv, q): # Decryption
    cipher_inv = (cipher*r_inv) % q
    plain_txt = ""
    private_key = private_key[::-1]
    for i in range(len(private_key)):
        if private_key[i] <= cipher_inv:
            plain_txt =  "1" + plain_txt
            cipher_inv = cipher_inv - private_key[i]
        else:
            plain_txt =  "0" + plain_txt
    return plain_txt

"""
Networking Implementation.
"""

def comm(host, port):
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        if host and port:
            logger.info(f'Connecting with {host} on port {port}.')
            exchange(udpSocket, host, port)
        else:
            bind_to_local(udpSocket)
            exchange(udpSocket, host, port)
    except Exception as e:
        logger.error(e)
    finally:
        udpSocket.close()

def exchange(skt, host, port):
    choice = input('share or receive? ')
    if choice == "share":
        n = int(input("Enter the number of bits you would like to send: "))
        pr_key = super_increasing_sequence(n)
        logger.info(f"My private key is {pr_key}.")
        q = generate_q(pr_key)
        logger.info(f"q value is {q}.")
        r = generate_r(q)
        logger.info(f"r value is {r}.")
        pb_key = public_key(pr_key, q, r)
        logger.info(f"My public key is {pb_key}.")
        pb_key_ = json.dumps(pb_key)
        logger.info(f"Sending public key to teammate.")
        skt.sendto(pb_key_.encode('utf-8'), (host, port))
        cipher_txt, addr = skt.recvfrom(2048)
        logger.info(f"Received ciphertext.")
        cipher = int(cipher_txt.decode('utf-8'))
        r_inv = inverse(r, q)
        logger.info(f"Decrypting ciphertext.")
        plain_txt = decrypt_f(cipher, pr_key, r_inv, q)
        logger.info(f"Plain text obtained is {plain_txt}.")
    elif choice == "receive":
        key, addr = skt.recvfrom(2048)
        pb_key_ = key.decode('utf-8')
        logger.info(f"Public key received is: {pb_key_}.")
        pb_key = json.loads(pb_key_)
        length = len(pb_key)
        logger.info(f"Received publiic key {pb_key_}.")
        message = input(f'Enter the message to be sent of {length} bits: ')
        logger.info("Encrypting message.")
        cipher_txt = encrypt_f(message, pb_key)
        cipher = json.dumps(cipher_txt)
        skt.sendto(cipher.encode('utf-8'), addr)
        logger.info("Sent ciphertext to teammate.")
    
def bind_to_local(connSocket):
    localhost = socket.gethostname()
    connSocket.bind((localhost, 0))
    host = connSocket.getsockname()[0]
    port = connSocket.getsockname()[1]
    logger.info(f'Accepting connection -----> {host} :: {port}')
    print(f'Accepting connection -----> {host} :: {port}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--host', action = 'store', help = "address")
    parser.add_argument('-p', '--port', type = int, help = "port")
    args = parser.parse_args()
    comm(args.host, args.port)
    




    
  
