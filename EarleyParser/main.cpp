#include "mainwindow.h"
#include <QApplication>

#include <cstdlib>
#include <iostream>
#include <algorithm>

#include "earley.h"
using namespace std;
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
