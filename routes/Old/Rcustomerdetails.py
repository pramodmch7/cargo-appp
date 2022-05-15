from flask import Blueprint, jsonify, request, current_app as app, make_response
import uuid0 as ID
import jwt
import datetime
from functools import wraps
from datetime import datetime

from models.customerdetails import *
from models.userdetailsc import UserDetailC


CustomerRoute = Blueprint('CustomerRoute', __name__)


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
            # print(current_user.Email)
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@CustomerRoute.route('/api/gacu', methods=['GET'])
@token_required
def getCustomers(current_user):
    Customers = CustomerDetails.getAllCustomer()

    data = []
    for index, customer in enumerate(Customers):
        if current_user.HUsrAdmin == True or current_user.HUsrAdmin == False:
            Data = {}
            Data2 = {}
            Data['slno'] = index+1
            Data['id'] = customer.id
            Data['CN'] = customer.HcustName.split('~')[0]
            Data['CPH'] = customer.HcustPhone.split('~')[0]
            Data['CSF'] = customer.HcustStatus.split('~')[0]
            Data['LO'] = customer.HcustLocation.split('~')[0]
            data.append(Data)

            Data2['slno'] = index+2
            Data2['id'] = customer.id
            Data2['CN'] = customer.HcustName.split('~')[1]
            Data2['CPH'] = customer.HcustPhone.split('~')[1]
            Data2['CSF'] = customer.HcustStatus.split('~')[1]
            Data2['LO'] = customer.HcustLocation.split('~')[1]
            data.append(Data2)
        # else:
        #     return{'message': 'You Are Not Admin', 'status': 200}

    return{'message': data, 'status': 200}
