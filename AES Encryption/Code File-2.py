# CSEN 233 Extra Credit 1
# Key-Exchange Protocol Implementation with AES
# Members: Yukun Li (yli26@scu.edu) & Chirag Radhakrishna (cradhakrishna@scu.edu)
# --------------------------------------------------------------------------------

import time
import math
import random
import socket
import logging
from AES_Yukun import encrypt_f,decrypt_f

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filename="csen233ec1liyukun.logs", filemode="a")
logger = logging.getLogger(__name__)

def select_private_key(p):
    while True:
        try:
            a = int(input(f"Select private key b/w 1 and {p - 1}: "))
            if 1 <= a < p:
                logger.info(f"User has selected a private key a: {a}.")
                return a
            else:
                print("The private key must be b/w 1 and p-1.")
        except ValueError:
            print("Your private key must be an integer.")


def shared_secret(value, a, p):
    logger.info("User has obtained the information and is calculating the shared secret key.")
    return pow(value, a, p)

def p_value(n):
    return (random.randrange(2**(n-1)+1, 2**n-1))

def q_value(p):
    while True:
        x = random.randint(2, p-1)
        if math.gcd(x, p) == 1:
            return x

def public_values(conn):
    ch = input("share or receive public key:")
    if ch == "share":
        p = int(p_value(50)) # n has been set to 50. This range was determined beforehand.
        q = int(q_value(p))
        print("Sharing public key:")
        print("P:", p)
        print("Q:", q)
        try:
            conn.send(b"ready")
            time.sleep(1)
            conn.recv(1024)
            conn.send(str(p).encode())
            conn.send(str(q).encode())
        except Exception as e:
            return None, None
        return p, q
    elif ch == "receive":
        try:
            signal = conn.recv(1024)
            if signal != b"ready":
                raise Exception("Unexpected signal")
            print("Received signal to receive public key.")
            conn.send(b"ack")
            p = int(conn.recv(1024).decode())
            q = int(conn.recv(1024).decode())
            print("Received public key:")
            print("P:", p)
            print("Q:", q)
        except Exception as e:
            print(f"Error receiving public key: {e}")
            return None, None
        return p, q

def key_exchange(connection, pr_key, p, q):
    A = pow(q, pr_key, p)
    logger.info("User has combined the private key with and p and q.")
    logger.info(f"Sending value {A} for shared secret calculation.")
    connection.send(str(A).encode())
    logger.info("Receiving information (B Value) for shared secret calculation.")
    B = int(connection.recv(1024).decode())
    logger.info(f"Partner's value: {B}")
    shared_secret_key = shared_secret(B, pr_key, p)
    logger.info(f"The shared secret calculated at this side is: {shared_secret_key}.")
    message = "Hello, this is a secure message."
    encrypted_message = encrypt_f(message, shared_secret_key)
    connection.sendall(encrypted_message.encode())
    logger.info("Encrypted message sent.")
    received_encrypted_message = connection.recv(1024)
    logger.info("Received encrypted message.")
    decrypted_message = decrypt_f(received_encrypted_message, shared_secret_key)
    logger.info(f"Received and decrypted message: {decrypted_message}")

def accept():
    partner_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    addr = socket.gethostbyname(host)
    partner_addr = (addr, 0)
    partner_skt.bind(partner_addr)
    partner_skt.listen(1)
    logger.info('Starting to accept connection on {} port {}'.format(*partner_addr))
    print('Starting to accept connection on {} port {}'.format(partner_skt.getsockname()[0],
                                                               partner_skt.getsockname()[1]))
    conn, addr = partner_skt.accept()
    try:
        logger.info(f"Connected with partner: {addr}.")
        p, q = public_values(conn)
        secret = select_private_key(p)
        key_exchange(conn, secret, p, q)
    except Exception as e:
        logger.error(f"Error occured as follows: {e}.")
    finally:
        conn.close()


def connect(partner_addr, port_number):
    partner_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    partner_skt.connect((partner_addr, port_number))
    p, q = public_values(partner_skt)
    secret = select_private_key(p)
    key_exchange(partner_skt, secret, p, q)
    partner_skt.close()


def main():
    while True:
        mode = input("Select an option: (Accept/Connect): ").lower()
        if mode == "accept":
            logger.info("Accepting a connection from partner.")
            accept()
            break
        elif mode == "connect":
            address = input("Enter the address to connect to: ")
            port_number = int(input("Enter the port: "))
            connect(address, port_number)
            break
        else:
            print("Choose correct option.")
            continue

if __name__ == "__main__":
    main()
