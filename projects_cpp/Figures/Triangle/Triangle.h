#pragma once
#include "../figures.h"
#ifndef TRIANGLE_H
#define TRIANGLE_H

template <class T>
class Triangle : public GeometricFigure {
private:
    T side1, side2, side3;
    Point vertex1, vertex2, vertex3;
public:
    Triangle(T _side1, T _side2, T _side3);
    Triangle(Point _vertex1, Point _vertex2, Point _vertex3);

    double calc_area();

    double calc_perimeter();

    string name();

};

template <class T>
Triangle<T>::Triangle(Point _vertex1, Point _vertex2, Point _vertex3) {
    side1 = distance(_vertex1, _vertex2);
    side2 = distance(_vertex2, _vertex3);
    side3 = distance(_vertex3, _vertex1);
}

template <class T>
double Triangle<T>::calc_area(){
    double square = (side1 + side2 + side3) / 2;
    return sqrt(square * (square - side1) * (square - side2) * (square - side3));
}

template <class T>
double Triangle<T>::calc_perimeter() {
    return side1 + side2 + side3;
}

template <class T>
string Triangle<T>::name(){
    return "Triangle";
}

template <class T>
Triangle<T>::Triangle(T _side1, T _side2, T _side3) {
    side1 = _side1;
    side2 = _side2;
    side3 = _side3;
}

#endif