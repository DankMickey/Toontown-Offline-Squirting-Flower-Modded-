from direct.stdpy.thread import start_new_thread
from direct.stdpy.threading import Lock
import socket, urllib, json, traceback

import ShardAPIManagerUD

lock = Lock()

def _print(msg):
    with lock:
        print msg
        
RES_401 = ("401 Not Implemented", "text/html", "The requested resource was not implemented yet.")
RES_404 = ("404 Not Found", "text/html", "The requested resource was not found.")

def _encode(d):
    return json.dumps(d, sort_keys = True, indent = 4, separators = (',', ': '))

class ShardAPIWebServer:
    def __init__(self, mgr):
        self.mgr = mgr
        
        self.listenSock = socket.socket()
        self.listenSock.bind(("0.0.0.0", 19200))
        self.listenSock.listen(100)
        
    def run(self):
        while True:
            s, addr = self.listenSock.accept()
            
            try:
                s.settimeout(.5)
                data = s.recv(10240)
                if not data:
                    s.close()
                    continue
                    
                headers, data = data.split('\r\n\r\n')
                headers = filter(None, headers.replace('\n', '\r').split('\r'))
                
                response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html; charset=latin-1\r\n\r\nMalformed request."
                
                try:
                    request = headers.pop(0)
                    method, path, _ = request.split()
                    path = urllib.unquote(path)
                    
                    if method != "GET":
                        response = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html; charset=latin-1\r\n\r\nYou must GET all requests."
                        
                    hDict = {}
                    for header in headers:
                        h, val = header.split(':', 1)
                        hDict[h] = val
                        
                    args = {}
                    if '?' in path:
                        path, argdata = path.rsplit('?', 1)
                        argdata = argdata.split('&')
                        for arg in argdata:
                            a, val = arg.split('=', 1)
                            args[a] = val
                        
                    response = "HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html; charset=latin-1\r\n\r\nUnable to process your request."
                    with lock:
                        code, content, body = self.handleRequest(path, hDict, args)
                    response = "HTTP/1.1 %s\r\nContent-Type: %s; charset=latin-1\r\n\r\n%s" % (code, content, body)
                    
                except:
                    s.send(response)
                    s.close()
                    raise
                    
                try:
                    s.send(response)
                    s.close()
                    
                except socket.error:
                    pass
                    
            except Exception as e:
                if not 'timed out' in repr(e):
                    _print('%r caused ShardAPIWebServer.run to raise (%s)' % (addr, e))
                    traceback.print_exc()
                    
    def handleRequest(self, path, hDict, args):
        path = path.strip('\n\r /').split('/', 1)
        
        if len(path) > 1:
            root, path = path
            
        else:
            root = ""
            
        if root == "api":
            return self.handleAPIRequest(path, hDict, args)
            
        elif root == "res":
            return RES_401
            
        else:
            return self.handleGraphRequest(path, hDict, args)
            
    def handleAPIRequest(self, path, hDict, args):
        if path == "shards":
            shardId = args.get('shardId')
            if shardId is not None:
                try:
                    shardId = int(shardId)
                    assert shardId >= 0
                    
                except:
                    return ("200 OK", "text/plain", '{"error": "shardId must an unsigned integer"}')
                    
            lang = args.get('lang', 'en').lower()
            
            if not ShardAPIManagerUD.setLanguageContext(lang):
                return ("200 OK", "text/plain", '{"error": "No such language"}')
                
            data = self.mgr.writeDict()
            ShardAPIManagerUD.setLanguageContext(None)
            
            if not shardId:
                return ("200 OK", "text/plain", _encode(data))
                
            else:                  
                if not shardId in data:
                    return ("200 OK", "text/plain", '{"error": "No such shard"}')
                    
                return ("200 OK", "text/plain", _encode({shardId: data[shardId]}))
                
        elif path == "invasions":
            shardId = args.get('shardId')
            if shardId is not None:
                try:
                    shardId = int(shardId)
                    assert shardId >= 0
                    
                except:
                    return ("200 OK", "text/plain", '{"error": "shardId must an unsigned integer"}')
                    
            data = self.mgr.listInvasions()
            
            if not shardId:
                return ("200 OK", "text/plain", _encode(data))
                
            else:                    
                if not shardId in data:
                    return ("200 OK", "text/plain", '{"error": "No such shard"}')
                    
                return ("200 OK", "text/plain", _encode({shardId: data[shardId]}))
                
        elif path == "buildings":
            if not self.mgr.shards:
                return ("200 OK", "text/plain", "{}")
                
            lang = args.get('lang', 'en')
            if not ShardAPIManagerUD.setLanguageContext(lang):
                return ("200 OK", "text/plain", '{"error": "No such language"}')
                
            data = self.mgr.writeDict()
            
            shardId = args.get('shardId')
            
            if shardId is not None:
                try:
                    shardId = int(shardId)
                    assert shardId >= 0
                    
                except:
                    return ("200 OK", "text/plain", '{"error": "shardId must an unsigned integer"}')
                    
                if not shardId in data:
                    return ("200 OK", "text/plain", '{"error": "No such shard"}')
                    
            del data

            track = args.get('track')
            if track is not None:
                if track not in ('s', 'm', 'l', 'c'):
                    return ("200 OK", "text/plain", '{"error": "Building track must be s, l, m or c"}')
                    
            height = args.get('height')
            if height is not None:
                try:
                    height = int(height)
                    assert 1 <= height <= 5
                    
                except:
                    return ("200 OK", "text/plain", '{"error": "Building height must an integer between 1 and 5 (both inclusive)"}')
                    
            mh = args.get('mh')
            if mh is not None:
                try:
                    mh = int(mh)
                    assert 1 <= mh <= 5
                    
                except:
                    return ("200 OK", "text/plain", '{"error": "Building max height must an integer between 1 and 5 (both inclusive)"}')
                    
            type = args.get('type', 'suit')
            if not type in ('cogdo', 'suit', 'both'):
                return ("200 OK", "text/plain", '{"error": "Building type must be cogdo, suit or both"}')
                
            if type == 'both':
                type = None
                
            shardList = self.mgr.shards.values()
                
            locationType = "shard" # default
            
            location = args.get('location')
            
            if location:
                try:
                    location = int(location)
                    
                except:
                    return ("200 OK", "text/plain", '{"error": "Location must an integer (zoneId)"}')
                    
                locationType = "street" if location % 1000 else "hood"
                
            if locationType != "shard":
                if locationType == "hood":
                    if not location in shardList[0].hoods:
                        return ("200 OK", "text/plain", '{"error": "Invalid location for hood"}')
                        
                    locationFunc = lambda s: s.hoods[location]
                    
                else:
                    hoodId = location - (location % 1000)
                    if not hoodId in shardList[0].hoods:
                        return ("200 OK", "text/plain", '{"error": "Invalid location for street"}')
                        
                    elif not location in shardList[0].hoods[hoodId].streets:
                        return ("200 OK", "text/plain", '{"error": "Invalid location for street"}')
                        
                    locationFunc = lambda s: s.hoods[hoodId].streets[location]
                
            def scanSingleShard(shard):
                if locationType == "hood":
                    return self.__findBuildingOnHood(locationFunc(shard), track, height, mh, type)
                    
                elif locationType == "street":
                    return self.__findBuildingOnStreet(locationFunc(shard), track, height, mh, type)
                    
                return self.__findBuildingOnShard(shard, track, height, type)
                
            if shardId is None:
                r = {}
                for i, shard in self.mgr.shards.items():
                    r.update({i: scanSingleShard(shard)})
                    
                return ("200 OK", "text/plain", _encode(r))
                
            else:
                return ("200 OK", "text/plain", _encode(scanSingleShard({shardId: self.mgr.shards[shardId]})))
    
    def handleGraphRequest(self, path, hDict, args):
        return RES_401
        
    def __findBuildingOnStreet(self, street, track = None, height = None, mh = None, type = "suit"):
        r = {}
        for block in street.blocks.values():
            if type:
                if block.type != type:
                    continue
            
            if track:
                if block.track != track:
                    continue
                    
            if (height or mh) and type == "suit":
                if block.height < height:
                    continue
                    
                if block.height > mh:
                    continue
                    
            r.setdefault(block.branchZone, []).append({block.number: block.writeDict()})
            
        return r
     
    def __findBuildingOnHood(self, hood, track = None, height = None, mh = None, type = "suit"):
        r = {}
        for street in hood.streets.values():
            r.update(self.__findBuildingOnStreet(street, track, height, type))
            
        return r
        
    def __findBuildingOnShard(self, shard, track = None, height = None, mh = None, type = "suit"):
        r = {}
        for hood in shard.hoods.values():
            r.update({hood.hoodId: self.__findBuildingOnHood(hood, track, height, type)})
            
        return r
        
def start(mgr):
    ws = ShardAPIWebServer(mgr)
    start_new_thread(ws.run, [])
    return ws
    