# from kavenegar import *
# # from custom_auth_daneshjooyar.settings import Kavenegar_API
# from random import randint
# # from zeep import Client
# # from . import models
# import datetime
# import time
# # from background_task import background
#
# # Create your tests here.
# def send_otp(mobile, otp):
#     # mobile = [mobile, ]
#     try:
#         api = KavenegarAPI('685731774C596932364B416F782B7450324B6D2B6D3746456B575A474B71696B7175395A7A72745A4733303D')
#         params = {
#             'receptor': "09014431228",
#             'template': 'sendsms',
#             'token': "1234",
#             'type': 'sms',  # sms vs call
#         }
#         response = api.verify_lookup(params)
#         print(response)
#
#     except APIException as e:
#         print(e)
#     except HTTPException as e:
#         print(e)