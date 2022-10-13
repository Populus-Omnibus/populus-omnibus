import asyncio
import json
import sys
from filehandler import readsettings as read
from filehandler import decode as decrypt
from filehandler import encode as encrypt

async def handle_echo(reader, writer):
    sys.stdout = open('/home/ubuntu/server/server_log.log', 'a')
    size = await reader.read(4)
    data = await reader.read(int.from_bytes(size, "big"))
    print(int.from_bytes(size, "big"))
    message = decrypt(msg=data.decode())
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr}")
    tempdict = json.loads(read(segment="mc_acc"))
    recdict = json.loads(message)

    #print(f"Received {message!r} from {addr!r}")
    for token in list(tempdict.keys()):
        if tempdict[token]["token"] == recdict["token"]:
            sentdict = encrypt(msg=(json.dumps(tempdict[token])))
            bytenum = len(sentdict)
            writer.write(bytenum.to_bytes(4, "big"))
            writer.write(sentdict.encode())
            print("küldve")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            sys.stdout.close()
            return
            
    mydict = {"token": None}
    sentdict = encrypt(json.dumps(mydict))
    bytenum = len(sentdict)
    writer.write(bytenum.to_bytes(4, "big"))
    writer.write(sentdict.encode())
    await writer.drain()
    print("küldve üres")
    writer.close()
    await writer.wait_closed()
    sys.stdout.close()

async def socketserver():
    sys.stdout = open('/home/ubuntu/server/server_log.log', 'a')
    server = await asyncio.start_server(
        handle_echo, '0.0.0.0', 12345)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    sys.stdout.close()
    
    async with server:
        await server.serve_forever()
    

asyncio.run(socketserver())