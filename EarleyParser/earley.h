
#ifndef EARLEY_H
#define EARLEY_H

#include <string>
#include <vector>
#include <map>
#include "gramatica.h"
#include "registro.h"

using namespace std;

class Earley {
public:
    Earley(const Gramatica& g, const string& cad);
    bool parse();
private:
    Gramatica grammar;
    string cadena;
    vector<vector<Registro> > registros;
    map<char,bool> check_var;
    int j;

    void initialization();
    void clausure();
    bool advance();
    void termination();

    void comprobar() const;
};

#endif /* EARLEY_H */
