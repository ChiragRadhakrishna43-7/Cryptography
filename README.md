<p align='justify'><b><h1>1. Knapsack Encryption</h1></b><br/>
The Merkle–Hellman knapsack cryptosystem was one of the earliest public key cryptosystems. It was published by Ralph Merkle and Martin Hellman in 1978. <i><b>(Source: Wikipedia)</b></i><br/><br/></p>
  
<b>STEP 1: DEFINE A SUPER-INCREASING SEQUENCE-</b> <br/>
The super-increasing sequence is the user's private key.
![Screenshot 2024-06-08 155257](https://github.com/ChiragRadhakrishna43-7/Cryptography/assets/121251823/8389b1df-483e-402d-8f65-9e9f886fbd0f)

<b>STEP 2: DEFINE FUNCTIONS THAT GENERATE q AND r VALUES-</b> <br/>
These two variables help generate the public key & are actively used in decryption.
![Screenshot 2024-06-08 155700](https://github.com/ChiragRadhakrishna43-7/Cryptography/assets/121251823/58641848-3944-4ad3-8898-16921056d003)

<b>STEP 3: DEFINE THE PUBLIC-KEY FUNCTION-</b> <br/>
The public key is a non-super increasing sequence.
![Screenshot 2024-06-08 155905](https://github.com/ChiragRadhakrishna43-7/Cryptography/assets/121251823/349cf6e7-92ef-411b-b16c-2d38b6420d1f)

<b>STEP 4: ENCRYPTION FUNCTION IMPLEMENTATION-</b> <br/>
The encrypted ciphertext is an integer.<br/>
![Screenshot 2024-06-08 160259](https://github.com/ChiragRadhakrishna43-7/Cryptography/assets/121251823/14369eb5-1664-40a0-a7ae-f3e4610e2762)

<b>STEP 5: DECRYPTION-</b> <br/>
Compute r inverse. There are several ways to calculate and obtain the inverse of r. Using the extended Euclidean algorithm is one example.<br/>
![Screenshot 2024-06-08 161138](https://github.com/ChiragRadhakrishna43-7/Cryptography/assets/121251823/f44cef95-a946-4685-a7b7-f9afeb7cbe9b)
</p>

<p align='justify'><b><h1>2.AES Encryption</h1></b><br/>
Implementation of a symmetric encryption scheme using the AES (Advanced Encryption Standard) algorithm, with additional functionality for padding and unpadding plaintext data.</p>

<b>Main Functions-</b>
<p align='justify'><b>encrypt_f(plain_txt, shared_secret):</b> Encrypts a plaintext message plain_txt using a shared secret key shared_secret.<br/> <i>The encryption process involves:</i><br/>
Padded the plaintext using a block size of AES.block_size (typically 16 bytes). Generating a random initialization vector (IV) of the same size as the block size. Encrypting the padded plaintext using AES in CBC mode with the shared secret key and the IV. Encoding the encrypted data using Base64.</p>
<br/>
<p align='justify'><b>decrypt_f(cipher_txt, shared_secret):</b> Decrypts a ciphertext message cipher_txt using a shared secret key shared_secret.<br/> <i>The decryption process involves:</i><br/>
Decoding the Base64-encoded ciphertext. Extracting the IV from the beginning of the decoded data. Decrypting the ciphertext using AES in CBC mode with the shared secret key and the IV. Unpadding the decrypted plaintext using a custom function.</p>
<br/>
<b>Additional Functions-</b>
<p align='justify'><b>pad(plain_text):</b>Adds padding to the plaintext data to ensure it is aligned with the AES block size.</p>
<p align='justify'><b>unpad(plain_txt):</b>Removes padding from the decrypted plaintext data.</p>
<p align='justify'><b>int_to_bytes(integer):</b>Converts an integer to a bytes object.</p>
<b>Notes-</b>
<p align='justify'> The shared_secret key is used as input to both encryption and decryption functions. This key is assumed to be shared between the parties involved in the encryption and decryption process.
The hashlib.sha256 function is used to generate a hash of the shared secret key, which is then used as the encryption key. The code uses the AES module from the cryptography library, which provides an implementation of the AES algorithm. The get_random_bytes function generates a random bytes object of the same size as the AES block size.</p>
