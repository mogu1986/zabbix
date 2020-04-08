#!/usr/bin/python

import sys, redis, json, re, struct, time, socket, argparse

parser = argparse.ArgumentParser(description='Zabbix Redis status script')
parser.add_argument('redis_hostname',nargs='?',default='localhost')
parser.add_argument('metric',nargs='?')
parser.add_argument('redis_port',nargs='?',type=int, default=6379)
parser.add_argument('-d','--db',dest='db',action='store',help='Redis server db',default='none')
parser.add_argument('-a','--auth',dest='redis_pass',action='store',help='Redis server pass',default=None)
args = parser.parse_args()


# Name of monitored server like it shows in zabbix web ui display
redis_hostname = args.redis_hostname if args.redis_hostname else socket.gethostname()

class Metric(object):
    def __init__(self, host, key, value, clock=None):
        self.host = host
        self.key = key
        self.value = value
        self.clock = clock

    def __repr__(self):
        result = None
        if self.clock is None:
            result = 'Metric(%r, %r, %r)' % (self.host, self.key, self.value)
        else:
            result = 'Metric(%r, %r, %r, %r)' % (self.host, self.key, self.value, self.clock)
        return result


def _recv_all(sock, count):
    buf = ''
    while len(buf)<count:
        chunk = sock.recv(count-len(buf))
        if not chunk:
            return buf
        buf += chunk
    return buf

def main():
    if redis_hostname and args.metric:
        client = redis.StrictRedis(host=redis_hostname, port=args.redis_port, password=args.redis_pass)
        server_info = client.info()

        if args.metric:
            if args.db and args.db in server_info.keys():
                server_info['key_space_db_keys'] = server_info[args.db]['keys']
                server_info['key_space_db_expires'] = server_info[args.db]['expires']
                server_info['key_space_db_avg_ttl'] = server_info[args.db]['avg_ttl']

            def llen():
                print(client.llen(args.db))

            def llensum():
                llensum = 0
                for key in client.scan_iter('*'):
                    if client.type(key) == 'list':
                        llensum += client.llen(key)
                print(llensum)

            def list_key_space_db():
                if args.db in server_info:
                    print(args.db)
                else:
                    print('database_detect')

            def default():
                if args.metric in server_info.keys():
                    print(server_info[args.metric])

            {
                'llen': llen,
                'llenall': llensum,
                'list_key_space_db': list_key_space_db,
            }.get(args.metric, default)()

        else:
            print('Not selected metric')
    else:
        client = redis.StrictRedis(host=redis_hostname, port=args.redis_port, password=args.redis_pass)
        server_info = client.info()

        a = []
        for i in server_info:
            a.append(Metric(redis_hostname, ('redis[%s]' % i), server_info[i]))

        llensum = 0
        for key in client.scan_iter('*'):
            if client.type(key) == 'list':
                llensum += client.llen(key)
        a.append(Metric(redis_hostname, 'redis[llenall]', llensum))


if __name__ == '__main__':
    main()
