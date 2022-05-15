from tkinter import Pack
from flask import Blueprint, jsonify, request, current_app as app, make_response, send_from_directory
import json
import datetime
import uuid0 as ID
import jwt
import qrcode
import qrcode.image.svg
import base64
from io import BytesIO
import os
import re
from PyPDF2 import PdfFileMerger, PdfFileReader


from models.packageinfo import *
from models.userdetailsn import UserdetailsnDetails
from models.transportationinfo import TransportationinfoDetails
from models.customerdetails import CustomerDetails
from codes.packageinfodicGen import *
from codes.AuthToken import token_required
from codes.PDFData import pdfData
from codes.GeneratePDF import GenPDF, PDF
from codes.DownloadDoc import DownloadFile

PackageinfoRoute = Blueprint('PackageinfoRoute', __name__)


@PackageinfoRoute.route('/api/gapkg', methods=['GET'])
@token_required
def getAllPackages(current_user):
    DBData = PackageinfoDetails.getAll()
    data = []
    for index, _data in enumerate(DBData):
        if not _data.HPkgDeleted:
            if current_user.HUsrAdmin or _data.HPkgLocationFrom == current_user.HUsrLocation:
                Data = Convert_Format(index, _data)
                data.append(Data)

    return{'message': data, 'status': 200}


@PackageinfoRoute.route('/api/gacpkg', methods=['GET'])
@token_required
def getCreatedPackages(current_user):
    DBData = PackageinfoDetails.getStatusCodeP(7676)
    data = []
    for index, _data in enumerate(DBData):
        if not _data.HPkgDeleted:
            if _data.HPkgLocationFrom == current_user.HUsrLocation or current_user.HUsrAdmin:
                Data = Convert_Format(index, _data)
                data.append(Data)
    # print(data)
    return{'message': data, 'status': 200}


@PackageinfoRoute.route('/api/gadpkg', methods=['GET'])
@token_required
def getDispatchPackages(current_user):
    DBData = PackageinfoDetails.getStatusCodeP(7677)
    data = []
    for index, _data in enumerate(DBData):
        if not _data.HPkgDeleted:
            if _data.HPkgLocationFrom == current_user.HUsrLocation or current_user.HUsrAdmin:
                Data = Convert_Format(index, _data)
                data.append(Data)
    # print(data)
    return{'message': data, 'status': 200}


@PackageinfoRoute.route('/api/gatpkg', methods=['GET'])
@token_required
def getTransitPackages(current_user):
    DBData = PackageinfoDetails.getStatusCodeP(7677)
    data = []
    for index, _data in enumerate(DBData):
        if not _data.HPkgDeleted:
            if _data.HPkgLocationTo == current_user.HUsrLocation or current_user.HUsrAdmin:
                Data = Convert_Format(index, _data)
                data.append(Data)
    # print('I am coming form Transit Package. Route is "atpkg"')
    # print(data)
    return{'message': data, 'status': 200}


@PackageinfoRoute.route('/api/gaapkg', methods=['GET'])
@token_required
def getArrivePackages(current_user):
    DBData = PackageinfoDetails.getStatusCodeP(7678)
    data = []
    for index, _data in enumerate(DBData):
        if not _data.HPkgDeleted:
            if _data.HPkgLocationTo == current_user.HUsrLocation or current_user.HUsrAdmin:
                Data = Convert_Format(index, _data)
                data.append(Data)
    # print(data)
    return{'message': data, 'status': 200}


@PackageinfoRoute.route('/api/gadelpkg', methods=['GET'])
@token_required
def getDeliveredPackages(current_user):
    DBData = PackageinfoDetails.getStatusCodeP(7679)
    data = []
    for index, _data in enumerate(DBData):
        if not _data.HPkgDeleted:
            if _data.HPkgLocationFrom == current_user.HUsrLocation or current_user.HUsrAdmin or _data.HPkgLocationTo == current_user.HUsrLocation:
                Data = Convert_Format(index, _data)
                data.append(Data)
    # print(data)
    return{'message': data, 'status': 200}


@PackageinfoRoute.route('/api/anpkg', methods=['POST'])
@token_required
def AddNewData(current_user):
    data = request.get_json()
    Id = str(ID.generate())
    fileId = str(ID.generate())

    UNumber = f'Pkg{len(PackageinfoDetails.getAll())+1}'

    serialNo = None

    if len(PackageinfoDetails.getAll()) <= 0:
        serialNo = '00001'
    else:
        serialNo = format(
            int(PackageinfoDetails.getAll()[-1].HPkgLRNo) + 1, '05d')

    img = qrcode.make(UNumber)

    buffered = BytesIO()
    img.save(buffered)
    buffered.seek(0)
    image_byte = buffered.getvalue()
    img_str = "data:image/png;base64," + base64.b64encode(image_byte).decode()

    PackageDate = datetime.fromisoformat(data['PCD']).date()
    PackageCreatedDateTime = datetime.now()
    PackageDeliveryDate = datetime.fromisoformat(data['PADD']).date()
    PackageStatusCode = 7676
    PackageStatus = "Created"
    PackageAllStatus = '7676~Created|'
    AdvanceAmt = 0
    if data['hpkgadvanceamount'] != '':
        AdvanceAmt = data['hpkgadvanceamount']

    NewData = PackageinfoDetails(
        id=Id,
        HPkgLRNo=serialNo,
        HPkgName=data['hpkgname'],
        HPkgWeight=data['hpkgweight'],
        HPkgFragile=data['hpkgfragile'],
        HPkgCustomerFromName=data['hpkgcustomerfromname'],
        HPkgLocationFrom=data['hpkglocationfrom'],
        HPkgPhoneFrom=data['hpkgphonefrom'],
        HPkgCustomerToName=data['hpkgcustomertoname'],
        HPkgLocationTo=data['hpkglocationto'],
        HPkgPhoneTo=data['hpkgphoneto'],
        HPkgArticlesCount=data['hpkgarticlescount'],
        HPkgTransportingCharges=data['hpkgtransportingcharges'],
        HPkgLoadingCharges=data['hpkgloadingcharges'],
        HPkgApproximateDeliveryDate=PackageDeliveryDate,
        HPkgAdvanceAmount=AdvanceAmt,
        HPkgBalanceAmount=float(data['hpkgtransportingcharges'])+float(
            data['hpkgloadingcharges'])-float(AdvanceAmt),
        HPkgStatusFrom=PackageStatus,
        HPkgStatusCodeFrom=PackageStatusCode,
        HPkgAllStatus=PackageAllStatus,
        HPkgQrCode=img_str,
        HPkgCreatedD=datetime.today().date(),
        HPkgCreatedDT=datetime.today(),
        HPkgCreatedBy=current_user.HUsrEmail,
        HPkgSlipName=fileId
    )
    PackageinfoDetails.saveDB(NewData)

    Data = pdfData(current_user, serialNo, AdvanceAmt, data)

    PDF()
    PDFName = GenPDF(serialNo, datetime.today().date(), Data, fileId)

    CId = str(ID.generate())
    Customers = len(CustomerDetails.getAllCustomer())
    NewCustomer = CustomerDetails(
        id=CId,
        HcustUniqueNo=f'CUST{Customers + 1}',
        HcustName=data['hpkgcustomerfromname'],
        HcustPhone=data['hpkgphonefrom'],
        HcustStatus='From',
        HcustLocation=data['hpkglocationfrom'],
        HcustCreatedDate=datetime.today(),
        HcustCreatedDateTime=datetime.now(),
    )

    CustomerDetails.saveCustomer(NewCustomer)

    CId = str(ID.generate())
    Customers = len(CustomerDetails.getAllCustomer())
    NewCustomer = CustomerDetails(
        id=CId,
        HcustUniqueNo=f'CUST{Customers + 1}',
        HcustName=data['hpkgcustomertoname'],
        HcustPhone=data['hpkgphoneto'],
        HcustStatus='To',
        HcustLocation=data['hpkglocationto'],
        HcustCreatedDate=datetime.today(),
        HcustCreatedDateTime=datetime.now(),
    )

    CustomerDetails.saveCustomer(NewCustomer)

    return{'status': 200, 'message': 'New Data Added', 'code': f'Created'}


@PackageinfoRoute.route('/api/dowlsfile/<id>', methods=['GET'])
@token_required
def DownloadLSFile(current_user, id):
    DBData = PackageinfoDetails.getById(id)

    data = DownloadFile(
        FileNameId=DBData.HPkgSlipName,
        patha=app.config['upload_path'],
        FileName=f"{DBData.HPkgCustomerFromName}-{DBData.HPkgPhoneFrom}-{DBData.HPkgLocationFrom}"
    )

    return data


@PackageinfoRoute.route('/api/gdpidata', methods=['GET'])
@token_required
def GetDefaultData(current_user):
    DBData = PackageinfoDetails.getAll()

    serialNo = None

    if len(PackageinfoDetails.getAll()) <= 0:
        serialNo = '00001'
    else:
        serialNo = format(
            int(PackageinfoDetails.getAll()[-1].HPkgLRNo) + 1, '05d')

    data = {
        'ledserno': serialNo,
        'leddate': datetime.today().strftime('%d/%m/%Y'),
        'leduser': current_user.HUsrFirstName,
        'ledloc': current_user.HUsrLocation
    }

    return{'message': data, 'status': 200}


@PackageinfoRoute.route('/api/blkdispkg', methods=['PUT'])
@token_required
def getBulkDispatchedPackages(current_user):
    Data = request.get_json()
    # print(Data)
    for pkgDis in Data['data']:

        Package = PackageinfoDetails.getById(pkgDis['id'])

        PackageStatusCode = 7677
        PackageStatus = "Dispatched^Arriving"
        PackageAllStatus = f'7676~Created|7677~{PackageStatus}|'
        PackageDispatchDate = datetime.now()

        if Package:
            print(pkgDis['id'])
            Package.HPkgStatusFrom = PackageStatus
            Package.HPkgStatusCodeFrom = PackageStatusCode
            Package.HPkgAllStatus = PackageAllStatus

            Package.HPkgTravelsDetails = Data['SelectedTravel']['id']
            Package.HPkgVehicleDetails = Data['BusNumber']

            Package.HPkgDispatchD = datetime.today().date()
            Package.HPkgDispatchDT = PackageDispatchDate
            Package.HPkgDispatchBy = current_user.HUsrEmail

            PackageinfoDetails.updateDB(Package)

    return{'status': 200, 'message': 'Package has been dispatched', 'code': f'Dispatched'}


@PackageinfoRoute.route('/api/blktrapkg', methods=['PUT'])
@token_required
def getBulkTransitPackages(current_user):
    Data = request.get_json()
    # print(Data)
    for pkgDis in Data['data']:

        Package = PackageinfoDetails.getById(pkgDis['id'])

        PackageStatusCode = 7678
        PackageStatus = "Arrived"
        PackageAllStatus = '7676~Created|7677~Dispatched^Arriving|7678~Arrived|'
        PackageArrivedDate = datetime.now()

        if Package:
            Package.HPkgStatusFrom = PackageStatus
            Package.HPkgStatusCodeFrom = PackageStatusCode
            Package.HPkgAllStatus = PackageAllStatus

            Package.HPkgArrivingD = datetime.today().date()
            Package.HPkgArrivingDT = PackageArrivedDate
            Package.HPkgArrivingBy = current_user.HUsrEmail

            PackageinfoDetails.updateDB(Package)

    return{'status': 200, 'message': 'Package has been dispatched', 'code': f'In Transit'}


@PackageinfoRoute.route('/api/blkdilpkg', methods=['PUT'])
@token_required
def getBulkDeliverPackages(current_user):
    Data = request.get_json()
    # print(Data)
    for pkgDis in Data['data']:

        Package = PackageinfoDetails.getById(pkgDis['id'])

        PackageStatusCode = 7679
        PackageStatus = "Delivered"
        PackageAllStatus = '7676~Created|7677~Dispatched|7678~Arrived|7679~Delivered|'
        PackageDeliverDate = datetime.now()

        if Package:
            Package.HPkgStatusFrom = PackageStatus
            Package.HPkgStatusCodeFrom = PackageStatusCode
            Package.HPkgAllStatus = PackageAllStatus
            Package.HPkgBalAmtReceived = float(Package.HPkgTransportingCharges) + float(
                Package.HPkgLoadingCharges) - float(Package.HPkgAdvanceAmount)
            Package.HPkgDeliveryD = datetime.today().date()
            Package.HPkgDeliveryDT = PackageDeliverDate
            Package.HPkgDeliveredBy = current_user.HUsrEmail

            PackageinfoDetails.updateDB(Package)

    return{'status': 200, 'message': 'Package has been dispatched', 'code': f'Delivered'}


@PackageinfoRoute.route('/api/udata/<id>', methods=['PUT'])
@token_required
def UpdateData(current_user, id):
    data = request.get_json()
    DBData = PackageinfoDetails.getById(id)
    if DBData:
        DBData.HPkgLRNo = data['hpkglrno']
        DBData.HPkgCustomerFromName = data['hpkgcustomerfromname']
        DBData.HPkgLocationFrom = data['hpkglocationfrom']
        DBData.HPkgPhoneFrom = data['hpkgphonefrom']
        DBData.HPkgCustomerToName = data['hpkgcustomertoname']
        DBData.HPkgLocationTo = data['hpkglocationto']
        DBData.HPkgPhoneTo = data['hpkgphoneto']
        DBData.HPkgArticlesCount = data['hpkgarticlescount']
        DBData.HPkgTransportingCharges = data['hpkgtransportingcharges']
        DBData.HPkgLoadingCharges = data['hpkgloadingcharges']
        DBData.HPkgApproximateDeliveryDate = data['hpkgapproximatedeliverydate']
        DBData.HPkgAdvanceAmount = data['hpkgadvanceamount']
        DBData.HPkgBalanceAmount = data['hpkgbalanceamount']
        DBData.HPkgStatusFrom = data['hpkgstatusfrom']
        DBData.HPkgStatusCodeFrom = data['hpkgstatuscodefrom']
        DBData.HPkgAllStatus = data['hpkgallstatus']
        DBData.HPkgQrCode = data['hpkgqrcode']
        DBData.HPkgCreatedD = datetime.datetime.today.date()
        DBData.HPkgCreatedDT = datetime.datetime.today()
        DBData.HPkgCreatedBy = current_user.HUsrEmail
        PackageinfoDetails.updateDB(PackageinfoDetails)
    return{'status': 200, 'message': 'Data Updated', 'code': f'Update'}