import gi

from CrearFactura import CrearFactura
from Inventario import Inventario
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

class TiendaOlivica():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("TiendaOlivica.glade")
        self.ventana = builder.get_object("Main")

        cabeceira = Gtk.HeaderBar(title="Ventana principal")
        cabeceira.set_subtitle("Bienvenido a la tienda olivica")
        cabeceira.props.show_close_button = True
        self.ventana.set_titlebar(cabeceira)

        señales = {
            "on_btnFactura_clicked": self.on_btnFactura_clicked,
            "on_btnInventario_clicked": self.on_btnInventario_clicked,
            "on_btnSalir_clicked": Gtk.main_quit,
            "on_Main_destroy": Gtk.main_quit
        }
        builder.connect_signals(señales)

        self.ventana.show_all()
    def on_btnFactura_clicked(self, boton):
        self.ventana.hide()
        CrearFactura(self.ventana)
    def on_btnInventario_clicked(self, boton):
        self.ventana.hide()
        Inventario(self.ventana)
if __name__=="__main__":
    TiendaOlivica()
    Gtk.main()