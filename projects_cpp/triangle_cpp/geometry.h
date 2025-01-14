#pragma once
#include <iostream>
#include <cmath>
#ifndef _GEOMETRY_H
#define _GEOMETRY_H
using namespace std;
class Point {
public:
    double x, y;
    Point();
    Point(double _x, double _y);
};

class Triangle {
public:
    Point vertexes[3];
    double area;
};

// Расстояние между двумя точками по их координатам
double calcDistance(const Point& pa, const Point& pb);

// Площадь треугольника по координатам точек
double calcTriangleArea(Triangle& tr);

// Вспомогательная функция для вычисления площади
double calcAreaBySides(double a, double b, double c);

// Сравнение площадей треугольников
bool operator <=(const Triangle& tr1, const Triangle& tr2);

// Функции очистки
void clearPoint(Point& p);
void clearTriangle(Triangle& tr);

#endif
