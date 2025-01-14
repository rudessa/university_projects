#pragma once
#include "../figures.h"

#ifndef RECTANGLE_H
#define RECTANGLE_H

template <class T>
class Rectangle : public GeometricFigure {
private:
    T side1, side2;
public:
    Rectangle(T _side1, T _side2);
    Rectangle(Point p1, Point p2, Point p3, Point p4);
    Rectangle(T p1x, T p1y, T p2x, T p2y, T p3x, T p3y, T p4x, T p4y);

    double calc_area();

    double calc_perimeter();

    string name();
};

template <class T>
Rectangle<T>::Rectangle(Point p1, Point p2, Point p3, Point p4) {
    side1 = distance(p1, p2);
    side2 = distance(p2, p3);
}

template <class T>
double Rectangle<T>::calc_area() {
    return side1 * side2;
}

template <class T>
double Rectangle<T>::calc_perimeter() {
    return 2 * (side1 + side2);
}

template <class T>
string Rectangle<T>::name() {
    return "Rectangle";
}

template <class T>
Rectangle<T>::Rectangle(T _side1 , T _side2) {
    side1 = _side1;
    side2 = _side2;
}

template <class T>
Rectangle<T>::Rectangle(T p1x, T p1y, T p2x, T p2y, T p3x, T p3y, T p4x, T p4y) {
    side1 = distance(Point(p1x, p1y), Point(p2x, p2y));
    side2 = distance(Point(p2x, p2y), Point(p3x, p3y));
}
#endif