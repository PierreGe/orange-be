# Orange.be API
A python written interface to send sms using orange.be's API
 
## First Use

#### First config your email and phone number in config.

`phone_nr='049999999'`

`email='lol@lol.com'`

(Note :There won't be an email verification, so it does not need to be correct)

#### Then ask for a token

`sms=api.EAPI(config.phone_nr,config.email) `

`sms.startRegistration()`

You will receive a 4 digit code by text .

(Note : Do not leak it, Mobistar does not provide an easy way to revoke it)

#### Get your password and permanent key. 

`code` is the four digit received by text.

`password, permanentKey = sms.verifyRegistration(code)`

Congrats, you're all set.

## Send Text

####Create an object mobistarAPI

`sms=api.EAPI(config.phone_nr, config.email, password, permanentKey)`

####Send the actual text

`id = sms.sendSMS("+32494675432","Hello dear friend")`

#### And if you would like, you can check your text status :

`msisdn, status, statusId = sms.checkStatus(id)`

## Requirements

See `requirements.txt`
