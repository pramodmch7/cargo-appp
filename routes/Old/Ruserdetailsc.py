from flask import Blueprint, jsonify, request, current_app as app, make_response
import uuid0 as ID
import jwt
import datetime
from datetime import datetime

from models.userdetailsc import *
# from models.usersnew import *

UserRoute = Blueprint('UserRoute', __name__)


@UserRoute.route('/api/gau', methods=['GET'])
def getMigrateUser():
    NewUsers = UserDetailC.getAllUserC()

    data = []
    for index, user in enumerate(NewUsers):

        Data = {}
        Data['slno'] = index+1
        Data['id'] = user.id
        Data['FN'] = user.HUsrFirstName
        Data['LN'] = user.HUsrLastName
        Data['MN'] = user.HUsrMiddleName
        Data['EM'] = user.HUsrEmail
        Data['PH'] = user.HUsrPhone
        Data['AD'] = user.HUsrAdmin
        Data['ACT'] = user.HUsrActive
        Data['RN'] = user.HUsrRoleName
        Data['RCD'] = user.HUsrCreatedDate
        Data['RCDT'] = user.HUsrCreatedDateTime
        Data['AV'] = user.HUsrAvatar
        Data['LO'] = user.HUsrLocation

        data.append(Data)

    return{'message': data, 'status': 200}


@UserRoute.route('/api/anu', methods=['POST', 'PUT'])
def MigrateUser():
    Data = request.get_json()
    # print(json.load(data))
    # data = json.loads(Adata)
    # print(data)
    # print(request.POST)

    if request.method == 'POST':

        for data in Data:
            Users = len(UserDetailC.getAllUserC())
            # print(Data)
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

            # Id = str(ID.generate())
            # print(Users)
            NewUser = UserDetailC(
                id=data['id'],
                HUsrUniqueNo=f'USER{Users + 1}',
                HUsrFirstName=data['FN'],
                HUsrLastName=data['LN'],
                HUsrMiddleName=data['MN'],
                HUsrPhone=data['PH'],
                HUsrEmail=data['EM'],
                HUsrPassword=data['PWD'],
                HUsrAdmin=AdminB,
                HUsrActive=ActiveB,
                HUsrRoleName=data['RN'],
                HUsrAvatar=data['AV'],
                HUsrCreatedDate=datetime.datetime.today(),
                HUsrCreatedDateTime=datetime.datetime.now(),
            )

            UserDetailC.saveUserC(NewUser)

    # if request.method == 'PUT':
    #     print('Yes PUT Method')
    #     for data in Data:
    #         getOriginalData = UserNewDetails.getidNU(data['id'])

    #         if getOriginalData:
    #             getOriginalData.Migrat = 'Migrated'
    #             getOriginalData.MigratedD = datetime.date.today()
    #             getOriginalData.Migrated = datetime.datetime.now()
    #             getOriginalData.updateNU()

    return{'status': 200, 'message': 'New User Added', 'code': f'Created'}


@UserRoute.route('/api/login', methods=['POST'])
def Login():

    print('Yes Login Route!')

    print(request)

    auth = request.authorization
    # print(auth)
    if not auth or not auth.username or not auth.password:
        # return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        return jsonify({'message': 'Please enter valid email and password', 'status': 401})

    user = UserDetailC.query.filter_by(HUsrEmail=auth.username).first()

    if not user:
        # return make_response('Could not verify', 501, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        return jsonify({'message': 'Please enter valid email', 'status': 501})

    # if check_password_hash(user.password, auth.password):
    if user.HUsrPassword == auth.password:
        token = jwt.encode({'public_id': user.id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=250)}, app.config['SECRET_KEY'])
        print(token.decode('utf-8'))
        if user.HUsrAdmin:
            return jsonify({'token': token.decode('utf-8'), 'roles': [1001, 1002], 'user': user.HUsrEmail})

        return jsonify({'token': token.decode('utf-8'), 'roles': [1002], 'user': user.HUsrEmail})

    # return make_response('Could not verify', 601, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    return jsonify({'message': 'Could not verify. Please try again', 'status': 601})


'''
@UserRoute.route('/api/gau', methods=['GET'])
def getUsers():
    Users = UserDetailC.getAllNU()

    data = []
    for index, user in enumerate(Users):

        Data = {}
        Data['slno'] = index+1
        Data['FN'] = user.FirstName
        Data['LN'] = user.LastName
        Data['MN'] = user.MiddleName
        Data['AC'] = user.Access
        Data['ACT'] = user.isActive
        Data['RN'] = user.RoleName
        Data['CD'] = user.CreatedD
        Data['AV'] = user.Avatar
        Data['EM'] = user.Email
        # Data['Location'] = user.Location

        data.append(Data)

    return{'message': data, 'status': 200}


@UserRoute.route('/api/anu', methods=['POST'])
def addUser():
    Data = request.get_json()

    if request.method == 'POST':

        for data in Data:
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

            NewUser = UserDetailC(
                id=data['id'],
                FirstName=data['FN'],
                LastName=data['LN'],
                MiddleName=data['MN'],
                Email=data['EM'],
                UserPassword=data['PWD'],
                Admin=AdminB,
                isActive=ActiveB,
                RoleName=data['RN'],
                Avatar=data['AV'],
            )

            UserDetailC.saveUserC(NewUser)

    # if request.method == 'PUT':
    #     print('Yes PUT Method')
    #     for data in Data:
    #         getOriginalData = UserNewDetails.getidNU(data['id'])

    #         if getOriginalData:
    #             getOriginalData.Migrat = 'Migrated'
    #             getOriginalData.MigratedD = datetime.date.today()
    #             getOriginalData.Migrated = datetime.datetime.now()
    #             getOriginalData.updateNU()

    return{'status': 200, 'message': 'New User Added', 'code': f'Created'}


@UserRoute.route('/api/login', methods=['POST'])
def Login():

    print('Yes Login Route!')

    print(request)

    auth = request.authorization
    # print(auth)
    if not auth or not auth.username or not auth.password:
        # return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        return jsonify({'message': 'Please enter valid email and password', 'status': 401})

    user = UserNewDetails.query.filter_by(Email=auth.username).first()

    if not user:
        # return make_response('Could not verify', 501, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        return jsonify({'message': 'Please enter valid email', 'status': 501})

    # if check_password_hash(user.password, auth.password):
    if user.UserPassword == auth.password:
        token = jwt.encode({'public_id': user.id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=250)}, app.config['SECRET_KEY'])
        print(token.decode('utf-8'))
        if user.Admin:
            return jsonify({'token': token.decode('utf-8'), 'roles': [1001, 1002], 'user': user.Email})

        return jsonify({'token': token.decode('utf-8'), 'roles': [1002], 'user': user.Email})

    # return make_response('Could not verify', 601, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    return jsonify({'message': 'Could not verify. Please try again', 'status': 601})
'''
