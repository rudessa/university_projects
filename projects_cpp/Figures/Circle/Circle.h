#pragma once
#include <iostream>
#include "../figures.h"

const double M_PI = 3.14;

#ifndef CIRCLE_H
#define  CIRCLE_H

template <class T>
class Circle : public GeometricFigure {
private:
    Point center;
    T radius;
public:
    Circle(Point _center, T _radius);
    Circle(T center_x, T center_y, T radius_);

    double calc_area();

    double calc_perimeter();

    string name();
};


template <class T>
double Circle<T>::calc_area() {
    return M_PI * radius * radius;
}

template <class T>
double Circle<T>::calc_perimeter() {
    return 2 * M_PI * radius;
}

template <class T>
string Circle<T>::name() {
    return "Circle";
}

template <class T>
Circle<T>::Circle(Point _center, T _radius) {
    center = _center;
    radius = _radius;
}

template <class T>
Circle<T>::Circle(T center_x, T center_y, T radius_) {
    center.y = center_y;
    center.x = center_x;
    radius = radius_;
}
#endif