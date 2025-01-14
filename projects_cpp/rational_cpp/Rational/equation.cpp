#include"Rational.h"
#include"equation.h"
#include<iostream>
using namespace std;

void equation(Rational a, Rational b, Rational c) {
	Rational D = b.finding_the_pow(2) - Rational(4) * a * c;
	if (D < Rational(0)) {
		throw("Действительных корней нет");
	}
	if (a == Rational(0)) {
		cout << "Вычисляем корни" << endl;
		Rational x = -c / b;
		cout << x << endl;
		return;
	}
	if (D == Rational(0)) {
		cout << "Вычисляем корни" << endl;
		Rational x = (-b + finding_the_sqrt(D) / (Rational(2) * a));
		cout << x << endl;
		return;
	}
	cout << "Вычисляем корни" << endl;
	Rational x1 = (-b + finding_the_sqrt(D)) / (Rational(2) * a);
	Rational x2 = (-b - finding_the_sqrt(D)) / (Rational(2) * a);
	cout << x1 << " " << x2 << endl;
}