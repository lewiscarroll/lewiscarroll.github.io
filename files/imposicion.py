#!/usr/bin/python2 
# -*- coding: utf-8 -*-

"""
http://lewiscarroll.es/encuadernacion/
imposicion.py es un script escrito en python que te ayuda a reordenar las páginas de un pdf y preparar documentos para imprimir y encuadernar. El programa fue desarrollado originalmente por las compañeras de eigenLab y traducido al español y modificado por gente de Lewis Carroll.
"""

from PyPDF2 import PdfFileReader, PdfFileWriter
import argparse

CUADERNILLO_MIN = 4
CUADERNILLO_MAX = 11

def main():
    #-------------- ARGUMENT PARSING ---------------#
    parser = argparse.ArgumentParser( description="Recibe en input un libro en pdf y "
            "lo reordena para poderlo imprimir a 4 caras por hoja, a doble cara, para"
            "encuadernarlo." )

    parser.add_argument( '-i', '--input', nargs = 1,
            dest='input_file', type=str, required=True, help='Ruta al pdf del libro.'
            'rilegare.', metavar='input.pdf' )
    
    parser.add_argument( '-o', '--output', nargs = 1, default='out.pdf',
            dest='output_file', type=str, required=False, help='El nombre del archivo en'
            'el que se escribirá el documento reordenado. El valor por defecto es "out.pdf". ' 
            'Atención: el archivo se sobreescribirá si ya existe.', metavar='output.pdf' ) 

    parser.add_argument( '-k', '--sheet-number', nargs = 1, default=[0],
            dest='k', type=int, required=False, help='Número de hojas por las que estará'
            'formado cada cuadernillo (ej.: un cuadernillo de 7 páginas contiene 28 páginas).'
            'Si no pasas este argumento el script te preguntará el valor durante su ejecución',
            metavar='hojas por cuadernillo' )
    
    parser.add_argument( '-f', '--offset', nargs = 1, default=[0],
            dest='offset', type=int, required=False, help='Número de páginas iniciales'
            'del pdf que no quieres que salgan en el pdf final. Útil si la primera página del'
            'pdf es la portada y no se quiere imprimir.', metavar='offset' )
    
    parser.add_argument( '-b', '--begin-blank', nargs = 1, default=[0],
            dest='beg_blank', type=int, required=False, help='Número de páginas en blanco a'
            'insertar al inicio del documento final. Puede servir para posicionar los números de'
            'página en el lado correcto.', metavar='páginas blancas finales' )
    
    parser.add_argument( '-v', '--verbose', action='store_true', default=False,
            dest='verbose', required=False, help='Da informaciones detalladas sobre como'
            'se crea el pdf: Cuantos cuadernillos se imprimirán, de que tamaño son, de que página'
            'a que página contiene cada cuadernillo, cuantas páginas en blanco se han añadido al'
            'final para cuadrar el tamañó de los cuadernillos y una lista completa de las páginas'
            'que hay en cada hoja.' )
    
    args = parser.parse_args()
    #-----------------------------------------------#
    
    infile = args.input_file[0]
    outfile = args.output_file[0]
    boff = args.offset[0]
    bw_beg = args.beg_blank[0]

    VERBOSE = args.verbose
    if infile[ len(infile) - 4 : len( infile ) ] != '.pdf':
        print "El archivo de input no acaba en \'.pdf\', pruebo a abrirlo, pero probablemente haya errores..."
    
    # Intenta abrir el archivo de entrada
    try:
        book = PdfFileReader( infile, strict=False )
    except:
        print 'No ha sido posible abrir el archivo. Controla la dirección y los permisos de acceso al archivo.'
        exit()
    
    # Intenta abrir el archivo de  salida
    try:
        outf = open( outfile, "wb+" )
    except:
        print 'No ha sido posible crear el archivo de salida especificado. Controla los permisos de escritura.',
        exit()
    
    binded_book = PdfFileWriter()
    
    N = book.getNumPages() - boff
    if VERBOSE: print "Número de páginas a imprimir: "+str(N)
    
    #Propone distintas opciones para crear los cuadernillos
    if args.k[0] == 0:
        print "Número de hojas por cuadernillo: "
    
        for i in range(CUADERNILLO_MIN, CUADERNILLO_MAX):
            fc = N /( i * 4 )
            lp = N - (fc * i*4) 
            print "\t["+str(i)+"]", fc, "cuadernillos de", i, "hojas",
            if lp > 0:
                print "más alguna página blanca (TODO: arreglar esto)",
            print
    
        k_sel = raw_input( "Elige una opción: " )
        while k_sel.isdigit() == False or int(k_sel) > CUADERNILLO_MAX - CUADERNILLO_MIN + 1 or int(k_sel) < 1  :
            print "Opción no válida!"
            k_sel = raw_input( "Elige una opción: ")
        spf = CUADERNILLO_MIN + int( k_sel ) - 1
    else:
        spf = args.k[0]
    
    if VERBOSE:
        print "\a!! ATENCIÓN CON EL OFFSET INICIAL Y LAS PÁGINAS BLANCAS INICIALES !!"
        print "Controla dónde acaban los números de las páginas."
        print "Si no acaban en los lados externos puedes añadir una cantidad impar de páginas blancas al inicio.\n"
    
    if VERBOSE: print "Calculando el orden de las páginas...",
    pglist =  imposicion( N, k = spf, wb = bw_beg )
    if VERBOSE: print "OK"
    #Imprime estadísticas sobre la reordenación
    if VERBOSE: estadisticas( pglist )
    
    if VERBOSE: print "Generando el pdf reordenado...",
    #Creo una lista única de las páginas no separada por cuadernillos
    pages = []
    for i in pglist:
        pages.extend( i )
    
    #Creo el PDF
    for i in pages:
        if i == 0:
            #Añade una página vacía
            binded_book.addBlankPage()
        else:
            binded_book.addPage( book.getPage( i-1+boff ) )
    
    if VERBOSE: print "OK"
    
    if VERBOSE:
        print "Archivo \""+str(outfile)+"\" creado", binded_book.write(outf)
        print "OK"

def crea_cuadernillo( template, offset ):
    fascicolo = []
    for i in template:
        fascicolo.append( i + offset )
    return fascicolo

def estadisticas( book ):
    """Da un po' di statistiche utili e verbose su come e' stato creato il libro"""
    """da stampare; prende in input l'output di imposicion(), utile per non"""
    """fare stronzate in fase di stampa."""

    print "################## ESTADÍSTICAS ##################"

    print "El libro está compuesto por ", len( book ), "cuadernillos de ", len( book[0] ) / 4, "hojas."
    blank_page = 0

    for i in book[len(book)-1]:
        if i == 0:
            blank_page += 1
    if blank_page != 0:
        print "Se han añadido ", blank_page, "páginas en blanco para completar el último cuadernillo."

    print "Lista de los cuadernillos:"
    for i in book:
        first_page = 0
        last_page = 0
        blank_pages = 0
        for j in i:
            if j == 0:
                blank_pages += 1
            else:
                if first_page == 0 or j < first_page:
                    first_page = j
                if last_page == 0 or j > last_page:
                    last_page = j

        print "De página ", first_page, "a página", last_page,
        if blank_pages > 0:
            print ",", blank_pages, "páginas blancas."
        else:
            print

        for j in range( len( i ) / 4 ):
            print i[j*4 : j*4 + 4]

    print "#################################################"


def reordena( N ):
  """CHICHA"""
  if N % 4 != 0:
  	print "No puedo crear cuadernillos con un número de páginas no divisible por 4!"
	return []
  q = N / 4 - 1
  paginas= []
  paginas2= []
  #for f in range( q + 1, 0, -1): # Orden inverso
  #  hoja = [ 4*q - 2*f + 6, 2*f -1, 2*f, 4*q - 2*f +5 ] 
  #  paginas.extend(hoja)
  for f in range( q + 1, 0, -1): 
    hoja = [ 4*q - 2*f + 6, 2*f -1, 2*f, 4*q - 2*f +5 ] # TODO: Opción cambiar orden cuadernillo
    paginas.extend(hoja)
  for h in range(len(paginas)/4-1,-1,-1):
    hoja = paginas[h*4:h*4+4]
    paginas2.extend(hoja)

  return paginas2

def imposicion(N,k=6,offs=1, wb = 0 ):
  """ Permuta N páginas en cuadernillos de k hojas
	acepta un offset"""

  N +=  wb
  r = N % ( 4 * k ) # pagine in disavanzo
  h =  N / ( 4 * k ) # numero di fascicoli "completi"

  paginas = []
  templ = reordena( 4*k )

  #Genera los cuadernillos completos
  for i in range( h ):
      paginas.append( crea_cuadernillo( templ, 4*k*i ) )

  #Si el número de páginas no es divisible por las páginas del cuadernillo
  #crea un último cuadernillo con páginas blancas para llegar al número correcto.
  if r != 0:
      for j in range( len( templ ) ):
          if templ[j] > r or templ[j] == 4 * k:
            templ[j] = 0
          else:
            templ[j] += 4 * k * h
      paginas.append( templ )

  for i in range( len( paginas) ):
      for j in range( len( paginas[i] ) ):
          if paginas[i][j] != 0:
              if paginas[i][j] < wb:
                  paginas[i][j] = 0
              else:
                  paginas[i][j] -= wb

  return paginas#_pap_add( paginas, offs-1)

if __name__ == "__main__":
    # execute only if run as a script
    print("""\
Script todavía en fase de desarrollo, probablemente haya errores.
Usalo bajo tu propio riesgo. Antes de imprimir haz todas las comprobaciones posibles.

Próximamente subiremos a http://lewiscarroll.es una versión más estable.
""")
    main()
