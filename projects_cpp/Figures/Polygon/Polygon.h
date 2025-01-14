#pragma once
#include "../figures.h"
#include <vector>
#include <string>
#include <fstream>
#ifndef POLYGON_H
#define POLYGON_H


template <class T>
class Polygon : public GeometricFigure {
private:
    vector<Point> vertices;
public:
    Polygon(vector<Point> _vertices);
    Polygon(vector<T> _vertices);

    double calc_area();

    double calc_perimeter();

    string name();
};

template <class T>
double Polygon<T>::calc_area() {
    T area = 0;
    int n = vertices.size();
    for (size_t i = 0; i < n; ++i) {
        area += (vertices[i].x * vertices[(i + 1) % n].y - vertices[(i + 1) % n].x * vertices[i].y);
    }
    return fabs(area) / 2;
}

template <class T>
double Polygon<T>::calc_perimeter() {
    T perimeter = 0;
    int n = vertices.size();
    for (size_t i = 0; i < n; ++i) {
        perimeter += distance(vertices[i], vertices[(i + 1) % n]);
    }
    return perimeter;
}

template <class T>
string Polygon<T>::name() {
    return "Polygon";
}

template <class T>
Polygon<T>::Polygon(vector<Point> _vertices) {
    vertices = _vertices;
}

template <class T>
Polygon<T>::Polygon(vector<T> _vertices) {
    if (_vertices.size() % 2 != 0) {
        throw "Not enought coordinates";
    }

    for (size_t i = 0; i < _vertices.size() - 1; i++) {
        vertices.push_back(Point(_vertices[i], _vertices[i + 1]));
    }
}
#endif