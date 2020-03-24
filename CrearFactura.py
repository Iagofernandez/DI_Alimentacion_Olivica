import gi
from generarFactura import generarFactura


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2

class CrearFactura(Gtk.Window):
    def __init__(self,main):
        self.Main = main
        builder = Gtk.Builder()
        builder.add_from_file("Factura.glade")

        self.ventana = builder.get_object("Main")

        cabeceira = Gtk.HeadrBar(title="Crear Factura")
        cabeceira.set_subtitle("Guardar y generar factura")
        cabeceira.props.show_close_button = True

        self.ventana.set_titlebar(cabeceira)
        self.nombre = builder.get_object("txtNombre")
        self.direccion = builder.get_object("txtDireccion")
        self.telefono = builder.get_object("txtTelefono")
        self.productos = builder.get_object("productos")
        generarFactura = builder.get_object("generarFactura")

        self.modeloProductos = Gtk.ListStore(str)
        self.listaProductos = []
        try:
            baseDatos = dbapi2.connect("BaeDatos.dat")
            cursor = baseDatos.cursor()

            productos = cursor.execute("select nombre,precioUnidad from productos")
            for producto in productos:
                self.listaProductos.append([producto[0], producto[1]])
                self.modeloProductos.append(productos[0])

        except (dbapi2.DatabaseError):
            print("ERRORO ENE LA BASE DE DATOS")
        finally:
            print("CERRANDO CONEXIONES")
            cursor.close()
            baseDatos.close()

        self.cajaProductos= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        celdaCombo = Gtk.CellRendererText()
        self.cmbProductos =Gtk.ComboBox(model=self.modeloProductos)
        self.cmbProductos.pack_start(celdaCombo, True)
        self.cmbProductos.add_attribute(celdaCombo,"text",0)
        self.txtcantidad = Gtk.Entry()
        btnAñadir = Gtk.Button(label="+")
        btnAñadir.connect("click", self.on_btnAñadir_clicked)
        self.cajaProductos.pack_start(self.cmbProductos, True, True, 0)
        self.cajaProductos.pack_start(self.txtcantidad, True, True, 0)
        self.cajaProductos.pack_start(btnAñadir, True, True, 0)
        self.productos.add(self.cajaProductos)

        self.cajaLista = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.modelo = Gtk.ListStore(str, int)
        self.vista = Gtk.TreeView(model=self.modelo)
        celdaText = Gtk.CellRendererText()
        columnaNombre = Gtk.TreeViewColumn('Nombre Producto', celdaText, text=0)
        columnaNombre.set_sort_column_id(0)
        self.vista.append_column(columnaNombre)

        celdaText2 = Gtk.CellRendererText()
        columnaCantidad = Gtk.TreeViewColumn('Cantidad', celdaText2, text=1)
        self.vista.append_column(columnaCantidad)

        btnGuardar = Gtk.Button(label="GUARDAR")
        btnGuardar.connect("clicked", self.on_btnGuardar_clicked)
        self.cajaLista.pack_start(self.vista, True, True, 0)
        self.cajaLista.pack_start(btnGuardar, True, True, 0)
        self.productos.add(self.cajaLista)

        self.facturas = Gtk.ListStore(str)
        try:

            baseDatos = dbapi2.connect("BaseDeDatos.dat")
            cursor = baseDatos.cursor()

            leerFacturas = cursor.execute("select idFactura,nombreCliente from facturasClientes")
            for factura in leerFacturas:
                fac = str(factura[0]) + " - " + factura[1]
                self.facturas.append([fac])
        except (dbapi2.DatabaseError):
            print("ERROR EN LA BASE DE DATOS")
        finally:
            print("Cerramos la conexion a la BD")
            cursor.close()
            baseDatos.close()

        celdaCombo = Gtk.CellRendererText()
        self.cmbFacturas = Gtk.ComboBox(model=self.facturas)
        self.cmbFacturas.pack_start(celdaCombo, True)
        self.cmbFacturas.add_attribute(celdaCombo, "text", 0)
        btnGenerar = Gtk.Button(label="GENERAR FACTURA")
        btnGenerar.connect("clicked", self.on_btnGenerarFactura_clicked)
        generarFactura.pack_start(self.cmbFacturas, True, True, 0)
        generarFactura.pack_start(btnGenerar, True, True, 0)

        señales = {
            "on_btnVolver_clicked": self.on_btnVolver_clicked,
            "on_btnSalir_clicked": Gtk.main_quit,
            "on_Main_destroy": Gtk.main_quit
        }

        builder.connect_signals(señales)

        self.ventana.show_all()

        def on_btnVolver_clicked(self, boton):

            self.Main.show_all()
            self.ventana.hide()

        def on_btnAñadir_clicked(self, boton):

            indiceProducto = self.cmbProductos.get_active_iter()
            producto = self.cmbProductos.get_model()[indiceProducto][0]
            cantidad = self.txtcantidad.get_text()
            self.modelo.append([producto, int(cantidad)])

        def on_btnGuardar_clicked(self, boton):

            nombre = self.nombre.get_text()
            direccion = self.direccion.get_text()
            telefono = self.telefono.get_text()
            if (nombre == "" or direccion == "" or telefono == ""):
                print("No se han completado todos los campos")
            else:
                baseDatos = dbapi2.connect("BaseDeDatos.dat")
                cursor = baseDatos.cursor()
                cursorID = cursor.execute("SELECT idFactura FROM facturasClientes ORDER BY idFactura DESC LIMIT 1")
                idNuevo = cursorID.fetchone()[0] + 1
                insertarFactura = cursor.execute(
                    "insert into facturasClientes values('" + str(
                        idNuevo) + "','" + nombre + "','" + telefono + "','" + direccion +  "')")
                baseDatos.commit()
                print("DETALLES DE LA FACTURA AÑADIDOS CON EXITO")
                fac = str(idNuevo) + " - " + nombre
                self.facturas.append([fac])

            for lista in self.modelo:
                cursorIDProducto = cursor.execute("SELECT id FROM productos where nombre='" + lista[0] + "'")
                idProducto = cursorIDProducto.fetchone()[0]
                insertarFactura = cursor.execute(
                    "insert into facturasInfo values('" + str(idNuevo) + "','" + idProducto + "','" + str(
                        lista[1]) + "')")
                baseDatos.commit()
                print("INFO DE LA FACTURA AÑADIDA CON EXITO")

        def on_btnGenerarFactura_clicked(self, boton):

            indiceFactura = self.cmbFacturas.get_active_iter()
            facturaSeleccionada = self.cmbFacturas.get_model()[indiceFactura][0]
            factura = facturaSeleccionada.split(" - ")
            idFactura = factura[0]
            generarFactura(idFactura)

if __name__ == "__main__":
    CrearFactura()
    Gtk.main()