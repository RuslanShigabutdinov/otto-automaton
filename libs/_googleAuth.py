import base64
import urllib.parse
import hmac
import hashlib
import time
import struct

def generateTotp(secret, interval=30, digits=6):
    key = base64.b32decode(secret, casefold=True)
    msg = struct.pack(">Q", int(time.time() // interval))
    hmacSha1 = hmac.new(key, msg, hashlib.sha1).digest()
    offset = hmacSha1[-1] & 0x0F
    binary = struct.unpack(">I", hmacSha1[offset:offset+4])[0] & 0x7FFFFFFF
    return f"{binary % (10 ** digits):0{digits}d}"

def decodeOtp(otpString):
    if not otpString.startswith('otpauth-migration://offline?data='):
        return []
    data = base64.urlsafe_b64decode(urllib.parse.parse_qs(urllib.parse.urlparse(otpString).query)['data'][0])
    result = []
    i = 0
    while i < len(data):
        tag = data[i]
        i += 1
        if (tag >> 3) == 1 and (tag & 0x7) == 2:
            length, i = readVarint(data, i)
            paramData = data[i:i+length]
            i += length
            param = decodeParam(paramData)
            if param:
                result.append(param)
    return result

def readVarint(data, i):
    value = 0
    shift = 0
    while i < len(data):
        byte = data[i]
        value |= (byte & 0x7F) << shift
        i += 1
        if not (byte & 0x80):
            break
        shift += 7
    return value, i

def decodeParam(data):
    param = {'secret': '', 'name': '', 'issuer': ''}
    i = 0
    while i < len(data):
        tag = data[i]
        i += 1
        field = tag >> 3
        wire = tag & 0x7
        if field == 1 and wire == 2:
            length, i = readVarint(data, i)
            param['secret'] = base64.b32encode(data[i:i+length]).decode('utf-8').rstrip('=')
            i += length
        elif field == 2 and wire == 2:
            length, i = readVarint(data, i)
            param['name'] = data[i:i+length].decode('utf-8')
            i += length
        elif field == 3 and wire == 2:
            length, i = readVarint(data, i)
            param['issuer'] = data[i:i+length].decode('utf-8')
            i += length
        else:
            if wire == 0:
                _, i = readVarint(data, i)
            elif wire == 2:
                length, i = readVarint(data, i)
                i += length
    return param

if __name__ == "__main__":
    otp = 'otpauth-migration://offline?data=CkMKFHZxV2llQlNLV0dscnRnSVRHVzNQEgJKVhoMb3R0by1wYXJ0bmVyIAEoATACQhM4YThmODIxNzQ3MjE1NjE3NzM5CkMKFER1c3JPc1BTV2hoSWk1ZHhiTkZEEgJYTBoMb3R0by1wYXJ0bmVyIAEoATACQhNlYzIyOWUxNzQ3MjE1NjE3NzM5EAIYASAA'
    keys = decodeOtp(otp)
    for k in keys:
        print(f"Аккаунт: {k['name']}, Сервис: {k['issuer']}, Ключ: {k['secret']}")