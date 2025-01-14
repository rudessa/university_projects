#pragma once
#include <iostream>
using namespace std;
#ifndef _DATETIME_H
#define _DATETIME_H

class date {

public:
	int day, month, year, hour, minute, second;
	//конструкторы
	date();
	//параметры
	date(int day1, int month1, int year1);
	date(int day1, int month1, int year1, int hour1, int minute1, int second1);
	//перегрузка оператора
	friend istream& operator >>(istream& in, date& dt);
	friend ostream& operator <<(ostream& out, const date& r);
	double operator -(const date& r) const;
	double YD() const;
	date operator -(const int& r) const;

	date Grig_YD(double YD) const;

};
#endif