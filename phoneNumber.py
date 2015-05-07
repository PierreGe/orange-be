class PhoneNumber(object):
    class Invalid(Exception):
        pass
    class NotABelgianNumber(Exception):
        pass

    def __init__(self, text, int_prefix='+32', roaming = False):
        if isinstance(text,PhoneNumber):
            self.int_prefix = text.int_prefix
            self.number = text.number
        else:
            self.int_prefix = int_prefix
            text = str(text).replace(" ","")
            text = text.replace(".","")
            text = text.replace("/","")
            self.number = text
            if self.number[0] == '+':
                self.int_prefix = self.number[:3]
                self.number = self.number[3:]
            elif self.number[0] == '0':
                self.number = self.number[1:]

            if not self.number.isdigit():
                raise self.Invalid(text)
            if not roaming and not self.is_belgian_gsm():
                raise self.NotABelgianNumber("Error : roaming is off : " + self.int_prefix + self.number)

    def __str__(self):
        return self.int_prefix + self.number

    def __repr__(self):
        res = str(self)
        return ' '.join((res[:3], res[3:6], res[6:8], res[8:10], res[10:]))

    def __len__(self):
        """ """
        return len(self.int_prefix) + len(self.number)

    def is_belgian_gsm(self):
        return (
            self.int_prefix == '+32' and
            self.number[0] == '4' and
            self.number[1] in ('7', '8', '9') and
            len(self.number) == 9)

if __name__ == '__main__':
    p = PhoneNumber("+352691454545")
    print(p.int_prefix)
    print(p.number)
    print(not p.is_belgian_gsm())


