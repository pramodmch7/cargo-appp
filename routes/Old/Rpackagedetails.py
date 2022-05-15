import base64
from io import BytesIO
from flask import Blueprint, jsonify, request, current_app as app, make_response
import uuid0 as ID
import jwt
# import datetime
from functools import wraps
from datetime import datetime
import qrcode
import qrcode.image.svg

from models.packagedetails import PackageDetails
from models.customerdetails import CustomerDetails
# from models.branch import BranchDetails
from models.userdetailsc import UserDetailC


PackageRoute = Blueprint('PackageRoute', __name__)


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
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = UserDetailC.query.filter_by(
                id=data['public_id']).first()
            # print(current_user.HUsrEmail)
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@PackageRoute.route('/api/gacpkg', methods=['GET'])
@token_required
def getCreatedPackages(current_user):
    # print(f'Current User - {current_user.Email}')
    # print(f'Current User - {current_user.Spare1}')
    Packages = PackageDetails.getStatusCodeP(7676)

    # print('Packages Route')
    data = []
    for index, package in enumerate(Packages):
        if not package.HPkgDeleted:
            print(current_user.HUsrLocation)
            # if package.HPkgToLocation == current_user.HUsrLocation or package.HPkgFromLocation == current_user.HUsrLocation or current_user.HUsrAdmin:
            if package.HPkgFromLocation == current_user.HUsrLocation:
                # print('Yes This Is 7676')
                Data = {}
                Data["slno"] = index+1
                Data['id'] = package.id
                Data['PN'] = package.HPkgName

                Data['PDIST'] = package.HPkgDistance
                Data['PW'] = package.HPkgWeight

                Data['PDD'] = package.HPkgActualDeliveryDate

                Data['PC'] = package.HPkgQrCode

                Data['PSF'] = package.HPkgStatusFromCreted
                Data['PSFC'] = package.HPkgStatusCodeFromCreted
                Data['PDISD'] = package.HPkgDispatchDate

                Data['PST'] = package.HPkgStatusToArrive
                Data['PSTC'] = package.HPkgStatusCodeToArrive
                Data['PAD'] = package.HPkgArrivingDate

                Data["PkgDates"] = {'Dheading': 'Date:', 'Dvalue': str(datetime.fromisoformat(str(package.HPkgCreatedDate)).date()),
                                    'ADheading': 'Delivery Date:', 'ADvalue': str(datetime.fromisoformat(str(package.HPkgApproximateDeliveryDate)).date())
                                    }
                Data['PkgcustomerF'] = {'Location': package.HPkgFromLocation,
                                        'Name': package.HPkgCustomerName,
                                        'Phone': package.HPkgCustomerMobile
                                        }
                Data['PkgcustomerT'] = {'Location': package.HPkgToLocation,
                                        'Name': package.HPkgCustomerToName,
                                        'Phone': package.HPkgCustomerToMobile
                                        }

                Data['pkgfilamt'] = {'TAheading': 'Total:',
                                     'TAvalue': package.HPkgTotalAmount,
                                     'APheading': 'Advance:',
                                     'APvalue': package.HPkgAdvanceAmount,
                                     'BAheading': 'Balance:',
                                     'BAvalue': package.HPkgBalanceAmount,
                                     'GST': package.HPkgGST,
                                     'GAheading': 'GST:',
                                     'GAvalue': package.HPkgGSTAmount,
                                     'FAheading': 'Final Amount:',
                                     'FAvalue': package.HPkgFinalAmount,
                                     }

                data.append(Data)
    # print(data)
    return{'message': data, 'status': 200}


@PackageRoute.route('/api/gadpkg', methods=['GET'])
@token_required
def getDispatchPackages(current_user):
    # print(f'Current User - {current_user.Email}')
    # print(f'Current User - {current_user.Spare1}')
    Packages = PackageDetails.getStatusCodeP(7677)

    # print('Packages Route')
    data = []
    for index, package in enumerate(Packages):
        if not package.HPkgDeleted:
            print(current_user.HUsrLocation)
            # if package.HPkgToLocation == current_user.HUsrLocation or package.HPkgFromLocation == current_user.HUsrLocation or current_user.HUsrAdmin:
            if package.HPkgFromLocation == current_user.HUsrLocation:
                # print('Yes This Is 7676')
                Data = {}
                Data["slno"] = index+1
                Data['id'] = package.id
                Data['PN'] = package.HPkgName

                Data['PDIST'] = package.HPkgDistance
                Data['PW'] = package.HPkgWeight

                Data['PDD'] = package.HPkgActualDeliveryDate

                Data['PC'] = package.HPkgQrCode

                Data['PSF'] = package.HPkgStatusFromCreted
                Data['PSFC'] = package.HPkgStatusCodeFromCreted
                Data['PDISD'] = package.HPkgDispatchDate

                Data['PST'] = package.HPkgStatusToArrive
                Data['PSTC'] = package.HPkgStatusCodeToArrive
                Data['PAD'] = package.HPkgArrivingDate

                Data["PkgDates"] = {'Dheading': 'Date:', 'Dvalue': str(datetime.fromisoformat(str(package.HPkgCreatedDate)).date()),
                                    'ADheading': 'Delivery Date:', 'ADvalue': str(datetime.fromisoformat(str(package.HPkgApproximateDeliveryDate)).date())
                                    }
                Data['PkgcustomerF'] = {'Location': package.HPkgFromLocation,
                                        'Name': package.HPkgCustomerName,
                                        'Phone': package.HPkgCustomerMobile
                                        }
                Data['PkgcustomerT'] = {'Location': package.HPkgToLocation,
                                        'Name': package.HPkgCustomerToName,
                                        'Phone': package.HPkgCustomerToMobile
                                        }

                Data['pkgfilamt'] = {'TAheading': 'Total:',
                                     'TAvalue': package.HPkgTotalAmount,
                                     'APheading': 'Advance:',
                                     'APvalue': package.HPkgAdvanceAmount,
                                     'BAheading': 'Balance:',
                                     'BAvalue': package.HPkgBalanceAmount,
                                     'GST': package.HPkgGST,
                                     'GAheading': 'GST:',
                                     'GAvalue': package.HPkgGSTAmount,
                                     'FAheading': 'Final Amount:',
                                     'FAvalue': package.HPkgFinalAmount,
                                     }

                data.append(Data)
    # print(data)
    return{'message': data, 'status': 200}


@PackageRoute.route('/api/gatpkg', methods=['GET'])
@token_required
def getTransitPackages(current_user):
    # print(f'Current User - {current_user.Email}')
    # print(f'Current User - {current_user.Spare1}')
    Packages = PackageDetails.getStatusCodeP(7677)

    # print('Packages Route')
    data = []
    for index, package in enumerate(Packages):
        if not package.HPkgDeleted:
            print(current_user.HUsrLocation)
            # if package.HPkgToLocation == current_user.HUsrLocation or package.HPkgFromLocation == current_user.HUsrLocation or current_user.HUsrAdmin:
            if package.HPkgToLocation == current_user.HUsrLocation:
                # print('Yes This Is 7676')
                Data = {}
                Data["slno"] = index+1
                Data['id'] = package.id
                Data['PN'] = package.HPkgName

                Data['PDIST'] = package.HPkgDistance
                Data['PW'] = package.HPkgWeight

                Data['PDD'] = package.HPkgActualDeliveryDate

                Data['PC'] = package.HPkgQrCode

                Data['PSF'] = package.HPkgStatusFromCreted
                Data['PSFC'] = package.HPkgStatusCodeFromCreted
                Data['PDISD'] = package.HPkgDispatchDate

                Data['PST'] = package.HPkgStatusToArrive
                Data['PSTC'] = package.HPkgStatusCodeToArrive
                Data['PAD'] = package.HPkgArrivingDate

                Data["PkgDates"] = {'Dheading': 'Date:', 'Dvalue': str(datetime.fromisoformat(str(package.HPkgCreatedDate)).date()),
                                    'ADheading': 'Delivery Date:', 'ADvalue': str(datetime.fromisoformat(str(package.HPkgApproximateDeliveryDate)).date())
                                    }
                Data['PkgcustomerF'] = {'Location': package.HPkgFromLocation,
                                        'Name': package.HPkgCustomerName,
                                        'Phone': package.HPkgCustomerMobile
                                        }
                Data['PkgcustomerT'] = {'Location': package.HPkgToLocation,
                                        'Name': package.HPkgCustomerToName,
                                        'Phone': package.HPkgCustomerToMobile
                                        }

                Data['pkgfilamt'] = {'TAheading': 'Total:',
                                     'TAvalue': package.HPkgTotalAmount,
                                     'APheading': 'Advance:',
                                     'APvalue': package.HPkgAdvanceAmount,
                                     'BAheading': 'Balance:',
                                     'BAvalue': package.HPkgBalanceAmount,
                                     'GST': package.HPkgGST,
                                     'GAheading': 'GST:',
                                     'GAvalue': package.HPkgGSTAmount,
                                     'FAheading': 'Final Amount:',
                                     'FAvalue': package.HPkgFinalAmount,
                                     }

                data.append(Data)
    # print(data)
    return{'message': data, 'status': 200}


@PackageRoute.route('/api/gaapkg', methods=['GET'])
@token_required
def getArrivePackages(current_user):
    # print(f'Current User - {current_user.Email}')
    # print(f'Current User - {current_user.Spare1}')
    Packages = PackageDetails.getStatusCodeP(7678)
    # print(Packages)
    print('Packages Arrived Route')
    data = []
    for index, package in enumerate(Packages):
        if not package.HPkgDeleted:
            print(current_user.HUsrLocation)
            # if package.HPkgToLocation == current_user.HUsrLocation or package.HPkgFromLocation == current_user.HUsrLocation or current_user.HUsrAdmin:
            if package.HPkgToLocation == current_user.HUsrLocation:
                print('Yes This Is 7678')
                Data = {}
                Data["slno"] = index+1
                Data['id'] = package.id
                Data['PN'] = package.HPkgName

                Data['PDIST'] = package.HPkgDistance
                Data['PW'] = package.HPkgWeight

                Data['PDD'] = package.HPkgActualDeliveryDate

                Data['PC'] = package.HPkgQrCode

                Data['PSF'] = package.HPkgStatusFromCreted
                Data['PSFC'] = package.HPkgStatusCodeFromCreted
                Data['PDISD'] = package.HPkgDispatchDate

                Data['PST'] = package.HPkgStatusToArrive
                Data['PSTC'] = package.HPkgStatusCodeToArrive
                Data['PAD'] = package.HPkgArrivingDate

                Data["PkgDates"] = {'Dheading': 'Date:', 'Dvalue': str(datetime.fromisoformat(str(package.HPkgCreatedDate)).date()),
                                    'ADheading': 'Delivery Date:', 'ADvalue': str(datetime.fromisoformat(str(package.HPkgApproximateDeliveryDate)).date())
                                    }
                Data['PkgcustomerF'] = {'Location': package.HPkgFromLocation,
                                        'Name': package.HPkgCustomerName,
                                        'Phone': package.HPkgCustomerMobile
                                        }
                Data['PkgcustomerT'] = {'Location': package.HPkgToLocation,
                                        'Name': package.HPkgCustomerToName,
                                        'Phone': package.HPkgCustomerToMobile
                                        }

                Data['pkgfilamt'] = {'TAheading': 'Total:',
                                     'TAvalue': package.HPkgTotalAmount,
                                     'APheading': 'Advance:',
                                     'APvalue': package.HPkgAdvanceAmount,
                                     'BAheading': 'Balance:',
                                     'BAvalue': package.HPkgBalanceAmount,
                                     'GST': package.HPkgGST,
                                     'GAheading': 'GST:',
                                     'GAvalue': package.HPkgGSTAmount,
                                     'FAheading': 'Final Amount:',
                                     'FAvalue': package.HPkgFinalAmount,
                                     }

                data.append(Data)
    # print(data)
    return{'message': data, 'status': 200}


@PackageRoute.route('/api/gadelpkg', methods=['GET'])
@token_required
def getDeliveredPackages(current_user):
    # print(f'Current User - {current_user.Email}')
    # print(f'Current User - {current_user.Spare1}')
    print('Packages Delivered Route')
    Packages = PackageDetails.getStatusCodeP(7679)
    # print(Packages)
    data = []
    for index, package in enumerate(Packages):
        if not package.HPkgDeleted:
            print(current_user.HUsrEmail)
            if package.HPkgToLocation == current_user.HUsrLocation or package.HPkgFromLocation == current_user.HUsrLocation or current_user.HUsrAdmin:
                # if package.HPkgToLocation == current_user.HUsrLocation:
                print('Yes This Is 7679')
                Data = {}
                Data["slno"] = index+1
                Data['id'] = package.id
                Data['PN'] = package.HPkgName

                Data['PDIST'] = package.HPkgDistance
                Data['PW'] = package.HPkgWeight

                Data['PDD'] = package.HPkgActualDeliveryDate

                Data['PC'] = package.HPkgQrCode

                Data['PSF'] = package.HPkgStatusFromCreted
                Data['PSFC'] = package.HPkgStatusCodeFromCreted
                Data['PDISD'] = package.HPkgDispatchDate

                Data['PST'] = package.HPkgStatusToArrive
                Data['PSTC'] = package.HPkgStatusCodeToArrive
                Data['PAD'] = package.HPkgArrivingDate

                Data["PkgDates"] = {'Dheading': 'Date:', 'Dvalue': str(datetime.fromisoformat(str(package.HPkgCreatedDate)).date()),
                                    'ADheading': 'Delivery Date:', 'ADvalue': str(datetime.fromisoformat(str(package.HPkgApproximateDeliveryDate)).date())
                                    }
                Data['PkgcustomerF'] = {'Location': package.HPkgFromLocation,
                                        'Name': package.HPkgCustomerName,
                                        'Phone': package.HPkgCustomerMobile
                                        }
                Data['PkgcustomerT'] = {'Location': package.HPkgToLocation,
                                        'Name': package.HPkgCustomerToName,
                                        'Phone': package.HPkgCustomerToMobile
                                        }

                Data['pkgfilamt'] = {'TAheading': 'Total:',
                                     'TAvalue': package.HPkgTotalAmount,
                                     'APheading': 'Advance:',
                                     'APvalue': package.HPkgAdvanceAmount,
                                     'BAheading': 'Balance:',
                                     #  'BAvalue': package.HPkgBalanceAmount,
                                     'BAvalue': 0,
                                     'GST': package.HPkgGST,
                                     'GAheading': 'GST:',
                                     'GAvalue': package.HPkgGSTAmount,
                                     'FAheading': 'Final Amount:',
                                     'FAvalue': package.HPkgFinalAmount,
                                     }

                data.append(Data)
    # print(data)
    return{'message': data, 'status': 200}


@PackageRoute.route('/api/gapkg', methods=['GET'])
@token_required
def getPackages(current_user):
    # print(f'Current User - {current_user.Email}')
    # print(f'Current User - {current_user.Spare1}')
    Packages = PackageDetails.getAllP()

    # print('Packages Route')
    data = []
    for index, package in enumerate(Packages):
        if not package.HPkgDeleted:
            print(current_user.HUsrLocation)
            if package.HPkgToLocation == current_user.HUsrLocation or package.HPkgFromLocation == current_user.HUsrLocation or current_user.HUsrAdmin:
                print('Yes This Is True')
                Data = {}
                Data["slno"] = index+1
                Data['id'] = package.id
                Data['PN'] = package.HPkgName
                # Data['PLOF'] = package.HPgefrom
                # Data['PLOT'] = package.HPgedesti
                Data['PDIST'] = package.HPkgDistance
                Data['PW'] = package.HPkgWeight
                # Data['PCD'] = package.HPgecredt
                # Data['PCFN'] = package.HPgecfname
                # Data['PCFP'] = package.HPgecfphone
                # Data['PADD'] = package.HPgeapxdelidt
                # Data['PCTN'] = package.HPgectname
                # Data['PCTP'] = package.HPgectphone
                Data['PDD'] = package.HPkgActualDeliveryDate
                # Data['PTA'] = package.HPgetamt
                # Data['PAA'] = package.HPgeaamt
                # Data['PBA'] = package.HPgebamt
                # Data['PG'] = package.HPgegst
                # Data['PGA'] = package.HPgegamt
                # Data['PFA'] = package.HPgefamt
                Data['PC'] = package.HPkgQrCode

                Data['PSF'] = package.HPkgStatusFromCreted
                Data['PSFC'] = package.HPkgStatusCodeFromCreted
                Data['PDISD'] = package.HPkgDispatchDate

                Data['PST'] = package.HPkgStatusToArrive
                Data['PSTC'] = package.HPkgStatusCodeToArrive
                Data['PAD'] = package.HPkgArrivingDate

                Data["PkgDates"] = {'Dheading': 'Date:', 'Dvalue': str(datetime.fromisoformat(str(package.HPkgCreatedDate)).date()),
                                    'ADheading': 'Delivery Date:', 'ADvalue': str(datetime.fromisoformat(str(package.HPkgApproximateDeliveryDate)).date())
                                    }
                Data['PkgcustomerF'] = {'Location': package.HPkgFromLocation,
                                        'Name': package.HPkgCustomerName,
                                        'Phone': package.HPkgCustomerMobile
                                        }
                Data['PkgcustomerT'] = {'Location': package.HPkgToLocation,
                                        'Name': package.HPkgCustomerToName,
                                        'Phone': package.HPkgCustomerToMobile
                                        }

                Data['pkgfilamt'] = {'TAheading': 'Total:',
                                     'TAvalue': package.HPkgTotalAmount,
                                     'APheading': 'Advance:',
                                     'APvalue': package.HPkgAdvanceAmount,
                                     'BAheading': 'Balance:',
                                     'BAvalue': package.HPkgBalanceAmount,
                                     'GST': package.HPkgGST,
                                     'GAheading': 'GST:',
                                     'GAvalue': package.HPkgGSTAmount,
                                     'FAheading': 'Final Amount:',
                                     'FAvalue': package.HPkgFinalAmount,
                                     }

                data.append(Data)
    # print(data)
    return{'message': data, 'status': 200}


# Actual Delivery Date (AcDeliveryDateD) should auto update when Package received at Destination and after scanning code


@PackageRoute.route('/api/anpkg', methods=['POST'])
@token_required
def addPackage(current_user):
    Data = request.get_json()
    # print(data)
    Id = str(ID.generate())
    Packages = PackageDetails.getAllP()
    # print(len(Packages))
    newUnique = 0
    if len(Packages) > 0:
        getOldStr = Packages[len(Packages)-1]
        OStr = int(getOldStr.HPkgUniqueNo.split('.')[1])
        newNum = OStr + 1
        newStr = 'COM.'
        newUnique = newStr+str(newNum)
    else:
        newStr = 'COM.'
        newNum = 1111
        newUnique = newStr+str(newNum)

    # print(f'newUnique - {newUnique}')

    # if method == 'basic':
    #     factory = qrcode.image.svg.SvgImage
    # elif method == 'fragment':
    #     factory = qrcode.image.svg.SvgFragmentImage
    # else:
    #     factory = qrcode.image.svg.SvgPathImage

    # factory = qrcode.image.svg.SvgPathImage

    img = qrcode.make(newUnique)

    buffered = BytesIO()
    img.save(buffered)
    buffered.seek(0)
    image_byte = buffered.getvalue()
    img_str = "data:image/png;base64," + base64.b64encode(image_byte).decode()

    # print(img_str)

    # print((img))

    PackageDate = datetime.fromisoformat(Data['PCD']).date()
    PackageCreatedDateTime = datetime.now()
    PackageDeliveryDate = datetime.fromisoformat(Data['PADD']).date()
    PackageStatusCode = 7676
    PackageStatus = "Created"
    PackageAllStatus = '7676~Created|'

    PackageGSTAmount = float(Data['PTA'])*float(Data['PGST'])/100

    print(Data['PADD'])
    print(type(PackageDeliveryDate))
    print(PackageDeliveryDate)

    NewPackage = PackageDetails(
        id=Id,  # String
        HPkgUniqueNo=newUnique,  # String
        HPkgCreatedDateTime=PackageCreatedDateTime,  # DateTime
        HPkgApproximateDeliveryDate=PackageDeliveryDate,  # Date
        HPkgAllStatus=PackageAllStatus,  # Text
        HPkgName=Data['PN'],  # String
        HPkgDistance='Distance',  # String
        HPkgWeight=Data['PW'],  # String
        HPkgQrCode=img_str,  # Text
        HPkgFromLocation=Data['PFL'],  # String
        HPkgCustomerName=Data['PCFN'],  # String
        HPkgCustomerMobile=Data['PCFP'],  # String
        HPkgToLocation=Data['PTL'],  # String
        HPkgCustomerToName=Data['PCTN'],  # String
        HPkgCustomerToMobile=Data['PCTP'],  # String
        HPkgCreatedDate=PackageDate,  # Date

        #############################################
        HPkgCreatedBy=current_user.HUsrEmail,  # String
        #############################################

        HPkgStatusFromCreted=PackageStatus,  # String
        HPkgStatusCodeFromCreted=PackageStatusCode,  # Integer
        HPkgTotalAmount=float(Data['PTA']),  # Float
        HPkgAdvanceAmount=float(Data['PAA']),  # Float
        HPkgBalanceAmount=float(Data['PTA'])-float(Data['PAA']),  # Float
        HPkgGST=Data['PGST'],  # Float
        HPkgGSTAmount=PackageGSTAmount,  # Float
        HPkgFinalAmount=float(Data['PTA']) + PackageGSTAmount,  # Float
    )

    PackageDetails.saveP(NewPackage)

    CId = str(ID.generate())
    Customers = len(CustomerDetails.getAllCustomer())
    NewCustomer = CustomerDetails(
        id=CId,
        HcustUniqueNo=f'CUST{Customers + 1}',
        HcustName=f"{Data['PCFN']}~{Data['PCTN']}",
        HcustPhone=f"{Data['PCFP']}~{Data['PCTP']}",
        HcustStatus=f"{'From'}~{'To'}",
        HcustLocation=f"{Data['PFL']}~{Data['PTL']}",
        HcustCreatedDate=datetime.today(),
        HcustCreatedDateTime=datetime.now(),
    )

    # CustomerDetails.saveCustomer(NewCustomer)

    return{'status': 200, 'message': 'Package Created', 'code': f'Created'}


@PackageRoute.route('/api/upkg/<id>', methods=['PUT'])
@token_required
def updatePackage(current_user, id):
    Data = request.get_json()

    Package = PackageDetails.getidP(id)

    if Package:

        PackageDate = datetime.fromisoformat(Data['PCD']).date()
        PackageDeliveryDate = datetime.fromisoformat(Data['PADD']).date()
        PackageGSTAmount = float(Data['PTA'])*float(Data['PGST'])/100

        print(PackageDeliveryDate)
        print(type(PackageDeliveryDate))
        print(Data['PADD'])

        Package.HPkgApproximateDeliveryDate = PackageDeliveryDate
        Package.HPkgName = Data['PN']
        Package.HPkgDistance = 'Distance'
        Package.HPkgWeight = Data['PW']
        Package.HPkgFromLocation = Data['PFL']
        Package.HPkgCustomerName = Data['PCFN']
        Package.HPkgCustomerMobile = Data['PCFP']
        Package.HPkgToLocation = Data['PTL']
        Package.HPkgCustomerToName = Data['PCTN']
        Package.HPkgCustomerToMobile = Data['PCTP']

        #############################################
        Package.HPkgUpdatedBy = current_user.HUsrEmail
        #############################################

        Package.HPkgTotalAmount = float(Data['PTA'])
        Package.HPkgAdvanceAmount = float(Data['PAA'])
        Package.HPkgBalanceAmount = float(Data['PTA'])-float(Data['PAA'])
        Package.HPkgGST = Data['PGST']
        Package.HPkgGSTAmount = PackageGSTAmount
        Package.HPkgFinalAmount = float(Data['PTA']) + PackageGSTAmount
        Package.HPkgUpdatedDate = datetime.today()
        Package.HPkgUpdatedDateTime = datetime.now()

        PackageDetails.updateP(Package)

    return{'status': 200, 'message': 'Package was Updated', 'code': f'Updated'}


@PackageRoute.route('/api/dpkg/<id>', methods=['DELETE', 'PUT'])
@token_required
def deletePackage(current_user, id):

    Package = PackageDetails.getidP(id)

    if Package:
        Package.HPkgDeleted = True
        PackageDetails.updateP(Package)

    return{'status': 200, 'message': 'Package was deleted', 'code': f'Deleted'}


@PackageRoute.route('/api/dispkg/<id>', methods=['DELETE', 'PUT'])
@token_required
def DispatchPackage(current_user, id):

    Package = PackageDetails.getidP(id)

    PackageStatusCode = 7677
    PackageStatus = "Dispatched^Arriving"
    PackageAllStatus = f'7676~Created|7677~{PackageStatus}|'
    PackageDispatchDate = datetime.now()

    if Package:
        Package.HPkgStatusFromCreted = PackageStatus
        Package.HPkgStatusCodeFromCreted = PackageStatusCode
        Package.HPkgAllStatus = PackageAllStatus

        Package.HPkgDispatchDate = datetime.today()
        Package.HPkgDispatchDateTime = PackageDispatchDate

        #############################################
        Package.HPkgDispatchBy = current_user.HUsrEmail
        ############################################

        PackageDetails.updateP(Package)

    return{'status': 200, 'message': 'Package has been dispatched', 'code': f'Dispatched'}


@PackageRoute.route('/api/trapkg/<id>', methods=['DELETE', 'PUT'])
@token_required
def TransitPackage(current_user, id):

    # print(id)
    print('Yes This is Transit Route')
    Package = PackageDetails.getidP(id)

    PackageStatusCode = 7678
    PackageStatus = "Arrived"
    PackageAllStatus = '7676~Created|7677~Dispatched^Arriving|7678~Arrived|'
    PackageArrivedDate = datetime.now()

    if Package:
        Package.HPkgStatusFromCreted = PackageStatus
        Package.HPkgStatusCodeFromCreted = PackageStatusCode
        Package.HPkgAllStatus = PackageAllStatus

        Package.HPkgArrivingDate = datetime.today()
        Package.HPkgArrivingDateTime = PackageArrivedDate

        #############################################
        Package.HPkgArrivingBy = current_user.HUsrEmail
        #############################################

        PackageDetails.updateP(Package)

    return{'status': 200, 'message': 'Package Arrived', 'code': f'Arrived'}


# @PackageRoute.route('/api/aripkg/<id>', methods=['DELETE', 'PUT'])
# @token_required
# def ArrivedPackage(current_user, id):

#     # print(id)

#     Package = PackageDetails.getidP(id)

#     PackageStatusCode = 7678
#     PackageStatus = "Arrived"
#     PackageAllStatus = '7676~Created|7677~Dispatched|7678~Arrived|'
#     PackageArrivedDate = datetime.now()

#     if Package:
#         Package.StatusToArrive = PackageStatus
#         Package.StatusCodeToArrive = PackageStatusCode
#         Package.HPkgAllStatus = PackageAllStatus

#         Package.HPkgArrivingDate = datetime.today()
#         Package.HPkgArrivingDateTime = PackageArrivedDate

#         #############################################
#         Package.HPkgArrivingBy = current_user.HUsrEmail
#         #############################################

#         # PackageDetails.updateP(Package)

#     return{'status': 200, 'message': 'Package Arrived', 'code': f'Arrived'}


@PackageRoute.route('/api/dilpkg/<id>', methods=['DELETE', 'PUT'])
@token_required
def DeliverPackage(current_user, id):

    Package = PackageDetails.getidP(id)

    PackageStatusCode = 7679
    PackageStatus = "Delivered"
    PackageAllStatus = '7676~Created|7677~Dispatched|7678~Arrived|7679~Delivered'
    PackageDeliverDate = datetime.now()

    if Package:

        Package.HPkgStatusFromCreted = PackageStatus
        Package.HPkgStatusCodeFromCreted = PackageStatusCode
        Package.HPkgAllStatus = PackageAllStatus

        Package.HPkgActualDeliveryDate = datetime.today()
        Package.HPkgActualDeliveryDateTime = PackageDeliverDate

        #############################################
        Package.HPkgDeliveredBy = current_user.HUsrEmail
        #############################################

        PackageDetails.updateP(Package)

    return{'status': 200, 'message': 'Package has been Delivered', 'code': f'Delivered'}
