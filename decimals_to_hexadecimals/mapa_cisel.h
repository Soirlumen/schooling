#ifndef MAPA_CISEL_H
#define MAPA_CISEL_H
#include <map>
#include <string>
#include <iostream>

std::map<int, std::string> sestnactkovaCisla;

void inicializujMapu() {
    for (int i = 0; i < 10; i++) {
        sestnactkovaCisla[i] = std::to_string(i);
    }
    for (int i = 10; i < 16; i++) {
        char hexChar = static_cast<char>('A' + (i - 10));
        sestnactkovaCisla[i] = std::string(1, hexChar);
    }
}

#endif // MAPA_CISEL_H
