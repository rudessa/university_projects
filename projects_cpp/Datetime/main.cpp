#include<iostream>
#include"daretime.h"
using namespace std;


int main() {
	setlocale(LC_ALL, "ru-RU");
	date empty();//пустой конструктор
	date fill(23, 11, 2005);// заполненный конструктор
	date fill_1(23, 11, 2005, 4, 15, 3);
	date dates;
	//cin >> dates; //yyyy - MM - dd
	//cout << dates;
	date date_1 (28, 3, 2024);
	date date_2(23, 11, 2005);

	double result = date_2 - date_1;
	cout << result << endl;
	

	date result_date = fill -  256;
	cout << result_date<< endl;

	
}