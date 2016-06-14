# -*- coding: utf-8 -*-

import requests
from .phonenumber import PhoneNumberHandler
from xml.dom.minidom import parseString
from xml.sax.saxutils import escape


class EAPI(object):
    """An Orange (be) API client"""
    error = {
        100: "STATUS_SUCCESS",  # OK
        199: "STATUS_GENERAL_ERROR",  # General Error
        401: "STATUS_INVALID_MESSAGE_TYPE",  # Invalid message type
        402: "STATUS_INVALID_MESSAGE_ID",  # Invalid message id
        403: "STATUS_INVALID_DATE_FORMAT"  # Invalid date format
    }

    def __init__(self, roaming, phoneNumber, email, password="", permanentKey=""):
        self.url = "https://mobistar.msgsend.com/mmp/cp3"
        self._roaming = roaming
        self.password = password
        self.permanentKey = permanentKey
        self.phonenr = PhoneNumberHandler(phoneNumber)
        self.email = email

    def _authentication(self):
        """ Authentication method is with permanentKey """
        if len(self.phonenr) > 0 and len(self.permanentKey) > 0:
            return "<authentication>\n<username>" + str(
                self.phonenr) + "</username>\n<permanentKey>" + self.permanentKey + "</permanentKey>\n</authentication>\n";
        raise ValueError("No phone number and/or permanent key")

    def _request(self, content):
        HEADERS = {'Content-Type': 'application/xml', 'charset': 'UTF-8'}
        return requests.post(self.url, headers=HEADERS, data=content, verify=True)

    def _send_xml(self, code):
        """ Used for sending XML request to the server. """
        xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        xml += "<cp version=\"3.0\" locale=\"en-US\" timezone=\"UTC+1\" clientVersion=\"1.1\" clientProduct=\"eapi\">\n"
        xml += code + "\n</cp>\n"
        req = self._request(xml)
        if req.status_code != 200:
            raise Exception("Html request failed")
        print(req.text)
        DOMTree = parseString(req.text)
        response = DOMTree.documentElement
        if response.hasAttribute("code"):
            if not (int(response.getAttribute("code")) == 100):
                errorcode = int(response.getAttribute("code"))
                raise Exception("Api result: " + str(errorcode) + " = " + EAPI.error[errorcode])
        else:
            raise Exception("Unexcpected response from api")
        return req.text

    def startRegistration(self):
        """ Start registration using phone number and email"""
        xml = "<startRegistration msisdn=\"" + str(self.phonenr) + "\" email=\"" + self.email + "\"/>";
        self._send_xml(xml);
        # at this step, an sms was received by user

    def verifyRegistration(self, code):
        """Get password, permanentKey after you enter the code received on the phone"""
        xml = "<verifyRegistration msisdn=\"" + str(self.phonenr) + "\" pincode=\"" + code + "\" />"
        data = self._send_xml(xml)

        DOMTree = parseString(data)
        response = DOMTree.documentElement
        password = response.getElementsByTagName("password")[0].childNodes[0].data
        permanentKey = response.getElementsByTagName("permanentKey")[0].childNodes[0].data

        return password, permanentKey

    def sendSMS(self, recipient, text):
        # Add authentication (this is permanent key authentication described here)
        recipient = PhoneNumberHandler(recipient)  # important
        if recipient.getCountry() != self.phonenr.getCountry() and not self._roaming:
            class RoamingForbiddenException(Exception):
                pass
            raise RoamingForbiddenException("Roaming disabled in config")
        xml = self._authentication()
        # Add send message, this is the action we want to make
        xml += "<sendMessage>\n"
        # Add message type     
        xml += "<message type=\"SMS\">\n<text>" + escape(text) + "</text>\n"
        # Add recipients
        xml += "<recipients>\n"
        xml += "<recipient type=\"to\" addressType=\"msisdn\">" + str(recipient) + "</recipient>\n"
        xml += "</recipients>\n</message>\n</sendMessage>"
        data = self._send_xml(xml);
        DOMTree = parseString(data)
        response = DOMTree.documentElement
        messageID = response.getElementsByTagName("message")[0].childNodes[0].data
        return messageID

    def checkStatus(self, msg_id):
        """Check status of messages sent """
        xml = self._authentication()
        xml += "<statusReport>\n"
        xml += "<message messageId=\"" + msg_id + "\"/>\n"
        xml += "</statusReport>";

        data = self._send_xml(xml)
        DOMTree = parseString(data)
        response = DOMTree.documentElement
        recipients = response.getElementsByTagName('recipient')
        for recipient in recipients:
            if recipient.hasAttribute("status"):
                msisdn = recipient.getAttribute("msisdn")
                status = recipient.getAttribute("status")
                statusId = recipient.getAttribute("statusId")
        return msisdn, status, statusId

    def requestCapacity(self):
        """ Request API enabled capabilities
        Mobistar : <sms singleReplacementOfSpecialCharacters="1" specialCharacterSize="2" multipleLength="153" 
        spannedLength="5000" multipleLengthWithSpecialCharacters="153" singleLengthWithSpecialCharacters="160" 
        encoding="UTF-8" singleLength="160" spannedLengthWithSpecialCharacters="5000"/>
        """
        xml = self._authentication()
        xml += "<getCapabilities/>"
        data = self._send_xml(xml)
        return str(data)

    def history(self):
        """ Get the last 50 messages send trough this api"""
        xml = self._authentication()
        xml += "<history type=\"SMS\" maxResults=\"50\" />"
        data = self._send_xml(xml)
        return str(data)
