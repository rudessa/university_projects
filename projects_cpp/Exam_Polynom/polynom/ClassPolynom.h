#include <iostream>
#include <math.h>
#include "../Rational/Rational.h"
using namespace std;

// Polynom
template <class T>
class Polynom {
private:
	unsigned int deg;
	T* koef;  
public:
	void CorrectDeg();        
	Polynom(); 
	Polynom(unsigned int new_deg); 
	Polynom(unsigned int, T* new_koef);  

	Polynom(const Polynom<T>& t);
	~Polynom();

	unsigned int GetDeg() const; 
	T GetKoef(unsigned int i) const; 
	void SetKoef(T new_koef, unsigned int i);
	void ReplaceKoef(T new_koef);
	Polynom operator + (const Polynom<T>& t) const;	 
	Polynom operator - (const Polynom<T>& t) const;
	Polynom operator = (const Polynom<T>& t);

	template <class T>
	friend Polynom MultConst(double, Polynom<T>&);   

	Polynom operator * (const T K) const;
	Polynom operator * (const Polynom<T>& t) const; 

	Polynom operator / (const Polynom<T>& t);
	Polynom operator % (const Polynom<T>& t);	  

	Polynom Divide( const Polynom<T>& divisor, Polynom<T>& quotient, Polynom<T>& remainder);        

	Polynom Derivative(int order);    

	Polynom Integrate();

	template <class T>
	friend istream& operator>>(istream& in, Polynom<T>& r);
	template <class T>
	friend ostream& operator<<(ostream& out, const Polynom<T>& r);
	void delete_koef();
};
int factorial(int number);

// конструктор без параметров: создается полином нулевой степени
// с коэффициентом при нулевой степени равным нулю      
template <class T>
Polynom<T>::Polynom() {
	deg = 0;
	koef = new T[deg + 1];    
	koef[0] = 0.0;
}

//Этот конструктор принимает только один параметр - new_deg (степень создаваемого полинома). 
// Он инициализирует степень полинома с заданным значением и создает массив коэффициентов, 
// устанавливая все коэффициенты в начальное значение равное нулю.
template <class T>
Polynom<T>::Polynom(unsigned int new_deg) {
	deg = new_deg;
	koef = new T[deg + 1];
	for (int i = 0; i <= deg; i++)
		koef[i] = 0;   
}

// конструктор с параметрами
// new_deg - степень создаваемого полинома
// newkoef - указатель на new_deg+1 - элементный массив с коэффициентами 
// 	 		 полинома, где newkoef[i] - коффициент при i-й степени
//			 и newkoef[0] - коэффициент при нулевой степени
// В результате степень полинома будет наибольшим номером ненулевого
// элемента массива new_koef и меньше или равна new_deg (по определению степени полинома)
template <class T>
Polynom<T>::Polynom(unsigned int new_deg, T* new_koef) {
	deg = 0;
	for (int i = 0; i <= new_deg; i++)
		if (new_koef[i] != 0) deg = i;	  
	koef = new T[deg + 1];
	for (int i = 0; i <= deg; i++)
		koef[i] = new_koef[i]; 
}

//копирующий конструктор
template <class T>
Polynom<T>::Polynom(const Polynom<T>& f) {
	deg = f.deg;
	koef = new T[deg + 1];
	for (int i = 0; i <= deg; i++)
		koef[i] = f.koef[i];
}

//деструктор
template <class T>
Polynom<T>::~Polynom() {
	delete[] koef;
}
  
// функция получения степени полинома
template <class T>
unsigned int Polynom<T>::GetDeg() const {
	return deg;
}

// функция получения коэффициента при i-й степени
template <class T>
T Polynom<T>::GetKoef(unsigned int i) const {
	if (i <= deg)
		return koef[i];
	else
		return 0.0;
}

// функция задания коэффициента при i-й степени
template <class T>
void Polynom<T>::SetKoef(T new_koef, unsigned int i) {
	if (i <= deg) koef[i] = new_koef;
	CorrectDeg();
}

//Замена koef
template <class T>
void Polynom<T>::ReplaceKoef(T new_koef) {
	koef = new_koef;
	CorrectDeg();
}

//оператор сложения двух полиномов
template <class T>
Polynom<T> Polynom<T>::operator + (const Polynom<T>& t) const {
	int i;
	Polynom<T>* result;

	if (deg >= t.deg) {	      
		result = new Polynom<T>(deg, koef);
		for (i = 0; i <= t.deg; i++)
			result->koef[i] = result->koef[i] + t.koef[i];
	}
	else {		  
		result = new Polynom<T>(t.deg, t.koef);
		for (i = 0; i <= deg; i++)
			result->koef[i] = result->koef[i] + koef[i];
	}
	result->CorrectDeg();
	return *result;
}

// Оператор вычитания двух полиномов
template <class T>
Polynom<T> Polynom<T>::operator - (const Polynom<T>& t) const {
	int i;
	Polynom<T> result;

	if (deg >= t.deg) {        
		result = Polynom<T>(deg);
		for (i = 0; i <= deg; i++)
			result.koef[i] = koef[i];
		for (i = 0; i <= t.deg; i++)
			result.koef[i] -= t.koef[i];
	}
	else {        
		result = Polynom<T>(t.deg);
		for (i = 0; i <= t.deg; i++)
			result.koef[i] = -t.koef[i];
		for (i = 0; i <= deg; i++)
			result.koef[i] += koef[i];
	}
	result.CorrectDeg();
	return result;
}

//оператор присваивания
template <class T>
Polynom<T> Polynom<T>::operator = (const Polynom<T>& t) {
	deg = t.deg;
	delete[] koef;
	koef = new T[deg + 1];
	for (int i = 0; i <= deg; i++)
		koef[i] = t.koef[i];
	return *this;
}

//оператор умножения полинома на число
template <class T>
Polynom<T> Polynom<T>::operator * (const T K) const {
	Polynom<T> res = *this;
	return MultConst(K, res);
}

//функция реализующая умножение полинома на число
template <class T>
Polynom<T> MultConst(double K, Polynom<T>& t) {
	if (K == 0) {
		Polynom<T> result;
		return result;
	}
	else {
		int deg = t.GetDeg();
		T* tmp_koef = new T[deg + 1];
		for (int i = 0; i <= deg; i++)
			tmp_koef[i] = K * t.GetKoef(i);
		Polynom<T> result(deg, tmp_koef);
		delete[] tmp_koef;
		return result;
	}
}

// Оператор умножения полинома на полином
template <class T>
Polynom<T> Polynom<T>::operator* (const Polynom<T>& t) const {
	Polynom<T> k = t;
	Polynom<T> g = *this;
	unsigned int new_deg = g.deg + k.deg;
	T* new_koef = new T[new_deg + 1]();

	for (unsigned int i = 0; i <= g.deg; i++) {
		for (unsigned int j = 0; j <= k.deg; j++) {
			new_koef[i + j] += g.koef[i] * k.koef[j];
		}
	}
	Polynom<T> result(new_deg, new_koef);
	delete[] new_koef;
	return result;
}


int factorial(int number) {
	int a = 1;
	for (int i = 1; i <= number; i++) {
		a *= i;
	}
	return a;
}

// Оператор деления двух полиномов с получением частного
template <class T>
Polynom<T> Polynom<T>::operator / (const Polynom<T>& divisor) {
	Polynom<T> quotient;
	Polynom<T> remainder;
	Divide(divisor, quotient, remainder);
	return quotient;
}

// Оператор деления двух полиномов с получением остатка 
template <class T>
Polynom<T> Polynom<T>::operator % (const Polynom<T>& divisor) {
	Polynom<T> quotient;
	Polynom<T> remainder;
	Divide(divisor, quotient, remainder);
	return remainder;
}

// Функция деления двух полиномов с получением частного и остатка отдельно
template <class T>
Polynom<T> Polynom<T>::Divide(const Polynom<T>& divisor, Polynom<T>& quotient, Polynom<T>& remainder) {
	if (divisor.deg == 0 && divisor.koef[0] != 0) {
		// Если делитель - константа (ненулевая)
		double constant = divisor.koef[0];
		quotient = *this / constant;
		remainder = Polynom<T>();
		return remainder;
	}

	unsigned int dividendDeg = deg;
	unsigned int divisorDeg = divisor.deg;

	if (dividendDeg < divisorDeg) {  
		// Если степень делимого меньше степени делителя, возвращаем ноль в частном и делимое в остатке
		quotient = Polynom<T>();
		remainder = *this;
		return remainder;
	}

	Polynom<T> tmp(*this);
	Polynom<T> div(divisor);

	quotient = Polynom<T>(dividendDeg - divisorDeg + 1);

	for (unsigned int i = dividendDeg - divisorDeg + 1; i > 0; i--) {
		quotient.koef[i - 1] = tmp.koef[tmp.deg] / div.koef[div.deg];
		unsigned int j = 0;
		for (; j <= div.deg; j++) {
			tmp.koef[tmp.deg - j] -= quotient.koef[i - 1] * div.koef[div.deg - j];
		}
		tmp.CorrectDeg();
	}

	remainder = tmp;
	return remainder;
}

//Производные
template <class T>
Polynom<T> Polynom<T>::Derivative(int order) {
	if (order <= 0) {
		return *this;
	}

	int resultDeg = deg - order;
	if (resultDeg < 0) {
		return Polynom<T>();
	}

	T* resultKoef = new T[resultDeg + 1];

	for (int i = 0; i <= resultDeg; i++) {
		resultKoef[i] = koef[i + order] * factorial(i + order) / factorial(i);
	}

	Polynom<T> result(resultDeg, resultKoef);

	delete[] resultKoef;

	return result;
}

//Интегрирование
template <class T>
Polynom<T> Polynom<T>::Integrate() {
	int resultDeg = deg + 1;
	T* resultKoef = new T[resultDeg + 1];

	resultKoef[0] = 0;  // Коэффициент при свободном члене всегда 0 после интегрирования

	for (int i = 1; i <= resultDeg; i++) {
		resultKoef[i] = koef[i - 1] / i;
	}

	Polynom<T> result(resultDeg, resultKoef);

	delete[] resultKoef;

	return result;
}

// функция корректировки степени полинома: коэффициент 
// при максимальной степени должен быть ненулевым
template <class T>
void Polynom<T>::CorrectDeg() {
	while (deg > 0 && koef[deg] == 0) {
		deg--;
	}
}


template <class T>
void Polynom<T>::delete_koef() {
	delete[] koef;
}

//оператор ввода полинома
template <class T>
istream& operator>>(istream& in, Polynom<T>& r) {
	cout << "Input degree: ";
	in >> r.GetDeg();
	r.delete_koef();
	T temp_k = new T[r.GetDeg() + 1];
	r.ReplaceKoef(T);

	cout << "Input coefficients from lowest to highest degree:" << endl;
	for (int i = 0; i <= r.GetDeg(); ++i) {
		cout << "Coefficient for x^" << i << ": ";
		in >> r.GetKoef(i);
	}
	r.CorrectDeg(); // Корректируем степень полинома
	return in;
}

//оператор вывода полинома
template <class T>
std::ostream& operator<<(ostream& out, const Polynom<T>& r) {
	if (r.GetDeg() == 0 && r.GetKoef(0) == 0) {
		out << "0";
		return out;
	}

	bool firstTerm = true;

	for (int i = r.GetDeg(); i >= 0; --i) {
		if (r.GetKoef(i) == 0) { continue; }

		if (!firstTerm) {
			if (r.GetKoef(i) > 0) { out << " + "; }
			else { out << " - "; }
		}
		else {
			if (r.GetKoef(i) < 0) { out << "-"; }
			firstTerm = false;
		}

		T absCoef = abs(r.GetKoef(i));

		if (i == 0) {
			out << absCoef;
		}
		else if (i == 1) {
			if (absCoef == 1) { out << "X"; }
			else { out << absCoef << "X"; }
		}
		else {
			if (absCoef == 1) { out << "X^" << i; }
			else { out << absCoef << "X^" << i; }
		}
	}

	return out;
}