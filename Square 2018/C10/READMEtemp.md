The only symbols that print something are the rocket and aliens.
Using at least one alien will print rocket, so therefore we must include rocket in our code
So our solution will look like this: _____🚀____🚀 (the last character must be a rocket)
We also MUST include 🌗 thingy, because otherwise our output will be shorter than our input
🌗 thingy will make output size 5 times bigger so my first idea was to try to make input which will
consist of 2 repetitions of the same sequence that will produce output equal to 5 repetitions of the same sequence

This input (without the dashes):
📡🌗👽📡🚀-📡🌗👽📡🚀
Produces this output (without the dashes):
📡🌗👽📡🚀-📡🌗👽📡🚀-📡🌗👽📡🚀-📡🌗👽📡🚀-📡🌗👽📡🚀

I stumbled across it by trial and error, although there is a logical reasoning leading to it:
We have a logic before the rockets and we must paste the same logic between them as we want
our input to consist of 2 repetitions of the same sequence.
First of all our output must end with rocket and we cannot put a alien face at the end of the message (as it would mess up the rocket functionality),
so therefore we must put an alien face preceded by the satellite dish (so it will be reversed and put on the end).
We also must use exactly one 🌗 thingy.
Trying to insert other random reasonable symbols I finally stumbled across the correct input.

Now we want our output to be shorter, so we will have to obviously use the 🌓 thingy, though not directly
as it halves output, but our output sequence is repeating odd number of times so one repetition would be sliced in half.

We can try to increase number of repetitions of sequence by inserting more 🌗 things, but it will not lead us anywhere as
the number of repetitions will still be odd (and we want it to be even).
We can on the other hand paste another repetition manually into input (eg. 📡🌗👽📡🚀-📡🌗👽📡🚀-📡🌗👽📡🚀 or 📡🌗👽📡🚀-📡🌗👽📡🚀-📡🌗👽📡🚀-📡🌗👽📡🚀)
and the output produced will be equal to (5 * (repetitions in input - 1)) times 📡🌗👽📡🚀.
Therefore 📡🌗👽📡🚀-📡🌗👽📡🚀-📡🌗👽📡🚀-📡🌗👽📡🚀-📡🌗👽📡🚀 sequence consists of 5 repetitions and output consists of 20 repetitions - that's exaxtly 4 times more!
So we just must insert 🌓🌓 at the beginning of every repetition: 🌓🌓📡🌗👽📡🚀-🌓🌓📡🌗👽📡🚀-🌓🌓📡🌗👽📡🚀-🌓🌓📡🌗👽📡🚀-🌓🌓📡🌗👽📡🚀.
