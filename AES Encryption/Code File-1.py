# CSEN 233 Extra Credit 1 
# Key-Exchange Protocol Implementation
# AES Encryption using secret key calculated by Diffie Hellman key-exchange.

# Members: Chirag Radhakrishna (cradhakrishna@scu.edu) and Yukun Li (yli26@scu.edu)
#----------------------------------------------------------------------------------

# LIBRARIES
import time
import math
import socket
import random
import logging
from AES_Chirag import encrypt_f, decrypt_f


logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s', filename = "csen233ec1radhakrishnachirag.logs", filemode = "a")
logger = logging.getLogger(__name__)

plaintext = "Good Morning!!" # Plaintext (message) to be encrypted.

"""
P is a large prime number that is generated at random using the random.randrange().
Based on the value of p, the corresponding prime-modulo q is generated.
"""
def generate_p(n): # The n value is decided before and is hardcoded.
    return (random.randrange(2**(n-1)+1, 2**n-1))
def generate_q(p):
    while True:
        x = random.randint(2, p - 1)
        if math.gcd(x, p) == 1:
            return x
"""
The function select_secret allows the user to pick a private key/ secret at his/her end.
We have set its value to be not more than p. The range is between 1 and p-1.
"""
def select_secret(p): #pick secret key
    while True:
        try:
            b = input(f"Select a private key from 1 to {p-1}: ")
            b = int(b)
            if b in range(1,p):
                logger.info(f"User's private key is {b}.")
                return b
            else:
                print(f"Key should be in range 1 to {p-1}.")
        except ValueError:
            print("Secret key should be an integer.")
    
"""
The shared secret calculation function helps compute the shared secret key.
This computation yields the same key that is obtained at the other end. This key can be subsequently used for encryption and decryption.
"""
def shared_secret_calcn(info, b, p):
    logger.info("Compute shared secret key with partner's information.")
    return pow(info, b, p)

"""
The Diffie Hellman Key Exchange function helps us arrive at a common secret key.
After combining the private key via calculations, it faciliates the calculation of shared secret based on the data received.
"""
def diffie_hellman_ke(conn, scr_key, p, q):
    B = pow(q, scr_key,p)
    logger.info(f"Computed and sending value B: {B} to partner for secret key calculation.")
    conn.send(str(B).encode())
    A = float(conn.recv(1024).decode())
    logger.info(f"Received information for calculating the shared secret key.")
    logger.info(f"Value received- {A}")
    shared_secret = shared_secret_calcn(int(A), scr_key, p)
    logger.info(f"Shared secret key determined is: {shared_secret}.")
    return shared_secret

"""
The share ciphertext function encrypts the given message and sends the ciphertext to the other end.
The encrypt_f function is used from the AES module as part of the encryption process.
"""
def share_ciphertext(connection, message, ss_key): # function encrypts the message/plaintext and sends the resulting ciphertext to the other end.
    logger.info("Encrypting the plaintext by padding and using the shared secret key.")
    cipher_txt = encrypt_f(message, ss_key)
    logger.info(f"Encryption performed. Sending cipher text \n:{cipher_txt}.")
    connection.sendall(cipher_txt.encode())

"""
The decrypt ciphertext function decrypts the ciphertext recieved from the other side.
The decrypt_f function from the AES module is used as part of the decryption process.
"""
def decrypt_ciphertext(connection, shared_secret):
    cipher_txt = connection.recv(1024)
    logger.info(f"Received ciphertext from partner: {cipher_txt}.")
    logger.info("Decrypting the ciphertext.")
    plain_txt = decrypt_f(cipher_txt, shared_secret)
    logger.info(f"Plain text obtained is {plain_txt}.")

"""
Helps when one person is accepting another person to connect to begin the key-exchange followed by the encryption and decryption process.
"""
def accept():
    accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    partner_address = socket.gethostbyname(socket.gethostname())
    address = (partner_address, 0)
    accept_socket.bind(address)
    port = accept_socket.getsockname()[1]
    logger.info("Accepting a connection on {} port {}:".format(accept_socket.getsockname()[0], port))
    print("Accepting a connection on {} port {}:".format(accept_socket.getsockname()[0], port))
    accept_socket.listen(1)

    conn, addr = accept_socket.accept()
    try:
        logger.info(f"Received connection from: {partner_address}.")
        p, q = share_public(conn)
        logger.info(f"P is {p}.")
        logger.info(f"Q is {q}.")
        b = select_secret(p)
        shared_secret_key = diffie_hellman_ke(conn, b, p, q)
        share_ciphertext(conn, plaintext, shared_secret_key)
        decrypt_ciphertext(conn, shared_secret_key)
    except Exception as e:
        logger.error(f"Error is as follows:{e}.")
    finally:
        conn.close()

"""
Helps when one person is connecting with the other persons address and port number.
"""
def connect(addr, port_no):
    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.info(f"Connecting with {addr}.")
    connection_socket.connect((addr, port_no))
    try:
        p, q = share_public(connection_socket)
        logger.info(f"P is {p}.")
        logger.info(f"Q is {q}.")
        b = select_secret(p)
        shared_secret_key = diffie_hellman_ke(connection_socket, b, p, q)
        share_ciphertext(connection_socket, plaintext, shared_secret_key)
        decrypt_ciphertext(connection_socket, shared_secret_key)
    except Exception as e:
        logger.error(f"Error is as follows: {e}.")
    finally:
        connection_socket.close()

"""
This function helps share the public key (p, q).
"""
def share_public(conn):
    ch = input("share or receive public key:")
    if ch == "share":
        p = int(generate_p(50)) # n has been set to 50. This range was determined beforehand.
        q = int(generate_q(p))
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


if __name__ == "__main__":
    while True:
        choice = input("Enter accept or connect: ").lower()
        if choice == "accept":
            logger.info("Partner is connecting.")
            accept()
            break
        elif choice == "connect":
            addr = input("Enter the partner's address: ")
            port = int(input("Enter the port number: "))
            connect(addr, port)
            break
        else:
            print("Enter either accept or connect.")
            continue
