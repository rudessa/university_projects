#include <iostream>
#include "Rational.h"
#include <math.h>
using namespace std;

//Конструкторы
Rational::Rational() {
	numer = 0;
	denom = 1;
}

Rational::Rational(int number) {
	numer = number;
	denom = 1;
}

Rational::Rational(int n, int d) {
	numer = n;
	denom = d;
}

//Операторы присваивания
Rational& Rational::operator =(const Rational& r) {
	numer = r.numer;
	denom = r.denom;
	return *this;
}

Rational& Rational::operator +=(const Rational& r) {
	numer = (numer * r.denom + denom * r.numer);
	denom *= r.denom;
	// this - указатель на себя
	// *this - ссылка на себя
	simplify(); // упрощение
	return *this;
}

Rational& Rational::operator -=(const Rational& r) {
	return (*this += (-r));
}

Rational& Rational:: operator *=(const Rational& r) {
	numer *= r.numer;
	denom *= r.denom;
	simplify();
	return *this;
}
Rational& Rational:: operator /=(const Rational& r) {
	Rational temp = r;
	temp.numer = r.denom;
	temp.denom = r.numer;
	return *this *= temp;
}

//Операторы сложения, вычитания, умножения, деления;
Rational Rational::operator -() const {
	Rational r(-numer, denom);
	return r;
}

Rational Rational:: operator -(const Rational& r) const {
	Rational temp = *this;
	return temp -= r;
}

Rational Rational:: operator *(const Rational& r) const {
	Rational temp = *this;
	return temp *= r;
}

Rational Rational:: operator /(const Rational& r) const {
	Rational temp = *this;
	return temp /= r;
}

Rational Rational::operator +(const Rational& r) const {
	// this - указатель на себя
	// *this - ссылка на себя
	Rational res(*this);
	// Используем готовую операцию добавления
	return res += r;
}

Rational& Rational::operator ++() {
	numer += denom;
	return *this;
}

Rational Rational::operator ++(int) {
	Rational r(*this);
	numer += denom;
	return r;
}

Rational& Rational::operator --() {
	numer -= denom;
	return *this;
}
Rational Rational::operator --(int) {
	Rational r(*this);
	numer -= denom;
	return r;
}

//Операторы сравнения
Rational Rational:: the_common_denominator(const Rational& r) {
	Rational temp = *this;
	temp.numer *= r.denom;
	temp.denom *= r.denom;
	return temp;
	
}

bool Rational::operator ==(const Rational& r) const {
	return (numer == r.numer) && (denom == r.denom);
}

bool Rational::operator !=(const Rational& r) const {
	return !(*this == r);
}

bool Rational:: operator <=(const Rational& r) const {
	Rational temp1= *this;
	Rational temp2 = r;
	temp1.the_common_denominator(r);
	temp2.the_common_denominator(*this);
	return temp1.numer <= temp2.numer;
}

bool Rational:: operator >=(const Rational& r) const {
	return (r <= *this);
}

bool  Rational::operator <(const Rational& r) const {
	return !(*this >= r);
}

bool Rational:: operator >(const Rational& r) const {
	return !(*this <= r);
}


Rational::operator int() const {
	return numer / denom;
}
Rational::operator double() const {
	return ((double)numer) / denom;
}

istream& operator >>(istream& in, Rational& r) {
	in >> r.numer >> r.denom;
	return in;
}
ostream& operator <<(ostream& out, const Rational& r) {
	out << r.numer << "/" << r.denom;
	return out;
}


//Функции степени и нахождения корня, квадратное уравнние, simplify;
Rational Rational::finding_the_pow( int x) {
	Rational temp = *this;
	for (int i = 0; i < x-1; i++) {
		temp *= *this;
	}
	return temp;
}

void Rational::simplify() {
	int temp_n = abs(numer);
	int temp_d = denom;
	while (temp_n != 0 && temp_d != 0) {
		if (temp_n > temp_d) { temp_n%=temp_d; }
		else { temp_d %= temp_n; }
	}
	int NOD = (temp_d == 0) ? temp_n : temp_d; // проверка на 0;
	numer /= abs(NOD);
	denom /= abs(NOD);
}


Rational finding_the_sqrt(Rational a) {
	const Rational epsilon(1, 10000);
	Rational x_n = a;
	while (true) {
		Rational x_n_next = Rational(1, 2) * (x_n + (Rational(a) / x_n));
		x_n_next = round(x_n_next);
		if (abs(x_n_next - x_n) < epsilon) {
			return x_n_next;
		}
		x_n = x_n_next;
	}
}

Rational abs(Rational x) {
	Rational temp(x);
	if (x.numer < 0) {
		temp.numer = -temp.numer;
		return temp;
	}
	return temp;
}
Rational round(Rational r) {
	int exp;
	double num = double(r);
	double mantissa = frexp(num, &exp);
	r.numer = int(mantissa * pow(2, 10));
	r.denom = pow(2, -(exp - 10));
	return r;
}