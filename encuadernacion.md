---
layout: page
title: "Taller de encuadernación"
permalink: /encuadernacion/
---

Instrucciones y script para encuadernar libros y apuntes manualmente.
Proximamente subiremos más cosas.

# **imposicion.py**
**imposicion.py** es un script escrito en python que te ayuda a reordenar las
páginas de un pdf y preparar documentos para imprimir y encuadernar. El
programa fue desarrollado originalmente por las compañeras de eigenLab[1] y
traducido al español y modificado por gente de Lewis Carroll.

**Script todavía en fase de desarrollo, probablemente haya errores.
Usalo bajo tu propio riesgo. Antes de imprimir haz todas las comprobaciones posibles.**


### Descargar
Descargar [imposicion.py](/files/imposicion.py) (versión **beta**). 

### Instalación
El script necesita **python 2.7** y las librerías **PyPDF2** y **argparse**. Si
usas Linux lo más probable es que ya tengas instalado python 2.7. Para instalar
las librerías PyPDF2 y argparse te recomendamos usar un gestor de paquetes de
python, como **pip**. Si usas Debian o Ubuntu puedes instalar pip con el
siguiente comando:
{% highlight bash %}
  sudo apt install python-pip
{% endhighlight %}
Para instalar las librerías usando pip ejecuta los siguientes comandos:
{% highlight bash %}
  sudo pip install PyPDF2
  sudo pip install argparse
{% endhighlight %}

### Uso
Una vez instaladas las librerías y descargado el script, para ejecutarlo:

{% highlight bash %}
  python2.7 imposicion.py
{% endhighlight %}

Usar el script es muy sencillo. Para obtener instrucciones sobre como usarlo
ejecuta:
{% highlight bash %}
  python2.7 imposicion.py -h
{% endhighlight %}

Recomendamos usar siempre la opción **-v** al ejecutar el script, para tener
una referencia de que es lo que hace el programa.

¡Buena encuadernación!

#### Referencias
[1] Páginas de la wiki de eigenLab: [Rilegatura](https://wiki.eigenlab.org/Rilegatura),
[Stampa](https://wiki.eigenlab.org/Stampa#Fascicolazione_di_un_libro).
[Script original](https://git.eigenlab.org/biondo/bindinghelper/).

