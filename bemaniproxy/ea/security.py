from os import urandom
from typing import List

SECURITY_ID_HEADER = 0x01
SECURITY_ID_CHECKSUM = 0x6F


class SecurityID(object):
    """
    structure of a security ID, PCBID, or EAMID
    """
    header: int
    id: List[int]
    checksum: int

    def __init__(
            self,
            header: int = SECURITY_ID_HEADER,
            s_id: List[int] = None,
            checksum: int = SECURITY_ID_CHECKSUM
    ):
        self.header = header
        self.checksum = checksum

        if s_id is None:
            self.s_id = list(bytearray(urandom(8)))
        else:
            self.s_id = s_id

    @staticmethod
    def checksum_buffer(buffer: List[int]) -> int:
        """
        Calculates checksum with a buffer?
        :param buffer:
        :return:
        """
        # this mainly reorganizes the input buffer in a wierd way before feeding it into
        # checksum_calc
        new_buf = [buffer[1]]
        new_buf.extend([buffer[x] for x in range(7, 1, -1)])
        return SecurityID.checksum_calc(0, new_buf)

    @staticmethod
    def checksum_calc(initseed: int, idlist: List[int]) -> int:
        """
        Calculates checksum?
        :param initseed:
        :param idlist:
        :return:
        """
        """
        index = 0
        v4 = 0 # int
        result = 0 # unit8_t
        v6 = 0 # unsigned int
        v7 = 0 # signed int
        v8 = 0 # int
        v9 = 0 # unit8
        v10 = 0 # int
        v11 = 0 # unit8
        v12 = 0 # int
        v13 = 0 # uint8
        v14 = 0 # int
        """

        # sanity check
        if len(idlist) <= 0:
            return initseed

        result = initseed

        # NOTE: since v4 is just the length and its used entirely for iteration, we can replace
        # the do while loop a regular for each
        # v4 = len(idlist)
        for curr in idlist:
            # v6 is just the value of the currently looked at id piece
            # or curr in this case

            # v7 is 0 or 4, and each value from 0-7 is used in right shifting.
            # shift_by = 0 # v7

            # do-while loop until v7 < 8, however, since we set v7 to 0,
            #   it will always be less than 8 on first run, so we dont need to worry about
            #   doing it once
            # v8 / v10 / v12 / v14 are all checking if there is a value in the
            # least signifnant binary digit.

            # what this seems to do is take ech id piece (v6/curr) and
            # right shift it from 0-7, then xor with some rotation of RESULT/initseed/8C
            # if it contains a 1 in the least significant digit (1), then we xor that result
            # with 8C.

            # NOTE: ive moved the main shifting logic to the _weird_shift function
            result = _weird_shift(curr, result)

        return result

    def parse_from(self, str_id: str):
        """
        Parses a string id into a SecurityID
        :param str_id: string to parse
        :return: None
        """
        # log_assert(str)
        # log_assert(id)
        # return hex_decode(id, sizeof(struct security_id), str, strlen(str))

        # NOTE: ID in the above line would actually refer to this object.
        #   Therefore hex_decode is not directly translatable
        data = []
        if _hex_decode(str_id, data) and len(data) >= 10:
            # only do something if successful
            # the first number should be the header, next 8 digits the id, and last number should be checksum
            self.header = data[0]
            self.checksum = data[9]
            self.s_id = data[1:9]

    def prepare(self):
        """
        Prepares this security id (updates header and checksum)
        """
        # log_assert(id)

        # id->header = SECURITY_ID_HEADEr
        # id->checksum = security_id_checksum_buffer(id->id)
        self.header = SECURITY_ID_HEADER
        self.checksum = SecurityID.checksum_buffer(self.s_id)

    def to_str(self, id_only: bool) -> str:
        """
        Stringify this security id
        :param id_only: True to stringify id only, false stringifies all
        :return: string with stringified data
        """
        # hex_encode_uc
        # NOTE: hex_encode_uc uses id, which would actually refer to this object
        #   therefore hex_encodE_uc is not directly translatable

        data = []
        if id_only:
            data.extend(self.s_id)
        else:
            data = [self.header]
            data.extend(self.s_id)
            data.append(self.checksum)

        return _hex_encode(data)

    def verify(self) -> bool:
        """
        verifies this security id
        :return: True if verified, False if mismatch
        """
        # log_assert(id)
        # return id->header == SECURITY_ID_HEADER &&
        #   id->checksum == security_id_checksum_buffer(id->id)
        return (
                self.header == SECURITY_ID_HEADER
                and self.checksum == SecurityID.checksum_buffer(self.s_id)
        )


# default security id with updated header and checksum ready for use
security_id_default = SecurityID()


def _weird_shift(shiftee: int, result: int) -> int:
    """
    Performs wierd shift using simplified code
    :param shiftee: target to shift
    :param result: the current result
    :return: new result after shifting
    """
    for shift_by in range(8):
        result = _weird_shift_single(shiftee, shift_by, result)

    return result


def _weird_shift_expanded(shiftee: int, shift_by: int, result: int) -> int:
    """
    Performs the wierd shift used by checksum calc
    :param shiftee: item to shift
    :param shift_by: amount to shift by. (NOTE: should be 0 or 4 for correct logic)
    :param result: current shifting results
    :return: the result after being shifted
    """
    # See checksum_calc for explanations

    # v8 = (result ^ (v6 >> v7)) & 1
    # v9 = result >> 1
    has_one = (result ^ (shiftee >> shift_by)) & 1 > 0
    temp_shiftee = result >> 1

    # v8 contains a 1
    if has_one:
        temp_shiftee ^= 0x8C
        # v9 ^= 0x8C

    # v10 = (v9 ^ (v6 >> (v7 + 1))) & 1
    # v11 = v9 >> 1
    has_one = (temp_shiftee ^ (shiftee >> (shift_by + 1))) & 1 > 0
    temp_shiftee = temp_shiftee >> 1

    # v10 contains a 1
    if has_one:
        temp_shiftee ^= 0x8C
        # v11 ^= 0x8C

    # v12 = (v11 ^ (v6 >> (v7 + 2))) & 1
    # v13 = v11 >> 1
    has_one = (temp_shiftee ^ (shiftee >> (shift_by + 2))) & 1 > 0
    temp_shiftee = temp_shiftee >> 1

    # v12 contains a 1
    if has_one:
        temp_shiftee ^= 0x8C
        # v13 ^= 0x8C

    # v14 = (v13 ^ (v6 >> (v7 + 3))) & 1
    # result = v13 >> 1
    has_one = (temp_shiftee ^ (shiftee >> (shift_by + 3))) & 1 > 0
    temp_shiftee = temp_shiftee >> 1

    # v14 contains a 1
    if has_one:
        temp_shiftee ^= 0x8C
        # result ^= 0x8C

    return temp_shiftee


def _weird_shift_single(shiftee: int, shift_by: int, target: int) -> int:
    """
    performs one piece of the wierd shift
    :param shiftee: the main thing to shift
    :param shift_by: the amount to shift by
    :param target: the target to shift
    :return: the shifted target
    """
    # basically:
    #   1. shift the current id piece by an amount
    #   2. xor that with some value we currently have
    #   3. shift that target by 1 to the right
    #   4. if the result from step 2 has a 1 in the least sig digit, xor the result
    #       from step 3 with 0x8C
    has_one = (target ^ (shiftee >> shift_by)) & 1 > 0
    shifted = target >> 1
    if has_one:
        shifted ^= 0x8C

    return shifted


def tryparseint(value: str, base: int) -> int:
    """
    Trys to parse an int with given base. Returns -1 if failed to parse int.
    NOTE: do not use for negative values.
    :param value: value to parse
    :param base: base to use
    :return: 0 or positive integer
    """
    try:
        return int(value, base)
    except:
        return -1


def _hex_encode(target: List[int]) -> str:
    """
    Encodes data into a hex string using the hex_encode alg
    :param target: list of integers to encode
    :return: encoded string. will be "" if failed
    """
    # ALG:
    #   * each 8-bit integer is split into two
    #   * each 4 bits are converted to hex and put together
    #   1. for each integer, split it into the top and low 4 bits
    #   2. convert each 4 bits into hex
    hex_str = []
    for value in target:
        p1 = value >> 4  # high 4 bits (right shift erases bits on right)
        p2 = value & 15  # low 4 bits (bitwise and ensures we only get bits on right (15 = 1111))
        hex_str.append("{:X}".format(p1))
        hex_str.append("{:X}".format(p2))

    return "".join(hex_str)


def _hex_decode(hex_str: str, result: List[int]) -> bool:
    """
    Decodes a hex string using the hex_decode alg
    :param hex_str: string to decode
    :param result: list of integers to store the decoded values to
    :return: true on success, false on failure
    """
    # ALG:
    #   * each character of the hex string is 4 bits of the resulting 8 bit integer
    #   * therefore, 2 chars are needed to built 1 integer
    #   * the first char is considered the high 4 bits, while the 2nd char is the low 4 bits
    #   1. for each character, convert it to an int, base 16 (if possible)
    #   2. every two characters, bit shift the first one by 4 (left) then or the values to build an int
    for index in range(len(hex_str)):
        if index % 2 == 1:
            # for every odd piece, convert it and the character before.
            p1 = tryparseint(hex_str[index - 1], 16)
            p2 = tryparseint(hex_str[index], 16)

            # check if valid
            if p1 < 0 or p2 < 0:
                return False

            # now store as int
            result.append((p1 << 4) | p2)

    return True


def generate_pcbid():
    sec = SecurityID()
    sec.prepare()
    return sec.to_str(False)
