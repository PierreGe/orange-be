# -*- coding: utf-8 -*-



class PhoneNumberHandler(object):
    # ITU-T Telephone Code for ISO 3166-1 2 Letter Code
    INTL_PREFIX = {'+673': 'BN', '+670': 'TL', '+1-684': 'AS', '+676': 'TO', '+677': 'SB', '+674': 'NR', '+675': 'PG',
                   '+678': 'VU', '+679': 'FJ', '+500': 'FK', '+27': 'ZA', '+1-767': 'DM', '+1-284': 'VG', '+48': 'PL',
                   '+49': 'DE', '+968': 'OM', '+966': 'SA', '+45': 'DK', '+964': 'IQ', '+965': 'KW', '+962': 'JO',
                   '+382': 'ME', '+960': 'MV', '+43': 'AT', '+250': 'RW', '+251': 'ET', '+252': 'SO', '+253': 'DJ',
                   '+254': 'KE', '+255': 'TZ', '+256': 'UG', '+257': 'BI', '+258': 'MZ', '+421': 'SK', '+1-876': 'JM',
                   '+91': 'IN', '+1-473': 'GD', '+377': 'MC', '+376': 'AD', '+375': 'BY', '+374': 'AM', '+373': 'MD',
                   '+372': 'EE', '+371': 'LV', '+370': 'LT', '+92': 'PK', '+379': 'VA', '+378': 'SM', '+672': 'NF',
                   '+90': 'TR', '+971': 'AE', '+970': 'PS', '+973': 'BH', '+972': 'IL', '+975': 'BT', '+974': 'QA',
                   '+977': 'NP', '+976': 'MN', '+243': 'CD', '+242': 'CG', '+241': 'GA', '+240': 'GQ', '+247': 'AC',
                   '+246': 'IO', '+245': 'GW', '+244': 'AO', '+249': 'SD', '+248': 'SC', '+1-670': 'MP', '+996': 'KG',
                   '+995': 'GE', '+994': 'AZ', '+993': 'TM', '+992': 'TJ', '+1-787 and 1-939': 'PR', '+998': 'UZ',
                   '+66': 'TH', '+64': 'NZ', '+65': 'SG', '+62': 'ID', '+1-268': 'AG', '+60': 'MY', '+61': 'CC',
                   '+1-264': 'AI', '+1-784': 'VC', '+1-868': 'TT', '+1-649': 'TC', '+1-664': 'MS', '+90-392': 'CY',
                   '+1-441': 'BM', '+967': 'YE', '+886': 'TW', '+218': 'LY', '+216': 'TN', '+212': 'EH', '+213': 'DZ',
                   '+599': 'AN', '+98': 'IR', '+359': 'BG', '+358': 'FI', '+93': 'AF', '+354': 'IS', '+357': '',
                   '+356': 'MT', '+351': 'PT', '+350': 'GI', '+353': 'IE', '+352': 'LU', '+690': 'TK', '+691': 'FM',
                   '+692': 'MH', '+856': 'LA', '+855': 'KH', '+852': 'HK', '+853': 'MO', '+850': 'KP', '+269': 'KM',
                   '+501': 'BZ', '+502': 'GT', '+503': 'SV', '+7': 'RU', '+505': 'NI', '+506': 'CR', '+507': 'PA',
                   '+261': 'MG', '+509': 'HT', '+263': 'ZW', '+262': 'RE', '+265': 'MW', '+264': 'NA', '+267': 'BW',
                   '+291': 'ER', '+1-246': 'BB', '+47': 'SJ', '+1-242': 'BS', '+40': 'RO', '+963': 'SY', '+41': 'CH',
                   '+593': 'EC', '+590': 'GP', '+592': 'GY', '+81': 'JP', '+82': 'KR', '+961': 'LB', '+84': 'VN',
                   '+591': 'BO', '+86': 'CN', '+683': 'NU', '+682': 'CK', '+681': 'WF', '+680': 'PW', '+687': 'NC',
                   '+686': 'KI', '+685': 'WS', '+597': 'SR', '+689': 'PF', '+688': 'TV', '+355': 'AL', '+299': 'GL',
                   '+1-671': 'GU', '+290': 'TA', '+95': 'MM', '+44': 'JE', '+94': 'LK', '+358-18': 'AX', '+238': 'CV',
                   '+239': 'ST', '+373-533': 'MD', '+232': 'SL', '+233': 'GH', '+230': 'MU', '+231': 'LR', '+236': 'CF',
                   '+237': 'CM', '+234': 'NG', '+235': 'TD', '+297': 'AW', '+596': 'MQ', '+34': 'ES', '+36': 'HU',
                   '+31': 'NL', '+30': 'GR', '+33': 'FR', '+32': 'BE', '+39': 'IT', '+374-97': 'AZ', '+595': 'PY',
                   '+46': 'SE', '+63': 'PH', '+594': 'GF', '+598': 'UY', '+1-345': 'KY', '+1-340': 'VI', '+423': 'LI',
                   '+266': 'LS', '+20': 'EG', '+268': 'SZ', '+1': 'US', '+1-809 and 1-829': 'DO', '+226': 'BF',
                   '+504': 'HN', '+1-869': 'KN', '+222': 'MR', '+880': 'BD', '+508': 'PM', '+260': 'ZM', '+298': 'FO',
                   '+1-758': 'LC', '+58': 'VE', '+57': 'CO', '+56': 'CL', '+55': 'BR', '+54': 'AR', '+53': 'CU',
                   '+52': 'MX', '+51': 'PE', '+225': 'CI', '+224': 'GN', '+227': 'NE', '+420': 'CZ', '+221': 'SN',
                   '+220': 'GM', '+223': 'ML', '+389': 'MK', '+386': 'SI', '+387': 'BA', '+385': 'HR', '+229': 'BJ',
                   '+228': 'TG', '+380': 'UA', '+381': 'CS'}

    class InvalidNumber(Exception):
        pass

    def __init__(self, numberasstr):
        if isinstance(numberasstr, PhoneNumberHandler):
            self._intlPrefix = numberasstr._intlPrefix
            self._number = numberasstr._number
            self._country = numberasstr._country
        else:
            prefix = PhoneNumberHandler._findPrefix(numberasstr)
            self._intlPrefix = prefix
            self._number = numberasstr.replace(prefix, "")
            self._country = PhoneNumberHandler.INTL_PREFIX[prefix]

    @staticmethod
    def _findPrefix(number):
        """ find the prefix in a intl number (ITU-T Telephone Code) """
        for prefix in PhoneNumberHandler.INTL_PREFIX:
            if number[:len(prefix)] == prefix:
                return prefix
        raise PhoneNumberHandler.InvalidNumber("Unable to find prefix for: " + str(number))

    def getIntlPrefix(self):
        """ get intl prefix"""
        return self._intlPrefix

    def getCountry(self):
        """get ISO 3166-1 2 Letter Code for country """
        return self._country

    def __str__(self):
        """ str(PhoneNumber) """
        return self._intlPrefix + self._number

    def __len__(self):
        """ Lengh of phone number"""
        return len(self._intlPrefix) + len(self._number)


if __name__ == '__main__':
    p = PhoneNumberHandler("+33691454545")
    print(p._intlPrefix)
    print(p._number)
    print(p._country)
