# -*- coding: latin-1 -*-
import math

# input_String = '457z'


esc = '\u261d'
bad = '\u2639'

sevenbitdefault = (
    '@', '�', '$', '�', '�', '�', '�', '�', '�', '�', '\n', '�', '�', '\r', '�', '�',
    '\u0394', '_', '\u03a6', '\u0393', '\u039b', '\u03a9', '\u03a0', '\u03a8',
    '\u03a3', '\u0398', '\u039e', esc, '�', '�', '�', '�',
    ' ', '!', '"', '#', '�', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
    '�', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '�', '�', '�', '�', '�',
    '�', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '�', '�', '�', '�', '�'
)

sevenbitextended = (
    '\f', 0x0A,
    '^', 0x14,
    '{', 0x28,
    '}', 0x29,
    '\\', 0x2F,
    '[', 0x3C,
    '~', 0x3D,
    ']', 0x3E,
    '|', 0x40,
    '�', 0x65
)


def make_num(istr):
    try:
        istr = int(istr)
        if 0 <= istr <= 9:
            result = istr
        else:
            result = 16

    except Exception:
        pass
        istr = str(istr).upper()
        map_list = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
        result = map_list.get(istr, 16)
    return result


def int2bin(x, size):
    bin = "{0:08b}".format(int(x))
    return bin


def hex2num(number):
    tens = make_num(str(number)[0])
    ones = 0
    if len(number) > 1:
        ones = make_num(str(number)[1])
    if ones == 'X':
        return '00'
    return (tens * 16) + (ones * 1)


def bin2int(string):
    return int(string, 2)


def get7bit_extended_ch(code):
    for i in range(0, len(sevenbitextended), 2):
        if sevenbitextended[i + 1] == code:
            return sevenbitextended[i];
    return bad


def get_user_message(skip_characters, input, truelength):
    bytestring = ''
    octe_array = []
    rest_array = []
    septets_array = []
    s = 1
    count = 0
    matchcount = 0
    sms_Message = ''
    escaped = 0
    char_counter = 0
    byte_index = 0
    # Cut the input string into pieces of2 (just get the hex octets)
    for i in range(0, len(input), 2):
        hex = input[i:i + 2]
        bytestring = bytestring + int2bin(hex2num(hex), 8)
        byte_index = byte_index + 1
    # make two array's these are nessesery to
    for i in range(0, len(bytestring), 8):
        octe_array.insert(count, bytestring[i:i + 8])
        rest_array.insert(count, (octe_array[count])[0:s % 8])
        septets_array.insert(count, (octe_array[count])[(s % 8):8])

        count += 1
        s += 1
        if s == 8:
            s = 1

    for i in range(0, len(rest_array), 1):
        if i % 7 == 0:
            if i != 0:
                char_counter += 1
                chval = bin2int(rest_array[i - 1])
                if escaped:
                    sms_Message = sms_Message + get7bit_extended_ch(chval)
                    escaped = 0
                elif chval == 27 and char_counter > skip_characters:
                    escaped = 1
                elif char_counter > skip_characters:
                    sms_Message = sms_Message + sevenbitdefault[chval]
                matchcount += 1
            char_counter += 1
            chval = bin2int(septets_array[i])
            if escaped:
                sms_Message = sms_Message + get7bit_extended_ch(chval)
                escaped = 0
            elif chval == 27 and char_counter > skip_characters:
                escaped = 1
            elif char_counter > skip_characters:
                sms_Message = sms_Message + sevenbitdefault[chval]
            matchcount += 1
        else:
            char_counter += 1
            chval = bin2int((septets_array[i]) + rest_array[i - 1])
            if escaped:
                sms_Message = sms_Message + get7bit_extended_ch(chval)
                escaped = 0
            elif chval == 27 and char_counter > skip_characters:
                escaped = 1
            elif char_counter > skip_characters:
                sms_Message = sms_Message + sevenbitdefault[chval]
            matchcount += 1

    if matchcount != truelength:
        char_counter += 1
        chval = bin2int(rest_array[i - 1])
        if not escaped:
            if char_counter > skip_characters:
                sms_Message = sms_Message + sevenbitdefault[chval]
            elif char_counter > skip_characters:
                sms_Message = sms_Message + get7bit_extended_ch(chval)

    return sms_Message


def decode_gsm7_bit_packed(inp_string):
    new_string = ''

    for digit in inp_string:
        if make_num(digit) != 16:
            new_string += digit
        inp_string = new_string

    l = len(inp_string)
    septets = math.floor(l / 2 * 8 / 7)
    buffer = get_user_message(0, inp_string, septets)
    len_b = len(buffer)
    padding = '\r'
    if ((septets % 8 == 0 and len_b > 0 and buffer[len_b - 1] == padding) or (
            septets % 8 == 1 and len_b > 1 and buffer[len_b - 1] == padding and buffer[len_b - 2] == padding)):
        buffer = buffer[0:, len_b - 1]

    return buffer