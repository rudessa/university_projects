#pragma once
#include <iostream>
#include "../tringlee/geometry.h"
#ifndef _SEARCH_H
#define _SEARCH_H
using namespace std;

// Вставка треугольника
void findAndInsert(Triangle* trArray, int length, const Triangle& triangle);

// Поиск треугольников максимальной площади
void searchLargestTriangles(const Point* pointArray, int pointNum, Triangle* trArray, int maxTrNum);

#endif#pragma once
