babysponge
==========

Category: Crypto

297 points

27 solves

Task
----

We are given an implementation of a Keccak-type hashing algorithm and are asked to find two messages whose hashes are the same.

Solution
--------

In case you have never heard of the sponge construction you should read [this article](https://en.wikipedia.org/wiki/Sponge_function). I will use the following image for reference throughout this article as it will make explaining the solution much easier:

![sponge.png](sponge.png)

The only important part of the given Keccak implementation is the following function:

```python
def Keccak(rate, capacity, inputBytes, delimitedSuffix, outputByteLen):
    outputBytes = bytearray()
    state = bytearray([0 for i in range(200)])
    rateInBytes = rate//8
    blockSize = 0
    if (((rate + capacity) != 1600) or ((rate % 8) != 0)):
        return
    inputOffset = 0
    # === Absorb all the input blocks ===
    while(inputOffset < len(inputBytes)):
        blockSize = min(len(inputBytes)-inputOffset, rateInBytes)
        for i in range(blockSize):
            state[i] = state[i] ^ inputBytes[i+inputOffset]
        inputOffset = inputOffset + blockSize
        if (blockSize == rateInBytes):
            state = KeccakF1600(state)
            blockSize = 0
    # === Do the padding and switch to the squeezing phase ===
    state[blockSize] = state[blockSize] ^ delimitedSuffix
    if (((delimitedSuffix & 0x80) != 0) and (blockSize == (rateInBytes-1))):
        state = KeccakF1600(state)
    state[rateInBytes-1] = state[rateInBytes-1] ^ 0x80
    state = KeccakF1600(state)
    # === Squeeze out all the output blocks ===
    return state[:outputByteLen]
    while(outputByteLen > 0):
        blockSize = min(outputByteLen, rateInBytes)
        outputBytes = outputBytes + state[0:blockSize]
        outputByteLen = outputByteLen - blockSize
        if (outputByteLen > 0):
            state = KeccakF1600(state)
    return outputBytes
```

As you can see, every block of input is processed in the while loop. First, the first r bits of a state are xored with the current block of input, then the whole state (r + c bits) go through the KeccakF1600 function (labeled as f on our reference image). The way this function works is not important in case of this task so it's no use to read its source code. The only thing we should know is that it takes the entire state and outputs a new state and that it's independent of the input and round number.

The source code also provides some declarations of commonly used hashing algorithms in this section:

```python
def SHAKE128(inputBytes, outputByteLen):
    return Keccak(1344, 256, inputBytes, 0x1F, outputByteLen)

def SHAKE256(inputBytes, outputByteLen):
    return Keccak(1088, 512, inputBytes, 0x1F, outputByteLen)

def SHA3_224(inputBytes):
    return Keccak(1152, 448, inputBytes, 0x06, 224//8)

def SHA3_256(inputBytes):
    return Keccak(1088, 512, inputBytes, 0x06, 256//8)

def SHA3_384(inputBytes):
    return Keccak(832, 768, inputBytes, 0x06, 384//8)

def SHA3_512(inputBytes):
    return Keccak(576, 1024, inputBytes, 0x06, 512//8)
```

And they turn out to be a pretty good hint to solving the challenge. Take a good look at them and then compare them to the actual function used in our task: ```CompactFIPS202.Keccak(1552, 48, bytearray(msg), 0x06, 32)```. You can notice that the second argument corresponding to the capacity value (denoted c in the reference picture) is very small.

The simplest way to find a hash collision is to simply generate random messages and insert their hashes into a dictionary-like data structure until you stumble across a hash that was previously generated. When the hash value is n bits long then the approximate amount of messages you have to generate to find a collision is about ```2^(n/2)``` and that's due to the birthday paradox - in brief, having generated ```2^(n/2)``` messages, you have ```(2^(n/2))^2 = 2^n``` pairs of hashes and each pair has a ```1/2^n``` probability to have the exact same hash value, therefore with high probability you should have at least one pair with colliding hashes.

However our hash is 32 bytes = 256 bits long, so that is certainly too long to try to find a collision this way. But we know that the capacity of our sponge construction is relatively small. Let's look at the state of our hash right before entering the squeezing phase (look at the picture for the reference). If both our messages have the same state in this point, then their final hashes will also end up the same. Now imagine that we have two messages with the length of r bits that have the exact same last c bits of the state right before the squeezing phase. If we were to extend both of them by another block of input, both of them will first be xored with the new block and then run once more throught the f function. But we know that their last c bits are the same and we can easily calculate the xor of the first r bits of their states. If we were to append block full of zeros to the first message and block equal to this xor to the second message then their state right before going through the f function will be the same and therefore their final hashes will also be the same!

This means that we can now run a very simple attack: generate random 194 byte messages and calculate last c bits of their hash state right before the squeezing phase. After finding two messages with the colliding last c bits of the states, calculate the xor of first the r bits of their states. Append 194 null bytes to the first message and calculated xor to the second message. The resulting two messages should give the exact same hash values.

First of all we have to make some minor changes to the Keccak function in order for our attack to work properly: we must return the state right after the while loop ends and also we must return the full state array, not only first r bits as in the original implementation. The cracking script I've written in python can be found in the ```solver.py``` file, but it turned out to be extremely slow - after 3 hours of running it calculated only 5 million hashes (out of approximately 16 million required) and then it crashed with a memory error. I was therefore forced to implement my own Keccak algorithm in C++, which can be found in the ```solver.cpp``` file.

The C++ program was running for around 10 minutes when it found the collision on last c bits. All I had to do then was to copy both messages and paste them into the python solver script in place of the collision searching part. The final two messages with the same hashes were:

```
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c2d5850000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010a090e7e5ab3ebe5dfff38db8def275aea4e4faa4640b98f4dce9b7df173a1c41b8b08c65c2276d08ce5b8ee9984e90941038a5a379fbeb074d3af8d1f72a0203b8c4932a103d1da506d159b08bfa20b766b379257032bd1acb7b559a3562edc1781d190873afe80182e5d591e32088c9d7facf45fbe71d8dc702287eb6916f7b008c4527cc14ef8d53ff579435bad9266e7d3b4d1a329aec6e243305059fa2a81bdad01a7a4d67cd154ea039da461030ae4aaf1eea5b580771a5e76da8afd7a39a61f72b5
```

Passing them to the netcat server gave us a flag!

```flag{I_wAs_th3_sh4d0w_Of_the_waXwing_sLAin__By_the_fAlse_@4zure9_in_the_window_pan3}```