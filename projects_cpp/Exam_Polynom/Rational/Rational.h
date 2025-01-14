#pragma once
#include <iostream>

#ifndef _RATIONAL_H
#define _RATIONAL_H
using namespace std;

class Rational {
  void simplify();
  Rational to_same_denom(const Rational& r);
public:
  int numer, denom;

  Rational();

  Rational(int number);

  Rational(double number);

  Rational(int n, int d);

  Rational rational_sqrt();
  Rational pow(int x);

  Rational& operator =(const Rational& r);
  Rational& operator +=(const Rational& r);
  Rational& operator -=(const Rational& r); 
  Rational& operator *=(const Rational& r);
  Rational& operator /=(const Rational& r);
  Rational& operator +=(int number); 
  Rational& operator -=(int number); 
  Rational& operator *=(int number);  
  Rational& operator /=(int number); 
  Rational& operator +=(double number); 
  Rational& operator -=(double number); 
  Rational& operator *=(double number);  
  Rational& operator /=(double number);  

  Rational operator +(const Rational& r) const;
  Rational operator -(const Rational& r) const;
  Rational operator *(const Rational& r) const;
  Rational operator /(const Rational& r) const;
  Rational operator +(int number) const; 
  Rational operator -(int number) const; 
  Rational operator *(int number) const;  
  Rational operator /(int number) const; 
  Rational operator +(double number) const; 
  Rational operator -(double number) const; 
  Rational operator *(double number) const;  
  Rational operator /(double number) const; 
  Rational operator -() const;

  Rational operator ++();
  Rational operator --();
  Rational operator ++(int);
  Rational operator --(int);

  bool operator ==(const Rational& r) const;
  bool operator !=(const Rational& r) const;
  bool operator <(const Rational& r) const;
  bool operator >(const Rational& r) const;
  bool operator <=(const Rational& r) const;
  bool operator >=(const Rational& r) const;
  bool operator ==(int number) const;
  bool operator !=(int number) const;
  bool operator <(int number) const;
  bool operator >(int number) const;
  bool operator <=(int number) const;
  bool operator >=(int number) const;
  bool operator ==(double number) const;
  bool operator !=(double number) const;
  bool operator <(double number) const;
  bool operator >(double number) const;
  bool operator <=(double number) const;
  bool operator >=(double number) const;


  operator int() const;
  operator double() const;

  friend istream& operator >>(istream& in, Rational& r);
  friend ostream& operator <<(ostream& out, const Rational& r);

};

Rational abs(Rational r);


#endif