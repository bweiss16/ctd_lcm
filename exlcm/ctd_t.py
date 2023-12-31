"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class ctd_t(object):
    __slots__ = ["index", "depth", "temp"]

    __typenames__ = ["int64_t", "float", "float"]

    __dimensions__ = [None, None, None]

    def __init__(self):
        self.index = 0
        self.depth = 0.0
        self.temp = 0.0

    def encode(self):
        buf = BytesIO()
        buf.write(ctd_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">qff", self.index, self.depth, self.temp))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != ctd_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return ctd_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = ctd_t()
        self.index, self.depth, self.temp = struct.unpack(">qff", buf.read(16))
        return self
    _decode_one = staticmethod(_decode_one)

    def _get_hash_recursive(parents):
        if ctd_t in parents: return 0
        tmphash = (0x5872fad1cf9cccd8) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff) + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if ctd_t._packed_fingerprint is None:
            ctd_t._packed_fingerprint = struct.pack(">Q", ctd_t._get_hash_recursive([]))
        return ctd_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

    def get_hash(self):
        """Get the LCM hash of the struct"""
        return struct.unpack(">Q", ctd_t._get_packed_fingerprint())[0]

