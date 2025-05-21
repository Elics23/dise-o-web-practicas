from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# --- Configuración de la carpeta de subidas ---
# Carpeta donde se guardan las imágenes subidas
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Límite de tamaño de archivo (opcional, pero buena práctica)
# Por ejemplo, 16 MB (16 * 1024 * 1024 bytes)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# --- Extensiones de archivo permitidas (seguridad) ---
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    Verifica si la extensión del archivo es permitida.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Rutas de la aplicación ---

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None # Inicializa image_url a None para que la plantilla lo reciba

    if request.method == 'POST':
        # 1. Verificar si la parte 'image' está en la solicitud (si el input de archivo existe y se envió)
        if 'image' not in request.files:
            print("ERROR: No se encontró la parte 'image' en la solicitud.")
            # Podrías añadir un mensaje flash para el usuario aquí
            return redirect(request.url) 
        
        file = request.files['image']
        
        # 2. Si el usuario no seleccionó un archivo (campo vacío), el navegador envía un archivo sin nombre.
        if file.filename == '':
            print("ERROR: No se seleccionó ningún archivo.")
            # Podrías añadir un mensaje flash para el usuario aquí
            return redirect(request.url) 

        # 3. Si hay un archivo y es de una extensión permitida
        if file and allowed_file(file.filename):
            filename = file.filename
            # Construye la ruta completa para guardar el archivo
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Guarda el archivo en la ruta especificada
            try:
                file.save(filepath)
                # Genera la URL para acceder a la imagen desde el navegador
                image_url = url_for('static', filename=f'uploads/{filename}')
                print(f"Archivo subido exitosamente: {image_url}")
                # Aquí podrías guardar 'image_url' en una base de datos si es necesario
            except Exception as e:
                print(f"ERROR al guardar el archivo: {e}")
                # Podrías añadir un mensaje flash de error aquí
        else:
            print(f"ERROR: Tipo de archivo no permitido o archivo inválido: {file.filename}")
            # Podrías añadir un mensaje flash de error aquí para el usuario

    # Renderiza la plantilla HTML, pasando la URL de la imagen si se subió una
    return render_template('index.html', image_url=image_url)

@app.route('/galeria')
def galeria():
    # Aquí podrías obtener una lista de imágenes de la carpeta 'uploads'
    # para mostrarlas en la galería si 'diseno.html' lo necesita.
    # Por ejemplo:
    # uploaded_images = [url_for('static', filename=f'uploads/{f}') for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    # return render_template('diseno.html', images=uploaded_images)
    return render_template('diseno.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# --- Ejecución de la aplicación ---
if __name__ == '__main__':
    # Asegúrate de crear la carpeta de subidas si no existe al iniciar la aplicación
    # Esto es crucial para que los archivos se puedan guardar
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        print(f"Carpeta de subidas creada: {app.config['UPLOAD_FOLDER']}")
    
    app.run(debug=True) # debug=True es útil para el desarrollo, pero desactívalo en producción
