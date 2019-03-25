#include <cstdio>
#include <map>

using namespace std;

typedef unsigned long long int ull;

int bytes[200];
int input[200];
const int cap = 6;

ull rol64(ull a, int n)
{
    return (a >> (64 - (n % 64))) + (a << (n % 64));
}

void SHA3_calc()
{
    for (int i = 0; i < 200 - cap; i++)
        bytes[i] = input[i];
    for (int i = 200 - cap; i < 200; i++)
        bytes[i] = 0;
    ull **lanes = new ull*[5];
    for (int i = 0; i < 5; i++)
        lanes[i] = new ull[5];

    for (int x = 0; x < 5; x++)
        for (int y = 0; y < 5; y++)
        {
            lanes[x][y] = 0;
            for (int i = 0; i < 8; i++)
                lanes[x][y] += (ull)bytes[i + 8 * (x + 5 * y)] << (8 * i);
        }

    int R = 1;
    for (int round = 0; round < 24; round++)
    {
        ull *C = new ull[5];
        for (int i = 0; i < 5; i++)
            C[i] = lanes[i][0] ^ lanes[i][1] ^ lanes[i][2] ^ lanes[i][3] ^ lanes[i][4];
        ull *D = new ull[5];
        for (int i = 0; i < 5; i++)
            D[i] = C[(i+4)%5] ^ rol64(C[(i+1)%5], 1);
        for (int x = 0; x < 5; x++)
            for (int y = 0; y < 5; y++)
                lanes[x][y] ^= D[x];

        int X = 1;
        int Y = 0;
        ull current = lanes[X][Y];
        for (int t = 0; t < 24; t++)
        {
            int nX = Y;
            int nY = (2 * X + 3 * Y) % 5;
            X = nX;
            Y = nY;
            ull ncurrent = lanes[X][Y];
            lanes[X][Y] = rol64(current, (t+1)*(t+2)/2);
            current = ncurrent;
        }

        for (int y = 0; y < 5; y++)
        {
            ull *T = new ull[5];
            for (int x = 0; x < 5; x++)
                T[x] = lanes[x][y];
            for (int x = 0; x < 5; x++)
                lanes[x][y] = T[x] ^ ((~T[(x+1)%5]) & T[(x+2)%5]);
            delete[] T;
        }

        delete[] C;
        delete[] D;

        for (int j = 0; j < 7; j++)
        {
            R = ((R << 1) ^ ((R >> 7)*0x71)) & 0xff;
            if (R & 2)
                lanes[0][0] = lanes[0][0] ^ (1LL << ((1LL << j) - 1));
        }
    }

    for (int x = 0; x < 5; x++)
        for (int y = 0; y < 5; y++)
            for (int i = 0; i < 8; i++)
                bytes[i + 8 * (x + 5 * y)] = (lanes[x][y] >> (8 * i)) & 0xff;

    for (int x = 0; x < 5; x++)
        delete[] lanes[x];

    delete[] lanes;
}

void SHA3_print()
{
    for (int i = 0; i < 200; i++)
        printf("%x", bytes[i]);
    puts("");
}

char hexinput[400];

int hexdigit(char c)
{
    if (c < 'A')
        return c - '0';
    return c - 'A' + 10;
}

map<ull, ull> mapa;
typedef map<ull, ull>::iterator it;

int main()
{
    for (int i = 0; i < 200 - cap; i++)
        input[i] = 0;

    ull counter = -1;
    while (true)
    {
        counter += 1;
        if (counter % 1000 == 0)
            printf("%llu\n", counter);
        for (int i = 200 - cap - 8; i < 200 - cap; i++)
            input[i] = (counter >> (1600 - 8 * cap - 8 * i - 8)) & 0xff;

        SHA3_calc();
        ull capbytes = 0;
        for (int i = 200 - cap; i < 200; i++)
            capbytes += (ull)bytes[i] << (1592 - 8 * i);

        if (mapa.find(capbytes) != mapa.end())
        {
            printf("%llx\n\n", mapa[capbytes]);
            printf("%llx\n\n", capbytes);
            printf("%llx\n\n", counter);
            SHA3_print();
            for (int i = 0; i < 200; i++)
                printf("%x ", input[i]);
            return 0;
        }
        mapa[capbytes] = counter;
    }
}
