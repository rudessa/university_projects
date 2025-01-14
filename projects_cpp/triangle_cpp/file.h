#pragma once
#include "../tringlee/geometry.h"
#include <iostream>
#ifndef _FILE_H
#define _FILE_H
using namespace std;

// Подсчет числа точек во входном файле
int countPoints(const char* fileName);

// Чтение точек из входного файла
bool readPoints(const char* fileName, Point* pointArray, int maxPointNum);

// Вывод треугольников в выходной файл
bool writeTriangles(const char* fileName, const Triangle* trArray, int trNum);

// операция ввода
istream& operator>>(istream& in, Point& p);

// операция вывода
ostream& operator<<(ostream& out, const Point& p);
ostream& operator<<(ostream& out, const Triangle& tr);

#endif#pragma once
