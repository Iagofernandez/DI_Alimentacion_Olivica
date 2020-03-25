Tienda Olívica
**************

Este manual describe que realiza cada apartado del proyecto

La aplicación consta de 3 ventanas:
 * Una ventana principal
 * Una ventana inventario, para ver y añadir nuestros productos
 * Una ventana para generar facturas a nuestros clientes

TiendaOlivica
*************
Ventana principal en la cual hay 2 botones, permiten acceder a dos submenus de nuestro pryecto

Inventario
**********
Ventana que nos permite interactuar con nuestros productos a la venta, conocer y añadir nuevos productos
Cada producto nuevo adquiere un id automático, recogiendo el último id conocido.
Hay una base de datos con dos primeros productos

Existen botones en esta ventana:
 * Si se selecciona un producto y se le clicka a **BORRAR**, se elimina.
 * Otro botón es **MODIFICAR**, que nos permite seleccionar un producto y al clickar se abre un nuevo formulario para cambiar su información.
 * Otro botón es **AÑADIR** que nos permite añadir un nuevo producto.
 * **GENERAR INVENTARIO** crea un pdf con los productos existentes.

Factura
*******
Ventana que nos permite generar facturas para nuestros clientes o para nosotros mismos. Se debe introducir información sobre nuestro cliente.

Al igual que con los productos, tenemos una factura ya almacenada predeterminadamente.

Existen botones en esta interfaz:
 * Luego seleccionamos los productos que el cliente quiere adquirir y lo añadimos a la lista. Al final guardamos la informacion en el boton **GUARDAR** y esta quedara almacenada en la base de datos.
 * Al clicar el boton **GENERAR FACTURA** se creera un PDF con la informacion del cliente y la lista de productos adquirdos con su precio total.