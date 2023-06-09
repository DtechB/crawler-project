import gevent
import warnings
import sys
import dns.resolver
import time
import optparse
import os
import psycopg2
from decouple import config
from gevent import monkey
from gevent.pool import Pool
from gevent.queue import PriorityQueue
from multiprocessing import cpu_count
from datetime import datetime

warnings.simplefilter("ignore", category=UserWarning)
# monkey.patch_all()

threads_count = 50

absolute_path = os.path.dirname(__file__)

conn = psycopg2.connect(database="alpha", user=config(
    "DATABASE_USERNAME"), password=config('DATABASE_PASSWORD'), host="localhost", port="5432")
cur = conn.cursor()

subdomains = []

# Fetch subdomains


def FetchBrokenLinks():
    cur.execute("SELECT id, base, subdomain,ip from api_subdomain")
    rows = cur.fetchall()
    for row in rows:
        subdomains.append(row[2])


# Add subdomain
def AddSubdomain(base, subdomain, ip, site_id):
    if subdomain not in subdomains:
        subdomains.append(subdomain)
        cur.execute("INSERT INTO api_subdomain (created_at, base, subdomain,ip, site_id) \
                                                  VALUES ('{}', '{}', '{}', '{}', '{}')".format(str(datetime.now()), base, subdomain, ip, site_id))
        conn.commit()


class SubNameBrute:
    def __init__(self, target, site_id):
        self.start_time = time.time()
        self.target = target.strip()
        self.scan_count = self.found_count = 0
        self.console_width = os.get_terminal_size()[0] - 2
        self.site_id = site_id

        # create dns resolver pool ~ workers
        self.resolvers = [dns.resolver.Resolver(
            configure=False) for _ in range(50)]
        for resolver in self.resolvers:
            resolver.lifetime = resolver.timeout = 10.0

        self.print_count = 0
        self.STOP_ME = False

        # load dns servers and check whether these dns servers works fine ?
        self._load_dns_servers()

        # load sub names
        self.subs = []  # subs in file
        self.goodsubs = []  # checks ok for further exploitation
        subnamesAddress = "dict/subnames.txt"
        full_path_subname = os.path.join(absolute_path, subnamesAddress)
        self._load_subname(full_path_subname, self.subs)

        # load sub.sub names
        self.subsubs = []
        nextSubAddress = "dict/next_sub.txt"
        full_path_nextSub = os.path.join(absolute_path, nextSubAddress)
        self._load_subname(full_path_nextSub, self.subsubs)

        # results will save to target.txt
        global path
        path = os.path.join("results", target)
        if not os.path.exists(path):
            os.makedirs(path)

        self.outfile = open('%s/%s.txt' % (path, target), 'w')
        self.ip_dict = set()  #
        self.found_sub = set()

        # task queue
        self.queue = PriorityQueue()
        for sub in self.subs:
            self.queue.put(sub)

    """
        Load DNS Servers(ip saved in file), and check whether the DNS servers works fine
    """

    def _load_dns_servers(self):
        print('[*] Validate DNS servers ...')
        self.dns_servers = []

        # create a process pool for checking DNS servers, the number is your processors(cores) * 2, just change it!
        processors = cpu_count() * 2
        pool = Pool(processors)

        # read dns ips and check one by one
        dnsServersAddress = "dict/dns_servers.txt"
        full_path_dnsServers = os.path.join(absolute_path, dnsServersAddress)
        for server in open(full_path_dnsServers).readlines():
            server = server.strip()
            if server:
                pool.apply_async(self._test_server, (server,))

        pool.join()  # waiting for process finish
        self.dns_count = len(self.dns_servers)

        sys.stdout.write('\n')
        dns_info = '[+] Found {} available DNS Servers in total'.format(
            self.dns_count)
        print(dns_info)

        if self.dns_count == 0:
            print('[ERROR] No DNS Servers available.')
            sys.exit(-1)

    """
        test these dns servers whether works fine
    """

    def _test_server(self, server):

        # create a dns resolver and set timeout
        resolver = dns.resolver.Resolver()
        resolver.lifetime = resolver.timeout = 10.0

        try:
            resolver.nameservers = [server]
            answers = resolver.resolve('public-dns-a.baidu.com')
            if answers[0].address != '180.76.76.76':
                raise Exception('incorrect DNS response')
            self.dns_servers.append(server)
        except:
            self._print_msg('[-] Check DNS Server %s <Fail>   Found %s' %
                            (server.ljust(16), len(self.dns_servers)))

        self._print_msg('[+] Check DNS Server %s < OK >   Found %s' %
                        (server.ljust(16), len(self.dns_servers)))

    """
        load sub names in findSubDomains/dict/*.txt, one function would be enough
        file for read, subname_list for saving sub names
    """

    def _load_subname(self, file, subname_list):
        self._print_msg('[*] Load sub names ...')

        with open(file) as f:
            for line in f:
                sub = line.strip()
                if sub and sub not in subname_list:
                    tmp_set = {sub}

                    """
                        in case of the sub names which contains the following expression
                        and replace them {alphnum}, {alpha}, {num} with character and num
                    """
                    while len(tmp_set) > 0:
                        item = tmp_set.pop()
                        if item.find('{alphnum}') >= 0:
                            for _letter in 'abcdefghijklmnopqrstuvwxyz0123456789':
                                tmp_set.add(item.replace(
                                    '{alphnum}', _letter, 1))
                        elif item.find('{alpha}') >= 0:
                            for _letter in 'abcdefghijklmnopqrstuvwxyz':
                                tmp_set.add(item.replace(
                                    '{alpha}', _letter, 1))
                        elif item.find('{num}') >= 0:
                            for _letter in '0123456789':
                                tmp_set.add(item.replace('{num}', _letter, 1))
                        elif item not in subname_list:
                            subname_list.append(item)

    """
        for better presentation of brute force results, not really matters ...
    """

    def _print_msg(self, _msg=None, _found_msg=False):
        if _msg is None:
            self.print_count += 1
            if self.print_count < 100:
                return
            self.print_count = 0
            msg = '%s Found| %s Groups| %s scanned in %.1f seconds' % (
                self.found_count, self.queue.qsize(), self.scan_count, time.time() - self.start_time)
            sys.stdout.write(
                '\r' + ' ' * (self.console_width - len(msg)) + msg)
        elif _msg.startswith('[+] Check DNS Server'):
            sys.stdout.write('\r' + _msg + ' ' *
                             (self.console_width - len(_msg)))
        else:
            sys.stdout.write('\r' + _msg + ' ' *
                             (self.console_width - len(_msg)) + '\n')
            if _found_msg:
                msg = '%s Found| %s Groups| %s scanned in %.1f seconds' % (
                    self.found_count, self.queue.qsize(), self.scan_count, time.time() - self.start_time)
                sys.stdout.write(
                    '\r' + ' ' * (self.console_width - len(msg)) + msg)
        sys.stdout.flush()

    def _print_domain(self, msg):
        console_width = os.get_terminal_size()[0]
        msg = '\r' + msg + ' ' * (console_width - len(msg))
        sys.stdout.write(msg)

    def _print_progress(self):
        msg = '\033[0;31;47m%s\033[0m found | %s remaining | %s scanned in %.2f seconds' % \
              (self.found_count, self.queue.qsize(),
               self.scan_count, time.time() - self.start_time)

        console_width = os.get_terminal_size()[0]
        out = '\r' + ' ' * int((console_width - len(msg)) / 2) + msg
        sys.stdout.write(out)

    """
        important : assign task to resolvers
    """

    def _scan(self, j):
        self.resolvers[j].nameservers = [self.dns_servers[j % self.dns_count]]
        while not self.queue.empty():
            sub = self.queue.get(timeout=1.0)
            self.scan_count += 1

            try:
                cur_sub_domain = sub + '.' + self.target
                answers = self.resolvers[j].resolve(cur_sub_domain)
            except:
                continue

            if answers:
                ips = ', '.join(sorted([answer.address for answer in answers]))

                # exclude : intranet or kept addresses
                if ips in ['1.1.1.1', '127.0.0.1', '0.0.0.0', '0.0.0.1']:
                    continue
                if SubNameBrute.is_intranet(answers[0].address):
                    continue

                self.found_sub.add(cur_sub_domain)
                for answer in answers:
                    self.ip_dict.add(answer.address)

                if sub not in self.goodsubs:
                    self.goodsubs.append(sub)

                self.found_count += 1
                ip_info = '{} \t {}'.format(cur_sub_domain, ips)
                # print(ip_info)
                AddSubdomain(self.target, cur_sub_domain, ips, self.site_id)
                self.outfile.write(cur_sub_domain + '\t' + ips + '\n')
                self._print_domain(ip_info)
                sys.stdout.flush()
                self._print_progress()
                sys.stdout.flush()

    @staticmethod
    def is_intranet(ip):
        ret = ip.split('.')
        if len(ret) != 4:
            return True
        if ret[0] == '10':
            return True
        if ret[0] == '172' and 16 <= int(ret[1]) <= 32:
            return True
        if ret[0] == '192' and ret[1] == '168':
            return True
        return False

    def run(self):
        threads = [gevent.spawn(self._scan, i) for i in range(threads_count)]

        print('[*] Initializing %d threads' % threads_count)

        try:
            gevent.joinall(threads)
        except KeyboardInterrupt as e:
            msg = '[WARNING] User aborted.'
            sys.stdout.write('\r' + msg + ' ' *
                             (self.console_width - len(msg)) + '\n\r')
            sys.stdout.flush()


def wildcard_test(dns_servers, domain, level=1):
    try:
        r = dns.resolver.Resolver(configure=False)
        r.nameservers = dns_servers
        answers = r.resolve('lijiejie-not-existed-test.%s' % domain)
        ips = ', '.join(sorted([answer.address for answer in answers]))
        if level == 1:
            print('any-sub.%s\t%s' % (domain.ljust(30), ips))
            wildcard_test(dns_servers, 'any-sub.%s' % domain, 2)
        elif level == 2:
            exit(0)
    except Exception as e:
        return domain


def runSubdomain(id, url):
    FetchBrokenLinks()
    parser = optparse.OptionParser(
        'usage: %prog [options] target.com', version="%prog 2.0")
    parser.add_option('-f', dest='file', default='subnames.txt',
                      help='Dictionary file, default is subnames.txt.')
    parser.add_option('--full', dest='full_scan', default=False, action='store_true',
                      help='To carry out full bruteforce, subnames_full.txt will be used as dictionary file')
    parser.add_option('-t', '--threads', dest='threads', default=50, type=int,
                      help='Num of scan threads, 100 by default')

    # initialization ...
    d = SubNameBrute(target=url, site_id=id)
    wildcard_test(d.dns_servers, url)

    print('[*] Exploiting level-one sub domains of ', url)
    print('[+] There are %d subs waiting for trying ...' % len(d.queue))
    print('--------------------------------------')
    d.run()
    print('--------------------------------------')
    print('%d subnames found' % len(d.found_sub))
    print('[*] Program running %.1f seconds ' % (time.time() - d.start_time))

    print('Exploiting level-two sub domains ... ')
    time.sleep(1)

    d.queue = PriorityQueue()
    for subsub in d.subsubs:
        for sub in d.goodsubs:
            subname = subsub + '.' + sub
            d.queue.put(subname)

    print('There are %d subs waiting for trying ...' % len(d.queue))
    d.run()
    print()
    sys.stdout.flush()
    print('%d subnames found in total' % len(d.found_sub))

    """
        save ips and domains to files
    """

    ipFileName = url + '-ip.txt'
    subDomainsFileName = url + '-subdomain.txt'

    with open(os.path.join(path, ipFileName), 'w') as f:
        for ip in d.ip_dict:
            f.write(ip + '\n')

    with open(os.path.join(path, subDomainsFileName), 'w') as f:
        for domain in d.found_sub:
            f.write(domain + '\n')

    print('[*] Program running %.1f seconds ' % (time.time() - d.start_time))

    d.outfile.flush()
    d.outfile.close()
