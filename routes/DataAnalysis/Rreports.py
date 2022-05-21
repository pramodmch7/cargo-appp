
import os
from flask import Blueprint, jsonify, request, current_app as app, make_response, send_from_directory
from models.packageinfo import PackageinfoDetails
from werkzeug.utils import secure_filename
import json
import datetime
import uuid0 as ID
import jwt
from sqlalchemy import func, extract
from sqlalchemy.sql import text, select

from codes.packageinfodicGen import Convert, Convert_Format
from codes.AuthToken import token_required

FReports = Blueprint('FReports', __name__)


@FReports.route('/api/getreport/<dates>', methods=['GET'])
@token_required
def getPIReports(current_user, dates):
    DBData = PackageinfoDetails.getAll()

    FDate = dates.split('~')[0]
    LDate = dates.split('~')[1]

    # @classmethod
    # def getBikeCount(cls):
    #     return cls.query.with_entities(cls.HProinBikeID, func.count(cls.HProinBikeID)).group_by(cls.HProinBikeID).all()

    # @classmethod
    # def getByDates(cls, fdate, ldate):
    #     return cls.query.filter(cls.HPkgCreatedD.between(fdate, ldate)).all()

    DBDateData = PackageinfoDetails.query.filter(
        PackageinfoDetails.HPkgCreatedD.between(FDate, LDate)).all()

    # columns = [text('id'), text('HPkgLocationFrom'), text('HPkgCreatedD')]

    # for fd in DBDateData:
    #     print('*'*52)
    #     BranchBrekupData = fd.query(
    #         select(from_obj=PackageinfoDetails, columns=columns)).all()

    #     print(BranchBrekupData)

    DatesData = PackageinfoDetails.query.with_entities(

        func.count(PackageinfoDetails.HPkgLocationFrom),
        func.sum(PackageinfoDetails.HPkgTransportingCharges +
                 PackageinfoDetails.HPkgLoadingCharges),
        func.sum(PackageinfoDetails.HPkgAdvanceAmount),
        func.sum(PackageinfoDetails.HPkgBalanceAmount)
    ).filter(PackageinfoDetails.HPkgCreatedD.between(FDate, LDate)).all()

    BranchBrekupData = PackageinfoDetails.query.with_entities(
        PackageinfoDetails.HPkgLocationFrom,
        func.count(PackageinfoDetails.HPkgLocationFrom),
        func.sum(PackageinfoDetails.HPkgTransportingCharges +
                 PackageinfoDetails.HPkgLoadingCharges),
        func.sum(PackageinfoDetails.HPkgAdvanceAmount),
        func.sum(PackageinfoDetails.HPkgBalanceAmount)
    ).filter(PackageinfoDetails.HPkgCreatedD.between(FDate, LDate)).group_by(PackageinfoDetails.HPkgLocationFrom).all()

    # print(DatesData)

    # print(BranchBrekupData)

    # print(DBDateData)

    # CehckDBData = PackageinfoDetails.getBranchGroups(FDate, LDate)
    # print(len(CehckDBData))
    # for a in CehckDBData:
    #     print(a.HPkgLocationFrom)
    # print(len(DBDateData))

    Data = {
        'HHUDates': f"{FDate} to {LDate}",
        'HHUData': [
            {
                'HHUCount': '',
                'HHUTA': '',
                'HHUAA': '',
                'HHUBA': '',
            },
            [],
            []
        ],
    }
    for index, _data in enumerate(DatesData):
        Data['HHUData'][0]['HHUCount'] = _data[0]
        Data['HHUData'][0]['HHUTA'] = _data[1]
        Data['HHUData'][0]['HHUAA'] = _data[2]
        Data['HHUData'][0]['HHUBA'] = _data[3]

    for index, _Bdata in enumerate(BranchBrekupData):
        # print(_Bdata)
        DataJ = {}
        DataJ['slno'] = index+1
        DataJ['LF'] = _Bdata[0]
        DataJ['CO'] = _Bdata[1]
        DataJ['TA'] = _Bdata[2]
        DataJ['AA'] = _Bdata[3]
        DataJ['BA'] = _Bdata[4]
        Data['HHUData'][1].append(DataJ)

    data = []
    if len(DBDateData) > 0:
        for index, _data in enumerate(DBDateData):
            if current_user.HUsrAdmin == True:
                DatA = Convert(index, _data)
                # print('*'*52)
                # print(Data)
                # print('*'*52)
                data.append(DatA)
        Data['HHUData'][2] = data
    return{'message': Data, 'status': 200}

    # return make_response(jsonify({'message': data}), 200)
    # return{'message': data, 'status': 200}

    return make_response(jsonify({'message': []}), 200)


@FReports.route('/api/getreporty/<dates>', methods=['GET'])
@token_required
def getPIReportsYear(current_user, dates):

    # DBDateData = PackageinfoDetails.query.filter(
    #     PackageinfoDetails.HPkgCreatedD.between(FDate, LDate)).all()

    YearBrekupData = PackageinfoDetails.query.with_entities(
        PackageinfoDetails.HPkgLocationFrom,
        func.count(PackageinfoDetails.HPkgLocationFrom),
        func.sum(PackageinfoDetails.HPkgTransportingCharges +
                 PackageinfoDetails.HPkgLoadingCharges),
        func.sum(PackageinfoDetails.HPkgAdvanceAmount),
        func.sum(PackageinfoDetails.HPkgBalanceAmount)
    ).filter(func.strftime('%Y', PackageinfoDetails.HPkgCreatedD) == dates).group_by(PackageinfoDetails.HPkgLocationFrom).all()

    # .with_entities(
    #         PackageinfoDetails.HPkgLocationFrom,
    #         func.count(PackageinfoDetails.HPkgLocationFrom),
    #         func.sum(PackageinfoDetails.HPkgTransportingCharges +
    #                  PackageinfoDetails.HPkgLoadingCharges),
    #         func.sum(PackageinfoDetails.HPkgAdvanceAmount),
    #         func.sum(PackageinfoDetails.HPkgBalanceAmount)
    #     )

    # YearBrekupData = PackageinfoDetails.query.filter(
    #     extract('year', PackageinfoDetails.HPkgCreatedD) == dates).group_by(PackageinfoDetails.HPkgLocationFrom).all()

    # print('*'*52)
    # print(func.strftime('%Y', PackageinfoDetails.HPkgCreatedD) == dates)
    # print(extract('year', PackageinfoDetails.HPkgCreatedD))
    # print('*'*52)
    print(YearBrekupData)

    # data = []
    # if len(DBDateData) > 0:
    #     for index, _data in enumerate(DBDateData):
    #         if current_user.HUsrAdmin == True:
    #             Data = Convert(index, _data)
    #             data.append(Data)
    #     # return make_response(jsonify({'message': data}), 200)
    #     return{'message': data, 'status': 200}

    return make_response(jsonify({'message': []}), 200)


@FReports.route('/api/getreportym/<dates>', methods=['GET'])
@token_required
def getPIReportsYM(current_user, dates):
    DBData = PackageinfoDetails.getAll()

    Year = dates.split('~')[0]
    Month = dates.split('~')[1]

    # @classmethod
    # def getBikeCount(cls):
    #     return cls.query.with_entities(cls.HProinBikeID, func.count(cls.HProinBikeID)).group_by(cls.HProinBikeID).all()

    # @classmethod
    # def getByDates(cls, fdate, ldate):
    #     return cls.query.filter(cls.HPkgCreatedD.between(fdate, ldate)).all()

    # DBDateData = PackageinfoDetails.query.filter(
    #     PackageinfoDetails.HPkgCreatedD.between(FDate, LDate)).all()

    # columns = [text('id'), text('HPkgLocationFrom'), text('HPkgCreatedD')]

    # for fd in DBDateData:
    #     print('*'*52)
    #     BranchBrekupData = fd.query(
    #         select(from_obj=PackageinfoDetails, columns=columns)).all()

    #     print(BranchBrekupData)

    YearMonBrekupData = PackageinfoDetails.query.with_entities(
        PackageinfoDetails.HPkgLocationFrom,
        func.count(PackageinfoDetails.HPkgLocationFrom),
        func.sum(PackageinfoDetails.HPkgTransportingCharges +
                 PackageinfoDetails.HPkgLoadingCharges),
        func.sum(PackageinfoDetails.HPkgAdvanceAmount),
        func.sum(PackageinfoDetails.HPkgBalanceAmount)
    ).filter(func.strftime('%Y', PackageinfoDetails.HPkgCreatedD) == Year, func.strftime('%m', PackageinfoDetails.HPkgCreatedD) == Month).group_by(PackageinfoDetails.HPkgLocationFrom).all()

    print(YearMonBrekupData)

    # print(DBDateData)

    # CehckDBData = PackageinfoDetails.getBranchGroups(FDate, LDate)
    # print(len(CehckDBData))
    # for a in CehckDBData:
    #     print(a.HPkgLocationFrom)
    # print(len(DBDateData))
    # data = []
    # if len(DBDateData) > 0:
    #     for index, _data in enumerate(DBDateData):
    #         if current_user.HUsrAdmin == True:
    #             Data = Convert(index, _data)
    #             # print('*'*52)
    #             # print(Data)
    #             # print('*'*52)
    #             data.append(Data)
    #     # return make_response(jsonify({'message': data}), 200)
    #     return{'message': data, 'status': 200}

    return make_response(jsonify({'message': []}), 200)
