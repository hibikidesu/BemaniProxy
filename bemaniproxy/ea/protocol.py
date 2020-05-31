import binascii
import hashlib
from typing import Optional

from arc4 import ARC4
from kbinxml import KBinXML

from .binary import BinaryEncoding
from .lz77 import Lz77
from .node import Node
from .xml import XmlEncoding


class EAmuseException(Exception):
    """
    An exception thrown when we encounter an error with E-Amusement encapsulation.
    """


class EAmuseProtocol:
    """
    A wrapper object that encapsulates encoding/decoding the E-Amusement protocol by Konami.
    """
    SHARED_SECRET = b"\x69\xD7\x46\x27\xD9\x85\xEE\x21\x87\x16\x15\x70\xD0\x8D\x93\xB1\x24\x55\x03\x5B\x6D\xF0\xD8\x20\x5D\xF5"

    XML = 1
    BINARY = 2

    SHIFT_JIS_LEGACY = "shift-jis-legacy"
    SHIFT_JIS = "shift-jis"
    EUC_JP = "euc-jp"
    UTF_8 = "utf-8"

    def __init__(self) -> None:
        """
        Initialize the object.
        """
        self.last_text_encoding: Optional[str] = None
        self.last_packet_encoding: Optional[int] = None

    def __rc4_crypt(self, data: bytes, key: bytes) -> bytes:
        """
        Given a data blob and a key blob, perform RC4 encryption/decryption.

        Parameters:
            data - Binary string representing data to be encrypted/decrypted
            key - Binary string representing the key to use

        Returns:
            binary string representing the encrypted/decrypted data
        """
        return ARC4(key).decrypt(data)

    def __decrypt(self, encryption_key: str, data: bytes) -> bytes:
        """
        Given data and an optional encryption key, decrypt the data.

        Parameters:
            encryption_key - A string encryption key as returned from a HTTP request.
                             Should be in the form 1-xxyyzzww-aabb. If it is None, this
                             performs a null decrypt.
            data - Binary string representing data to transform.

        Returns:
            binary string representing transformed data
        """
        if data is None:
            return None

        if encryption_key:
            # Key is concatenated with the shared secret above
            version, first, second = encryption_key.split("-")
            key = binascii.unhexlify((first + second).encode("ascii")) + EAmuseProtocol.SHARED_SECRET

            # Next, key is sent through MD5 to derive the real key
            m = hashlib.md5()
            m.update(key)
            key = m.digest()
        else:
            key = None

        if key:
            # This is an encrypted old-style packet
            return self.__rc4_crypt(data, key)

        # No encryption
        return data

    def __encrypt(self, encryption_key: str, data: bytes) -> bytes:
        """
        Given data and an optional encryption key, encrypt the data.

        Parameters:
            encryption_key - A string encryption key as returned from a HTTP request.
                             Should be in the form 1-xxyyzzww-aabb. If it is None, this
                             performs a null decrypt.
            data - Binary string representing data to transform.

        Returns:
            binary string representing transformed data
        """
        # RC4 is symmetric
        return self.__decrypt(encryption_key, data)

    def __decompress(self, compression: str, data: bytes) -> bytes:
        """
        Given data and an optional compression scheme, decompress the data.

        Parameters:
            compression - A string specifying the compression used. Should
                          be of the form 'l7zz' or 'none'. You can also pass in
                          the python value None.
            data - Binary string representing data to transform.

        Returns:
            binary string representing transformed data
        """
        if data is None:
            return None

        if compression:
            if compression is None or compression == "none":
                # This isn't compressed
                return data
            elif compression == "lz77":
                # This is a compressed new-style packet
                lz = Lz77()
                return lz.decompress(data)
            else:
                raise EAmuseException(f"Unknown compression {compression}")

        # No compression
        return data

    def __compress(self, compression: str, data: bytes) -> bytes:
        """
        Given data and an optional compression scheme, compress the data.

        Parameters:
            compression - A string specifying the compression used. Should
                          be of the form 'l7zz' or 'none'. The python value
                          None will also be recognized as 'none'.
            data - Binary string representing data to transform.

        Returns:
            binary string representing transformed data
        """
        if data is None:
            return None

        if compression:
            if compression is None or compression == "none":
                # This isn't compressed
                return data
            elif compression == "lz77":
                # This is a compressed new-style packet
                lz = Lz77()
                return lz.compress(data)
            else:
                raise EAmuseException(f"Unknown compression {compression}")

        # No compression
        return data

    def __decode(self, data: bytes) -> Node:
        """
        Given data, decode the data into a Node tree.

        Parameters:
            data - Binary string representing data to decode.

        Returns:
            Node tree on success or None on failure.
        """
        # Assume it's a binary page
        binary = BinaryEncoding()
        ret = binary.decode(data, skip_on_exceptions=True)

        if ret is not None:
            # We got a result, it was binary
            self.last_text_encoding = binary.encoding
            self.last_packet_encoding = EAmuseProtocol.BINARY

            return ret

        try:
            data = KBinXML(data)
        except:
            pass

        # Assume its XML
        xml = XmlEncoding()
        ret = xml.decode(data, skip_on_exceptions=True)

        if ret is not None:
            # We got a result, it was XML
            self.last_text_encoding = xml.encoding
            self.last_packet_encoding = EAmuseProtocol.XML

            return ret

        # Couldn't decode
        raise EAmuseException("Unknown packet encoding")

    def __encode(self, tree: Node, text_encoding: str, packet_encoding: int) -> bytes:
        """
        Given a Node tree, encode the data into the given packet encoding.

        Parameters:
            tree - A Node object representing the root of the tree to encode.
            text_encoding - The text encoding for any strings that will be encoded.
                            Should be EAmuseProtocol.SHIFT_JIS, EAmuseProtocol.EUC_JP or
                            EAmuseProtocol.UTF8.
            packet_encoding - The encoding used for the packet. Should be EAmuseProtocol.XML
                              or EAmuseProtocol.BINARY.

        Returns:
            A string blob representing the encoded packet.
        """
        if packet_encoding == EAmuseProtocol.BINARY:
            # It's binary, encode it
            binary = BinaryEncoding()
            return binary.encode(tree, encoding=text_encoding)
        elif packet_encoding == EAmuseProtocol.XML:
            # It's XML, encode it
            xml = XmlEncoding()
            return xml.encode(tree, encoding=text_encoding)
        else:
            raise EAmuseException(f"Invalid packet encoding {packet_encoding}")

    def decode(self, compression: Optional[str], encryption: Optional[str], data: bytes) -> Node:
        """
        Given a request with optional compression and encryption set, decrypt,
        decompress and decode the data, returning a parsed tree.

        Parameters:
            compression - A string specifying the compression type, should be 'lz77' or 'none'.
                          The python value None can also be passed in.
            encryption - A string specifying the encryption key, or None if no encryption.
            data - A binary string of data to parse.

        Returns:
            A Node tree structure representing the parsed request, or None on failure.
        """
        data = self.__decrypt(encryption, data)
        data = self.__decompress(compression, data)
        return self.__decode(data)

    def encode(
            self,
            compression: Optional[str],
            encryption: Optional[str],
            tree: Node,
            text_encoding: Optional[str] = None,
            packet_encoding: Optional[int] = None,
    ) -> bytes:
        """
        Given a response with optional compression and encryption set, encode, compress
        and encrypt the data, returning a binary blob suitable for forwarding on a network.

        Parameters:
            compression - A string specifying the compression type, should be 'lz77' or 'none'.
                          The python value None can also be passed in.
            encryption - A string specifying the encryption key, or None if no encryption.
            data - A binary string of data to parse.
            text_encoding - A text encoding to use. If not provided, uses the text encoding of the
                            last decoded packet. See __encode for values.
            packet_encpding - A packet encoding to use. If not provided, uses the packet encoding
                              of the last decoded packet. See __encode for values.

        Returns:
            A blob of data representing the encoded packet.
        """
        # Either auto-set response based on request, or explicitly override in parameters
        if text_encoding is None:
            text_encoding = self.last_text_encoding
        if text_encoding is None:
            raise EAmuseException("Unknown text encoding")

        if packet_encoding is None:
            packet_encoding = self.last_packet_encoding
        if packet_encoding is None:
            raise EAmuseException("Unknown packet encoding")

        # Clear last packet since we sent a response
        self.last_text_encoding = None
        self.last_packet_encoding = None

        data = self.__encode(tree, text_encoding, packet_encoding)
        data = self.__compress(compression, data)
        return self.__encrypt(encryption, data)
