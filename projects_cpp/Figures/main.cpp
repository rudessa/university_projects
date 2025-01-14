#include<iostream>
#include <string>
#include <vector>
#include"figures.h"
#include "Triangle/triangle.h"
#include "Rectangle/rectangle.h"
#include "Polygon/polygon.h"
#include "Circle/circle.h"
#include "Ellipse/ellipse.h"

using namespace std;

int main() {
	//rect
	Point p1 = Point(0, 0);
	Point p2 = Point(3, 0);
	Point p3 = Point(3, 8);
	Point p4 = Point(0, 8);
	vector<int> pts = { 2, 4, 6, 8, 10, 12, 15, 17, 16, 12, 17, 10, 18, 3 };

	vector<GeometricFigure*> geo_fig;

	Triangle<int>* tri = new Triangle<int>(p1, p2, p3);
	geo_fig.push_back(tri);

	Rectangle<int>* rec = new Rectangle<int>(p1, p2, p3, p4);
	geo_fig.push_back(rec);

	Polygon<int>* pol = new Polygon<int>(pts);
	geo_fig.push_back(pol);

	Circle<int>* cir = new Circle<int>(p3, 9);
	geo_fig.push_back(cir);

	Ellipse<int>* ell = new Ellipse<int>(p2, 9, 4);
	geo_fig.push_back(ell);

	for (size_t i = 0; i < geo_fig.size(); i++) {
		cout << "Figure: " << geo_fig[i]->name() << " Area: " << geo_fig[i]->calc_area() << " Perimeter: " << geo_fig[i]->calc_perimeter() << endl;
	}






}
