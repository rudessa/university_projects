#include<iostream>
#include <sstream>
#include"daretime.h"
using namespace std;

date::date() {
    year = 0, month = 0, day = 0, hour = 0, minute = 0, second = 0;
}

date::date(int day1, int month1, int year1) {
    year = year1;
    month = month1;
    day = day1;
    hour = 0;
    minute = 0;
    second = 0; 
}

date::date(int day1, int month1, int year1, int hour1, int minute1, int second1) {
    year = year1;
    month = month1;
    day = day1;
    hour = hour1;
    minute = minute1;
    second = second1;
}

//перегрузка операторов
istream& operator >>(std::istream& is, date& dt) {
    string input;
    is >> input;
    stringstream ss(input);
    ss >> dt.year;
    ss.ignore(1); // Пропускаем разделитель
    ss >> dt.month;
    ss.ignore(1); // Пропускаем разделитель
    ss >> dt.day;
    dt.hour = 0;
    dt.minute = 0;
    dt.second = 0;
    return is;
}
ostream& operator <<(ostream& out, const date& r) {
    out << r.day << "." << r.month << "." << r.year << " " << r.hour << ":" << r.minute << ":" << r.second;
    return out;
}

double date:: operator -(const date& r) const {
    double YD_first = YD();
    double YD_second = r.YD();
    double result = YD_first - YD_second;
    return abs(result);
}

date date::Grig_YD(double YD) const{
    //Добавляем 0.5 к исходному значению Юлианского дня, 
    // и положим Z равной целой части, 
    // а F — дробной части полученного числа.
    YD += 0.5;
    int A; int al; int B; int C; int D; int E;
    int Z = int(YD);
    double F = YD - Z;
    if (Z < 2299161) {
        A = Z;
    }
    else{
        al = int((Z - 1867216.25) / 36524.25);
        A = Z + 1 + al - int(al / 4);
    }
    B = A + 1524;

    C = int((B - 122.1) / 365.25);

    D = int(365.25 * C);

    E = int((B - D) / 30.6001);
    //День месяца (с десятичной дробной частью) равен:
    date Grig_date(0,0,0);
    Grig_date.day = B - D - int(30.6001 * E) + F;
    //Номер месяца есть:
    if (E < 14) {
        Grig_date.month= E - 1;
    }
    if (E == 14 or E == 15) {
        Grig_date.month = E - 13;
    }
    //Номер года есть:
    if (Grig_date.month > 2) {
        Grig_date.year = C - 4716;
    }
    if (Grig_date.month == 1 or Grig_date.month == 2) {
        Grig_date.year = E - 4715;
    }
    
    return Grig_date;
}



date date:: operator -(const int& r) const {
    double YD_date = YD();
    date Date;
    YD_date -= r;
    Date = Grig_YD(YD_date);
    return Date;
}

double date:: YD() const {
    date temp(*this);
    if (month == 1 || month == 2){
        temp.year = year - 1;
        temp.month = month + 12;
    }
    int A = int(temp.year / 100);
    int B = 2 - A + int(A / 4);
    double YD_mean = int(365.25 * (temp.year + 4716)) + int(30.6001 * (temp.month + 1)) + temp.day + B - 1524.5;
    return YD_mean;
}