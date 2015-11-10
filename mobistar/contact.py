import config
import difflib
import csv
import phonenumber


class GoogleContactsCSV(object):
    """docstring for Contacts"""
    def __init__(self):
        self.contactCsv = config.contactFile
        self.fullNamecontactDict = {}
        self.firstNamecontactDict = {}
        self._parseCsv()

    def _findBestNumber(self, list):
        """ """
        for phone in list:
            try:
                p = phonenumber.PhoneNumber(phone)
                return p
            except:
                pass

    def _parseCsv(self):
        """ """
        with open(self.contactCsv) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                firstname = row['First Name']
                fullName = row['First Name'] + " " +row['Last Name']
                number = self._findBestNumber([row['Primary Phone'], row['Mobile Phone'],row['Other Phone'], row['Home Phone'], row['Home Phone 2']])
                if number:
                    self.fullNamecontactDict[fullName] = number
                    self.firstNamecontactDict[firstname] = number

    def findClosestFullName(self, name):
        """ """
        winner = difflib.get_close_matches(name.capitalize(), self.fullNamecontactDict.keys(),1,0)
        return winner[0]

    def findClosestFirstname(self, name):
        """ """
        winner = difflib.get_close_matches(name.capitalize(), self.firstNamecontactDict.keys(),1,0)
        return winner[0]

    def getNumber(self,name):
        return self.fullNamecontactDict[name]
        

if __name__ == '__main__':
    c = GoogleContactsCSV()
    c.findClosest("phlaurentin ennechette") # closest math working :D