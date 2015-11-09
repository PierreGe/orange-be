from mobistar import mobistarAPI
import config

sms=mobistarAPI.EAPI(config.phone_nr,config.email)    #Initialize with your settings

# demande un token
sms.startRegistration()
# le user recoit le token par sms
code = input("Entrez le code reçu pas sms : ")
password, permanentKey = sms.verifyRegistration(code)

# on re-cré l'objet avec le password et permanentKey
sms=mobistarAPI.EAPI(config.phone_nr, config.email, password, permanentKey)    #Initialize with your settings

id = sms.sendSMS("+32494675432","Hello")

msisdn, status, statusId = sms.checkStatus(id)