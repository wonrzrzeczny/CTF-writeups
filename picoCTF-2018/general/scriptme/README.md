Script me
=========

500 points, 478 solves

Statement
---------

Can you understand the language and answer the questions to retrieve the flag? Connect to the service with ```nc 2018shell2.picoctf.com 1542```

Solution
--------

This one was just weird. Not really sure what's going on in there, maybe the task references something well-known that I'm just not aware of.

We work with a group of objects (correct bracket sequences) with defined addition operation and we are given some examples of how does the addition of the sequences works. Our task is to determine how does the addition operation work and then to write a script to perform this additions.

For every bracket sequence I will define its depth as the maximum number of "not closed" opening brackets up to some point in it. For example: () has depth 1, (()) has depth 2, (()()) has depth 2 and (()(())) has depth 3. The way this bracket sequence adding works is that the sequences with larger depth "absorb" the ones with the smaller depth (as explained in the examples on nc).

More precisely:
* Sequences with equal depth are placed one next to another () + () = ()()
* If the left sequence has larger depth then the right one will be placed inside of it, right before its last ending bracket: (()(())) + () = (()(()) () )
* If the right sequence has larger depth then the situation is analogical to the previous one.

Here is my script, written in python, which adds a set of sequences:
```python
def depth(s):
    d = 0
    out = 0
    for i in range(len(s)):
        if s[i] == '(':
            d += 1
        else:
            d -= 1
        if d > out:
            out = d
	return out

def merge(s1, s2):
    if depth(s1) == depth(s2):
        return s1 + s2
    if depth(s1) < depth(s2):
        return "(" + s1 + s2[1:]
    if depth(s2) < depth(s1):
        return s1[:-1] + s2 + ")"

s = input()
literals = s.split(' + ')

out = literals[0]
for x in range(1, len(literals)):
    out = merge(out, literals[x])
print(out)
```

The depth function calculates the depth for given bracket sequece. Merge function returns the sum of two bracket sequences. The script splits the input into array of literals and then it performs additions from left to right and prints out the output. Now all that is left to do in order to get the flag is to connect using nc and paste answers to generated questions.
