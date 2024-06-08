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
</p>
