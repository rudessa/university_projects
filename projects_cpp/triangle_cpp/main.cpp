#include <iostream>
#include <locale.h>
#include "../tringlee/geometry.h"
#include "../tringlee/search.h"
#include "../tringlee/file.h"


using namespace std;

int main() {
    setlocale(LC_ALL, "Russian");

    char* inFileName = new char[256];
    char* outFileName = new char[256];

    cout << "Введите имя входного файла: ";
    cin.getline(inFileName, 256);
    cout << "Введите имя выходного файла: ";
    cin.getline(outFileName, 256);

    cout << "Запуск кода" << endl;

    int pointNum = countPoints(inFileName);
    if (pointNum < 0) {
        cout << "Входной файл не существует" << endl;
        return -2;
    }
    else if (pointNum < 4) {
        cout << "Входной файл слишком мал" << endl;
        return -3;
    }

    Point* pointArray = new Point[pointNum];

    if (!readPoints(inFileName, pointArray, pointNum)) {
        cout << "Ошибка при вводе точки" << endl;
        return -3;
    }

    const int maxTrNum = 3;
    Triangle trArray[maxTrNum];

    searchLargestTriangles(pointArray, pointNum, trArray, maxTrNum);
    if (!writeTriangles(outFileName, trArray, maxTrNum)) {
        cout << "Не получилось записать результат" << endl;
        return -4;
    }

    cout << "Программа успешно завершена" << endl;
    delete[] pointArray;
    delete[] inFileName;
    delete[] outFileName;
    return 0;
}
