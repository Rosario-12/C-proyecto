from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
#rosario2junio.mysql.pythonanywhere-services.com
#app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://rosario2junio:prueba1234@rosario2junio.mysql.pythonanywhere-services.com/rosario2junio$proyecto'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/agendamedica'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino las tablas
class Paciente(db.Model):   # la clase Producto hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    apellido=db.Column(db.String(100))
    edad=db.Column(db.Integer)
    imagen=db.Column(db.String(400))
    def __init__(self,nombre,apellido,edad,imagen):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.apellido=apellido
        self.edad=edad
        self.imagen=imagen




    #  si hay que crear mas tablas , se hace aqui




with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class PacienteSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido','edad','imagen')




paciente_schema=PacienteSchema()            # El objeto producto_schema es para traer un producto
pacientes_schema=PacienteSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto




# crea los endpoint o rutas (json)
@app.route('/paciente',methods=['GET'])
def get_Paciente():
    all_paciente=Paciente.query.all()         # el metodo query.all() lo hereda de db.Model
    result=pacientes_schema.dump(all_paciente)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla




@app.route('/paciente/<id>',methods=['GET'])
def get_paciente(id):
    paciente=Paciente.query.get(id)
    return paciente_schema.jsonify(paciente)   # retorna el JSON de un producto recibido como parametro


@app.route('/paciente/<id>',methods=['DELETE'])
def delete_paciente(id):
    paciente=Paciente.query.get(id)
    db.session.delete(paciente)
    db.session.commit()                     # confirma el delete
    return paciente_schema.jsonify(paciente) # me devuelve un json con el registro eliminado


@app.route('/paciente', methods=['POST']) # crea ruta o endpoint
def create_paciente():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    edad=request.json['edad']
    imagen=request.json['imagen']
    new_paciente=Paciente(nombre,apellido,edad,imagen)
    db.session.add(new_paciente)
    db.session.commit() # confirma el alta
    return paciente_schema.jsonify(new_paciente)


@app.route('/paciente/<id>' ,methods=['PUT'])
def update_paciente(id):
    paciente=Paciente.query.get(id)
 
    paciente.nombre=request.json['nombre']
    paciente.apellido=request.json['apellido']
    paciente.edad=request.json['edad']
    paciente.imagen=request.json['imagen']


    db.session.commit()    # confirma el cambio
    return paciente_schema.jsonify(paciente)    # y retorna un json con el producto
 


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000



