import base64
import hashlib
import socket
import struct

import array
from isort.pie_slice import native_str
from ruamel_yaml.compat import utf8


def compute_accept_value(key):
    """Computes the value for the Sec-WebSocket-Accept header,
    given the value for Sec-WebSocket-Key.
    """
    sha1 = hashlib.sha1()
    sha1.update(key)
    sha1.update(b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11")  # Magic value
    return base64.b64encode(sha1.digest())


def accept_connection(headers):
    # fields = ("SEC_WEBSOCKET_KEY", "SEC_WEBSOCKET_VERSION")
    # if not all(map(headers.get, fields)):
    #     raise ValueError("Missing/Invalid WebSocket headers")

    accept_header = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: WebSocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Accept: %s\r\n"
        "\r\n" % (
            compute_accept_value(
                headers["Sec-WebSocket-Key"].encode("utf8")
            ).decode("utf8")
        )
    )
    return accept_header.encode('utf8')


def mask_or_unmask(mask, data):
    """Websocket masking function.
    `mask` is a `bytes` object of length 4; `data` is a `bytes` object of any length.
    Returns a `bytes` object of the same length as `data` with the mask applied
    as specified in section 5.3 of RFC 6455.
    This pure-python implementation may be replaced by an optimized version when available.
    """
    mask = array.array("B", mask)
    unmasked = array.array("B", data)
    print('error: ', mask, unmasked)
    for i in range(len(data)):
        unmasked[i] = unmasked[i] ^ mask[i % 4]
    return unmasked.tobytes()


def WebSockReadFrame(dbyte):
    b1 = dbyte[0]
    fin = b1 >> 7 & 1
    opcode = b1 & 0xf

    b2 = dbyte[1]
    mask = b2 >> 7 & 1
    length = b2 & 0x7f

    print('WebSK len = ',length)
    length_data = ""
    dbyte_rdix = 2;
    if length == 0x7e:
        length_data = dbyte[dbyte_rdix:dbyte_rdix+2]
        dbyte_rdix += 2
        length = struct.unpack('!H', length_data)[0]
    elif length == 0x7f:
        length_data = dbyte[dbyte_rdix:dbyte_rdix+8]
        dbyte_rdix += 8
        length = struct.unpack('!Q', length_data)[0]

    mask_key = ''
    if mask:
        mask_key = dbyte[dbyte_rdix:dbyte_rdix+4]
        dbyte_rdix += 4
    data = dbyte[dbyte_rdix:dbyte_rdix+length]
    if mask:
        data = mask_or_unmask(mask_key, data)
    return fin, opcode, data


def WebSocketRead(codes):
    fin, opcode, data = WebSockReadFrame(codes)
    if opcode in (0x1, 0x2):    #文本或二进制信息
        return (opcode, data)
    elif opcode == 0x8:         #关闭信息
        close_code = None
        close_reason = None
        if len(data) >= 2:
            close_code = struct.unpack('>H', data[:2])[0]
        if len(data) > 2:
            close_reason = data[2:]
        print('WebSockRead: 0x8 close=',close_code,close_reason)
        return (opcode, None)
    elif opcode == 0x9:
        return (opcode, data)


def WebSocketWrite(bdata):
    wts = struct.pack('!B', 0x81)
    length = len(bdata)
    wts += struct.pack('!B',length)
    print(wts)
    wts += bdata
    print(wts)
    return wts


def create_socketServer():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', 9913))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.listen(5)
    except Exception as e:
        print('Exception:',str(e))
        return
    else:
        print('Server running...')

    # try:
    while True:
        conn, addrid = sock.accept()
        data = conn.recv(1024)
        print(data.decode())
        print("*************************")

        header_dict = {}
        header, _ = str(data).split(r'\r\n\r\n', 1)
        for line in header.split(r'\r\n')[1:]:
            key, val = line.split(':', 1)
            header_dict[key] = val[1:]
            print("%s,%s"%(key,header_dict[key]))

        # print(header_dict['Sec-WebSocket-Key'])

        requested = accept_connection(header_dict)
        print('**************************')
        print(requested)
        conn.send(requested)

        print('Send the handshake data')
        print('*******************************')

        while True:
            tx = conn.recv(1024)
            print(tx)
            opcode, txda = WebSocketRead(tx)
            print(opcode, txda)
            if txda is None:
                break
            info = txda.decode()
            wrt = ''
            if info == 'sx':
                wrt = 'ABC测试信息查看。'
                conn.send(WebSocketWrite(wrt.encode()))

        print('This WebSocke is Closed!')
        conn.close
    # except Exception as e:
    #     print('Error X:',str(e))


create_socketServer()
