from colorama import Cursor
from flask import Flask
from flask import render_template,request
from flaskext.mysql import MySQL
from flask import redirect
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
 conn=mysql.connect() #Nos conectamos a la base de datos
 cursor=conn.cursor() #Sobre el cursor vamos a realizar 
 sql="SELECT * FROM `sistema2`.`empleados`;" #"SELECT * FROM `sistema2`.`empleados`;
 cursor.execute(sql) #Ejecutamos la sentencia SQL sobre el cursor.
 db_empleados = cursor.fetchall()
 conn.commit()#cerramos la conexion 
    #Devolvemos codigo HTML para ser renderizado.
 return render_template('empleados/index.html', empleados = db_empleados)

@app.route('/destroy/<int:id>')
def destroy(id):
 sql= "DELETE FROM `sistema2`.`empleados` WHERE id=%s;"
 conn=mysql.connect()
 cursor=conn.cursor() #id: any
 Cursor.execute(sql,(id))
 conn.commit()
 return redirect("/")

@app.route('/edit/<int:id>')
def edit(id):
 conn=mysql.connect()
 cursor=conn.cursor() #id: any
 Cursor.execute("SELECT * FROM `sistema2`.`empleados`WHERE id=%s;", (id))
 # sql= "SELECT FROM `sistema2`.`empleados`WHERE id=%s;"
 empleados= cursor.fetchall()
 conn.commit()
 return render_template('empleados/edit.html', empleados = empleados)
  
@app.route('/create')
def create():
 return render_template('empleados/create.html')

@app.route('/store',methods=['POST'])
def storage():
    _nombre = request.form['txtName']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
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
    
@app.route('/update',methods=['POST'])
def update():
    _nombre = request.form['txtName']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id=request.form['txtFoto']
    sql = "UPDATE `sistema2`.`empleados` SET `nombre`=%s `correo`=%s `correo`=%s WHERE d=;"
    datos=(_nombre,_correo,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
if __name__=="__main__":
    app.run(debug=True)
    #return render_template('empreados/create.html')
    