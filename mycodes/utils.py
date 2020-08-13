def pad(data, block_size=16):
    pad_len = block_size - len(data) % block_size
    if type(data) not in {bytes, bytearray}:
        data = data.encode()
    return data + pad_len * bytes([pad_len])

def unpad(padded_data, block_size=16):
    pdata_len = len(padded_data)
    pad_len = padded_data[-1]
    if pdata_len % block_size:
        raise ValueError("data not padded properly")
    return padded_data[:-pad_len].decode()

bfh = lambda: bytes.fromhex

def int_to_hex(i, length=1):
    bs = length - len(i)