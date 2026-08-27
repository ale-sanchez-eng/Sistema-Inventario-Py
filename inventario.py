from datetime import datetime

from database import conectar
from producto import Producto


class Inventario:

    def agregar_producto(self, nombre, categoria, precio, stock):
        """Agrega un nuevo producto a la base de datos."""

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO productos (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
        """, (nombre, categoria, precio, stock))

        producto_id = cursor.lastrowid

        conexion.commit()
        conexion.close()

        # Si el producto se crea con stock mayor a 0,
        # registramos ese stock como una entrada inicial.
        if stock > 0:
            self.registrar_movimiento(
                producto_id,
                "ENTRADA",
                stock
            )

        return producto_id

    def listar_productos(self):
        """Devuelve una lista con todos los productos."""

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, nombre, categoria, precio, stock
            FROM productos
            ORDER BY id
        """)

        filas = cursor.fetchall()
        conexion.close()

        productos = []

        for fila in filas:
            producto = Producto(
                fila[0],
                fila[1],
                fila[2],
                fila[3],
                fila[4]
            )

            productos.append(producto)

        return productos

    def buscar_producto(self, texto):
        """Busca productos por nombre o categoría."""

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, nombre, categoria, precio, stock
            FROM productos
            WHERE nombre LIKE ?
               OR categoria LIKE ?
            ORDER BY nombre
        """, (f"%{texto}%", f"%{texto}%"))

        filas = cursor.fetchall()
        conexion.close()

        productos = []

        for fila in filas:
            productos.append(
                Producto(
                    fila[0],
                    fila[1],
                    fila[2],
                    fila[3],
                    fila[4]
                )
            )

        return productos

    def obtener_producto(self, producto_id):
        """Busca un producto por su ID."""

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, nombre, categoria, precio, stock
            FROM productos
            WHERE id = ?
        """, (producto_id,))

        fila = cursor.fetchone()
        conexion.close()

        if fila is None:
            return None

        return Producto(
            fila[0],
            fila[1],
            fila[2],
            fila[3],
            fila[4]
        )

    def modificar_producto(self, producto_id, nombre, categoria, precio):
        """Modifica los datos principales de un producto."""

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE productos
            SET nombre = ?,
                categoria = ?,
                precio = ?
            WHERE id = ?
        """, (nombre, categoria, precio, producto_id))

        conexion.commit()

        modificado = cursor.rowcount > 0

        conexion.close()

        return modificado

    def eliminar_producto(self, producto_id):
        """Elimina un producto y sus movimientos asociados."""

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            DELETE FROM productos
            WHERE id = ?
        """, (producto_id,))

        conexion.commit()

        eliminado = cursor.rowcount > 0

        conexion.close()

        return eliminado

    def registrar_movimiento(self, producto_id, tipo, cantidad):
        """Registra una entrada o salida de stock."""

        producto = self.obtener_producto(producto_id)

        if producto is None:
            return False, "El producto no existe."

        if cantidad <= 0:
            return False, "La cantidad debe ser mayor a cero."

        tipo = tipo.upper()

        if tipo not in ("ENTRADA", "SALIDA"):
            return False, "Tipo de movimiento inválido."

        if tipo == "SALIDA" and cantidad > producto.stock:
            return False, "No hay suficiente stock disponible."

        conexion = conectar()
        cursor = conexion.cursor()

        if tipo == "ENTRADA":
            cursor.execute("""
                UPDATE productos
                SET stock = stock + ?
                WHERE id = ?
            """, (cantidad, producto_id))

        else:
            cursor.execute("""
                UPDATE productos
                SET stock = stock - ?
                WHERE id = ?
            """, (cantidad, producto_id))

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        cursor.execute("""
            INSERT INTO movimientos (
                producto_id,
                tipo,
                cantidad,
                fecha
            )
            VALUES (?, ?, ?, ?)
        """, (
            producto_id,
            tipo,
            cantidad,
            fecha
        ))

        conexion.commit()
        conexion.close()

        return True, "Movimiento registrado correctamente."

    def productos_stock_bajo(self, limite=5):
        """Devuelve los productos con stock igual o menor al límite."""

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, nombre, categoria, precio, stock
            FROM productos
            WHERE stock <= ?
            ORDER BY stock ASC
        """, (limite,))

        filas = cursor.fetchall()
        conexion.close()

        productos = []

        for fila in filas:
            productos.append(
                Producto(
                    fila[0],
                    fila[1],
                    fila[2],
                    fila[3],
                    fila[4]
                )
            )

        return productos

    def ver_movimientos(self):
        """Devuelve el historial de movimientos."""

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                movimientos.id,
                productos.nombre,
                movimientos.tipo,
                movimientos.cantidad,
                movimientos.fecha
            FROM movimientos
            INNER JOIN productos
                ON movimientos.producto_id = productos.id
            ORDER BY movimientos.id DESC
        """)

        movimientos = cursor.fetchall()

        conexion.close()

        return movimientos