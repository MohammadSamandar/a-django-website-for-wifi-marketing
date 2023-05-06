from kavenegar import *
from shandizgalleria.settings import Kavenegar_API
from random import randint
from zeep import Client
from . import models
import datetime
import time
# from background_task import background



def send_otp(mobile, otp):
    mobile = [mobile, ]
    try:
        api = KavenegarAPI(Kavenegar_API)
        params = {
            'receptor': mobile,
            'template': 'sendsms',
            'token': otp,
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)

        # print(response)

    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


# @background(schedule=10)
def send_otp_soap(mobile, otp):

    time.sleep(10)
    client = Client('http://api.kavenegar.com/soap/v1.asmx?WSDL')
    receptor = [mobile, ]

    empty_array_placeholder = client.get_type('ns0:ArrayOfString')
    receptors = empty_array_placeholder()
    for item in receptor:
        receptors['string'].append(item)

    api_key = '685731774C596932364B416F782B7450324B6D2B6D3746456B575A474B71696B7175395A7A72745A4733303D'
    template = 'sendsms'
    token = 'Your OTP is {}'.format(otp)
    sender = '10008663'
    status = 0
    status_message = ''

    result = client.service.SendSimpleByApikey(api_key,template,
                                               sender,
                                               token,
                                               receptors,
                                               0,
                                               1,
                                               status,
                                               status_message)
    print(result)
    print('OTP: ', otp)


def get_random_otp():
    return randint(1000, 9999)


def check_otp_expiration(mobile):
    try:
        user = models.BusinessCustomer.objects.get(mobile=mobile)
        now = datetime.datetime.now()
        otp_time = user.otp_create_time
        diff_time = now - otp_time
        print('OTP TIME: ', diff_time)

        if diff_time.seconds > 60:
            return False
        return True

    except models.BusinessCustomer.DoesNotExist:
        return False

