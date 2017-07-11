import sh
import os
import datetime
import time

REMOTE_WEB_SERVER = 'root@109.68.190.75'
SOURCE_DIR = '/var/log/nginx/'
DESTINATION_DIR = '/sv_weblogs/vtb24leasing/'
DATE_SHIFT = 1
NAMES_PREFIX = 'acc'
NAMES_POSTFIX = '_access.log.gz'


def get_dateprefix(lt):
    return "{0}{1}{2}".format(str(lt.tm_year), (str(lt.tm_mon) if lt.tm_mon > 9 else '0' + str(lt.tm_mon)),
                              str(lt.tm_mday))


yesterday = time.localtime(time.time() - 86400 * DATE_SHIFT)
source_date = datetime.date(yesterday.tm_year, yesterday.tm_mon, yesterday.tm_mday)
source_month = source_date.strftime('%b')
destination_file_name = get_dateprefix(yesterday) + NAMES_POSTFIX

remote_server = sh.ssh.bake(REMOTE_WEB_SERVER)

file_list = remote_server.ls('-l {}'.format(SOURCE_DIR)).stdout.decode('utf-8').split('\n')

for filename in file_list[1:-1]:
    fa = filename.split()
    if NAMES_PREFIX in fa[8]:
        curr_day, curr_month = fa[6], fa[5]
        if curr_month == source_month and curr_day == str(yesterday.tm_mday):
            source_file_name = fa[8]
            break

os.system('scp {}:{}{} {}{}'.format(REMOTE_WEB_SERVER, SOURCE_DIR, source_file_name,
                                    DESTINATION_DIR, destination_file_name))
