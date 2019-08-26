Power
=====

Category: crypto

Points: 208

Solves: 19

Statement
---------

RSA is to boring. Raise to the power of x instead.

[power.py](http://static.allesctf.net/power-7919baccbb5643b6bf263d5f026709e6030980a15c3d6b49ef1eb5b52c0ee64a.py)

```nc hax.allesctf.net 1337```

Solution
--------

Given server will ask us for a number ```x``` and respond with ```x**x modulo p```, where ```p``` is some secret prime value. Additionally, we are given a ```challenge``` value everytime we are asked to send ```x```. If we manage to send such value, that ```x**x modulo p = challenge```, we will be rewarded with a flag.

Obviously, our first task is to find the value ```p```, which is unknown to us. We can do this using pretty standard method: send some value ```x``` such that ```x**x > p```. The value we get as a response will be equal to ```x``` minus some multiple of ```p```. This means that ```x**x - response``` will be a multiple of ```p```. Calculating this value for several different ```x``` and taking GCD of them will result in ```p```.

The harder part will be to actually find an ```x``` value such that ```x**x modulo p = challenge```, once we know ```p```. The solution here is very simple and elegant, yet tricky. As we can send arbitrarily large number (not necessarily smaller than ```p```) we can use the fact, that ```k*p + x modulo p = x``` for any integer ```k```. Also from Fermat's theorem we know that ```a ** (p - 1) modulo p = 1```. Therefore ```a ** l(p - 1) modulo p = 1``` for any integer ```l```. Therefore if we can find ```x``` such that ```x = l*(p - 1) + 1``` and ```x = k*p + challenge``` (1), then ```x ** x modulo p = x ** (l(p - 1) + 1) modulo p = x ** 1 modulo p = k*p + challenge modulo p = challenge``` and we are done.

To find ```x``` satisfying (1) we simply have to solve congruences: ```x = 1 modulo (p - 1)``` and ```x = challenge modulo p```, which can be done easily using either chinese remainder theorem or just simple arithmetics.

Flag: ```ALLES{n0t_100%_elgamal_but_cl0s3}```
