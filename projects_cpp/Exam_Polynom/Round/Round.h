#include "../Rational/Rational.h"
#include <iostream>
#ifndef ROUND_H
#define ROUND_H
using namespace std;

Rational round(Rational r);
Rational chain_round(Rational r);
Rational constructFromContinuedFraction(Rational arr[], int size);

#endif