# -*- coding: utf-8 -*-

from orange import api

try:
    import config
except:
    print("FATAL : configure the file config.py (rename config.py.sample to config.py and edit it)")

sms = api.EAPI(config.roaming, config.phone_nr, config.email, config.password,
                      config.permanentKey)  # Initialize with your settings

if not config.password:
    # ask for a token
    sms.startRegistration()
    # use receive a token by text
    code = input("Entrez le code reçu pas sms : ")
    password, permanentKey = sms.verifyRegistration(code)
    print("You can edit the config.py file now")
else:
    # we re-create the o password et permanentKey

    id = sms.sendSMS("+32484999999", "Hello")

    msisdn, status, statusId = sms.checkStatus(id)
    # print(sms.history())
