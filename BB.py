import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


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
    "Agua": 1.00
}

# Datos del pedido y historial de pedidos
datos_pedido = {
    "hotdog": [],
    "hamburguesa": [],
    "papas": [],
    "bebida": []
}
historial_pedidos = []

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

# Función para enviar el pedido
def enviar_pedido():
    nombre = entrada_nombre.get()
    pedido = []
    total = 0.0
    
    for categoria in datos_pedido.values():
        for item, cantidad in categoria:
            pedido.append(f"{item} ({cantidad})")
            total += precios[item] * cantidad
    
    if not nombre:
        messagebox.showerror("Error", "Por favor ingrese su nombre.")
        return
    
    if not pedido:
        messagebox.showerror("Error", "Por favor seleccione al menos un artículo.")
        return
    
    detalles_pedido = f"Nombre: {nombre}\nPedido: {', '.join(pedido)}\nTotal: ${total:.2f}"
    messagebox.showinfo("Detalles del Pedido", detalles_pedido)
    
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
        
        boton_disminuir = tk.Button(marco_item, text="-", command=lambda q=var_cantidad: disminuir_cantidad(q), bg='white', font=("Arial", 16), width=2)
        boton_disminuir.pack(side='left', padx=5)
        
        entrada_cantidad = tk.Label(marco_item, textvariable=var_cantidad, fg='white', bg='black', font=("Arial", 16), width=3)
        entrada_cantidad.pack(side='left', padx=5)
        
        boton_incrementar = tk.Button(marco_item, text="+", command=lambda q=var_cantidad: incrementar_cantidad(q), bg='white', font=("Arial", 16), width=2)
        boton_incrementar.pack(side='left', padx=5)
        
        boton_agregar = tk.Button(marco_item, text="Agregar", command=lambda i=item, q=var_cantidad: agregar_articulo(categoria, i, q, etiqueta_subtotal), bg='white', font=("Arial", 16))
        boton_agregar.pack(side='left', padx=5)
    
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

# Agregar una imagen en la parte superior de la ventana
try:
    imagen = Image.open("BB.png")  # Actualizar la ruta de la imagen
    imagen = imagen.resize((1600, 150), Image.ANTIALIAS)
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

