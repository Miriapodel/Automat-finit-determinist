# Pentru a semnala ca o stare este initiala, in fisierul de configurare va fi trecuta in stilul q0, s
# Acelasi lucru pentru starile finale, doar ca f in loc de s
# In actions, tranzitiile sunt de genul: stare_inceput, input, stare_viitoare

def citire_fisier(nume_fisier):
    # Adaug toate datele din fisier intr-o variabila

    fisier = []
    try:
        with open(nume_fisier) as f:
            for linie in f:
                fisier.append(linie)

        return fisier

    # Tratez cazul in care fisierul nu exista si trimit o eroare

    except:
        print("Fisierul nu exista")
        return None


def citire_secventa():
    with open("secventa.in") as f:
        return f.readline() # returneaza sirul de caractere primit ca input


def file_parser(fisier):
    structura_fisier = {} # dictionarul in care va fi retinut structura fisierului
    sectiune_curenta = ''

    for linie in fisier:
        if linie[0] == '[' and linie[-2] == ']':  # Verific daca linia curenta anunta inceputul unei noi sectiuni

            # Populez dictionarul in stilul structurii fisierului. Fiecare sectiune este o cheie ale carei valori sunt
            # datele care se afla in sectunea respectiva

            nume_sectiune = linie.rstrip('\n').strip(']').lstrip('[') # scap de caracterele nefolositoare si pastrez doar numele secitunii
            sectiune_curenta = nume_sectiune
            if nume_sectiune not in structura_fisier:
                if nume_sectiune == 'Actions': # in cazul in care sectiunea curenta este actions datele vor fi pastrate intr un dictionar pentru a le folosi si verifica mai usor
                    structura_fisier[nume_sectiune] = {}
                else:
                    structura_fisier[nume_sectiune] = []
        else:
            if linie[0] != '#' and sectiune_curenta != '':  # Verific daca linia curenta este un comentariu, iar in caz afirmativ o ignor
                data = linie.rstrip('\n')

                if sectiune_curenta == 'Actions':
                    sec_actions.append(data) # adaug datele in lista sec_actions pentru a le verifica corectitudinea ulterior
                    data = data.split(", ") # impart datele primite in parti componente

                    if data[0] not in structura_fisier[sectiune_curenta]: # verific daca starea de la care se pleaca a fost introdusa pana acum in dictionar
                        structura_fisier[sectiune_curenta][data[0]] = {}
                    if data[1] not in structura_fisier[sectiune_curenta][data[0]]: # verific daca semnalul care schimba starea a fost introdus in dictionar
                        structura_fisier[sectiune_curenta][data[0]][data[1]] = {}
                        structura_fisier[sectiune_curenta][data[0]][data[1]] = data[2] # adaug starea destinatie in dictionar

                else:
                    structura_fisier[sectiune_curenta].append(data)

    return structura_fisier


def verificare_corectitudine_sigma(structura):
    if 'Sigma' not in structura:
        print("Nu exista alfabetul")
        return False

    elif len(structura['Sigma']) == 0:
        print("Sectiunea Sigma este goala")
        return False

    else:

        if sorted(structura['Sigma']) != sorted(list(set(structura['Sigma']))): # verific daca elementele dictionarului sunt unice
            print("Alfabetul nu are elemente unice")
            return False

    return True


def verificare_corectitudine_States(structura):
    if 'States' not in structura:
        print("Nu exista States")
        return False

    elif len(structura['States']) == 0:
        print("Sectiunea States este goala")
        return False

    else:

        # Verific daca exista o stare initiala si cel putin o stare finala

        exista_stare_finala = False
        exista_stare_initiala = False

        for element in structura['States']:
            componente = element.split(", ") # impart sirul pe componente in cazul in care pe langa stare mai este si un caracter care ne zice tipul ei
            numar_componente = len(componente) # salvez numarul de componente intr-o variabila
            if numar_componente == 2: # cazul in care o stare poate fi doar de inceput sau doar finala
                if componente[1] == 's':
                    if exista_stare_initiala is True:
                        print("Exista mai multe stari initiale")
                        return False
                    else:
                        exista_stare_initiala = True
                else:
                    if componente[1] == 'f':
                        exista_stare_finala = True
            elif numar_componente == 3: # cazul in care o stare poate fi si de inceput si finala
                if componente[1] == 's':
                    if exista_stare_initiala is True:
                        print("Exista mai multe stari initiale")
                        return False
                    else:
                        exista_stare_initiala = True
                if componente[1] == 'f':
                    exista_stare_finala = True

        if exista_stare_finala is not True or exista_stare_initiala is not True:
            print("Nu exista stari initiale sau finale")
            return False

    return True


def verificare_corectitudine_Actions(structura):
    if 'Actions' not in structura:
        print("Nu exista sectiunea Actions")
        return False

    elif len(structura['Actions']) == 0:
        print("Sectiunea Actions este goala")
        return False

    # Verific daca datele din actions sunt corecte, mai exact daca cele trei elemente trimise pe cate o linie apartin sectiunii
    # States ( primul element si al treilea ) si sectiunii Sigma ( elementul din mijloc )

    states = [x[0:2] for x in
              structura['States']]  # Salvez doar starile intr-o variabila separata pentru a fi mai usor de accesat
    actions = {}

    for action in sec_actions:
        componente = action.split(", ")

        if len(componente) != 3:
            print("Datele din Actions nu sunt complete") # verific daca o linie din sectiunea actions contine doua stari si un semnal care face o stare sa treaca in cealalta
            return False

        if componente[0] not in states or componente[2] not in states or componente[1] not in structura['Sigma']: # verific daca primele doua elemente apartin multimii de stari si daca cea din mijloc apartine limbajului
            print("Datele din Actions nu sunt corecte")
            return False

        # Fiecare prima componenta este o stare pe care o salvez in dictionar ca si cheie. Apoi, celelalte doua componente ( un element din sigma
        # si o alta stare ) sunt slavate ca si chei din dictionarul asociat primei componente. Fac acest lucru pentru a verifica usor
        # daca o stare este dusa in mod unic intr-o alta stare si daca un semnal duce starea curenta intr-o singura stare

        if componente[0] not in actions:
            actions[componente[0]] = {}
            actions[componente[0]][componente[1]] = {}
            actions[componente[0]][componente[2]] = {}
        else:
            if componente[1] not in actions[componente[0]]:
                actions[componente[0]][componente[1]] = {}
            else:
                print("Datele din Actions nu sunt corecte")
                return False

            if componente[2] not in actions[componente[0]]:
                actions[componente[0]][componente[2]] = {}
            else:
                print("Datele din Actions nu sunt corecte")
                return False

    return True


def verificare_corectitudine_fisier(structura):
    corect_Sigma = verificare_corectitudine_sigma(structura)

    if corect_Sigma is False:
        return False

    corect_States = verificare_corectitudine_States(structura)

    if corect_States is False:
        return False

    corect_Actions = verificare_corectitudine_Actions(structura)

    if corect_Actions is False:
        return False

    return True


def determinare_stari_initiala_finala(dfa):
    stare_initiala = 0
    stari_finale = []

    for stare in dfa['States']:
        componente = stare.split(", ") # impart sirul in componente in caz ca este format din mai multe, de exemplu starea si un caracter care determina daca este stare finala sau de inceput
        numar_componente = len(componente)

        if numar_componente > 1: # in cazul in care starea este urmata de un caracter care ne zice tipul ei
            if componente[1] == 's':
                stare_initiala = componente[0]
                if numar_componente == 3:  # verific daca starea esti si finala si de inceput
                    if componente[2] == 'f':
                        stari_finale.append(componente[0])
            elif componente[1] == 'f':
                stari_finale.append(componente[0])

    return stare_initiala, stari_finale


def emulate_dfa(dfa, sir, stare_inceput, stari_finale):
    stare_curenta = stare_inceput

    for c in sir:
        if c not in dfa['Sigma']: # verific daca caracterele din sirul primit ca input apartin limbajului
            return False
        if c not in dfa['Actions'][stare_curenta]: # verific daca caracterul duce starea curenta intr-o alta stare
            return False
        stare_curenta = dfa['Actions'][stare_curenta][c]

    if stare_curenta in stari_finale: # verific daca starea in care am ajuns la final se afla in multimea starilor finale
        return True
    else:
        return False


def start_app():
    nume_fisier = "date.in"
    date_fisier = citire_fisier(nume_fisier)

    if date_fisier is not None:
        structura_fisier = file_parser(date_fisier)  # structurez datele primite intr-un dictionar care pastreaza structura fisierului de configurare

        if structura_fisier is False:
            print("Structura fisierului de configurare nu este corecta")
            return

        if verificare_corectitudine_fisier(structura_fisier) is True:

            stare_init, stari_fin = determinare_stari_initiala_finala(structura_fisier)

            secventa = citire_secventa()  # citesc input-ul

            print(emulate_dfa(structura_fisier, secventa, stare_init,
                              stari_fin))  # afiseaza true daca automatul accepta string-ul sau false in contrar


sec_actions = []  # variabila folosita pentru a stoca datele din sectiuna actions neprocesate, pentru a putea fi verificata mai usor

start_app()
