import struct

level_names = ['customlevel1',
               'customlevel2',
               'customlevel3',
               'customlevel4',
               'customlevel5',
               'customlevel6',
               'customlevel7',
               'customlevel8',
               'testlevel']

def hash32(s):
    h = 0x811c9dc5
    for c in s:
        h = ((h ^ ord(c)) * 0x1000193) & 0xffffffff
    h = (h * 0x2001) & 0xffffffff
    h = (h ^ (h >> 0x7)) & 0xffffffff
    h = (h * 0x9) & 0xffffffff
    h = (h ^ (h >> 0x11)) & 0xffffffff
    h = (h * 0x21) & 0xffffffff
    return h

def write_int(f, val):
    f.write(struct.pack('<i', val))

def write_bool(f, val):
    f.write(b'\x01' if val else b'\x00')

def write_float(f, val):
    f.write(struct.pack('<f', val))

def write_color(f, val):
    r, g, b, a = val
    write_float(f, r)
    write_float(f, g)
    write_float(f, b)
    write_float(f, a)

def write_vec3(f, val):
    x, y, z = val
    write_float(f, x)
    write_float(f, y)
    write_float(f, z)

def write_string(f, val):
    write_int(f, len(val))
    f.write(val.encode('ascii'))

def write_hash(f, val):
    f.write(struct.pack('<I', hash32(val)))

def write_hex(f, val):
    f.write(bytearray.fromhex(val))

def write_hex_reverse(f, val):
    f.write(bytearray.fromhex(val)[::-1])

def read_int(s, pos):
    return struct.unpack('<i', s[pos:pos+4])[0]

def read_bool(s, pos):
    return True if b'\x01' == s[pos] else False

def read_float(s, pos):
    return struct.unpack('<f', s[pos:pos+4])[0]

def read_color(s, pos):
    r = read_float(s, pos)
    g = read_float(s, pos+4)
    b = read_float(s, pos+8)
    a = read_float(s, pos+12)
    return (r, g, b, a)

def read_vec3(s, pos):
    x = read_float(s, pos)
    y = read_float(s, pos+4)
    z = read_float(s, pos+8)
    return (x, y, z)

def read_string(s, pos):
    slen = read_int(s, pos)
    pos += 4
    return s[pos:pos+slen].decode('ascii')

def read_hex(s, pos):
    return s[pos:pos+4].hex()

def read_hex_reverse(s, pos):
    return s[pos:pos+4][::-1].hex()
