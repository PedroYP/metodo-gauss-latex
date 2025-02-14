import sys

codigo_completo_latex = ""

def imprimir_matriz_consola(matriz, n_columnas, es_ampliada):
    for fila in matriz:
        contador = 1
        for componente in fila:
            print("\t",componente, end="")
            if es_ampliada[0] and contador == n_columnas:
                print("\t|", end="")
            contador += 1
        print("\n")
    

def imprimir_transformacion_consola(OEM):
    contador = 1
    OEM_pulida = "\n--> "

    for char in OEM:
        if char == "\\":
            if contador % 2 == 0:
                OEM_pulida += " \n--> "
            else:
                OEM_pulida += ""
            contador+=1
        else:
            OEM_pulida += char

    print(OEM_pulida[:-4])


def Latex_recopilador(bloque_latex):
    global codigo_completo_latex
    codigo_completo_latex += bloque_latex


def Latex_intercambio(indice_fila_inicial, indice_fila_final):
    latex_intercambio_fila_x_fila =f"""
    \\[ 
	\\xrightarrow{{
        \\begin{{matrix}}
            f_{indice_fila_inicial} \\times f_{indice_fila_final}
        \\end{{matrix}}
    }}
    \\]"""

    Latex_recopilador(latex_intercambio_fila_x_fila)


def Operacion_fila(fila_fija, fila_iter, indice_columna, indice_fila, iter):
    pivote = fila_fija[indice_columna] #indice columna porque el vector ya lo tenemos "fila_fija", ahora la columna encuentra al componente
    a_cero = fila_iter[indice_columna]
    operacion_latex = ""

    if a_cero != 0:
        if pivote*a_cero>0:
            pivote = abs(pivote) # Mucho cuidado, esto solo se puede hacer aca porque el signo termina siendo
            a_cero = abs(a_cero) # importante cuando volvamos a la funcion Gauss, se hará producto y resta
            signo_operacion = '-'
        else:
            pivote = abs(pivote)
            a_cero = -abs(a_cero) # importante cuando volvamos a la funcion Gauss, se hará producto y resta
            signo_operacion = '+' # - x - = +
        if pivote != 1 and a_cero != 1:
            #MCD
            pivote_abs = abs(pivote)
            a_cero_abs = abs(a_cero)            
            while pivote_abs != a_cero_abs:
                if pivote_abs > a_cero_abs:
                    pivote_abs -= a_cero_abs
                else:
                    a_cero_abs -= pivote_abs
            pivote = int(pivote/pivote_abs)
            a_cero = int(a_cero/a_cero_abs)
            #OJO: indice_fila para imprimir sobre la flechita (latex)
            operacion_latex=f"{abs(pivote) if abs(pivote) != 1 else ""}f_{iter+1} {signo_operacion} {abs(a_cero)}f_{indice_fila+1} \\\\"
        elif pivote == a_cero:
            operacion_latex=f"f_{iter+1} {signo_operacion} f_{indice_fila+1} \\\\"
        elif pivote == 1:
            operacion_latex=f"f_{iter+1} {signo_operacion} {abs(a_cero) if abs(a_cero) != 1 else ""}f_{indice_fila+1} \\\\"
        else:
            operacion_latex=f"{abs(pivote)}f_{iter+1} {signo_operacion} f_{indice_fila+1} \\\\"
    return operacion_latex, pivote, a_cero

def Latex_operaciones(OEM_latex):
    if OEM_latex: #Solo si hay una operación que imprimir
        latex_transformacion =f"""
    \\[ 
	\\xrightarrow{{
        \\begin{{matrix}}
        {OEM_latex}
        \\end{{matrix}}
    }}
    \\]"""
        imprimir_transformacion_consola(OEM_latex) ###CONSOLA
    else:
        latex_transformacion=''
    Latex_recopilador(latex_transformacion)

def Buscar_pivote(matriz, indice_fila, indice_columna):
    vector_columna_auxiliar = [matriz[i][indice_columna] for i in range(len(matriz))] #Desde cero, para que los indices concuerden con los de la matriz original
    hay_pivote = False
    hubo_intercambio = False
    #indice_fila es clave, es el indice cero relativo 
    if 1 in vector_columna_auxiliar[indice_fila:]: #Importante, queremos saber si hay 1 pero desde la fila que ya venimos trabajando en adelante
        hay_pivote = True
        if vector_columna_auxiliar.index(1) == indice_fila:
            pass
        else:
            matriz[indice_fila], matriz[vector_columna_auxiliar[indice_fila:].index(1)+indice_fila] = matriz[vector_columna_auxiliar[indice_fila:].index(1)+indice_fila], matriz[indice_fila]
            hubo_intercambio = True
            Latex_intercambio(vector_columna_auxiliar.index(1)+1, indice_fila+1)
    elif vector_columna_auxiliar[indice_fila] != 0:  #Con tal que no sea cero no hay problema
        hay_pivote = True
    else:
        for i in range(indice_fila+1, len(vector_columna_auxiliar)):
            if vector_columna_auxiliar[i] != 0:
                matriz[indice_fila], matriz[i] = matriz[i], matriz[indice_fila] #Intercambiando Columnas -> se requiere latex
                hay_pivote = True
                print(f"\n--> f{indice_fila} x f{i}\n") ###CONSOLA INTERCAMBIO
                hubo_intercambio=True
                Latex_intercambio(indice_fila+1, i+1)
                break
    return hay_pivote, hubo_intercambio        

def Gauss(matriz, n_columnas, es_ampliada):
    indice_fila = 0
    indice_columna = 0
    while ((indice_fila<len(matriz)-1) and (indice_columna < n_columnas)):
        OEM_latex = ""
        hay_pivote, hubo_intercambio = Buscar_pivote(matriz, indice_fila, indice_columna)
        #Esto después de haber elegido el pivote correcto
        if hubo_intercambio:
            Latex_matriz(matriz, n_columnas, es_ampliada)
            imprimir_matriz_consola(matriz, n_columnas, es_ampliada)
        if hay_pivote:
            for j in range(indice_fila+1,len(matriz)):
                OEM_latex_iteracion, pivote, a_cero = Operacion_fila(matriz[indice_fila], matriz[j], indice_columna, indice_fila, j) #indice_columna indica el pivote
                OEM_latex+=OEM_latex_iteracion
                for k in range(len(matriz[j])):
                    if a_cero != 0:
                        matriz[j][k] = pivote*matriz[j][k] - matriz[indice_fila][k]*a_cero
            Latex_operaciones(OEM_latex)
            if a_cero != 0: #Para que no se imprima la misma matriz, y peor aún, sin "contexto" (flechita) al costado, pues, si a_cero, no pasa nada
                Latex_matriz(matriz, n_columnas, es_ampliada)
                imprimir_matriz_consola(matriz, n_columnas, es_ampliada)
            indice_fila+=1
            indice_columna+=1
        else:
            indice_columna+=1

def Latex_matriz(matriz, n_columnas, es_ampliada):
    columnas = "c"*n_columnas
    if es_ampliada[0]:
        columnas +=f"|{'c'*es_ampliada[1]}"
    componentes = ""
    for fila in matriz:
            componentes += "&".join(str(j) for j in fila) + "\\\\\n\t"
    latex_inicio = f"""
\\[
    \\left(\\begin{{array}}{{{columnas}}}

	"""
    latex_final = """
    \\end{array}\\right)
\\]"""
    Latex_recopilador(latex_inicio + componentes + latex_final)

#EMPIEZA EL main
matriz=[]

try:
    es_ampliada = [True] if input("¿Desea trabajar con una matriz ampliada? S/N: ") in ['s', 'S'] else [False]
    n_filas = int(input("Ingrese el número de filas: "))
    n_columnas = int(input("Ingrese el número de columnas: "))
    if es_ampliada[0]:
        n_columnas_ampliacion = int(input("Ingrese el número de columnas de la matriz ampliación (EL NÚMERO DE FILAS NECESARIAMENTE SERÁ EL MISMO): "))
    print("Ingrese los componentes de la matriz A "+str(n_filas)+"x"+str(n_columnas))

    for i in range(n_filas):
        filas_temporal = []
        for j in range(n_columnas):
            componente_input = input("Ingrese la componente pos " + str(i+1) + str(j+1) + ": ")
            if componente_input == "":
                componente_input = 0
                print(componente_input)
            filas_temporal.append(int(componente_input))
        matriz.append(filas_temporal)

    if es_ampliada[0]:
        print("Ingrese los componentes de la matriz B (ampliación) "+str(n_filas)+"x"+str(n_columnas_ampliacion))
        es_ampliada.append(n_columnas_ampliacion)

        for i in range(n_filas):
            for j in range(n_columnas_ampliacion):
                componente_input = input("Ingrese la componente pos " + str(i+1) + str(j+1) + ": ")
                if componente_input == "":
                    componente_input = 0
                    print(componente_input)
                matriz[i].append(int(componente_input))
except:
    print("Ha ingresado un valor no permitido. Fin del Programa")
    sys.exit(1)

print("-"*60)
print("\n\tLA MATRIZ INGRESADA ES:\n")
imprimir_matriz_consola(matriz, n_columnas, es_ampliada)
print("-"*60)


Latex_matriz(matriz, n_columnas, es_ampliada)

print("="*60)
print("\n\tESCALONANDO LA MATRIZ CON EL MÉTODO DE GAUSS\n")
print("="*60)


Gauss(matriz, n_columnas, es_ampliada)


#Toque final LaTeX

def Latex_suprimir_corchetes(codigo, pares_indices, max_op):
    contador = 0
    for i in range(-1,-len(pares_indices),-1):
        if contador != 2*max_op-1:
            codigo = codigo[:pares_indices[i][0]] + codigo[pares_indices[i][0]+3:pares_indices[i][1]-1] + codigo[pares_indices[i][1]+4:]
            contador+=1
        else:
            contador = 0
            continue
    return codigo

indices_corchetes = []

i_cierre=0
while True:
    i_cierre = codigo_completo_latex.find(r"\]", i_cierre+1)
    i_apertura = codigo_completo_latex.find(r"\[", i_cierre+1)

    if i_apertura == -1 or i_cierre == -1:
        #print(indices_corchetes)
        break

    indices_corchetes.append([i_cierre, i_apertura])

codigo_completo_latex=Latex_suprimir_corchetes(codigo_completo_latex, indices_corchetes, 1)

print("="*60)
print("\n\t    EL CÓDIGO EN LATEX ES EL SIGUIENTE:\n")
print("\t    Recuerde utilizar los paquetes \n\n\t\t \\usepackage{amsmath}\n\t\t \\usepackage{amssymb}\n")
print("="*60)

print(codigo_completo_latex)


import os

directorio_script = os.path.dirname(os.path.abspath(__file__))
ruta_txt = os.path.join(directorio_script, "eliminacion_gauss_latex.txt")

contador = 1
while os.path.exists(ruta_txt): #para que no sobreescriba
    ruta_txt = os.path.join(directorio_script, f"eliminacion_gauss_latex_{contador}.txt")
    contador += 1

with open(ruta_txt, "w") as archivo:
    # Escribe el contenido de la variable en el archivo
    archivo.write(codigo_completo_latex)