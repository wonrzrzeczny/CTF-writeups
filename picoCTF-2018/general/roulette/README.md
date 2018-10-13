Roulette
========

350 points, 429 solves

Statement
---------
This Online [Roulette](https://2018shell2.picoctf.com/static/46f10459dc84c1b88b62ab8740afdb19/roulette) Service is in Beta. 
Can you find a way to win $1,000,000,000 and get the flag? [Source](https://2018shell2.picoctf.com/static/46f10459dc84c1b88b62ab8740afdb19/roulette.c).
Connect with ```nc 2018shell2.picoctf.com 21444```

Solution
--------

This one was cool, probably one of my favourites on pico. We are given a game consisting of series of bets. For each bet we select some amount of money we have and then we guess a number from 1 to 36. If we guess correctly we earn the same amount of money and if we guess incorrectly then we lose it.

After reading source code we can see, that in order to get the flag we must win at least 3 bets and we must earn at least 1,000,000,000 in less than 16 games. Based on that we can identify two things that we probably must exploit somehow:

* We must find a way to win every bet
* Even if we win all 16 rounds, we still won't have enough money, so there must be a way to earn more than we already own during one bet.

The first part is actually not that hard to achieve. After inspecting the code, we can see that our starting money is set using dev/urandom and that the same exact number is used to initialize seed in srand function! This way we can write our own C program looking like this:
```c
srand( <Insert starting money here> );
for (int i = 0; i < 32; i++)
	printf("%d", rand() % 36);
```

Now that we know which values are generated by rand calls during the game, we know which number we must select in order to win every bet. There is a small catch, however. Every second rand call is made to generate random message that is displayed after each bet. So the values we must input to guess correctly are displayed by our own program as the first, third, fifth, etc.

As I said before, even if we win every bet, we will earn around 450M, so it's still not enough to get the flag. So we must find a way to win more money from the single bet, than we currently own. The program checks if we bid more than our current balance. But it doesn't check if the value we input is negative! Let's try to bid -1,000,000$. The program still claims that we don't have enough money to make this bet. That's strange. After inspecting the source code we can notice, that the program uses its own function to read from input:
```c
long get_long() 
{
    printf("> ");
    uint64_t l = 0;
    char c = 0;
    while(!is_digit(c))
        c = getchar();
    while(is_digit(c)) 
    {
        if(l >= LONG_MAX) 
        {
            l = LONG_MAX;
            break;
        }
        l *= 10;
        l += c - '0';
        c = getchar();
    }
    while(c != '\n')
        c = getchar();
    return l;
}
```
So the minus sign is basically ignored and inputing -1000000 will result in program thinking that we entered 1,000,000. But it's not a problem! We can use integer overflow to our advantage. For instance, the value of 3,000,000,000 is larger than maximum number that integer can hold, so it will turn into something arount -1,000,000,000. The get_long function is checking if the number entered is larger than LONG_MAX, but it's easy to see that this check is not working too well. Therefore we can input 3000000000 and it would get accepted by the program. There still is a problem however. If we input a negative amount of money and win the bet, we will in fact lose it and become bankrupt (and this will end the game immediately). But we can also lose the bet! This way we lose -1,000,000,000$ which in fact means that we earn 1,000,000,000$ and get the flag! Yay.
