import gi

gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from sqlite3 import dbapi2
from generarInventario import generarInventario

class Inventario(Gtk.Window):
    def __init__(self, main):
        self.Main = main
        self.añadir = False

        builder = Gtk.Builder()
        builder.add_from_file("Diseño.glade")
        self.ventana = builder.get_object("Main")

        cabeceira = Gtk.HeaderBar(title="Inventario")
        cabeceira.set_subtitle("Informacion de los productos de la tienda")
        cabeceira.props.show_close_button = True
        self.ventana.set_titlebar(cabeceira)

        self.mainBox = builder.get_object("mainBox")
        self.modelo = Gtk.ListStore(str, str, str, int, float)

        try:
            baseDatos = dbapi2.connect("BaseDatos.dat")
            cursor = baseDatos.cursor()

            productos = cursor.execute("select * from productos")
            for producto in productos:
                self.modelo.append([producto[0], producto[1], producto[2], producto[3], producto[4]])

        except (dbapi2.DatabaseError):
            print("EROR EN LA BAS DE DATOS")
        finally:
            print("CERRANDO CONEXIONES")
            cursor.close()
            baseDatos.close()
        self.vista = Gtk.TreeView(model = self.modelo)
        self.mainBox.pack_start(self.vista, True, True, 0)

        celdaText = Gtk.CellRendererText()
        colunmaNombreProd = Gtk.TreeViewColumn('Nombre Producto',  celdaText, text=1)
        colunmaNombreProd.set_sort_column_id(0)
        self.vista.append_column(colunmaNombreProd)

        celdaText2 = Gtk.CellRendererText()
        colunmaDescripcion = Gtk.TreeViewColumn('Descripcion', celdaText2, text=2)
        self.vista.append_column(colunmaDescripcion)

        celdaText3 = Gtk.CellRendererText(xalign=1)
        columnaStock = Gtk.TreeViewColumn('Stock', celdaText3, text=3)
        columnaStock.set_sort_column_id(2)
        self.vista.append_column(columnaStock)

        celdaText4 = Gtk.CellRendererText(xalign=1)
        columnaPrecio = Gtk.TreeViewColumn('Precio/Unidad', celdaText4, text=4)
        columnaPrecio.set_sort_column_id(3)
        self.vista.append_column(columnaPrecio)

        cajaControles = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btnAñadir = Gtk.Button(label="AÑADIR")
        btnAñadir.connect("clicked", self.on_btnAñadir_clicked)
        cajaControles.pack_start(btnAñadir, True, True, 0)
        btnModificar = Gtk.Button(label="MODIFICAR")
        btnModificar.connect("clicked", self.on_btnModificar_clicked)
        cajaControles.pack_start(btnModificar, True, True, 0)
        btnBorrar = Gtk.Button(label="BORRAR")
        btnBorrar.connect("clicked", self.on_btnBorrar_clicked)
        cajaControles.pack_start(btnBorrar, True, True, 0)
        self.mainBox.add(cajaControles)

        self.cajaModificar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.txtNombre = Gtk.Entry()
        self.txtDescripcion = Gtk.Entry()
        self.txtStock = Gtk.Entry()
        self.txtPrecio = Gtk.Entry()

        btnGuardar = Gtk.Button(label="Guardar")
        btnGuardar.connect("clicked", self.on_btnGuardar_clicked)
        self.cajaModificar.pack_start(self.txtNombre, True, True, 0)
        self.cajaModificar.pack_start(self.txtDescripcion, True, True, 0)
        self.cajaModificar.pack_start(self.txtStock, True, True, 0)
        self.cajaModificar.pack_start(self.txtPrecio, True, True, 0)

        self.cajaModificar.pack_start(btnGuardar, True, True, 0)
        self.mainBox.add(self.cajaModificar)

        cajaInventario = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btnGenerarInventario = Gtk.Button(label="GENERAR INVENTARIO")
        btnGenerarInventario.connect("clicked", self.on_btnGenerarInventario_clicked)
        cajaInventario.pack_start(btnGenerarInventario, True, True, 0)
        self.mainBox.add(cajaInventario)

        señales = {
            "on_btnVolver_clicked": self.on_btnVolver_clicked,
            "on_btnSalir_clicked": Gtk.main_quit,
            "on_Main_destroy": Gtk.main_quit
        }

        builder.connect_signals(señales)

        self.initial_show(self.ventana)

    def initial_show(self, ventana):
        ventana.show_all()
        self.cajaModificar.hide();
    def on_btnVolver_clicked(self, boton):
        self.Main.show_all()
        self.ventana.hide()
    def on_btnAñadir_clicked(self, boton):
        self.cajaModificar.show();
        self.añadir = True
    def on_btnModificar_clicked(self, boton):
        self.cajaModificar.show()
        self.añadir= False
        seleccion = self.vista.get_selection()
        modelo, punteiro = seleccion.get_selected()
        modelo, punteiro = seleccion.get_selected()
        if punteiro is not None:
            self.txtNombre.set_text(modelo[punteiro][1])
            self.txtDescripcion.set_text(modelo[punteiro][2])
            self.txtStock.set_text(str(modelo[punteiro][3]))
            self.txtPrecio.set_text(str(modelo[punteiro][4]))

    def on_btnGuardar_clicked(self, boton):
        if(self.añadir==True):
            try:
                baseDatos =dbapi2.connect("BaseDatos.dat")
                cursor = baseDatos.cursor()
                cursorID = cursor.execute("SELECT id FROM 'productos' ORDER BY id DESC LIMIT 1")
                lastid = cursorID.fetchone()[0].split("pro")
                idNuevo = "pro" + str(int(lastid[1]) + 1)
                nombre = self.txtNombre.get_text()
                descripcion = self.txtDescripcion.get_text()
                stock = self.txtStock.get_text()
                precio = self.txtPrecio.get_text()
                if (nombre == "" or descripcion == "" or stock == "" or precio == ""):
                   print("No se han completado todos los campos")
                else:
                     cursor.execute( "insert into productos values('" + idNuevo + "','" + nombre + "','" + descripcion + "','" + stock + "','" + precio + "',')")
                     baseDatos.commit()
                     print("PRODUCTO AÑADIDO CON EXITO")
                     self.modelo.append([idNuevo, nombre, descripcion, int(stock), float(precio)])
                     self.cajaModificar.hide();
            except (dbapi2.DatabaseError):
                print("ERROR EN LA BASE DE DATOS")

            finally:
                print("Cerramos la conexion a la BD")
                cursor.close()
                baseDatos.close()

        else:
            seleccion = self.vista.get_selection()
            modelo, puntero = seleccion.get_selected()
            if puntero is not None:
                idPro = modelo[puntero][0]
                nombre = self.txtNombre.get_text()
                descripcion = self.txtDescripcion.get_text()
                stock = self.txtStock.get_text()
                precio = self.txtPrecio.get_text()
                if (nombre == "" or descripcion == "" or stock == "" or precio == "" ):
                    print("No se han completado todos los campos")
                    try:
                        baseDatos =dbapi2.connect("BaseDatos.dat")
                        cursor = baseDatos.cursor()
                        cursor.execute("UPDATE productos SET nombre = '" + nombre + "', descripcion = '" + descripcion + "', cantidadStock=" + stock + ", precioUnidad=" + precio + "'  WHERE id = '" + idPro + "'")
                        baseDatos.commit()
                        print("Producto actulizado con exito")
                        self.modelo.remove(puntero)
                        self.modelo.append([idPro, nombre, descripcion, int(stock), float(precio)])
                        self.cajaModificar.hide();
                        self.txtNombre.set_text("")
                        self.txtDescripcion.set_text("")
                        self.txtStock.set_text("")
                        self.txtPrecio.set_text("")
                    except(dbapi2.DatabaseError):
                          print("ERROR EN LA BASE DE DATOS")
                    finally:
                         print("Cerramos la conexion a la BD")
                         cursor.close()
                         baseDatos.close()

    def on_btnBorrar_clicked(self, boton):
        seleccion = self.vista.get_selection()
        modelo, puntero = seleccion.get_selected()
        if puntero is not None:
            idPro = modelo[puntero][0]
            ##Conectamos con la base de datos
            try:
                baseDatos = dbapi2.connect("BaseDatos.dat")
                cursor = baseDatos.cursor()
                cursor.execute("DELETE FROM productos WHERE id = '" + idPro + "'")
                baseDatos.commit()
                print("Producto eliminado con exito")
                self.modelo.remove(puntero)
            except (dbapi2.DatabaseError):
                print("ERROR EN LA BASE DE DATOS")
            finally:
                print("Cerramos la conexion a la BD")
                cursor.close()
                baseDatos.close()

    def on_btnGenerarInventario_clicked(self, boton):

        generarInventario()
if __name__ == "__main__":
    Inventario()
    Gtk.main()