import gi

from CrearFactura import generarFactura
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
            "on_btn"
        }

