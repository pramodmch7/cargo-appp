from dataclasses import dataclass
from modulefinder import packagePathMap
import os
from flask import Blueprint, jsonify, request, current_app as app, make_response, send_from_directory
from models.packageinfo import PackageinfoDetails
from werkzeug.utils import secure_filename
import json
import datetime
import uuid0 as ID
import jwt

from codes.packageinfodicGen import Convert_Format
from codes.AuthToken import token_required

FReports = Blueprint('FReports', __name__)


@FReports.route('/api/getreport/<id>', methods=['GET'])
@token_required
def getPIReports(current_user, id):
    DBData = PackageinfoDetails.getAll()

    FDate = id.split('~')[0]
    LDate = id.split('~')[1]

    DBDateData = PackageinfoDetails.getByDates(FDate, LDate)

    data = []
    if len(DBDateData) > 0:
        for index, _data in enumerate(DBDateData):
            if current_user.HUsrAdmin == True:
                Data = Convert_Format(index, _data)
                data.append(Data)
        return{'message': data, 'status': 200}
    return make_response(jsonify({'message': []}), 200)
