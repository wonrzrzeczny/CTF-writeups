C2: flipping bits
=================

Category: cryptology

Statement
---------

Disabling C2 requires cracking a RSA message. You have [two ciphertexts](https://2018.squarectf.com/puzzles/c2_270ca724dbf97278bf1b/flipping_bits.jar). The public key is (e1, n).

Fortunately (this time), space rabiation caused some bit flibs and the second ciphertext was encrypted with a faulty public key (e2, n). Can you recover the plaintexts?

Solution
--------

We are given two ciphertexts encrypted using RSA. The modulus used for both encrypted messages was the same and the exponents used were 13 for the first one and 15 for the second one (that is: ct1 = msg1^13 mod modulus and ct2 = msg2^15 mod modulus). First of all I assumed that both ciphertexts represent the same message (because otherwise the challenge would be nearly impossible to solve). To check if that is true we can simply see if ct1^15 mod modulus = ct2^13 mod modulus (as ct1^15 = msg1^(13*15) and ct2^13 = msg2^(13*15)).

Now we are sure that both ciphertexts corresponds to the same message. What we would like to do is to divide ct2 by ct1 in order to get msg^2 (as msg^15/msg^13 = msg^2), but this operation won't yield the correct result as our ct1 and ct2 values were taken modulo some number. Although we can calculate multiplicative inverse of ct1. Then multiplying ct2 by this inverse and taking the result modulo modulus we will get msg^2 mod modulus.

Now we can hope that msg^2 was not larger than modulus. And hopefully for us - it wasn't! So we can just take normal square root of the value. Now we just need to change the number to hex representation and convert it to ascii to get the flag: ```flag-54d3db5c1efcd7afa579c37bcb560ae0```
