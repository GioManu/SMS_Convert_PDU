import random


class PDU:

    @staticmethod
    def getPDU(msg, phone):  # ძირითადი მეთოდი
        msgLen = len(msg)
        headerPhone = PDU.convertPhone(phone)
        if msgLen <= 70:
            header = PDU.generateHeader(-1)
            header += "{}{}".format(str(headerPhone['len']), str(headerPhone['phone']))
            header += "0008AA{}".format(PDU.decToHex(msgLen * 2))
            pdu_msg = header + PDU.encodeMSG(msg)
            return {"len": int(len(pdu_msg[2:]) / 2), "msg": pdu_msg}
        else:
            chunks = [msg[i:i + 63] for i in range(0, len(msg), 63)]
            pdu_msgs = list()
            refNum = PDU.generateRefNum()
            for it in range(len(chunks)):
                text = PDU.encodeMSG(chunks[it])
                header = PDU.generateHeader(it)
                header += "{}{}".format(str(headerPhone['len']), str(headerPhone['phone']))
                header += "0008{}".format(PDU.decToHex(int((len(text) + 14) / 2)))
                header += PDU.generate6BUDH(refNum, len(chunks), it + 1)
                pdu_msg = header + text
                pdu_msgs.append({"len": int(len(pdu_msg[2:]) / 2), "msg": pdu_msg})
            return pdu_msgs

    @staticmethod
    def generateHeader(udh):
        if udh == -1:
            return '001100'
        else:
            return '0041{}'.format("0{}".format(udh) if udh < 10 else udh)

    @staticmethod
    def decToHex(dec):
        hx = str(hex(dec))[2:].upper()
        return str("0{}".format(hx) if len(hx) == 1 else "{}".format(hx))

    @staticmethod
    def generate6BUDH(refNum, maxChunks, curChunk):
        UDH = "060804{}".format(refNum)
        UDH += "{}".format(maxChunks) if maxChunks >= 10 else "0{}".format(maxChunks)
        UDH += "{}".format(curChunk) if curChunk >= 10 else "0{}".format(curChunk)
        return UDH

    @staticmethod
    def generateRefNum():
        ls = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        return ''.join(random.sample(ls, 4))

    @staticmethod
    def encodeMSG(msg):
        res = str()
        for e in msg:
            res += '%04x' % ord(e)
        return res.upper()

    @staticmethod
    def oddswap(st):
        s = list(st)
        for c in range(0, len(s), 2):
            t = s[c]
            s[c] = s[c + 1]
            s[c + 1] = t
        return "".join(s)

    @staticmethod
    def convertPhone(PHONE_NUM):
        if len(PHONE_NUM) == 9:
            PHONE_NUM = "995{0}".format(PHONE_NUM)
        elif PHONE_NUM[0] == "+":
            PHONE_NUM = PHONE_NUM[1:]
        return {
            "len": PDU.decToHex(len(PHONE_NUM)),
            "phone": "91{}".format(PDU.oddswap(PHONE_NUM))
        }
