import random


# Inicializa el tablero de tamaño fxc dependiendo de la dificultad elegida.
# @f: Cantidad de filas.
# @c: Cantidad de columnas.
def CrearTablero(f, c):
    matriz = []
    a = []
    for i in range(f):
        matriz.append([])
        for j in range(c):
            matriz[i].append(0)
    return matriz


# Llena el tablero de asteriscos indicando que es un tablero vacío.
# @filas: cantidad de filas.
# @columnas: cantidad de columnas.
def TableroVacío(filas, columnas):
    matriz = []
    for i in range(filas):
        matriz.append([])
        for j in range(columnas):
            matriz[i].append("*")

    return matriz


# Imprime una matriz. Esta función es llamada por DefinirTablero() y crea una maztriz de nxn
#que contiene las minas y una matriz nxn que contiene el tablero visible al jugador cuando juega.
# @matriz: Una matriz de tamaño nxn.
def Emitir(matriz):
    for i in range(len(matriz)):
        print(str(i).rjust(2), end=" ")
    print()
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 10:
                matriz[i][j] = 0
            print(str(matriz[i][j]).rjust(2), end=" ")
        print(i)

    print()


# Fija la cantidad de minas en el tablero dependiendo de la dificutad elegida.
# @tablero: El tablero creado de tamaño nxn.
# @minas: Cantidad de minas.
def Minas(tablero, minas):
    num_minas = 0
    fila = 0
    columna = 0
    while num_minas < minas:
        fila = random.randint(0, len(tablero) - 1)
        columna = random.randint(0, len(tablero) - 1)
        if tablero[fila][columna] != 9:
            tablero[fila][columna] = 9
            num_minas += 1
            CercaniaMinas(fila, columna, tablero)
    return (tablero)


# Establece la cercanía de las minas teniendo en cuenta los bordes del tablero.
# @fila: Una fila del tablero que va desde 0 hasta n.
# @columna: Una columna del tablero que va desde 0 hasta n.
def CercaniaMinas(fila, columna, tablero):
    for i in range(-1, 2):
        if fila + i >= 0 and fila + i <= len(tablero) - 1:
            for j in range(-1, 2):
                if columna + j >= 0 and columna + j <= len(tablero) - 1:
                    if tablero[fila + i][columna + j] != 9:
                        tablero[fila + i][columna + j] += 1


# Destapa la casilla elegida e informa si se ha perdido la partida al encontrar una mina
# @tablero_minado: Es el tablero descubierto e invisible para el jugador. Contiene todas las minas.
# @tablero_visible: El tablero visible para el jugador. Muestra la cantidad de minas en las cercanías sobre las casillas descubiertas.
# @fila: La fila elegida.
# @columna: La columna elegida.
def Destapar(tablero_minado, tablero_visible, fila, columna):
    if tablero_minado[fila][columna] == 9:
        print("Te has encontrado con una mina, ¡perdiste!")
        tablero_visible[fila][columna] = "BOOM"

    elif tablero_minado[fila][columna] == 0:
        tablero_minado[fila][columna] = 10
        for i in range(-1, 2):
            for j in range(-1, 2):
                if fila + i >= 0 and fila + i < (len(tablero_minado)):
                    if columna + j >= 0 and columna + j < (len(tablero_minado)):
                        Destapar(tablero_minado, tablero_visible, fila + i, columna + j)
    else:
        tablero_visible[fila][columna] = tablero_minado[fila][columna]
    return tablero_visible


# Devuelve la cantidad de casillas no descubiertas
# @tablero_visible: El tablero visible para el jugador. Muestra la cantidad de casillas sin descubrir.
def CantidadDeCeldasTapadas(tablero_visible):  # Nombre de función cambiado de "CeldasDestapdas" a "CantidadDeCeldasTapadas"
    n = 0
    for i in range(len(tablero_visible)):
        for j in range(len(tablero_visible[i])):
            if tablero_visible[i][j] == "*":
                n = n + 1

    return n


# Muestra la opción en pantalla para elegir la dificultad.
def MenuPrincipal():
    print("Bienvenido al Buscaminas.")
    dificultad = input("Elige un nivel de dificultad:\n1-Facil\n2-Intermedio\n3-Avanzado\n") # Esto es horrible. Funciona pero sin excepciones.
    nivel = int(dificultad)
    if nivel < 1 or nivel > 3:
        print("Nivel elegido no existe")
        MenuPrincipal()
    DefinirTablero(nivel)

# Función principal. Llama a las otras funciones para crear el tablero de acuerdo a la dificultad elegida.
# @nivel: Puede ser 1, 2 o 3.
def DefinirTablero(nivel):
    num_minas = 0
    if nivel == 1:
        tablero = CrearTablero(8, 8)
        tablero_visible = TableroVacío(8, 8)
        tablero_minado = Minas(tablero, 10)
        minas = 10
    elif nivel == 2:
        tablero = CrearTablero(16, 16)
        tablero_visible = TableroVacío(16, 16)
        tablero_minado = Minas(tablero, 40)
        minas = 40
    elif nivel == 3:
        tablero = CrearTablero(22, 22)
        tablero_visible = TableroVacío(22, 22)
        tablero_minado = Minas(tablero, 99)
        minas = 99

    Emitir(tablero_visible)

    fila_usuario = int(input("Ingrese el número de la fila que desea explorar: "))

    if fila_usuario > len(tablero_visible):
        fila_usuario = int(input("Debe ser menor, ingrese otra fila: "))

    columna_usuario = int(input("Ingrese el número de columna: "))  # Avisa que el número fila ingresada es inválida antes de pedir el número de columna.

    if columna_usuario > len(tablero_visible):
        columna_usuario = int(input("Debe ser menor, ingrese otra columna: "))

    tablero_visible = Destapar(tablero_minado, tablero_visible, fila_usuario, columna_usuario)
    Emitir(tablero_visible)

    n = CantidadDeCeldasTapadas(tablero_visible)
    while tablero_minado[fila_usuario][columna_usuario] != 9 and n > minas:
        fila_usuario = int(input("Ingrese el número de la fila que desea explorar: "))
        columna_usuario = int(input("Ingrese el número de columna: "))
        if fila_usuario > len(tablero_visible):
            fila_usuario = int(input("Debe ser menor, ingrese otra fila: "))
        if columna_usuario > len(tablero_visible):
            columna_usuario = int(input("Debe ser menor, ingrese otra columna: "))
        tablero_visible = Destapar(tablero_minado, tablero_visible, fila_usuario, columna_usuario)
        Emitir(tablero_visible)
        n = CantidadDeCeldasTapadas(tablero_visible)

    if n == minas and tablero_minado[fila_usuario][columna_usuario] != 9:
        print("Has ganado, ¡Felicitaciones!")
    else:
        reintentar = input("Quieres jugar otra vez? S/N ")
        reintentar = reintentar.upper()
        if reintentar == "S" or reintentar == "SI":
            MenuPrincipal()
        else:
            print("Gracias por jugar")


MenuPrincipal()

