from colorama import Cursor
from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL
from flask import request, redirect
from datetime import datetime

from flaskext.mysql import MySQL

app=Flask(__name__)

mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='sistema2'

mysql.init_app(app)

@app.route('/')
def index():
    #sql="INSERT INTO `sistema2`.`empleados` (`id`, `nombre`, `correo`, `foto`)\
   #VALUES (NULL, 'Xavito', 'xavito7@gmail.com.ar', 'fotojosias.jpg');"
   #conn=mysql.connect()
   #cursor=conn.cursor()
   #cursor.execute(sql)
   #conn.commit()
   #return render_template("empleados/index.html")
   #return render_template('empleados/index.html')
   #
    sql="SELECT * FROM `sistema2`.`empleados`;"
    conn=mysql.connect() #Nos conectamos a la base de datos
    cursor=conn.cursor() #Sobre el cursor vamos a realizar 
    cursor.execute(sql) #Ejecutamos la sentencia SQL sobre el cursor.
 #Copiamos el contenido del cursor a una variable
    #return render_template('empleados/index.html')
   # db_empleados = Cursor.fetchall()
    conn.commit()
    #return render_template('empleados/index.html')
    #, empleados = db_empleados
    
@app.route('/create')
def create():
     return render_template('empleados/create.html')

@app.route('/store',methods=['POST'])
def storage():
    _nombre = request.form['textName']
    _correo = request.form['textCorreo']
    _foto = request.files['textFoto']
    #Guardamos en now los datos de fecha y hora
    now = datetime.now()
    #y en tiempo almacenamos una cadena con esos datos    
    tiempo = now.strftime("%m%d%Y")
    #si el nombre de la foto ha sido proporcionado en el form...
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
    #Guardamos la foto en la carpeta uploads.
    _foto.save("uploads/"+nuevoNombreFoto)
    #y armamos una tupla con esos valores:
    datos = (_nombre,_correo, nuevoNombreFoto)
    
    #Armamos la sentencia SQL que va a almacenar estos datos en la BD:
    sql = "INSERT INTO `sistema2`.`empleados` \
    (`id`,`nombre`,`correo`,`foto`)\
    VALUES (NULL, %s, %s, %s);"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
   
    
    return render_template('empleados/index.html')
    
if __name__=="__main__":
    app.run(debug=True, port=8050)
    #return render_template('empreados/create.html')
    