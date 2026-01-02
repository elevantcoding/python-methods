""" 
Cipher Engine 
by ElevantCoding

 Procedures in this module:
---------------------------------------------------------------------------------------------------------------------------------------------------
 get_rand_val, get_rand_char, replace_char_at_index, get_altervals, generate_ciph, num_cipher, cipher_string, decipher_string, validate_xor_range
---------------------------------------------------------------------------------------------------------------------------------------------------
 cipher_string performs a custom obfuscation using randoms, Xor and an on-the-fly, random numeric cipher.
 this obfuscation results in a 256-character hex string (128 encoded chars).
 decipher_string reverses the obfuscation to the original string value.

"""
import random


def get_rand_val(lower, upper):
    
    """ Get a random value between lower and upper bound vals """

    if lower > upper:
        lower, upper = upper, lower
    return random.randint(lower, upper)

def get_rand_char(lower = 32, upper = 255):

    """ Get a random character from printable range 32 to 255, excluding 127 """

    if lower > upper:
        lower, upper = upper, lower

    lower = max(lower, 32) # select the larger of the two
    upper = min(upper, 255) # select the smaller of the two

    while True:
            num = random.randint(lower, upper)
            if num != 127:
                return chr(num)

def replace_char_at_index(orig_string, idx, new_char):

    """ Replace a character in a string at the specified index """
    
    if idx < 0 or idx >= len(orig_string):
        return orig_string
    if len(new_char) != 1:
        return orig_string
    
    return orig_string[:idx] + new_char + orig_string[idx + 1:]

def get_altervals(getvals, cipher: bool):

    """ Alter numeric values - when cipher is true, use one method, when 
     cipher is false, use reverse of cipher method """

    if not isinstance(cipher,bool):
        raise TypeError("cipher must be a boolean")
    
    if len(getvals) == 0:
        return getvals
    
    if not all(c in "0123456789" for c in getvals):
        return getvals
    
    returnvals = ""
    for v in range(len(getvals)): 
        num = int(getvals[v])
        if ((v + 1) % 2 !=0) == cipher:  
            stepVal = 1
        else:
            stepVal = - 1

        num = (num + stepVal + 10) % 10
        returnvals += str(num)

    return returnvals

def generate_ciph():
    
    """ return 10-char string, no duplicate chars """

    ciph = ""
    while len(ciph) < 10:
        char = get_rand_char(52,126)
        if char not in ciph:
            ciph = ciph + char
    return ciph

def num_cipher(chars: str, cipher: bool, ciph: str):
    
    """ return a string that is ciphered or deciphered 
        based on 10-char string in ciph """

    if len(chars) == 0:
        return chars
    if len(ciph) != 10:
        return chars
    if cipher == True and not all(c in "0123456789" for c in chars):
        return chars
         
    KEY = "0123456789"

    result = ""
    for i in range(len(chars)):
        char = chars[i]
        if cipher == True:
            pos = KEY.index(char)
            result = result + ciph[pos]
        else:
            pos = ciph.index(char)
            result = result + KEY[pos]

    return result

def cipher_string(mytextstring: str):
    
    """ cipher a string
        create a key using
        - a random six-digit number,
        - a random one-digit number,
        - last index position of values used for xor
        - original string length
        - num cipher
    """
    maxstrlen = 128

    stringtocipher = mytextstring.strip()

    if len(stringtocipher) == 0:
        return ""

    # random value formatted for six digits and one-digit random val between 2 and 6
    vals = str(get_rand_val(0, 999999)).zfill(6) 
    randval = get_rand_val(2, 6)
    
    strLen = len(stringtocipher)
    i = strLen
    loops = strLen * randval
    v = -1
    altervals = vals

    # using the random-generated numerals, alter the ascii values of each char 
    # working through the string from right to left randval times
    for loopcount in range(loops):
        i = i - 1
        v = v + 1

        if i < 0:
            i = strLen - 1
        if v > (len(altervals) - 1): 
            v = 0
            altervals = get_altervals(altervals, True)

        char = stringtocipher[i]
        getasc = ord(char)
        getval = int(altervals[v])
        addasc = getasc ^ getval # Xor
        addchar = chr(addasc)
        stringtocipher = replace_char_at_index(stringtocipher, i, addchar)

    # add 1 to v to match 1-based indexing for cross-compatibility with VBA
    v = v + 1

    # create a prefix for the cipher, this will be the key to decipher
    prefix = altervals + str(randval) + str(v) + str(strLen).zfill(3)
    
    ciph = generate_ciph()    
    ciphprefix = num_cipher(prefix, True, ciph)
    
    prefix = ciphprefix + ciph
    
    prefixlen = len(prefix)

    if strLen > (maxstrlen - prefixlen):
        raise ValueError('String longer than defined parameters.')
    
    availablelen = maxstrlen - prefixlen
    spacing = 0
    if strLen < availablelen:
        spacing = int(availablelen / strLen)
    
    # pad random chars between the ciphered chars if space allows
    if spacing == 0:
        paddedString = stringtocipher
    else:
        paddedString = ""
        s = spacing
        i = 0
        for p in range(availablelen):
            if s == spacing:
                s = 1
            else:
                s += 1
            
            if s == 1 and i < strLen:
                paddedString = paddedString + stringtocipher[i]
                i += 1
            else:
                paddedString += get_rand_char()
    
    # Attach the prefix / key to the padded string cipher
    paddedString = prefix + paddedString
    hexString = paddedString.encode('latin-1').hex().upper()
    
    # String is ciphered
    return hexString

def decipher_string(myCipherstring):
    
    """ decipher a string created by cipher_string
        retrieve the prefix / key consisting
        - a random six-digit number,
        - a random one-digit number,
        - last index position of values used for xor
        - original string length
        - num cipher
        (vertical bars used for illustration only and are not in the prefix)
        -----------------------------------------------------------
        000000|0|0|000|aaaaaaaaaa
        -----------------------------------------------------------
     """
    
    prefixlen = 21
    maxstrlen = 128

    myCipherstring = myCipherstring.strip()
    
    if len(myCipherstring) == 0:
        return ""
    
    stringtoDecipher = bytes.fromhex(myCipherstring).decode('latin-1')
    
    prefix = stringtoDecipher[:prefixlen]
    
    numciph = prefix[-10:]
    prefix = prefix[:-10]
    
    prefix = num_cipher(prefix, False, numciph)

    if len(prefix) != 11 or not all(c in "0123456789" for c in prefix):
        return ""
    
    chars = prefix[-3:]
    strLen = int(chars)    
    
    prefix = prefix[:len(prefix)-3]
    
    char = prefix[-1:]
    v = int(char)
    
    # subtract 1 from v
    v = v - 1

    prefix = prefix[:len(prefix) - 1]

    char = prefix[-1:]
    randval = int(char)

    prefix = prefix[:len(prefix)-1]

    chars = prefix
    altervals = str(chars)
    
    paddedString = stringtoDecipher[prefixlen:]
    
    availablelen = maxstrlen - prefixlen
    spacing = int((availablelen) / strLen)
    if spacing < 1:
        spacing = 1
    
    # remove padding
    stringtoDecipher = ""
    i = 0
    s = 1
    for p in range(availablelen):
        if s == 1:
            stringtoDecipher += paddedString[p]
            i += 1
            if i == strLen:
                break
        s += 1
        if s > spacing:
            s = 1

    i = 0 
    loops = strLen * randval
    altervalsOrig = altervals
    altervalsLen = v + 1    
    altervals = altervals[:altervalsLen]
    idx = strLen - 1

    # reverse traversal through string and reverse altervals using get_altervals
    for loopcount in range(loops):
        if i > idx: # reset index
            i = 0
        
        if v < 0:
            if len(altervals) < 6:
                altervals = altervalsOrig

            altervals = get_altervals(altervals, False)
            v = (len(altervals) - 1)
        
        char = stringtoDecipher[i]
        getasc = ord(char)
        getval = int(altervals[v])
        addasc = getasc ^ getval
        addchar = chr(addasc)
        stringtoDecipher = replace_char_at_index(stringtoDecipher,i, addchar)

        i += 1
        v -= 1
    
    # string is deciphered
    return stringtoDecipher

def validate_xor_range():
    """
    Confirms that applying XOR between any printable ASCII char (32-255)
    and numeric keys 0-9 never produces a value outside the printable range.

    This guarantees that XOR-based cipher output always remains printable

    """
    c = 0
    for i in range(32, 256):
        for k in range(0, 10):
            x = i ^ k
            if x < 32 or x > 255:
                c = c + 1
                print(i, " Xor ", k, " is ", x)
    return c

            

