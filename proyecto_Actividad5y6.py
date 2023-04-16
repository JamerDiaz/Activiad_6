import sqlite3
from datetime import datetime


class Presentacion:
    @staticmethod
    def ingresar_item():
        print("Ingrese los datos del ítem:")
        nombre = input("Nombre: ")
        cantidad = int(input("Cantidad: "))
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {"nombre": nombre, "cantidad": cantidad, "fecha_modificacion": fecha_hora}

    @staticmethod
    def mostrar_inventario(inventario):
        print("Inventario:")
        print("{:<20} {:<10} {:<10}".format("Nombre", "Cantidad", "Fecha modificación"))
        for item in inventario:
            print("{:<20} {:<10} {}".format(item["nombre"], item["cantidad"], item["fecha_modificacion"]))


class LogicaDeNegocio:
    def __init__(self):
        self.inventario = []
        self.acceso_a_datos = AccesoADatos()

    def agregar_item(self, item):
        for i, item_existente in enumerate(self.inventario):
            if item_existente["nombre"] == item["nombre"]:
                cantidad = item.get("cantidad")
            if isinstance(cantidad, int):
                self.inventario[i]["cantidad"] += cantidad
                break
            else:
                print("El valor ingresado en cantidad no es un número válido")
                break
        self.inventario.append(item)


        self.acceso_a_datos.guardar_en_bd(self.inventario)
        print(f"{item['cantidad']} {item['nombre']} agregado al inventario el {item['fecha_modificacion']}")

    def eliminar_item(self, item):
        for i, item_existente in enumerate(self.inventario):
            if item_existente["nombre"] == item["nombre"]:
                if item_existente["cantidad"] >= item["cantidad"]:
                    self.inventario[i]["cantidad"] -= item["cantidad"]
                    self.acceso_a_datos.guardar_en_bd(self.inventario)
                    print(f"{item['cantidad']} {item['nombre']} eliminado del inventario el {item['fecha_modificacion']}")
                else:
                    print(f"No se pudo eliminar {item['cantidad']} {item['nombre']}. La cantidad disponible es {item_existente['cantidad']}")
                break
        else:
            print(f"No se pudo eliminar {item['cantidad']} {item['nombre']}. El ítem no se encuentra en el inventario.")

    def obtener_inventario(self):
        self.cargar_inventario()
        return self.inventario

    def guardar_inventario_bd(self):
        self.acceso_a_datos.guardar_en_bd(self.inventario)
        print("Inventario guardado en la base de datos.")

    def cargar_inventario_bd(self):
        self.inventario = self.acceso_a_datos.cargar_desde_bd()
        print("Inventario cargado desde la base de datos.")
        return self.inventario

    def cargar_inventario(self):
        self.inventario = self.acceso_a_datos.cargar_desde_bd()


class AccesoADatos:
    def __init__(self):
        self.conexion = sqlite3.connect('inventario.db')
        self.cursor = self.conexion.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                fecha_modificacion TEXT NOT NULL
            )
        """)

    def guardar_en_bd(self, inventario):
        self.cursor.execute("DELETE FROM inventario")
        for item in inventario:
            self.cursor.execute("""
                INSERT INTO inventario (nombre, cantidad, fecha_modificacion) VALUES (?, ?, ?)
            """, (item["nombre"], item["cantidad"], item["fecha_modificacion"]))

        self.conexion.commit()
    
    def cargar_desde_bd(self):
        inventario = []
        self.cursor.execute("SELECT * FROM inventario")

        for row in self.cursor.fetchall():
            item = {
                "nombre": row[1],
                "cantidad": row[2],
                "fecha_modificacion": row[3]
            }

            inventario.append(item)

        return inventario
    
if __name__ == '__main__':
        logica = LogicaDeNegocio()
        logica.cargar_inventario()
        Presentacion.mostrar_inventario(logica.inventario)

while True:
    print("¿Qué desea hacer?")
    print("1. Agregar ítem")
    print("2. Eliminar ítem")
    print("3. Mostrar inventario")
    print("4. Guardar inventario en base de datos")
    print("5. Cargar inventario desde base de datos")
    print("6. Salir")

    opcion = input("> ")

    if opcion == "1":
        item = Presentacion.ingresar_item()
        logica.agregar_item(item)

    elif opcion == "2":
        item = Presentacion.ingresar_item()
        logica.eliminar_item(item)

    elif opcion == "3":
        inventario = logica.obtener_inventario()
        Presentacion.mostrar_inventario(inventario)

    elif opcion == "4":
        logica.guardar_inventario_bd()

    elif opcion == "5":
        logica.cargar_inventario_bd()
        inventario = logica.obtener_inventario()
        Presentacion.mostrar_inventario(inventario)

    elif opcion == "6":
        break

    else:
        print("Opción inválida.")


