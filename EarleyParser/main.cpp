#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <fstream>
#include "earley.h"

using namespace std;
void open()
{
    ifstream file;
    file.open("gramatica.txt");
    string ss;
    file >> ss;
    cout << ss ;
}
int main() {
    string name="gramatica.txt";
    string cad="abc";
    //Gramatica gram(name);
    //Earley ear(gram,cad);
    open();
}
