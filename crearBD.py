import os
from sqlite3 import dbapi2


try:
    baseDatos = dbapi2.connect("BaseDatos.dat")
    cursor = baseDatos.cursor()

    cursor.execute("create table productos(id text, nombre text, descripcion text, cantStock number , precioUnidad number )")
    cursor.execute("create table facturasClientes(idFactura number, nombreCliente text, telefono text, direccion text)")
    cursor.execute("create table facturasInfo(idFactura number , idProducto text, cantidad number)")

    cursor.execute("insert into productos values('pro1', 'Pepino','Malaga',3,1.20)")
    cursor.execute("insert into productos values ('pro2', 'tomate','Cádiz', 5, 2.00)")

    cursor.execute("insert into facturasClientes values(1, 'Bar Barcelona','986121314','Calle Barcelona nº12')")

    cursor.execute("insert into facturasInfo values(1,'pro1',1)")

    baseDatos.commit()

except(dbapi2.DatabaseError):
    print("Error en la base de datos")
finally:
    print("Cerrando conexion")
    cursor.close()
    baseDatos.close()



