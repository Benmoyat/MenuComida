import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import win32print
import win32ui
import win32con

# Precios de cada artículo
precios = {
    "Hot-Dog Regular": 2.50,
    "Hot-Dog con Queso": 3.00,
    "Hot-Dog Picante": 3.50,
    "Hamburguesa Clásica": 5.00,
    "Hamburguesa con Queso": 5.50,
    "Hamburguesa con Tocino": 6.00,
    "Papas Fritas Regulares": 2.00,
    "Papas Fritas Rizadas": 2.50,
    "Papas Fritas de Camote": 3.00,
    "Cola": 1.50,
    "Jugo de Naranja": 2.00,
    "Agua": 1.00,
    "Extra": 500.00  # Precio del extra
}

# Datos del pedido y historial de pedidos
datos_pedido = {
    "hotdog": [],
    "hamburguesa": [],
    "papas": [],
    "bebida": []
}
historial_pedidos = []

# Diccionario para guardar las variables de cantidad
variables_cantidad = {
    "hotdog": [],
    "hamburguesa": [],
    "papas": [],
    "bebida": []
}

# Función para actualizar el precio total
def actualizar_total():
    total = 0.0
    for categoria in datos_pedido.values():
        for item, cantidad in categoria:
            total += precios[item] * cantidad
    etiqueta_total.config(text=f"Total: ${total:.2f}")

# Función para actualizar el subtotal para una categoría específica
def actualizar_subtotal(etiqueta_subtotal, categoria):
    subtotal = 0.0
    for item, cantidad in datos_pedido[categoria]:
        subtotal += precios[item] * cantidad
    etiqueta_subtotal.config(text=f"Subtotal: ${subtotal:.2f}")

# Función para regresar al menú principal
def regresar_al_principal():
    marco_principal.tkraise()

# Función para imprimir el pedido con manejo de saltos de línea
def imprimir_pedido(detalles_pedido):
    printer_name = 'Brother DCP-T510W'  # Nombre exacto de la impresora
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    hDC.StartDoc("Pedido")
    hDC.StartPage()

    # Ajustar la fuente y tamaño del texto
    hDC.SetMapMode(win32con.MM_TWIPS)
    font = win32ui.CreateFont({
        "name": "Arial",
        "height": -360,  # Tamaño de la fuente 18 puntos en TWIPS
        "weight": 400
    })
    hDC.SelectObject(font)

    # Escribir el texto en la página con manejo de saltos de línea
    margin_top = -100
    margin_left = 100
    line_height = 360  # Altura de la línea en TWIPS (equivalente al tamaño de la fuente)
    max_width = 8000  # Ajusta este valor según el ancho de la página y la fuente

    lines = dividir_texto_en_lineas(detalles_pedido, max_width, hDC)
    y = margin_top
    for line in lines:
        hDC.TextOut(margin_left, y, line)
        y -= line_height  # Mover hacia abajo para la siguiente línea

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()

# Función para dividir el texto en líneas según el ancho máximo
def dividir_texto_en_lineas(texto, max_width, hDC):
    palabras = texto.split()
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        if hDC.GetTextExtent(linea_actual + " " + palabra)[0] > max_width:
            lineas.append(linea_actual)
            linea_actual = palabra
        else:
            if linea_actual:
                linea_actual += " " + palabra
            else:
                linea_actual = palabra

    if linea_actual:
        lineas.append(linea_actual)

    return lineas

# Función para enviar el pedido
def enviar_pedido():
    nombre = entrada_nombre.get()
    pedido = []
    total = 0.0
    
    for categoria in datos_pedido.values():
        for item, cantidad in categoria:
            pedido.append(f"- {item} ({cantidad})")
            total += precios[item] * cantidad
    
    if not nombre:
        messagebox.showerror("Error", "Por favor ingrese su nombre.")
        return
    
    if not pedido:
        messagebox.showerror("Error", "Por favor seleccione al menos un artículo.")
        return
    
    detalles_pedido = f"Nombre: {nombre}\nPedido:\n" + "\n".join(pedido) + f"\nTotal: ${total:.2f}"
    
    # Mostrar los detalles del pedido y preguntar si desea imprimir
    if messagebox.askokcancel("Detalles del Pedido", detalles_pedido):
        # Imprimir el pedido solo si se hace clic en "OK"
        imprimir_pedido(detalles_pedido)
        
        # Agregar el pedido al historial
        historial_pedidos.append({"nombre": nombre, "pedido": pedido, "total": total})
        
        # Limpiar los datos del pedido actual
        limpiar_pedido()

# Función para agregar artículos al pedido
def agregar_articulo(categoria, item, var_cantidad, etiqueta_subtotal):
    cantidad = int(var_cantidad.get())
    datos_pedido[categoria].append((item, cantidad))
    actualizar_total()
    actualizar_subtotal(etiqueta_subtotal, categoria)

# Función para incrementar la cantidad
def incrementar_cantidad(var_cantidad):
    cantidad = int(var_cantidad.get())
    cantidad += 1
    var_cantidad.set(cantidad)

# Función para disminuir la cantidad
def disminuir_cantidad(var_cantidad):
    cantidad = int(var_cantidad.get())
    if cantidad > 0:
        cantidad -= 1
        var_cantidad.set(cantidad)

# Función para limpiar el subtotal de una categoría
def limpiar_subtotal(categoria, etiqueta_subtotal):
    datos_pedido[categoria] = []
    actualizar_total()
    actualizar_subtotal(etiqueta_subtotal, categoria)
    # Restablecer las variables de cantidad
    for var in variables_cantidad[categoria]:
        var.set("0")

# Función para crear el marco de la categoría
def crear_marco_categoria(categoria, items):
    marco = tk.Frame(root, bg='black')
    
    etiqueta = tk.Label(marco, text=f"Seleccione {categoria.title()}:", fg='white', bg='black', font=("Arial", 20))
    etiqueta.pack(pady=10)
    
    etiqueta_subtotal = tk.Label(marco, text="Subtotal: $0.00", fg='white', bg='black', font=("Arial", 20))
    etiqueta_subtotal.pack(pady=10)
    
    for item in items:
        marco_item = tk.Frame(marco, bg='black')
        marco_item.pack(pady=5)
        
        etiqueta_item = tk.Label(marco_item, text=item, fg='white', bg='black', font=("Arial", 16))
        etiqueta_item.pack(side='left', padx=10)
        
        var_cantidad = tk.StringVar(value="0")
        variables_cantidad[categoria].append(var_cantidad)
        
        boton_disminuir = tk.Button(marco_item, text="-", command=lambda q=var_cantidad: disminuir_cantidad(q), bg='white', font=("Arial", 16), width=2)
        boton_disminuir.pack(side='left', padx=5)
        
        entrada_cantidad = tk.Label(marco_item, textvariable=var_cantidad, fg='white', bg='black', font=("Arial", 16), width=3)
        entrada_cantidad.pack(side='left', padx=5)
        
        boton_incrementar = tk.Button(marco_item, text="+", command=lambda q=var_cantidad: incrementar_cantidad(q), bg='white', font=("Arial", 16), width=2)
        boton_incrementar.pack(side='left', padx=5)
        
        boton_agregar = tk.Button(marco_item, text="Agregar", command=lambda i=item, q=var_cantidad: agregar_articulo(categoria, i, q, etiqueta_subtotal), bg='white', font=("Arial", 16))
        boton_agregar.pack(side='left', padx=5)

    # Agregar opción "Extra" a la categoría
    marco_extra = tk.Frame(marco, bg='black')
    marco_extra.pack(pady=5)
    
    etiqueta_extra = tk.Label(marco_extra, text="Extra", fg='white', bg='black', font=("Arial", 16))
    etiqueta_extra.pack(side='left', padx=10)
    
    var_cantidad_extra = tk.StringVar(value="0")
    variables_cantidad[categoria].append(var_cantidad_extra)
    
    boton_disminuir_extra = tk.Button(marco_extra, text="-", command=lambda q=var_cantidad_extra: disminuir_cantidad(q), bg='white', font=("Arial", 16), width=2)
    boton_disminuir_extra.pack(side='left', padx=5)
    
    entrada_cantidad_extra = tk.Label(marco_extra, textvariable=var_cantidad_extra, fg='white', bg='black', font=("Arial", 16), width=3)
    entrada_cantidad_extra.pack(side='left', padx=5)
    
    boton_incrementar_extra = tk.Button(marco_extra, text="+", command=lambda q=var_cantidad_extra: incrementar_cantidad(q), bg='white', font=("Arial", 16), width=2)
    boton_incrementar_extra.pack(side='left', padx=5)
    
    boton_agregar_extra = tk.Button(marco_extra, text="Agregar", command=lambda q=var_cantidad_extra: agregar_articulo(categoria, "Extra", q, etiqueta_subtotal), bg='white', font=("Arial", 16))
    boton_agregar_extra.pack(side='left', padx=5)

    boton_limpiar_subtotal = tk.Button(marco, text="Limpiar Subtotal", command=lambda: limpiar_subtotal(categoria, etiqueta_subtotal), bg='red', font=("Arial", 16))
    boton_limpiar_subtotal.pack(pady=10)
    
    boton_regresar = tk.Button(marco, text="Regresar", command=regresar_al_principal, bg='white', font=("Arial", 16))
    boton_regresar.pack(pady=10)
    
    return marco

# Función para limpiar el pedido
def limpiar_pedido():
    global datos_pedido
    datos_pedido = {key: [] for key in datos_pedido}
    actualizar_total()
    for categoria in variables_cantidad:
        for var in variables_cantidad[categoria]:
            var.set("0")
    for marco, etiqueta in etiquetas_subtotales.items():
        etiqueta.config(text="Subtotal: $0.00")
    entrada_nombre.delete(0, tk.END)
    marco_principal.tkraise()

# Función para ver el historial de pedidos
def ver_historial():
    texto_historial = ""
    total_ventas = 0.0  # Variable para almacenar el total de todas las ventas
    for index, pedido in enumerate(historial_pedidos, start=1):
        info_pedido = f"Pedido {index}:\nNombre: {pedido['nombre']}\nArtículos: {', '.join(pedido['pedido'])}\nTotal: ${pedido['total']:.2f}\n\n"
        texto_historial += info_pedido
        total_ventas += pedido['total']  # Sumar el total de cada pedido al total de ventas

    # Añadir el total de todas las ventas al texto del historial
    texto_historial += f"\nTotal de Ventas: ${total_ventas:.2f}"
    
    etiqueta_historial.config(text=texto_historial)
    marco_historial.tkraise()

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Pedidos BIG Baguette")
root.geometry("1600x900")
root.configure(bg='black')

# Crear marcos
marco_principal = tk.Frame(root, bg='black')
marco_principal.place(relx=0, rely=0, relwidth=1, relheight=1)
marco_hotdog = crear_marco_categoria("hotdog", ["Hot-Dog Regular", "Hot-Dog con Queso", "Hot-Dog Picante"])
marco_hamburguesa = crear_marco_categoria("hamburguesa", ["Hamburguesa Clásica", "Hamburguesa con Queso", "Hamburguesa con Tocino"])
marco_papas = crear_marco_categoria("papas", ["Papas Fritas Regulares", "Papas Fritas Rizadas", "Papas Fritas de Camote"])
marco_bebida = crear_marco_categoria("bebida", ["Cola", "Jugo de Naranja", "Agua"])
marco_historial = tk.Frame(root, bg='black')

# Diccionario para guardar las etiquetas de subtotales
etiquetas_subtotales = {
    "hotdog": marco_hotdog.winfo_children()[1],
    "hamburguesa": marco_hamburguesa.winfo_children()[1],
    "papas": marco_papas.winfo_children()[1],
    "bebida": marco_bebida.winfo_children()[1]
}

# Agregar una imagen en la parte superior de la ventana
try:
    imagen = Image.open("BB.png")  # Actualizar la ruta de la imagen
    imagen = imagen.resize((1600, 150))
    foto = ImageTk.PhotoImage(imagen)
    # Agregar imagen al marco_principal
    etiqueta_imagen = tk.Label(marco_principal, image=foto, bg='black')
    etiqueta_imagen.image = foto  # Mantener una referencia a la imagen
    etiqueta_imagen.grid(row=0, columnspan=2, pady=10)
except Exception as e:
    messagebox.showerror("Error", f"Error al cargar la imagen: {e}")

# Entrada de nombre de usuario
etiqueta_nombre = tk.Label(marco_principal, text="Nombre:", fg='white', bg='black', font=("Arial", 20))
etiqueta_nombre.grid(row=1, column=0, pady=10, padx=10, sticky='e')
entrada_nombre = tk.Entry(marco_principal, font=("Arial", 20), width=30)
entrada_nombre.grid(row=1, column=1, pady=10, padx=10, sticky='w')

# Botones del menú principal
boton_hotdog = tk.Button(marco_principal, text="Hot-Dog", command=marco_hotdog.tkraise, bg='white', font=("Arial", 20), width=20)
boton_hotdog.grid(row=2, columnspan=2, pady=10, padx=10)
boton_hamburguesa = tk.Button(marco_principal, text="Hamburguesa", command=marco_hamburguesa.tkraise, bg='white', font=("Arial", 20), width=20)
boton_hamburguesa.grid(row=3, columnspan=2, pady=10, padx=10)
boton_papas = tk.Button(marco_principal, text="Papas Fritas", command=marco_papas.tkraise, bg='white', font=("Arial", 20), width=20)
boton_papas.grid(row=4, columnspan=2, pady=10, padx=10)
boton_bebidas = tk.Button(marco_principal, text="Bebidas", command=marco_bebida.tkraise, bg='white', font=("Arial", 20), width=20)
boton_bebidas.grid(row=5, columnspan=2, pady=10, padx=10)
boton_historial = tk.Button(marco_principal, text="Historial de Pedidos", command=ver_historial, bg='white', font=("Arial", 20), width=20)
boton_historial.grid(row=6, columnspan=2, pady=10, padx=10)

# Etiqueta del total
etiqueta_total = tk.Label(marco_principal, text="Total: $0.00", fg='white', bg='black', font=("Arial", 20))
etiqueta_total.grid(row=7, columnspan=2, pady=10)

# Botón para enviar el pedido
boton_enviar = tk.Button(marco_principal, text="Enviar Pedido", command=enviar_pedido, bg='white', font=("Arial", 20), width=20)
boton_enviar.grid(row=8, columnspan=2, pady=10)

# Botón para limpiar el pedido
boton_limpiar = tk.Button(marco_principal, text="Limpiar Pedido", command=limpiar_pedido, bg='red', font=("Arial", 20), width=20)
boton_limpiar.grid(row=9, columnspan=2, pady=10)

# Marco del historial de pedidos
etiqueta_historial = tk.Label(marco_historial, text="", fg='white', bg='black', font=("Arial", 16), justify='left')
etiqueta_historial.pack(pady=10, padx=10)
boton_regresar = tk.Button(marco_historial, text="Regresar", command=regresar_al_principal, bg='white', font=("Arial", 20), width=20)
boton_regresar.pack(pady=10)

# Colocar los marcos en la misma posición
for marco in [marco_principal, marco_hotdog, marco_hamburguesa, marco_papas, marco_bebida, marco_historial]:
    marco.place(relx=0, rely=0, relwidth=1, relheight=1)

# Elevar el marco principal al inicio
marco_principal.tkraise()

# Ejecutar la aplicación
if __name__ == "__main__":
    root.mainloop()
