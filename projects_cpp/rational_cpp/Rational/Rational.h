#pragma once
#include <iostream>
using namespace std;
#ifndef _RATIONAL_H
#define _RATIONAL_H
class Rational {
	public:
	int denom, numer;
	Rational();
	Rational(int number);
	Rational(int n, int d);
	Rational& operator =(const Rational& r);
	Rational& operator +=(const Rational& r);
	void simplify();
	Rational operator +(const Rational& r) const;
	Rational operator -() const;
	Rational& operator -=(const Rational& r);
	Rational operator -(const Rational& r) const;
	Rational& operator *=(const Rational& r);
	Rational operator *(const Rational& r) const;
	Rational operator /(const Rational& r) const;
	Rational& operator /=(const Rational& r);

	Rational& operator ++(); // префикс
	Rational operator ++(int); // постфикс

	Rational& operator --(); // префикс
	Rational operator --(int); // постфикс

	/////Операторы сравнения
	bool operator ==(const Rational& r) const;
	bool operator !=(const Rational& r) const;
	bool operator <=(const Rational& r) const;
	bool operator >=(const Rational& r) const;
	bool operator <(const Rational& r) const;
	bool operator >(const Rational& r) const;
	Rational the_common_denominator(const Rational& r);

	//Функции степени и нахождения корня;
	Rational finding_the_pow(int x);

	operator int() const;
	operator double() const;

	friend istream& operator >>(istream& in, Rational& r);
	friend ostream& operator <<(ostream& out, const Rational& r);
};

Rational finding_the_sqrt(Rational a);
Rational abs(Rational x);
Rational round(Rational r);
#endif
