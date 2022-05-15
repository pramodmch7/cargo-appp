from flask import Blueprint, jsonify, request, current_app as app, make_response
import uuid0 as ID
import jwt
import datetime
from functools import wraps
from datetime import datetime

from models.branchdetails import *
from models.userdetailsc import *

BranchRoute = Blueprint('BranchRoute', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # print(token)
            # print(app.config['SECRET_KEY'])
            data = jwt.decode(
                token, app.config['SECRET_KEY'])
            # print(data)

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'])
            current_user = UserDetailC.query.filter_by(
                id=data['public_id']).first()
            # print(current_user.HUerem)
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@BranchRoute.route('/api/gabr', methods=['GET'])
@token_required
def getBranchs(current_user):
    Branchs = BranchDetails.getAllBranch()

    data = []
    for index, branch in enumerate(Branchs):
        # if current_user.HUeradmin == True or current_user.Admin == False:
        if not branch.HBrDeleted:
            Data = {}
            Data['slno'] = index+1
            Data['id'] = branch.id
            Data['BUN'] = branch.HBrUniqueNo
            Data['BN'] = branch.HBrName
            Data['LO'] = branch.HBrLocation
            Data['AD'] = branch.HBrAddress
            Data['PH'] = branch.HBrPhone
            Data['LT'] = branch.HBrLatitude
            Data['LG'] = branch.HBrLongitude
            Data['User'] = branch.HBrAuthorisedUser
            # Data['CD'] = branch.HBrCreatedDate

            data.append(Data)
        # else:
        #     return{'message': 'You Are Not Admin', 'status': 200}

    return{'message': data, 'status': 200}


@BranchRoute.route('/api/anbr', methods=['POST'])
@token_required
def addBranch(current_user):
    data = request.get_json()
    # print(data)
    if current_user.HUsrAdmin == True:
        Branchs = len(BranchDetails.getAllBranch())
        CheckBranch = BranchDetails.getNameBranch(data['BN'])
        if not CheckBranch:
            Id = str(ID.generate())
            BrachCodeGen = f'BRAN{Branchs + 1}'
            NewBranch = BranchDetails(
                id=Id,
                HBrUniqueNo=BrachCodeGen,
                HBrName=data['BN'],
                HBrLocation=data['LO'],
                HBrAddress=data['AD'],
                HBrPhone=data['PH'],
                HBrLatitude=data['LT'],
                HBrLongitude=data['LG'],
                HBrAuthorisedUser=data['User'],
                HBrCreatedDate=datetime.datetime.today(),
                HBrCreatedDateTime=datetime.datetime.now()
            )

            BranchDetails.saveBranch(NewBranch)

            AUser = UserDetailC.getEmailUserC(data['User'])

            if AUser:
                # print('Successfuly Got Search User Name Email form DB')
                AUser.HUsrLocation = data['LO']
                UserDetailC.updateUserC(AUser)
            return{'status': 200, 'message': 'New Branch Created', 'code': f'Created'}
        else:
            return{'status': 202, 'message': 'Branch is Already Exists', 'code': f'Exists'}
    return{'status': 401, 'message': 'You Are Not Admin', 'code': f'Unauthorize'}


@BranchRoute.route('/api/edbr/<id>', methods=['PUT'])
@token_required
def updateBranch(current_user, id):
    if current_user.HUsrAdmin == True:
        # print('Yes Branch Edit Route!')
        # print(id)

        data = request.get_json()
        # print(data)

        BranchUpdate = BranchDetails.getidBranch(id)

        if BranchUpdate:
            BranchUpdate.HBrName = data['BN']
            BranchUpdate.HBrLocation = data['LO']
            BranchUpdate.HBrAddress = data['AD']
            BranchUpdate.HBrPhone = data['PH']
            BranchUpdate.HBrLatitude = data['LT']
            BranchUpdate.HBrLongitude = data['LG']
            BranchUpdate.HBrAuthorisedUser = data['User']
            BranchUpdate.HBrUpdatedDate = datetime.datetime.today()
            BranchUpdate.HBrUpdatedDateTime = datetime.datetime.now()

            BranchDetails.updateBranch(BranchUpdate)

            AUser = UserDetailC.getEmailUserC(data['User'])

            if AUser:
                # print('Successfuly Got Search User Name Email form DB')
                AUser.HUsrLocation = data['LO']
                UserDetailC.updateUserC(AUser)

            return{'status': 200, 'message': 'Branch Updated', 'code': f'Updated'}
    return{'status': 200, 'message': 'You Are Not Authorized', 'code': f'Unauthorised'}
    # print(request)

    # auth = request.authorization
    # # print(auth)
    # if not auth or not auth.username or not auth.password:
    #     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # user = UserDetails.query.filter_by(Email=auth.username).first()

    # if not user:
    #     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # # if check_password_hash(user.password, auth.password):
    # if user.Password == auth.password:
    #     token = jwt.encode({'public_id': user.id, 'exp': datetime.datetime.utcnow(
    #     ) + datetime.timedelta(minutes=25)}, app.config['SECRET_KEY'])
    #     print(token.decode('utf-8'))
    #     return jsonify({'token': token.decode('utf-8'), 'roles': [1001], 'user': user.Email})

    # return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@BranchRoute.route('/api/dbr/<id>', methods=['DELETE', 'PUT'])
@token_required
def deleteBranch(current_user, id):
    if current_user.HUsrAdmin == True:
        # print('Yes Branch Edit Route!')
        # print(id)

        # data = request.get_json()
        # print(data)

        BranchUpdate = BranchDetails.getidBranch(id)

        if BranchUpdate:
            BranchUpdate.HBrDeleted = True
            BranchUpdate.HBrUpdatedDate = datetime.datetime.today()
            BranchUpdate.HBrUpdatedDateTime = datetime.datetime.now()

            BranchDetails.updateBranch(BranchUpdate)

            return{'status': 200, 'message': 'Branch Deleted', 'code': f'Deleted'}
    return{'status': 200, 'message': 'You Are Not Authorized', 'code': f'Unauthorised'}
