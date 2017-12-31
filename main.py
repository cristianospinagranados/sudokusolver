import numpy as np

# Matriz del sudoku recien leido
# Los ceros significan celdas vacias
sudoku = np.matrix('0 0 4 7 5 2 0 0 0; 0 0 0 0 0 0 0 0 6; 0 0 0 0 0 0 0 3 0; 4 7 0 0 0 0 3 0 0; 0 0 5 0 3 0 6 0 0; 0 1 0 0 0 4 0 9 0; 9 0 0 0 0 0 0 5 0; 0 0 0 2 1 0 0 0 9; 0 0 7 9 0 5 0 8 0')

# Matriz de booleanos de igual dimension del sudoku para validar 
# las casillas que ya se hayan leido, inicialmente todos estan en false
leido = np.zeros((9, 9), dtype=bool)

# Diccionario con los arrays de numeros faltantes de las casillas sin llenar
faltantes = {}

# Stack con indices de casillas y el numero a borrar de entre sus posibles
# por ejemplo 429 significa que para la casilla 4,2 el 9 ya no es solucion
descartar = []

#Verifica en un conjunto de datos si hay alguna respuesta por descarte
def aux_profunda(a,b,x,d,e,f,g,h,i,tipo,z):
    total = {'1':[],'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[],'9':[]}
    for c in faltantes:
        if tipo == 'recuadro':
            if c==a or c==b or c==x or c==d or c==e or c==f or c==g or c==h or c==i:
                for y in faltantes[c]:
                        total[str(y)].append(c)
        elif tipo == 'columna':
            if c.endswith(str(z)): 
                for y in faltantes[c]:
                    total[str(y)].append(c)
        else:
            if c.startswith(str(z)):
                for y in faltantes[c]:
                    total[str(y)].append(c)
    for numero in total:
            if len(total[numero])== 1:
                if sudoku[int(total[numero][0][0]),int(total[numero][0][1])] == 0:
                    leido[int(total[numero][0][0]),int(total[numero][0][1])] = True
                    sudoku[int(total[numero][0][0]),int(total[numero][0][1])] = numero
                    del faltantes[str(total[numero][0][0])+str(total[numero][0][1])];
                    llenar_stack(int(total[numero][0][0]),int(total[numero][0][1]),numero)
    total.clear()
    descartar_stack()
# Cuando existe una fila, columna, o recuadro menor en el que solo una casilla
# Pueda tomar un valor, es decir, esa casilla debe tener ese valor
# pero que no lo toma porque tiene otros posibles y se estanca
def busqueda_profunda():
    #Recorrer las columnas
    for x in range(0,9):  
        aux_profunda('','','','','','','','','','columna',x)
    
    #Recorrer las filas
    for x in range(0,9):
        aux_profunda('','','','','','','','','','fila',x)
        
    #En cada recuadro verifica si hay soluciones por descarte
    aux_profunda('00','01','02','10','11','12','20','21','22','recuadro',0)
    aux_profunda('03','04','05','13','14','15','23','24','25','recuadro',0)
    aux_profunda('06','07','08','16','17','18','26','27','28','recuadro',0)
    aux_profunda('30','31','32','40','41','42','50','51','52','recuadro',0)
    aux_profunda('33','34','35','43','44','45','53','54','55','recuadro',0)
    aux_profunda('36','37','38','46','47','48','56','57','58','recuadro',0)
    aux_profunda('60','61','62','70','71','72','80','81','82','recuadro',0)
    aux_profunda('63','64','65','73','74','75','83','84','85','recuadro',0)
    aux_profunda('66','67','68','76','77','78','86','87','88','recuadro',0)
    
# Dado un indice de la matriz de sudoku
# Llena una pila de los elementos que
# dicho indice puede afectar, es decir, la fila, la columna
# y el cuadrado menor al que pertenece
# El tercer parametro se refiere al valor que se 
# descartara en los elementos afectados
def llenar_stack(i,j,n):
    #recorrido de la fila
    for x in range(1,9): # itera 8 veces, no importa el x
        if sudoku[i,(j+x)%9] > 0:
            if leido[i,(j+x)%9] == False:
                leido[i,(j+x)%9] = True
                llenar_stack(i,(j+x)%9,sudoku[i,(j+x)%9])
        else: # dicho vecino no esta lleno
            if str(i)+str((j+x)%9)+str(n) not in descartar:
                descartar.append(str(i)+str((j+x)%9)+str(n))
    # recorrido de la columna           
    for x in range(1,9):
        if sudoku[(i+x)%9,j] > 0:
            if leido[(i+x)%9,j] == False:
                leido[(i+x)%9,j] = True
                llenar_stack((i+x)%9,j,sudoku[(i+x)%9,j])
        else: # dicho vecino no esta lleno
            if str((i+x)%9)+str(j)+str(n) not in descartar:
                descartar.append(str((i+x)%9)+str(j)+str(n))
    # Recorrido del cuadro menor
    # Asignacion del cuadro menor al que pertenece
    if i < 3:
        ix = 0
    elif i > 5:
        ix = 6
    else:
        ix = 3
    if j < 3:
        jx = 0
    elif j > 5:
        jx = 6
    else:
        jx = 3
    #bajar ambas coordenadas
    if sudoku[((i+1)%3)+ix,((j+1)%3)+jx] > 0:
        if leido[((i+1)%3)+ix,((j+1)%3)+jx] == False:
            leido[((i+1)%3)+ix,((j+1)%3)+jx] = True
            llenar_stack(((i+1)%3)+ix,((j+1)%3)+jx,sudoku[((i+1)%3)+ix,((j+1)%3)+jx])
    else: # dicho vecino no esta lleno
        if str(((i+1)%3)+ix)+str(((j+1)%3)+jx)+str(n) not in descartar:
            descartar.append(str(((i+1)%3)+ix)+str(((j+1)%3)+jx)+str(n))
    #Correrse a la derecha            
    if sudoku[((i+1)%3)+ix,((j+2)%3)+jx] > 0:
        if leido[((i+1)%3)+ix,((j+2)%3)+jx] == False:
            leido[((i+1)%3)+ix,((j+2)%3)+jx] = True
            llenar_stack(((i+1)%3)+ix,((j+2)%3)+jx,sudoku[((i+1)%3)+ix,((j+2)%3)+jx])
    else: # dicho vecino no esta lleno
        if str(((i+1)%3)+ix)+str(((j+2)%3)+jx)+str(n) not in descartar:
            descartar.append(str(((i+1)%3)+ix)+str(((j+2)%3)+jx)+str(n))
    #Bajar            
    if sudoku[((i+2)%3)+ix,((j+2)%3)+jx] > 0:
        if leido[((i+2)%3)+ix,((j+2)%3)+jx] == False:
            leido[((i+2)%3)+ix,((j+2)%3)+jx] = True
            llenar_stack(((i+2)%3)+ix,((j+2)%3)+jx,sudoku[((i+2)%3)+ix,((j+2)%3)+jx])
    else: # dicho vecino no esta lleno
        if str(((i+2)%3)+ix)+str(((j+2)%3)+jx)+str(n) not in descartar:
            descartar.append(str(((i+2)%3)+ix)+str(((j+2)%3)+jx)+str(n)) 
    #Correrse a la izquierda            
    if sudoku[((i+2)%3)+ix,((j+1)%3)+jx] > 0:
        if leido[((i+2)%3)+ix,((j+1)%3)+jx] == False:
            leido[((i+2)%3)+ix,((j+1)%3)+jx] = True
            llenar_stack(((i+2)%3)+ix,((j+1)%3)+jx,sudoku[((i+2)%3)+ix,((j+1)%3)+jx])
    else: # dicho vecino no esta lleno
        if str(((i+2)%3)+ix)+str(((j+1)%3)+jx)+str(n) not in descartar:
            descartar.append(str(((i+2)%3)+ix)+str(((j+1)%3)+jx)+str(n))
# Recorre todo el stack y a cada celda destino
# se le descarta el valor indicado, si una celda destino
# queda con un unico valor, se toma como la respuesta de
# esa celda y se llama llenar_stack() para determinar a
# cuales celdas afecta esa nueva respuesta
def descartar_stack():
    while(len(descartar) > 0):
        cima_stack = descartar.pop()
        i = int(cima_stack[0])
        j = int(cima_stack[1])
        n = int(cima_stack[2])
        if cima_stack[:2] in faltantes:
            try:
                faltantes[cima_stack[:2]].remove(n)
            except ValueError:
                pass
            if len(faltantes[cima_stack[:2]]) == 1:
                hallado = faltantes[cima_stack[:2]][0]
                del faltantes[cima_stack[:2]];
                leido[i,j] = True
                sudoku[i,j] = hallado
                llenar_stack(i,j,hallado)
                
# En la lectura del sudoku, a cada celda vacia se le crea
# un array del 1 al 9, ya que de inicio pueden tomar cualquier valor de esos
for i in range(0,9):
    for j in range(0,9):
        if sudoku[i,j] == 0:
            faltantes[str(i)+str(j)] = [1,2,3,4,5,6,7,8,9]

# MAIN
# Recorre todas las casillas y se saltea las que ya se usaron en la cola
# Para saber si se usaron en la cola se usa la matriz leido
for i in range(0,9):
    for j in range(0,9):
        # Si aun no ha sido leido se procede 
        if not leido[i,j]:            
            # Si la celda actual tiene un valor fijo se llena una pila
            # de las celdas que la actual puede afectar
            if sudoku[i,j] > 0:
                leido[i,j] = True
                llenar_stack(i,j,sudoku[i,j])
                descartar_stack()
for x in range(0,3): #Valor editable
    busqueda_profunda()
    descartar_stack()
    
if len(faltantes) > 0:
    print "No se pudo resolver el sudoku :("
    print sudoku
else:
    print "La solucion es"
    print sudoku
