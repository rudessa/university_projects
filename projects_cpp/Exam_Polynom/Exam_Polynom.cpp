#include "polynom/ClassPolynom.h"
#include"iostream"
#include"math.h"
#include "Rational/Rational.h"
using namespace std;

int main() {
	setlocale(LC_ALL, "ru-RU");

	Rational koeff1[] = { Rational(1,4), Rational(2, 5), Rational(4,5)}; // Создаем полиномы 
	//Сложение двух многочленов
	cout << "Сложение двух многочленов: " << endl;
	Polynom<Rational> polyn(2, koeff1);
	Rational koeff2[] = { Rational(3,7), Rational(2,3)};
	Polynom<Rational> quan(1, koeff2);

	Polynom<Rational> result_add = polyn + quan;// Складываем полиномы P(x) и Q(x)
	cout << "Многочлен 1: " << polyn << endl << "Многочлен 2: " << quan << endl << "Многочлен 1 + Многочлен 2 = " << result_add << endl;

	Rational koeff3[] = { Rational(2, 4), Rational(3,6), Rational(5, 2) }; // Создаем еще один полином 
	Polynom< Rational> res(2, koeff3);

	result_add = polyn + res;// Складываем полиномы P(x) и R(x)
	cout << "Многочлен 1: " << polyn << endl << "Многочлен 2: " << res << endl << "Многочлен 1 + Многочлен 2 = " << result_add << endl << endl;


	//Вычитание двух многочленов
	cout << "Вычитание двух многочленов: " << endl;
	Rational koeffi1[] = { Rational(2,5), Rational(6,9), Rational(5,10)}; // Создаем полиномы 
	Polynom< Rational> poligonn(2, koeffi1);
	Rational koeffi2[] = { Rational(4,8), Rational(1,3), Rational(1,5) };
	Polynom<Rational> count(1, koeffi2);
	Polynom<Rational> result_subtrac = poligonn - count; // Вычитаем полиномы P(x) и Q(x)
	cout << "Многочлен 1: " << poligonn << endl << "Многочлен 2: " << count << endl << "Многочлен 1 - Многочлен 2 = " << result_subtrac << endl;

	Rational koef3[] = { Rational(3,5), Rational(6,9), Rational(5,10) }; // Создаем еще один полином
	Polynom<Rational> ress(2, koef3);
	result_subtrac = poligonn - ress;// Вычитаем полиномы P(x) и R(x)
	cout << "Многочлен 1: " << poligonn << endl << "Многочлен 2: " << ress << endl << "Многочлен 1 - Многочлен 2 = " << result_subtrac << endl << endl;

	//Умножение
	cout << "Умножение многочлена на многочлен: " << endl;
	Rational koef1[] = { Rational(3,5), Rational(4,9), Rational(6,10) }; // Создаем полиномы 
	Polynom<Rational> polinom(2, koef1);
	Rational koef2[] = { Rational(2,5), Rational(2,9), Rational(4,10) };
	Polynom<Rational> quantity(1, koef2);
	Polynom<Rational> result = polinom * quantity; // Умножаем полиномы P(x) и Q(x)
	cout << "Многочлен 1: " << polinom << endl << "Многочлен 2: " << quantity << endl << "Многочлен 1  * Многочлен 2 = " << result << endl << endl;


	//Деление
	cout << "Деление многочленов: " << endl;
	Polynom<Rational> p1(3, new Rational[4]{ Rational(1,5), Rational(6,9), Rational(5,10), Rational(2,5) });    
	Polynom<Rational> p2(2, new Rational[3]{ Rational(2,5), Rational(6,9), Rational(5,8) });       
	cout << "Многочлен 1: " << p1 << endl << "Многочлен 2: " << p2 << endl;

	Polynom<Rational> q = p1 / p2;                         // Частное от деления p1 на p2
	Polynom<Rational> r = p1 % p2;                         // Остаток от деления p1 на p2
	cout << "Частное от деления p1 на p2: " << q << endl << "Остаток от деления p1 на p2: " << r << endl;

	Polynom<Rational> q2, r2;
	p1.Divide(p2, q2, r2);                       // Частное и остаток от деления p1 на p2 отдельно
	cout << "Частное и остаток от деления p1 на p2 отдельно: " << "(" << q2 << ")" << "*" << "(" << p2 << ")" << "+" << "(" << r2 << ")" << endl << endl;


	//Производные
	cout << "Взятия производной произвольного порядка с получением нового объекта-многочлена: " << endl;
	Polynom<Rational> p(4, new Rational[5]{ Rational(2,3), Rational(2,9), Rational(7,10), Rational(2,5), Rational(6,9) });   
	cout << "Полином: " << p << endl;

	Polynom<Rational> derivative1 = p.Derivative(1);         
	Polynom<Rational> derivative2 = p.Derivative(2);        
	cout << "Производная первого порядка: " << derivative1 << endl << "Производная второго порядка: " << derivative2 << endl << endl;


	//Интегрирование
	cout << "Операцию интегрирования многочлена: " << endl;
	Polynom<Rational> p3(4, new Rational[5]{Rational(2, 3), Rational(1, 6), Rational(3, 5), Rational(7, 9), Rational(4, 5)});  
	Polynom<Rational> integral = p3.Integrate();          
	cout << "Многочлен: " << p3 << endl << "Интеграл: " << integral << endl << endl;

}