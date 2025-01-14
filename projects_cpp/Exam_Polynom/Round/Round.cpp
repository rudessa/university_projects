#include "Round.h"
#include "../Rational/Rational.h"
#include <iostream>
using namespace std;

Rational EPSILONN(1, 5000);
const int MAX_SIZE = 100;

Rational round(Rational r) {
    double num = double(r);
    num = int(num * 100 + 0.5) / 100.0;
    Rational temp(num);

    return temp;
}

Rational constructFromContinuedFraction(Rational arr[], int size) {
    Rational result;
    if (size == 1) {
        result = arr[0];
    }
    else {
        for (int i = size - 2; i >= 0; --i) {
            if (i == size - 2) {
                result = arr[i];
            }
            else {
                result = arr[i] + Rational(1) / result;
            }
        }
    }
    return Rational(1) / result;
}
Rational chain_round(Rational r) {
    if (r.numer % r.denom == 0) {
        return r;
    }
    Rational next, int_part, fractional_part, result;
    Rational continuedFractional[MAX_SIZE];
    int size = 0;
    try {
        int_part = Rational(int(r));
        fractional_part = r - int_part;

        while (abs(fractional_part) > EPSILONN and fractional_part != 0) {
            fractional_part = Rational(1) / fractional_part;
            next = Rational(int(fractional_part));
            fractional_part -= next;
            if (size >= MAX_SIZE) {
                throw overflow_error("Превышен размер массива");
            }
            continuedFractional[size++] = next;

            if (fractional_part.numer == 0) {
                break;
            }
        }

        if (size != 0) {
            result = constructFromContinuedFraction(continuedFractional, size);
            return result + int_part;
        } else {
            return int_part;
        }

    }
    catch (const char* ex) {
        cerr << ex;
    }
}
