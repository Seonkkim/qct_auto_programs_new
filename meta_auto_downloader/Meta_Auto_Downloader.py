#!/bin/python

'''
Description
 Meta Download script for Qualcomm Automotive CE Korea
Author
 Name : Charlie Kang
 Email : c_hwanch@qti.qualcomm.com
'''

import subprocess, time, os, errno, glob, sys, logging, signal, argparse, random
from threading import Thread, Event
from Logger import *
from filelock import FileLock

from datetime import datetime
import pytz
from dateutil.tz import tzlocal
import requests, yaml, json

CUR_PATH='/local2/mnt'
FINDBUILD='/prj/qct/asw/qctss/linux/bin//FindBuild'
PREFIX='/prj/qct/asw/crmbuilds'
OPENGROK_SRC = 'local2/mnt/opengrok/src'
BUILD_PATH='common/build'
BUILD_PATH_ALT='common/tools/meta'
PYTHON_GEN_MIN='gen_minimized_build.py'

META_BUILD_ROOT=CUR_PATH+'/META_BUILD'
WATCH_DIR=CUR_PATH+'/watch'
WATCH_LIST=WATCH_DIR+'/watch_list.txt'

META_LOG=WATCH_DIR+'/_meta_down_c.log'
DB_URL = "https://automotive-linux:9999/db/"

START_TIME = 9
END_TIME = 10
MAX_DOWNLOAD_CNT = 3

class Meta_Auto_Downloader:
    def __init__(self, log_file=META_LOG):
	self.log_file = log_file
	self.__stop = False
	cmd = 'chmod 777 -R '+ log_file
        proc = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	self.logger = Logger('worker-{0}'.format(os.getpid()), self.log_file)
	self.child = 0
        self.tz = tzlocal()
    def __search_meta__(self):
	sp_list = []
	#with FileLock(WATCH_LIST) as lock:
        #    lock.__enter__()
        #    f = open(lock.file_name, 'r')
        #    list = f.readlines()
        #    f.close()
        #    lock.release()

	while True: 
	    try:	
		response = requests.get(DB_URL+'sp/', headers={"Content-Type": "application/json"}, verify=False)
		break
	    except:
		print("Connection refused by the server..")
		print("Let me sleep for 5 seconds")
		print("ZZzzzz...")
		time.sleep(5)
		print("Was a nice sleep, now let me continue...")
		continue
		
		
	sp_list = response.json()
        for sp in sp_list:
            sp = yaml.safe_load(json.dumps(sp))
            self.logger.log('search_meta', {
                'sp': sp['name']
            })
            sp = sp['name']
            proc = subprocess.Popen([FINDBUILD, sp+'-*', '-lo', '-com', '-se', '0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, error) = proc.communicate()
            self.logger.log('find_build', {
                'stdout' : 'Start FindBuild',#stdout
		'content' : stdout
            })
            lines = stdout.split('\n')
            isNew = False
            BUILD_ID = ""
            BUILD_DATE = ""
            LINUX_PATH = ""
            build_list = []
            global MAX_DOWNLOAD_CNT
            for line in lines:
                if 'Build:' in line:
                    BUILD_ID = line.split()[1]
                    if '.c' not in sp and '.c' in BUILD_ID:
                        continue	
                    if 'APQ8096AU.LA.1.3' in BUILD_ID and 'c1' not in BUILD_ID or 'MSM8996AU.QX.1.0' in BUILD_ID:
		    	MAX_DOWNLOAD_CNT = 6
			print('MAX_DOWNLOAD_CHANGED->6')
		    else: 
			MAX_DOWNLOAD_CNT = 3 
		    build_list.append(BUILD_ID)
		    
            
	    

	    if len(build_list) > MAX_DOWNLOAD_CNT:
                latest_build_list = build_list[len(build_list)-MAX_DOWNLOAD_CNT:]
                old_build_list = build_list[:len(build_list)-MAX_DOWNLOAD_CNT]
            else:
                latest_build_list = build_list[:]
                old_build_list = []
            for BUILD_ID in latest_build_list:
                isNew = False
                isRegular = False
                META_MIN_OUTPUT=META_BUILD_ROOT+'/'+BUILD_ID
                
                if not os.path.isdir(META_MIN_OUTPUT):
                    isNew = True
                    self.logger.log('find_build', {
                        'build_id': BUILD_ID,
                        'status': 'new'
                    })
                else:
                    self.logger.log('find_build', {
                        'build_id': BUILD_ID,
                        'status': 'aleady_exists'
                    })
		    continue
                    apps, plf_tag = self.__find_plf_tag__(BUILD_ID)
                    try:
                        if not apps == '':
                            f_plf = open(META_BUILD_ROOT+'/'+BUILD_ID+'/apps_plf_tag', 'w')
                            f_plf.write(apps+ '\n')
                            f_plf.write(plf_tag)
                            f_plf.close()
                            self.logger.log('find_plf_tag', {
                                'status': 'apps_plf_tag write done'
                            })
                    except Exception as ex:
                        self.logger.log('find_plf_tag', {
                            'status': 'apps_plf_tag write failed',
                            'sys_msg': str(ex)
                        })                

                proc = subprocess.Popen([FINDBUILD, BUILD_ID, '-lo', '-com', '-se', '0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                (stdout, error) = proc.communicate()
                self.logger.log('find_build', {
                    'stdout' : 'Start FindBuild'#stdout
                })
                lines2 = stdout.split('\n')
                for line2 in lines2:
                    if isNew and 'BuildDate:' in line2:
                        BUILD_DATE = line2.split()[1]
                        RELEASE_YEAR = BUILD_DATE.split()[0].split('/')[2]
                        if(int(RELEASE_YEAR) < 2018):
                            self.logger.log('find_plf_tag', {
                                'status': 'It is old.'
                            })
                            isNew = False
                    if isNew and 'LinuxPath:' in line2:
                        LINUX_PATH = line2.split()[1]
                        #self.__copy_meta_min__(BUILD_ID, LINUX_PATH, META_MIN_OUTPUT)
                        apps, plf_tag = self.__find_plf_tag__(BUILD_ID)
                        self.__mkdir_p__(META_BUILD_ROOT+'/'+BUILD_ID)
                        for r, d, f in os.walk(META_BUILD_ROOT+'/'+BUILD_ID):
                            os.chmod(r, 0o777)
                        try:
                            if not apps == "":
                                f_plf = open(META_BUILD_ROOT+'/'+BUILD_ID+'/apps_plf_tag', 'w')
                                f_plf.write(apps+ '\n')
                                f_plf.write(plf_tag)
                                f_plf.close()
                                self.logger.log('find_plf_tag', {
                                    'status': 'apps_plf_tag write done'
                                })
                        except Exception as ex:
                            self.logger.log('find_plf_tag', {
                                'status': 'apps_plf_tag write failed',
                                'sys_msg': str(ex)
                            })
	    for BUILD_ID in old_build_list:
		META_MIN_OUTPUT=META_BUILD_ROOT+'/'+BUILD_ID
		if os.path.isdir(META_MIN_OUTPUT):
		    TAG_FILE = META_MIN_OUTPUT+'/'+'apps_plf_tag'
		    if os.path.isfile(TAG_FILE):
			try:			    
			    f = open(TAG_GILE)
			    src_name = f.readline().split()[0]
			    rm_src_build = 'rm -rf' + OPENGROK_SRC +'/'+src_name
			    os.chmod(OPENGROK_SRC+src_name,0o777)
			    proc = subprocess.Popen(rm_src_cmd.split(), stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    	    proc.communicate()
			    self.logger.log('remove_old_internal_src',{
                            	'src' : src_name,
                            	'status' : 'remove done'
				})
		    	except Exception as ex:
			    self.logger.log('remove_old_internal_src',{
			        'src' : BUILD_ID + ' old',
			        'status' : 'remove failed',
				'sys_msg' : str(ex)
				})
		    try:
			rm_build_cmd = 'rm -rf ' + META_MIN_OUTPUT
		        proc = subprocess.Popen(rm_build_cmd.split(), stdin=subprocess.PIPE, stderr=subprocess.PIPE)
		        proc.communicate()
			self.logger.log('remove_old_build',{
                            'build_id' : BUILD_ID,
                            'status' : 'remove done'
                            })
		    except Exception as ex:
                        self.logger.log('remove_old_build',{
                            'src' : BUILD_ID,
                            'status' : 'remove failed',
			    'sys_msg' : str(ex)
			    })     

    def __find_plf_tag__(self, BUILD_ID):
        if not os.path.isfile(META_BUILD_ROOT+'/'+BUILD_ID+'/'+'apps_plf_tag'):
            self.logger.log('find_plf_tag', {
                'status': 'new'
            })
        else:
            self.logger.log('find_plf_tag', {
                'status': 'aleady_exists'
            })
        proc = subprocess.Popen([FINDBUILD, BUILD_ID, '-lo', '-com', '-se', '0', '-info=MainMake'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, error) = proc.communicate()
        self.logger.log('find_plf_tag', {
            'status': 'FindBuild -lo -com -se 0 -info=MainMake',
        })
        words = stdout.split()
        apps_id = ""
        gvm_id = ""
        plf_tag = ""
        for word in words:
            if 'tz_' not in word and 'apps:' in word:
		
                apps_id = word.split(':')[1]
                print apps_id
                self.logger.log('find_plf_tag', {
                    'status':'apps id found',
                    'apps': apps_id
                })
                parsing = apps_id.split('.')
                #for i in range(1, len(parsing)):
                parsing.remove(parsing[-1])
                str_search = ""
                if not 'LE' in apps_id :
                    for j in parsing:
                        str_search += j
                        if not j == parsing[-1]:
                            str_search += '.'
                else:
                    str_search = apps_id
                proc = subprocess.Popen([FINDBUILD, str_search, '-info=plf'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                (stdout2, error2) = proc.communicate()
                if not stdout2 == "":
		    plf_tag = stdout2
                    #if 'Could' in stdout2:
                    #    plf_tag = (stdout2.split('\n'))[1]
                    #else:
                    #    plf_tag = stdout2
                    self.logger.log('find_plf_tag', {
                        'status':'plf tag found',
                        'command': FINDBUILD + ' ' + str_search + ' -info=plf',
                        'plf_tag': plf_tag
                    })
                if not 'HQX' in BUILD_ID:
                    break
            if 'gvm:' in word:
                gvm_id = word.split(':')[1]
                print gvm_id
                self.logger.log('find_plf_tag', {
                    'status': 'gvm id found',
                    'gvm': gvm_id
                })
                break
        if 'HQX' in BUILD_ID:
            self.__find_gvm_tag__(BUILD_ID, gvm_id)
	
        return apps_id, plf_tag
    def __find_gvm_tag__(self, BUILD_ID, gvm_id):
        if not os.path.isfile(META_BUILD_ROOT+'/'+BUILD_ID+'/'+'gvm_plf_tag'):
            self.logger.log('find_gvm_tag', {
                'status': 'new'
            })
        else:
            self.logger.log('find_plf_tag', {
                'status': 'aleady_exists'
            })
	    return 0
        gvm_tag = ""
        proc = subprocess.Popen([FINDBUILD, gvm_id, '-info=plf'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, error) = proc.communicate()
        if not stdout == "":
	    gvm_tag = stdout
            #if 'Could' in stdout:
            #    gvm_tag = (stdout.split('\n'))[1
            #else:
            #    gvm_tag = stdout
            self.logger.log('find_gvm_tag', {
                'status': 'gvm tag found',
                'command': FINDBUILD + ' ' + gvm_id + ' -info=plf',
                'gvm_tag': gvm_tag
            })
	self.__mkdir_p__(META_BUILD_ROOT+'/'+BUILD_ID)
        for r, d, f in os.walk(META_BUILD_ROOT+'/'+BUILD_ID):
            os.chmod(r, 0o777)
        try:
            if not gvm_id == "":
                f_plf = open(META_BUILD_ROOT+'/'+BUILD_ID+'/gvm_plf_tag', 'w')
                f_plf.write(gvm_id+ '\n')
                f_plf.write(gvm_tag)
                f_plf.close()
                self.logger.log('find_plf_tag', {
                    'status': 'gvm_plf_tag write done'
                })
        except Exception as ex:
            self.logger.log('find_plf_tag', {
                'status': 'gvm_plf_tag write failed',
                'sys_msg': str(ex)
            })
    """
    def __copy_meta_min__(self, BUILD_ID, LINUX_PATH, META_MIN_OUTPUT):
        TOOL_PATH=LINUX_PATH+'/'+BUILD_PATH+'/'+PYTHON_GEN_MIN
        if not os.path.isfile(TOOL_PATH):
            TOOL_PATH=LINUX_PATH+'/'+BUILD_PATH_ALT+'/'+PYTHON_GEN_MIN
            self.logger.log('toolpath', {
                'alternative': 'true',
                'path': TOOL_PATH
            })
        else:
            self.logger.log('toolpath', {
                'alternative': 'false',
                'path': TOOL_PATH
            })
        if not os.path.isfile(TOOL_PATH):
            self.logger.log('tool', {
                'status': 'not_found',
                'path': PYTHON_GEN_MIN
            })
            return
        else:
            self.logger.log('tool', {
                'status': 'exists',
                'path': PYTHON_GEN_MIN
            })
        self.__mkdir_p__(META_MIN_OUTPUT+'.doing')
        for r, d, f in os.walk(META_MIN_OUTPUT+'.doing'):
            os.chmod(r, 0o777)
        try :
            proc = subprocess.Popen(['grep', '\"gen_minimized_build.py -- dest=<dest>\"', TOOL_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (GEN_TOOL_VER, error) = subprocess.communicate()
            OUTPUT_OPTION="--dest="
        except :
            OUTPUT_OPTION=""
        COMMAND = 'python '+TOOL_PATH+" "+OUTPUT_OPTION+META_MIN_OUTPUT+'.doing'
        self.logger.log('copy_meta', {
            'status': 'running',
            'command': COMMAND,
            'build_id': BUILD_ID
        })
        stdout, stderr, returncode = self.__exec_command__(['python', TOOL_PATH, OUTPUT_OPTION+META_MIN_OUTPUT+'.doing'], 36000)
        self.logger.log('copy_meta', {
            'status': returncode,
            'stdout': stdout,
            'stderr': stderr,
            'command': COMMAND,
            'build_id': BUILD_ID
        })
        os.rename(META_MIN_OUTPUT+'.doing', META_MIN_OUTPUT)
    def __exec_command__(self, command, timeout):
        done = Event()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.child = process.pid

        watcher = Thread(target=self.__kill_on_timeout__, args=(done, timeout, process))
        watcher.daemon = True
        watcher.start()

        stdout, stderr = process.communicate()
        done.set()

        return stdout, stderr, process.returncode
    """
    def __kill_on_timeout__(self, done, timeout, process):
        if not done.wait(timeout):
            process.kill()
    def __mkdir_p__(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else :
                raise
    def main(self):
        self.logger.log('start', {
            'pid': os.getpid()
        })
        random.seed(os.getpid())
        while not self.__stop and not os.path.isfile('/var/log/meta_auto_down/meta.log'):
            now_hour = datetime.now(tz=self.tz).hour
            if now_hour == START_TIME or now_hour == END_TIME:
        	self.logger.log('message', 'It\'s time to start')
    		self.__search_meta__()
            time.sleep(600)
        self.logger.log('stop', {
            'pid': os.getpid()
        })
        return 0
    def stop(self):
        self.__stop = True


