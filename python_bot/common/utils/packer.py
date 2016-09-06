import base64

__all__ = ["pack_string", "unpack_string"]


def __int_encode(x):
    b = x.to_bytes((x.bit_length() // 8) + 1, byteorder='little')
    return base64.b85encode(b).decode()


def __int_decode(string):
    b = base64.b85decode(string.encode())
    return int.from_bytes(b, byteorder='little')


def pack_string(*args):
    results = []
    for i in args:
        if isinstance(i, int):
            results.append(__int_encode(i))
        else:
            results.append(base64.b85encode(str(i).encode()).decode())
    return " ".join(results)


def unpack_string(data, types):
    if not data:
        return []
    data = data.split()

    if len(data) != len(types):
        return []

    result = []
    for d, t in zip(data, types):
        if t == int:
            result.append(__int_decode(d))
        else:
            result.append(base64.b85decode(d.encode()).decode())
    return result
