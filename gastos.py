import json
from datetime import datetime

ARCHIVO = "datos.json"

def cargar_datos():
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "categorias": {},
            "medios_pago": {},
            "ingresos": {},
            "asientos": 0
        }

def guardar_datos(datos):
    with open(ARCHIVO, "w") as f:
        json.dump(datos, f, indent=4)

def agregar_categoria(nombre):
    datos = cargar_datos()
    nombre = nombre.lower()

    if nombre in datos["categorias"]:
        raise ValueError("La categoría ya existe")

    datos["categorias"][nombre] = 0
    guardar_datos(datos)

def agregar_medio(nombre):
    datos = cargar_datos()
    nombre = nombre.lower()

    if nombre in datos["medios_pago"]:
        raise ValueError("El medio ya existe")

    datos["medios_pago"][nombre] = 0
    guardar_datos(datos)

def cargar_gasto(monto, categoria, medio):
    datos = cargar_datos()

    categoria = categoria.lower()
    medio = medio.lower()

    fecha = datetime.now().strftime("%d/%m/%Y")


    if categoria in datos["categorias"]:
        datos["categorias"][categoria] += monto
    elif categoria in datos["medios_pago"]:
        datos["medios_pago"][categoria] += monto
    elif categoria in datos["ingresos"]:
        datos["ingresos"][categoria] += monto
    else:
        raise ValueError("Cuenta origen inexistente")

    if medio in ["sueldo", "intereses"]:
        if medio in datos["categorias"]:
            datos["categorias"][medio] += monto
        elif medio in datos["medios_pago"]:
            datos["medios_pago"][medio] += monto
        elif medio in datos["ingresos"]:
            datos["ingresos"][medio] += monto
        else:
            raise ValueError("Cuenta destino inexistente")
    else:
        if medio in datos["categorias"]:
            datos["categorias"][medio] -= monto
        elif medio in datos["medios_pago"]:
            datos["medios_pago"][medio] -= monto
        elif medio in datos["ingresos"]:
            datos["ingresos"][medio] -= monto
        else:
            raise ValueError("Cuenta destino inexistente")

    datos["asientos"] += 1
    nro_asiento = datos["asientos"]

    guardar_datos(datos)
    
    ancho_desc = 55
    ancho_monto = 15

    titulo = f"Asiento: {nro_asiento}"

    if nro_asiento == 1:
        header = (
            f"{titulo:<{ancho_desc}} | {'DEBE':^{ancho_monto}} | {'HABER':^{ancho_monto}} |\n"
        )
    else:
        header = (
            f"{titulo:-<{ancho_desc}} | {'-'*ancho_monto} | {'-'*ancho_monto} |\n"
        )

    linea_debe_desc = f"{fecha} ({categoria}) {categoria.capitalize()}"
    linea_haber_desc = f"{fecha} ({medio}) {medio.capitalize()}"

    linea_debe = (
        f"{linea_debe_desc:<{ancho_desc}} | {monto:>{ancho_monto},.2f} | {'':>{ancho_monto}} |\n"
    )

    linea_haber = (
        f"{linea_haber_desc:<{ancho_desc}} | {'':>{ancho_monto}} | {monto:>{ancho_monto},.2f} |\n"
    )

    with open("Gastos.txt", "a", encoding="utf-8") as op:
        op.write(header)
        op.write(linea_debe)
        op.write(linea_haber)
    
def resumen_mes_actual():
    datos = cargar_datos()

    categorias = datos["categorias"]
    medios = datos["medios_pago"]

    total = sum(categorias.values())

    if total == 0:
        return "No hay gastos cargados."

    texto = "📊 Resumen mensual\n\n"

    for cat, monto in categorias.items():
        if monto > 0:
            porcentaje = (monto / total) * 100
            texto += f"{cat.capitalize()}: ${monto} ({porcentaje:.1f}%)\n"

    texto += f"\nTotal: ${total}\n\n💳 Pagos:\n"

    for medio, monto in medios.items():
        if monto > 0:
            porcentaje = (monto / total) * 100
            texto += f"{medio}: ${monto} ({porcentaje:.1f}%)\n"

    return texto

def limp():
    datos = cargar_datos()

    for cat in datos["categorias"]:
        datos["categorias"][cat] = 0

    for medio in datos["medios_pago"]:
        datos["medios_pago"][medio] = 0

    for ingreso in datos["ingresos"]:
        datos["ingresos"][ingreso] = 0

    datos["asientos"] = 0

    guardar_datos(datos)

    with open("Gastos.txt", "w") as f:
        f.write("")

    return "Sistema reiniciado correctamente."


# limp()
# Agregar categoria:
# agregar_categoria("nombre")
# Agregar medio:
# agregar_medio("nombre")