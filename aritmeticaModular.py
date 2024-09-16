# (1) Operaciones basicas

def calcularMódulo(a: int,b: int) -> int: # a: Dividendo, b: Divisor
    quociente = a // b
    residuo = a - (b*quociente)
    return residuo

def sumaModular(a: int,b: int, c: int) -> int: # a: Primer número, b: Segundo número, c: Módulo
    return calcularMódulo(a+b,c)

def restaModular(a: int,b: int, c: int) -> int: # Funciona igual que la suma modular
    return calcularMódulo(a-b,c)

def multiplicaciónModular(a: int,b: int, c: int) -> int: # Funciona igual que la suma modular
    return calcularMódulo(a*b,c)

# (2) Inversa modular

def MCD(a: int,b: int) -> int: # Implementa el algoritmo de Euclides
    while b != 0: 
        a, b = b, calcularMódulo(a,b) 
    return a

def coprimos(a: int,b: int) -> bool: 
    if (MCD(a,b) == 1):
        return True
    
    return False

def inversoModular(a: int,b) -> int: # a: Número, b: Módulo
    if (coprimos(a,b)):
        for i in range(b):
            if (calcularMódulo(a*i,b) == 1):
                return i
            
    return None
