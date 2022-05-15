from flask import Flask, app, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from db import db

from routes.Rpackageinfo import *
from routes.Rcustomerdetails import *
from routes.Rbranchinfo import *
from routes.Ruser import *
from routes.Ruserdetailsn import *
from routes.Rtransportationinfo import *
from routes.DataAnalysis.Ruserhome import UserHome
from routes.DataAnalysis.Rreports import FReports

# from resources.Rusersnew import *
# from resources.Rroles import *


app = Flask(__name__, static_folder='./build', static_url_path='/')
# app = Flask(__name__)
CORS(app)
migrate = Migrate(app, db)
# app.config['SQLALCHEMY_DATABASE_URI'] = postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Cargodata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'key'
app.config['upload_path'] = 'D:\\1Projects\\Komitla\\Cargo-AppV7\\cargo-backend\\pdfAsset\\CRecip'

db.init_app(app)


@app.before_first_request
def createTabels():
    db.create_all()


@app.errorhandler(404)
def notFound(e):
    return app.send_static_file('index.html')


@app.route('/')
def home():
    # return 'HanUmaN'
    return app.send_static_file('index.html')


app.register_blueprint(PackageinfoRoute)
app.register_blueprint(CustomerRoute)
app.register_blueprint(BranchinfoRoute)
app.register_blueprint(UserdetailsnRoute)
app.register_blueprint(TransportationinfoRoute)
app.register_blueprint(UserRoute)
app.register_blueprint(UserHome)
app.register_blueprint(FReports)


if __name__ == '__main__':
    #from db import db
    # db.init_app(app)
    app.run(host='0.0.0.0', debug=True, port='5012')
