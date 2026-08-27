from database import crear_tablas
from inventario import Inventario


def mostrar_menu():
    print("\n" + "=" * 45)
    print("     SISTEMA DE INVENTARIO")
    print("=" * 45)

    print("1. Agregar producto")
    print("2. Listar productos")
    print("3. Buscar producto")
    print("4. Modificar producto")
    print("5. Eliminar producto")
    print("6. Registrar entrada de stock")
    print("7. Registrar salida de stock")
    print("8. Ver productos con stock bajo")
    print("9. Ver historial de movimientos")
    print("0. Salir")

    print("=" * 45)


def pedir_entero(mensaje, minimo=None):
    """Pide un número entero válido."""

    while True:
        try:
            numero = int(input(mensaje))

            if minimo is not None and numero < minimo:
                print(f"El número debe ser mayor o igual a {minimo}.")
                continue

            return numero

        except ValueError:
            print("Error: ingresá un número válido.")


def pedir_float(mensaje, minimo=None):
    """Pide un número decimal válido."""

    while True:
        try:
            numero = float(input(mensaje))

            if minimo is not None and numero < minimo:
                print(f"El número debe ser mayor o igual a {minimo}.")
                continue

            return numero

        except ValueError:
            print("Error: ingresá un número válido.")


def agregar_producto(inventario):
    print("\n--- AGREGAR PRODUCTO ---")

    nombre = input("Nombre: ").strip()
    categoria = input("Categoría: ").strip()

    if not nombre or not categoria:
        print("El nombre y la categoría no pueden estar vacíos.")
        return

    precio = pedir_float("Precio: $", 0)
    stock = pedir_entero("Stock inicial: ", 0)

    producto_id = inventario.agregar_producto(
        nombre,
        categoria,
        precio,
        stock
    )

    print(f"\nProducto agregado correctamente. ID: {producto_id}")


def listar_productos(inventario):
    print("\n--- LISTA DE PRODUCTOS ---")

    productos = inventario.listar_productos()

    if not productos:
        print("No hay productos registrados.")
        return

    for producto in productos:
        print(producto)


def buscar_producto(inventario):
    print("\n--- BUSCAR PRODUCTO ---")

    texto = input("Ingresá un nombre o categoría: ").strip()

    productos = inventario.buscar_producto(texto)

    if not productos:
        print("No se encontraron productos.")
        return

    print("\nResultados:")

    for producto in productos:
        print(producto)


def modificar_producto(inventario):
    print("\n--- MODIFICAR PRODUCTO ---")

    producto_id = pedir_entero("Ingresá el ID del producto: ", 1)

    producto = inventario.obtener_producto(producto_id)

    if producto is None:
        print("El producto no existe.")
        return

    print("\nProducto actual:")
    print(producto)

    nombre = input("\nNuevo nombre: ").strip()
    categoria = input("Nueva categoría: ").strip()
    precio = pedir_float("Nuevo precio: $", 0)

    if not nombre or not categoria:
        print("El nombre y la categoría no pueden estar vacíos.")
        return

    inventario.modificar_producto(
        producto_id,
        nombre,
        categoria,
        precio
    )

    print("Producto modificado correctamente.")


def eliminar_producto(inventario):
    print("\n--- ELIMINAR PRODUCTO ---")

    producto_id = pedir_entero("Ingresá el ID del producto: ", 1)

    producto = inventario.obtener_producto(producto_id)

    if producto is None:
        print("El producto no existe.")
        return

    print("\nProducto:")
    print(producto)

    confirmar = input(
        "\n¿Estás seguro de eliminarlo? (S/N): "
    ).upper()

    if confirmar == "S":

        if inventario.eliminar_producto(producto_id):
            print("Producto eliminado correctamente.")

        else:
            print("No se pudo eliminar el producto.")

    else:
        print("Operación cancelada.")


def registrar_stock(inventario, tipo):
    if tipo == "ENTRADA":
        titulo = "REGISTRAR ENTRADA DE STOCK"
    else:
        titulo = "REGISTRAR SALIDA DE STOCK"

    print(f"\n--- {titulo} ---")

    producto_id = pedir_entero("ID del producto: ", 1)

    producto = inventario.obtener_producto(producto_id)

    if producto is None:
        print("El producto no existe.")
        return

    print("\nProducto seleccionado:")
    print(producto)

    cantidad = pedir_entero("Cantidad: ", 1)

    exito, mensaje = inventario.registrar_movimiento(
        producto_id,
        tipo,
        cantidad
    )

    print(mensaje)


def ver_stock_bajo(inventario):
    print("\n--- PRODUCTOS CON STOCK BAJO ---")

    limite = pedir_entero(
        "Mostrar productos con stock menor o igual a: ",
        0
    )

    productos = inventario.productos_stock_bajo(limite)

    if not productos:
        print("No hay productos con stock bajo.")
        return

    for producto in productos:
        print(producto)


def ver_movimientos(inventario):
    print("\n--- HISTORIAL DE MOVIMIENTOS ---")

    movimientos = inventario.ver_movimientos()

    if not movimientos:
        print("No hay movimientos registrados.")
        return

    for movimiento in movimientos:

        print(
            f"ID Movimiento: {movimiento[0]} | "
            f"Producto: {movimiento[1]} | "
            f"Tipo: {movimiento[2]} | "
            f"Cantidad: {movimiento[3]} | "
            f"Fecha: {movimiento[4]}"
        )


def main():

    crear_tablas()

    inventario = Inventario()

    while True:

        mostrar_menu()

        opcion = input("Seleccioná una opción: ").strip()

        if opcion == "1":
            agregar_producto(inventario)

        elif opcion == "2":
            listar_productos(inventario)

        elif opcion == "3":
            buscar_producto(inventario)

        elif opcion == "4":
            modificar_producto(inventario)

        elif opcion == "5":
            eliminar_producto(inventario)

        elif opcion == "6":
            registrar_stock(inventario, "ENTRADA")

        elif opcion == "7":
            registrar_stock(inventario, "SALIDA")

        elif opcion == "8":
            ver_stock_bajo(inventario)

        elif opcion == "9":
            ver_movimientos(inventario)

        elif opcion == "0":
            print("\n¡Gracias por usar el Sistema de Inventario!")
            break

        else:
            print("\nOpción inválida. Intentá nuevamente.")


if __name__ == "__main__":
    main()