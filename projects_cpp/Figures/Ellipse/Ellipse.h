#pragma once
#include "../figures.h"
const double pipi = 3.141592;

#ifndef ELLIPSE_H
#define ELLIPSE_H

template <class T>
class Ellipse : public GeometricFigure {
private:
    Point center;
    T radius1;
    T radius2;
public:
    Ellipse(Point _center, T _radius1, T _radius2);
    Ellipse(T center_x, T center_y, T _radius1, T _radius2);

    double calc_area();

    double calc_perimeter();

    string name();
};


template <class T>
double Ellipse<T>::calc_area() {
    return pipi * radius1 * radius2;
}

template <class T>
double Ellipse<T>::calc_perimeter() {
    return 2 * pipi * sqrt((radius1 * radius2 + radius1 * radius2) / 2);
}

template <class T>
string Ellipse<T>::name() {
    return "Ellipse";
}

template <class T>
Ellipse<T>::Ellipse(Point _center, T _radius1, T _radius2) {
    center = _center;
    radius1 = _radius1;
    radius2 = _radius2;
}

template <class T>
Ellipse<T>::Ellipse(T center_x, T center_y, T _radius1, T _radius2) {
    center.y = center_y;
    center.x = center_x;
    radius1 = _radius1;
    radius2 = _radius2;
}

#endif