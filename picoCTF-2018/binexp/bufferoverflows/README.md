buffer overflow 0
=================

150 points, 2477 solves

Statement
---------

Let's start off simple, can you overflow the right buffer in this [program](https://2018shell2.picoctf.com/static/7a1b5f87d2fa0b17afa0ee20a3870bb6/vuln) to get the flag? You can also find it in /problems/buffer-overflow-0_2_aab3d2a22456675a9f9c29783b256a3d on the shell server. [Source](https://2018shell2.picoctf.com/static/7a1b5f87d2fa0b17afa0ee20a3870bb6/vuln.c).

Solution
--------

This task serves as a introduction to buffer overflow exploit, something that we will be using very often in binary exploitation type tasks.

The argument we input is passed to this function:
```c
void vuln(char *input){
  char buf[16];
  strcpy(buf, input);
}
```
It uses ```strcpy``` function to copy input from argument to array ```buf```. We see that the size of array is very small (16), but the program has no protection against inputing more than 16 characters. Which basically means that we can input as many characters as we want. The characters that won't fit into the array will overwrite random bytes of program memory. Moreover, the overwritten bytes may happen to be something important, for instance the return adress of a function. Return adress basically tells the program to which instruction it's supposed to jump to after returning from the function call. So if the return adress will be replaced with some random junk the program will crash and return a segmentation fault error.

```c
signal(SIGSEGV, sigsegv_handler);
```

This line of code tells the program that in case of receiving segmentation fault it is supposed to call function ```sigsegv_handler```:

```c
void sigsegv_handler(int sig) {
  fprintf(stderr, "%s\n", flag);
  fflush(stderr);
  exit(1);
}
```

And the ```sigsegv_handler``` simply prints out our flag! So let's try it out! Typing ```./vuln aaaaaaaaaaaaaaaaaaaaaaaaaaaa``` into the shell makes the program print out the flag: ```picoCTF{ov3rfl0ws_ar3nt_that_bad_5d8a1fae}```
