from flask import Blueprint, jsonify, request, current_app as app, make_response
import json
import datetime
import uuid0 as ID
import jwt

from models.userdetailsn import *
from codes.userdetailsndicGen import *
from codes.AuthToken import token_required

UserdetailsnRoute = Blueprint('UserdetailsnRoute', __name__)


@UserdetailsnRoute.route('/api/gauserdata', methods=['GET'])
@token_required
def GetAll(current_user):
    DBData = UserdetailsnDetails.getAllAsc('HUsrFirstName')
    data = []
    for index, _data in enumerate(DBData):
        Data = Convert(index, _data)
        data.append(Data)
    return{'message': data, 'status': 200}


@UserdetailsnRoute.route('/api/guserdata/<email>', methods=['GET'])
@token_required
def GetUser(current_user, email):
    DBData = [UserdetailsnDetails.getByEmail(email)]
    data = []
    for index, _data in enumerate(DBData):
        Data = Convert(index, _data)
        data.append(Data)
    return{'message': data, 'status': 200}


@UserdetailsnRoute.route('/api/sec/anuserdata', methods=['POST'])
def AddNewUser():
    Data = request.get_json()

    for data in Data:
        Users = len(UserdetailsnDetails.getAll())
        # print(data['AD'])
        AdminB = None
        if data['AD'] == 'true':
            AdminB = True
        else:
            AdminB = False

        ActiveB = None
        if data['ACT'] == 'true':
            ActiveB = True
        else:
            ActiveB = False
        # print(data)
        NewUser = UserdetailsnDetails(
            id=data['id'],
            HUsrUniqueNo=f'USER{Users + 1}',
            HUsrFirstName=data['FN'],
            HUsrLastName=data['LN'],
            HUsrAddress=data['ADD'],
            HUsrPhone=data['PH'],
            HUsrEmail=data['EM'],
            HUsrPassword=data['PWD'],
            HUsrAdmin=data['AD'],
            HUsrActive=data['ACT'],
            HUsrRoleName=data['RN'],
            HUsrRoleId=data['RI'],
            HUsrAvatar=data['AV'],
            HUsrCreatedD=datetime.datetime.today(),
            HUsrCreatedDT=datetime.datetime.now(),
        )
        UserdetailsnDetails.saveDB(NewUser)
    return{'status': 200, 'message': 'New User Added', 'code': f'Created'}


@UserdetailsnRoute.route('/api/uuserdata/<id>', methods=['PUT'])
@token_required
def UpdateUser(current_user, id):
    data = request.get_json()
    DBData = UserdetailsnDetails.getById(id)
    if DBData:
        DBData.HUsrUniqueNo = data['husruniqueno']
        DBData.HUsrFirstName = data['husrfirstname']
        DBData.HUsrLastName = data['husrlastname']
        DBData.HUsrPhone = data['husrphone']
        DBData.HUsrAddress = data['husraddress']
        DBData.HUsrEmail = data['husremail']
        DBData.HUsrPassword = data['husrpassword']
        DBData.HUsrAdmin = data['husradmin']
        DBData.HUsrActive = data['husractive']
        DBData.HUsrRoleId = data['husrrolenumber']
        DBData.HUsrRoleName = data['husrrolename']
        DBData.HUsrAvatar = data['husravatar']
        DBData.HUsrCreatedD = data['HUsrCreatedD']
        DBData.HUsrCreatedDT = data['HUsrCreatedDT']
        UserdetailsnDetails.updateDB(UserdetailsnDetails)
    return{'status': 200, 'message': 'Data Updated', 'code': f'Update'}


@UserdetailsnRoute.route('/api/desuserdata/<id>', methods=['PUT'])
@token_required
def DissableUser(current_user, id):
    data = request.get_json()
    DBData = UserdetailsnDetails.getById(id)
    status_message = None
    if DBData:
        DBData.HUsrActive = False
        status_message = 'User Dissabled'
        UserdetailsnDetails.updateDB(UserdetailsnDetails)
    return{'status': 200, 'message': status_message, 'code': f'Dissabled'}


@UserdetailsnRoute.route('/api/enauserdata/<id>', methods=['PUT'])
@token_required
def EnableUser(current_user, id):
    data = request.get_json()
    DBData = UserdetailsnDetails.getById(id)
    status_message = None
    if DBData:
        DBData.HUsrActive = True
        status_message = 'User Enabled'
        UserdetailsnDetails.updateDB(UserdetailsnDetails)
    return{'status': 200, 'message': status_message, 'code': f'Enabled'}
