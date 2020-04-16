"""
DOCS:
https://linux.die.net/man/1/pdftotext
AUTOR: jaglame@gmail.com
"""

import subprocess
import tempfile
from collections import namedtuple


def pdf_to_text(pdfpath, first=None, last=None, nopgbrk=False, htmlmeta=False,
                encoding="UTF-8", enc="UTF-8", fiepath=None):
    """ Convierte un pdf a text """
    if not fiepath:
        # Si no se especifica una salida es temporal.
        f = tempfile.TemporaryFile(mode="w+", encoding=encoding)
    else:
        f = open(fiepath, "w+", encoding=encoding)

    cmd = []
    a = cmd.append

    a("pdftotext")  # converts Portable Document Format (PDF) files to plain text.

    a("-layout")  # Maintain (as best as possible) the original physical layout of the text

    a("-eol")  # Sets the end-of-line convention to use for text output
    a("unix")

    a("-enc")
    a(enc)

    if first:
        a("-f")  # Specifies the first page to convert.
        a(str(int(first)))

    if last:
        a("-l")  # Specifies the last page to convert. 
        a(str(int(last)))

    if nopgbrk:
        a("-nopgbrk")

    if htmlmeta:
        a("-htmlmeta")

    a(pdfpath)
    a("-")  # stdout
    p = subprocess.Popen(cmd, stdout=f, close_fds=True)
    p.wait()
    f.seek(0)
    
    # cerrar al finalizar.
    return f


def to_int(value):
    """ """
    if value:
        try:
            return int(value.replace(".", "").strip())
        except ValueError:
            pass
    return 0

def replace_chars():
    """ """
    pass

def create_records(f):
    """ 
    1. Problema de codificación de caracteres de orígen, ejemplo no se muestra correctamente la Ñ.
    """

    columns = ["nro", "ci", "nombre", "departamento", "distrito"]
    Record = namedtuple("Record", columns)

    prev_data = None

    for n, line in enumerate(f.readlines()):
        if n == 0 or line.startswith("\x0c"): ## 12 FF Avance de página
            continue  # Encabezado de Tabla

        # nro
        data = line.rstrip("\n").lstrip()
        if not data:
            continue
        if data.startswith("Pág"):
            continue

        parts = data.split(" ", 1)
        nro = to_int(parts[0])
        if not nro:
            #print("*** LINE ERROR ***")
            #print(prev_data)
            #print(data)
            continue
    
        prev_data = data

        # ci
        data = parts[1].lstrip()
        parts = data.split(" ", 1)
        ci = to_int(parts[0])
        
        nombre = ""
        departamento = ""
        distrito = ""
        
        try:

            # nombre
            data = parts[1].lstrip()
            parts = data.split("  ", 1)
            nombre = parts[0]

            # departamento
            data = parts[1].lstrip()
            parts = data.split("  ", 1)
            departamento = parts[0]

            # distrito
            data = parts[1].lstrip()
            parts = data.split("  ", 1)
            distrito = parts[0]

        except IndexError:
            pass

        record = (nro, ci, nombre, departamento, distrito)
        yield Record(*record)



def generar_grupo(pdfpath):
    """ """
    count = 0

    print("*** %s ***" % pdfpath)
    f = pdf_to_text(pdfpath, first=1, last=None)
    for record in create_records(f):
        count += 1
        print(record)

    f.close()
    print("count:", pdfpath, count)


def grupo1():
    """ """
    generar_grupo("grupo1.pdf")

def grupo2():
    """ """
    generar_grupo("grupo2.pdf")

def grupo3():
    """ """
    generar_grupo("grupo3.pdf")


def run():
    """ """
    grupo1()
    grupo2()
    grupo3()

if __name__ == "__main__":
    run()


