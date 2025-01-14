#include "sqrt.h"
#include <iostream>
using namespace std;
const int NEPS = 0.00000001;

double num_sqrt(int number) {
    bool is_negative = false;
    if (number < 0) { // numer может быть отрицательным, поэтому в таком случае выносим минус
        number = -number;
        is_negative = true;
    }
    double x = 1, nx;
    for (;;) {
        nx = (x + number / x) / 2;
        if (abs(x - nx) < NEPS or abs(x - nx) == 0)  break;
        x = nx;
    }
    x = int(x * 100 + 0.5) / double(100); // находим число с точностью до 2 знаков
    if (is_negative) {
        return -x;
    } return x;
}

