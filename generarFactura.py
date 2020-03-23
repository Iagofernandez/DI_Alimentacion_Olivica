import os

from reportlab.platypus import (SimpleDocTemplate,PageBreak, TableStyle, Table)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from sqlite3 import dbapi2

class generarFactura():
    def  __init__(self, id):
        idFactura = id
        factura = []

        factura.append(list(['','','TIENDA LA OLIVICA','','']))
        try:
            baseDatos = dbapi2.connect("BaseDatos.dat")
            cursor= baseDatos.cursor()
            detalles = cursor.execute("select nombreCliente, telefono, direccion from facturasClientes where idFactura='"+idFactura+"'")

            for cliente in detalles:
                factura.append(['Nombre de cliente: ', cliente[0],'','Nº Factura: ', idFactura])
                factura.append(['Telefono: ', cliente[1], '', '', ''])
                factura.append(['Direccion: ', cliente[2], '', '', ''])

        except (dbapi2.DatabaseError):
            print("ERROR EN LA BAS E DE DATOS")

        finally:
            print("Cerramos conexiones")
            cursor.close()
            baseDatos.close()

        factura.append(list(['','','','','']))
        factura.append(['CODIGO','PRODUCTO','CANTIDAD','PRECIO/UNIDAD','PRECIO'])

        try:
            baseDatos = dbapi2.connect("BaseDatos.dat")
            cursor=baseDatos.cursor()

            listaProductos = []
            total = 0
            productos = cursor.execute("select id,nombre,precioUnidad from productos")
            for producto in productos:
                listaProductos.append([producto[0],producto[1],producto[2]])

            detalesFactura = cursor.execute("select idProducto,cantidad from facturasInfo where idFactura='"+idFactura+"'")
            for pro in detalesFactura:
                for prod in listaProductos:
                    if (prod[0]==pro[0]):
                        precio = int(pro[1]*float(prod[2]))
                        factura.append([prod[0],prod[1],prod[2],precio])
                total = total + precio
            factura.append(['','','','PRECIO TOTAL:', str(total)+"€"])
        except (dbapi2.DatabaseError):
            print("ERRORO EM LA BAS E DE DATOS")
        finally:
            print ("CERRANDO CONEXIONES")
            cursor.close()
            baseDatos.close()


        print(factura)

        doc = SimpleDocTemplate("InformeFactura.pdf", pagesize=A4)

        guion = []

        taboa = Table(factura, colWidths=90, rowHeights=30)
        taboa.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkgreen),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (2, 5), (-1, -1), 'RIGHT'),
            ('ALIGN', (2, 5), (-1, -1), 'RIGHT'),

            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('BOX', (0, 1), (-1, 4), 1, colors.black),

            ('BOX', (0, 6), (-1, -2), 1, colors.black),

            ('INNERGRID', (0, 6), (-1, -2), 0.5, colors.grey)
        ]))

        guion.append(taboa)
        guion.append(PageBreak())

        doc.build(guion)

if __name__ == "__main__":
    generarFactura()






