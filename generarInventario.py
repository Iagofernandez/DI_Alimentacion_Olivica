import os
from reportlab.platypus import (SimpleDocTemplate, PageBreak, TableStyle, Table)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from sqlite3 import dbapi2

class generarInventario():
    def __init__(self):
        listaInventario = []

        listaInventario.append(list(['','','TIENDA LA OLIVICA','','','']))
        listaInventario.append(list(['Lista de productos','','','','','']))
        listaInventario.append(list(['CODIGO','NOMBRE','DESCRIPCION','STOCK','PRECIO']))

        try:
            baseDatos = dbapi2.connect("BaseDatos.dat")
            cursor = baseDatos.cursor()

            productos = cursor.execute("select * from productos")
            for producto in productos:
                listaInventario.append(list([producto[0],producto[1],producto[2],str(producto[3]),str(producto[4])]))
        except(dbapi2.DatabaseError):
            print("ERROR EN LA DATABSE")
        finally:
            print("Cerrando conexiones")
            cursor.close()
            baseDatos.close()

        doc = SimpleDocTemplate("InformeInventario.pdf", pagesize= A4)

        guion = []

        taboa = Table(listaInventario, colWidths=90, rowHeights=30)
        taboa.setStyle(TableStyle([
                 ('TEXTCOLOR', (0, 0), (-1, 1), colors.darkgreen),

                 ('TEXTCOLOR', (0, 4), (-1, -1), colors.black),

                 ('BOX', (0, 2), (-1, -4), 1, colors.black),

                 ('INNERGRID', (0, 2), (-1, -1), 0.5, colors.grey),

                 ('FONTSIZE', (0, 0), (-1, -1), 8),

                 ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                 ('ALIGN', (0, 0), (-1, -1), 'CENTER')
              ]))
        guion.append(taboa)
        guion.append(PageBreak)

        doc.build(guion)

if __name__== "__main__" :
    generarInventario()