#include <stack>
#include "mapa_cisel.h"
std::stack<int> zásobník;
std::string znaménko = "";

void převod(int číslo) {
    if (číslo < 0) {
        znaménko = "-";
        číslo *= -1;
    }
    int zbytek = 0;
    while (číslo != 0) {
        zbytek = číslo % 16;
        zásobník.push(zbytek);
        číslo = (číslo - zbytek)/16;
    }  
}
std::string složeníČísla() {
    std::string číslo = znaménko;
    while (!zásobník.empty()) {
        int index = zásobník.top();
        číslo = číslo + sestnactkovaCisla[index];
        zásobník.pop();
    }
    return číslo;
}
int main()
{
    inicializujMapu();
    převod(-453678);
    std::cout<< složeníČísla();
}
