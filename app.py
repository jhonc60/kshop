#from crypt import methods

# Importamos las librerías necesarias
from flask import Flask
from flask import render_template, request, redirect,  session
from flaskext.mysql import MySQL 
from datetime import datetime 
import os
from flask import send_from_directory

# Creamos una instancia de Flask
app=Flask(__name__)

# Establecemos una clave secreta para la sesión
app.secret_key = "kellymar2022"

# Creamos una instancia de MySQL
mysql=MySQL()

# Configuramos los parámetros de conexión a la base de datos
app.config['MYSQL_DATABASE_HOST'] = 'localhost' #jhonc60.mysql.pythonanywhere-services.com
app.config['MYSQL_DATABASE_USER'] = 'root' #jhonc60
app.config['MYSQL_DATABASE_PASSWORD'] = ''  # clave de  pythonanywhere.com CHy3QGZckSTt8E
app.config['MYSQL_DATABASE_DB'] = 'kshop_db'

# Inicializamos MySQL con la aplicación de Flask
mysql.init_app(app)

# Creamos una ruta para la página principal
@app.route('/')
def inicio():
    return render_template('sitio/index.html')

# Creamos una ruta para servir imágenes de la carpeta 'static'
@app.route('/static/<logo_imagen>')
def logo(logo_imagen):

    return send_from_directory(os.path.join('templates/sitio/static'), logo_imagen)

# Creamos una ruta para servir imágenes de la carpeta 'img'
@app.route('/img/<imagen>')
def imagenes(imagen):

    return send_from_directory(os.path.join('templates/sitio/img'), imagen)

# Creamos una ruta para servir archivos CSS de la carpeta 'css'
@app.route('/css/<archivocss>')
def css_link(archivocss):
    
    return send_from_directory(os.path.join('templates/sitio/css'), archivocss)

# Creamos una ruta para la página de catálogo
@app.route('/catalogo')
def catalogo():
        # Realizamos una consulta a la base de datos para obtener el catálogo de productos
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `catalogo`")
    catalogo=cursor.fetchall()
    conexion.commit()

    return render_template('sitio/catalogo.html', catalogo = catalogo)

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')



@app.route('/admin/')
def admin_index():
    if not 'login' in session:
        return redirect("/admin/login")
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']

    if _usuario=="admin" and _password=="123456789":
        session["login"]=True
        session["usuario"]="Administrador"
        return render_template('/admin/index.html')
    return render_template('admin/login.html', mensaje="Las credenciales no son las correctas")

@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')

@app.route('/admin/catalogo')
def admin_catalogo():

    if not 'login' in session:
        return redirect("/admin/login")

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `catalogo`")
    catalogo=cursor.fetchall()
    conexion.commit()
    
    

    return render_template("admin/catalogo.html", catalogo=catalogo,)


@app.route('/admin/catagologo/guardar', methods=['POST'])
def admin_catalogo_guardar():

    if not 'login' in session:
        return redirect("/admin/login")

    _nombre=request.form['txtNombre']
    _descripcion=request.form['txtDescripcion']
    _archivo=request.files['txtImagen']
    

    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename
        _archivo.save("templates/sitio/img/"+nuevoNombre)



    sql="INSERT INTO `catalogo` (`id`, `nombre`, `descripcion`, `imagen`) VALUES (NULL,%s, %s,%s);"
    datos=(_nombre,_descripcion,nuevoNombre)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/admin/catalogo')


   

@app.route('/admin/catalogo/borrar', methods=['POST'])
def admin_catalogo_borrar():

    if not 'login' in session:
        return redirect("/admin/login")

    _id=request.form['txtID']
   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT imagen FROM `catalogo` WHERE id=%s",(_id))
    catalogo=cursor.fetchall()
    conexion.commit()
    
    if os.path.exists("templates/sitio/img/"+str(catalogo[0][0])):
        os.unlink("templates/sitio/img/"+str(catalogo[0][0]))


    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM catalogo WHERE id=%s",(_id))
    catalogo=cursor.fetchall()
    conexion.commit()


    return redirect('/admin/catalogo')

#404 error
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('sitio/404.html'), 404



if __name__=='__main__':
    app.run(debug=True)