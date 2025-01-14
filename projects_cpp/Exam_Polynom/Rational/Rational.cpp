#include <iostream>
#include "Rational.h"
#include "../Round/Round.h"

using namespace std;
const int NEPS = 0.00000001;
Rational EPS(1, 2000);
const int EPSILON = 15;
const int ARR_SIZE = 100;
// constructors
Rational::Rational() {
  numer = 0;
  denom = 1;
}

Rational::Rational(int number) {
  numer = number;
  denom = 1;
}

Rational::Rational(double number) {
    int exp;
    double mant = std::frexp(number, &exp);
    if (exp - EPSILON < 0) {
        numer = static_cast<int>(mant * (1 << EPSILON));
        denom = 1 << -(exp - EPSILON);
    }
    else {
        numer = static_cast<int>(mant * (1 << EPSILON) * (1 << (exp - EPSILON)));
        denom = 1;
    }
  simplify();
}

Rational::Rational(int n, int d) {
  numer = n;
  denom = d;
}

// functions
void Rational::simplify() { // упрощаем дробь по алгоритму Евклида
  int num1 = abs(numer);
  int num2 = abs(denom);
  while (num1 != 0 && num2 != 0) {
    if (num1 >= num2) {
        num1 %= num2;
    } else {
        num2 %= num1;
    }
  }
  int nod = num1 + num2; // одно из чисел всегда 0, поэтому складывая находим НОД
  numer /= abs(nod);
  denom /= abs(nod);
}

Rational Rational::to_same_denom(const Rational& r) {
  if (numer > INT_MAX / r.denom or denom > INT_MAX / r.denom) {
    throw "Overflow";
  }
  numer *= r.denom;
  denom *= r.denom;

}

Rational Rational::rational_sqrt() {
    bool is_negative = false;
    Rational temp(*this);
    if (temp.numer < 0) {
        temp.numer = -temp.numer;
        is_negative = true;
    }
    Rational x = 1;
    Rational nx;
    Rational array[ARR_SIZE];
    int index = 0;
    for (int i = 0; i < 20; i++) {
        try {
            array[index++] = x;
            nx = (x + temp / x) / 2;
            if (abs(x - nx) < EPS) {
                break;
            }
            x = nx;
        }
        catch (const char* error) {
            x = chain_round(array[index-1]);
            array[index--] = Rational(0, 1);
        }
    }
    if (is_negative) {
        return -nx;
    } return nx;
}

Rational Rational::pow(int x) { // возвести дробь в целочисленную степень
  Rational res(*this);
  for (int i = 0; i < x - 1; i++) {
    res *= *this;
  }

  return res;
}


// =, +=, -=, *=, /=
Rational& Rational::operator =(const Rational& r) {
  numer = r.numer;
  denom = r.denom;

  return *this;
}
Rational& Rational::operator +=(const Rational& r) {
    unsigned long long int check = abs(long(numer)) * long(r.denom) + abs(long(r.numer)) * long(denom);
  if (numer > INT_MAX / r.denom or r.numer > INT_MAX / denom or denom > INT_MAX / r.denom or
      INT_MAX < check) {
    throw "Overflow";
  }
  numer = (numer * r.denom + r.numer * denom);
  denom *= r.denom;
  simplify();
  return *this;
}
Rational& Rational::operator -=(const Rational& r) {
  return (*this += (-r));
}
Rational& Rational::operator *=(const Rational& r) {
  if (numer > INT_MAX / abs(r.numer+NEPS) or denom > INT_MAX / r.denom) {
    throw "Overflow";
  }
  numer *= r.numer;
  denom *= r.denom;
  simplify();
  return *this;
}
Rational& Rational::operator /=(const Rational& r) {
  Rational res;

  res.denom = r.numer;
  res.numer = r.denom;

  return *this *= res;
}

Rational& Rational::operator +=(int number) {
  Rational res(number);

  return *this += res;
} 
Rational& Rational::operator -=(int number) {
  Rational res(number);

  return *this -= res;
} 
Rational& Rational::operator *=(int number) {
  Rational res(number);

  return *this *= res;
} 
Rational& Rational::operator /=(int number) {
  Rational res(number);

  return *this /= res;
} 

Rational& Rational::operator +=(double number) {
  Rational res(number);

  return *this += res;
} 
Rational& Rational::operator -=(double number) {
  Rational res(number);

  return *this -= res;
} 
Rational& Rational::operator *=(double number) {
  Rational res(number);

  return *this *= res;
} 
Rational& Rational::operator /=(double number) {
  Rational res(number);

  return *this /= res;
} 

// +, -, *, /
Rational Rational::operator +(const Rational& r) const {
  Rational res(*this);

  return res += r;
}
Rational Rational::operator -(const Rational& r) const {
  Rational res(*this);
  return (res += (-r));
}
Rational Rational::operator *(const Rational& r) const {
  Rational res(*this);

  return res *= r;
}
Rational Rational::operator /(const Rational& r) const {
  Rational res(*this);

  return res /= r;
}

Rational Rational::operator +(int number) const {
  Rational origin_rational(*this);
  Rational res(number);

  return origin_rational += res;
} 
Rational Rational::operator -(int number) const {
  Rational origin_rational(*this);
  Rational res(number);

  return origin_rational -= res;
} 
Rational Rational::operator *(int number) const {
  Rational origin_rational(*this);
  Rational res(number);

  return origin_rational *= res;
} 
Rational Rational::operator /(int number) const {
  Rational origin_rational(*this);
  Rational res(number);

  return origin_rational /= res;
} 

Rational Rational::operator +(double number) const {
  Rational origin_rational(*this);
  Rational res(number);

  return origin_rational += res;
} 
Rational Rational::operator -(double number) const {
  Rational origin_rational(*this);
  Rational res(number);

  return origin_rational -= res;
} 
Rational Rational::operator *(double number) const {
  Rational origin_rational(*this);
  Rational res(number);

  return origin_rational *= res;
} 
Rational Rational::operator /(double number) const {
  Rational origin_rational(*this);
  Rational res(number);

  return origin_rational /= res;
} 
Rational Rational::operator -() const {
  Rational r(-numer, denom);

  return r;
}

// ++, --
Rational Rational::operator ++() {
  numer += denom;
  return *this;
}
Rational Rational::operator --() {
  numer -= denom;

  return *this;
}
Rational Rational::operator ++(int) {
  Rational r(*this);

  numer += denom;

  return r;
}
Rational Rational::operator --(int) {
  Rational r(*this);

  numer -= denom;

  return r;
}

// ==, !=, <, >, <=, >=
bool Rational::operator ==(const Rational& r) const
{
  Rational res(*this);
  Rational res_1(r);

  res.to_same_denom(r);
  res_1.to_same_denom(*this);
  return res.numer == res_1.numer;
}
bool Rational::operator !=(const Rational& r) const
{
  return !(*this == r);
}
bool Rational::operator <(const Rational& r) const {
  return !(*this >= r);
}
bool Rational::operator >(const Rational& r) const {
  return !(*this <= r);
}
bool Rational::operator <=(const Rational& r) const {
  return (numer * r.denom <= r.numer * denom);
}
bool Rational::operator >=(const Rational& r) const {
  return (numer * r.denom >= r.numer * denom);
}

bool Rational::operator ==(int number) const {
  return (*this == Rational(number));
}
bool Rational::operator !=(int number) const {
  return (*this != Rational(number));
}
bool Rational::operator <(int number) const {
  return (*this < Rational(number));
}
bool Rational::operator >(int number) const {
  return (*this > Rational(number));
}
bool Rational::operator <=(int number) const {
  return (*this <= Rational(number));
}
bool Rational::operator >=(int number) const {
  return (*this >= Rational(number));
}

bool Rational::operator ==(double number) const {
  return (*this == Rational(number));
}
bool Rational::operator !=(double number) const {
  return (*this != Rational(number));
}
bool Rational::operator <(double number) const {
  return (*this < Rational(number));
}
bool Rational::operator >(double number) const {
  return (*this > Rational(number));
}
bool Rational::operator <=(double number) const {
  return (*this <= Rational(number));
}
bool Rational::operator >=(double number) const {
  return (*this >= Rational(number));
}



// int, double, abs
Rational::operator int() const {
  return numer / denom;
}
Rational::operator double() const {
  return ((double)numer) / denom;
}
Rational abs(Rational r) {
    Rational temp(r);
    temp.numer = abs(temp.numer);

    return temp;
}


// cin, cout
istream& operator >>(istream& in, Rational& r) {
  in >> r.numer >> r.denom;
  return in;
}
ostream& operator <<(ostream& out, const Rational& r) {
  if (r.numer % r.denom == 0) { // если наше число можно разделить, то выводим только целое число
    out << r.numer / r.denom;
  } else out << r.numer << "/" << r.denom;
  return out;
}