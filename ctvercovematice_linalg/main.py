import numpy as np  # knihovna numpy na pomoc s maticemi
import sympy as sp  # sympy pro symbolické výpočty využita v třídě pro výpočet vlastních čísel
from scipy.linalg import null_space

# hlavní třída, která funguje pro zadávání matic a kontroluje zda uživatel zadává správné hodnoty
class rodicmatic:
    def __init__(self):
        self.rozmer = 0  # proměnná pro  rozměr matice
        self.matice = None  # proměnná pro samotnou matici

    # metoda pro nastavení rozměru matice
    def nastav_rozmer(self):
        while True:  # cyklus pro opakovaný vstup od uživatele
            try:
                # získáme rozměr matice od uživatele
                self.rozmer = int(input('zadejte prosím kladné celé číslo pro rozměr čtvercové matice: '))
                if self.rozmer > 0:  # 0věříme, že je rozměr kladný
                    break

                else:
                    print('rozměr musí být kladné celé číslo')
            except ValueError:  # zachytíme chybu, pokud vstup není celé číslo
                print('Rozměr musí být kladné celé číslo')

    # metoda pro sestavení matice
    def sestav_matici(self):
        # uděláme nulovou matici daného rozměru
        self.matice = np.zeros((self.rozmer, self.rozmer), dtype=np.float64)
        i = 0  # index řádku
        while i < self.rozmer:  # cyklus  pro každý řádek matice
            # získáme prvky řádku od uživatele
            prvky = input(f'zadejte {self.rozmer} hodnot pro řádek {i + 1}, oddělené mezerou: ').split()
            if len(prvky) != self.rozmer:  # Ověříme počet prvků v řádku
                print('špatný počet prvků, zkuste to znovu')
                continue

            try:
                # převedeme prvky na čisla a uložíme do matice
                self.matice[i] = [float(prvek) for prvek in prvky]
            except ValueError:  # zachytíme chybu, pokud prvek není číslo
                print('zadejte pouze čísla, zkuste to znovu')
                continue
            i += 1  # Přejdeme na další řádek

    # celé sestavení matice, použitá v dalších odvozených třídách v metodě run
    def udelejmatici(self):
        self.nastav_rozmer()  # nastavíme rozměr matice
        self.sestav_matici()  # sestavíme matici


# třída pro výpočet determinantu, dědí od třídy rodicmatic
class Determinant(rodicmatic):
    def __init__(self):
        super().__init__()  # voláme konstruktor rodičovské třídy (bude stejné i v dalších třídách)
        self.determinant = 1  # základní hodnota  determinantu

    # metoda pro výpočet determinantu
    def calculate(self):
        rozmer = len(self.matice)  # zjistíme rozměr matice

        # cyklus přes všechny řádky matice
        for i in range(rozmer):
            # najdeme index řádku s maximálním absolutním prvkem v i tém sloupci
            max_rad = i + np.argmax(np.abs(self.matice[i:, i]))
            # prohodíme itý a max_rad řádek
            self.matice[[i, max_rad]] = self.matice[[max_rad, i]]
            # pokud jsme prohodili řádky,změníme znamenko determinantu
            if i != max_rad:
                self.determinant *= -1
            # nastavíme pivotový prvek
            pivot = self.matice[i, i]
            # pokud je pivotový prvek nula, determinant je nula a vyjdeme z for
            if pivot == 0:
                self.determinant = 0
                return 0
            # vynásobíme hodnotu determinantu pivotovým prvkem
            self.determinant *= pivot
            # normalizujeme itý řádek
            self.matice[i] /= pivot
            # odčítáme násobky itého řádku od všech následujících řádků
            for j in range(i + 1, rozmer):
                factor = self.matice[j, i]
                self.matice[j] -= factor * self.matice[i]
        return self.determinant  # vrátíme hodnotu determinantu

    # metoda která spustí celý výpočet (podobná i v dalších odvozených třídách)
    def run(self):
        super().udelejmatici()
        self.calculate()
        print('determinant:')
        print(self.determinant)


# třída pro výpočet inverzní matice, dědí od třídy rodicmatic
class inverzni_matice(rodicmatic):
    def __init__(self):
        super().__init__()
        self.invmat = None

    # metoda pro výpočet inverzní matice
    def calculate(self):
        rozmer = len(self.matice)  # zjistíme rozměr matice
        jedmat = np.identity(rozmer)  # vytvoříme jednotkovou matici stejného rozměru
        rozmat = np.hstack([self.matice, jedmat])  # rozšíříme naší matici o jednotkovou

        # procházíme matici a upravujeme ji do horního stupnovitého tvaru
        for i in range(rozmer):
            max_rad = i + np.argmax(np.abs(rozmat[i:, i]))  # najdeme index řádku s maximálním absolutním prvkem
            rozmat[[i, max_rad], :] = rozmat[[max_rad, i], :]  # prohodíme řádky
            pivot = rozmat[i, i]  # nastavíme pivotový prvek
            if pivot == 0:  # pokud je pivotový prvek nula, není k ní inverzní a vyskakujeme ze smyčky
                print('matice není regularní a není k ní inverzní')
                return
            rozmat[i, :] /= pivot  # normalizujeme itý řádek

            # odčítáme násobky i tého řádku od všech následujících řádků
            for j in range(i + 1, rozmer):
                rozmat[j, :] -= rozmat[i, :] * rozmat[j, i]

        # procházíme matici zpět a upravujeme ji do redukovaného řádkového tvaru
        for i in range(rozmer - 1, 0, -1):
            for j in range(i):
                rozmat[j, :] -= rozmat[i, :] * rozmat[j, i]

        # uložíme inverzní matici
        self.invmat = rozmat[:, rozmer:]
        print('matice k ní inverzní:')  # vypíšeme výsledek
        print(self.invmat)  # vypíšeme výslednou inverzní matici

    def run(self):
        super().udelejmatici()
        self.calculate()


class vlastni_cisla(rodicmatic):
    def __init__(self):
        super().__init__()
        self.lambd = sp.Symbol('σ')  # definitivně lambda :D (pro samotný kód naprosto nepodstatný, jaký znak tam bude)

    # pomocná metoda pro výpočet determinantu matice pomocí rozvoje (jiný styl než který používám pro determinant)
    def det_rozvojem(self, matrix):
        if matrix.shape == (1, 1):  # základní případ: matice 1x1
            return matrix[0, 0]
        det = 0
        # cyklus přes sloupce matice
        for j in range(matrix.shape[1]):
            vedlejsi_matice = matrix.minorMatrix(0, j)  # vytvoření vedlejší matice
            kofak = (-1) ** (0 + j) * matrix[0, j]  # vypočtení kofaktoru
            det += kofak * self.det_rozvojem(vedlejsi_matice)  # přidání kofaktoru do determinantu
        return det

    # pomocná metoda pro vytvoření matice (A-lambda*I)
    def lammat(self):
        sym_matice = sp.Matrix(self.matice)  # převedení matice na sympy matici (kvůli lambdě)
        jednotkova_mat = sp.eye(self.rozmer)  # vytvoření jednot. matice
        lambmat = sym_matice - (self.lambd * jednotkova_mat)  # ýpočtení matice (A-lambda*I)
        return lambmat

    # hlavní metoda pro výpočet vlastních čísel !pozor, v mém programu chci pouze reálná vlasntí čísla
    def calculate(self):
        lambda_matice = self.lammat()  # získání matice  (A-lambda*I)
        lambda_det = self.det_rozvojem(lambda_matice)  # výpočet determinantu této matice
        vlastcis = sp.solve(lambda_det, self.lambd)  # řešení rovnice vzniklé z determinantu
        # filtrace pouze reálných vlastních čísel
        realvlastcis = list(filter(lambda cislo: sp.im(cislo) == 0, vlastcis))
        realvlastcis = [float(cislo) for cislo in realvlastcis]  # převedení na float
        return realvlastcis

    def run(self):
        self.udelejmatici()
        vlastni_cisla = self.calculate()
        print(f"Vlastní čísla matice jsou: {vlastni_cisla}")


################## samotný program
print("Vítejte v programu pro výpočet matematických operací s čtvercovými maticemi!")

# smyčka programu
while True:
    # menu s možnostmi, které program nabízí
    print("1: výpočet determinantu")
    print("2: výpočet inverzní matice")
    print("3: výpočet vlastních čísel")
    print("4: ukončit")

    # uživatel zadá možnost
    volba = input("zadejte číslo odpovídající vaší volbě: ")

    # dle volby spustí danou třídu s výpočtem
    if volba == "1":
        d = Determinant()
        d.run()
    elif volba == "2":
        i = inverzni_matice()
        i.run()

    elif volba == "3":
        v = vlastni_cisla()
        v.run()
    elif volba == "4":
        print("děkuji za použití programu")  # ukončení programu
        break
    else:
        print("Neplatná volba, zkuste to znovu.")  # když uživatel zadá něco jiného než v nabídce

    # dotaz, zda uživatel chce pokračovat s dalšími výpočty a případně ukončí
    pokracovat = input("chcete pokrčovat?(ano/ne): ").lower()
    if pokracovat != "ano":
        print("děkuji za použití programu. Nashledanou!")
        break


