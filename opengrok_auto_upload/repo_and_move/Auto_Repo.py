#!/usr/bin/python

import os, subprocess, time, errno, glob, sys, logging, signal, argparse, random, pytz
from threading import Thread, Event
from Logger import *
from filelock import FileLock

from datetime import datetime
from dateutil.tz import tzlocal
import requests, yaml, json

META_WATCH = '/local2/mnt/watch'
META_BUILD = '/local2/mnt/META_BUILD'

GROK_LIST = META_WATCH + '/watch_list.txt'
SRC_TEMP_PATH = '/local2/mnt/opengrok_tmp'

OPENGROK = '/local2/mnt/opengrok'
#OPENGROK_SRC = '/local2/mnt/workspace/charlie/opengrok_temp'
P4_SCRIPT = '/local2/mnt/qct_auto_programs/p4_script.sh'
DB_URL = "https://automotive-linux:9999/db/"

AUTO_REPO_LOG=META_WATCH+'/auto_repo.log'
#START_TIME = 00
#END_TIME = 01
START_TIME = 22
END_TIME = 23
class Auto_Repo:
    def __init__(self, log_file=AUTO_REPO_LOG):
        self.log_file = log_file
        self.__stop = False
        self.logger = Logger('worker-{0}'.format(os.getpid()), self.log_file)
        self.child = 0
        self.tz = tzlocal()
    def __check_list(self):
        build_list = []
        dirs = os.listdir(META_BUILD)
        #with open(GROK_LIST, 'r') as f:
        #    sp_list = f.readlines()
        #sp_list = [x.strip() for x in sp_list]
        #for sp in sp_list:
        #    for build in dirs:
        #        if sp + '-' in build:
        #            build_list.append(build)
        #            #dirs.remove(build)

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
            for build in dirs:
                if sp['name'] + '-' in build:
                    build_list.append(build)
        build_list = list(set(build_list))
        return build_list
    def __check_APPS_ID(self, build_name):
        apps_id = ""
        try:
            with open(META_BUILD+'/'+build_name+'/'+'apps_plf_tag', 'r') as f:
                lines = f.readlines()
            lines = [x.strip() for x in lines]
            apps_id = lines[0]
        except:
            pass
        return apps_id
    def __check_GVM_ID(self, build_name):
        gvm_id = ""
        try:
            with open(META_BUILD+'/'+build_name+'/'+'gvm_plf_tag', 'r') as f:
                lines = f.readlines()
            lines = [x.strip() for x in lines]
            gvm_id = lines[0]
        except:
            pass
        return gvm_id
    def __check_AU_TAG(self, build_name):
        au_tag = ""
        if 'HQX.' in build_name:
            try:
                with open(META_BUILD+'/'+build_name+'/'+'gvm_plf_tag', 'r') as f:
                    lines = f.readlines()
                lines = [x.strip() for x in lines]
                au_tag = 'AU_' + lines[1].split('_AU_')[1].split('.plf')[0]
            except:
                pass
        else:
            try:
                with open(META_BUILD+'/'+build_name+'/'+'apps_plf_tag', 'r') as f:
                    lines = f.readlines()
                lines = [x.strip() for x in lines]
                au_tag = 'AU_' + lines[1].split('_AU_')[1].split('.plf')[0]
            except:
                pass
        return au_tag
    def __repo_init_and_sync(self, apps_id, au_tag):
        try:
            if 'LA' in apps_id or 'LE' in apps_id:
                    src = '/src/'
            else:
                    src = '/src/'
            if(os.path.isdir(OPENGROK + src + apps_id)):
                    #print('aleady exists')
                    self.logger.log('repo_init_and_sync', {
                        'status': 'aleady exists'
                    })
                    return False
            path = SRC_TEMP_PATH+'/'+apps_id
            print(path)
            try:
                os.makedirs(path)
                #print('mkdir')
                self.logger.log('repo_init_and_sync', {
                    'status': 'new'
                })
            except:
                #print('aleady exists')
                self.logger.log('repo_init_and_sync', {
                    'status': 'aleady exists'
                })
                return False
            os.chdir(path)
            #print('cd')
            if(os.path.isdir('.repo')):
                #print('aleady exists')
                self.logger.log('repo_init_and_sync', {
                    'status': 'aleady exists'
                })
                return False
            apps_id_split = apps_id.split('-')
            del apps_id_split[-1]
            apps_id =""
            for i in apps_id_split:
                apps_id = apps_id + i + '-'
            apps_id = apps_id[:len(apps_id)-1]
            #print(apps_id)
            #print(au_tag)
            repo_sync = '/usr/bin/repo sync -c --no-tags -j8'
            if not au_tag == '':
                if 'LV' in au_tag or 'LE.UM' in au_tag:
                    repo_command = '/usr/bin/repo init -u git://git.quicinc.com/le/manifest.git -b refs/tags/' + au_tag + ' -m versioned.xml --repo-url=git://git.quicinc.com/tools/repo.git --repo-branch=qc/stable'
                elif 'LA' in au_tag:
                    repo_command = '/usr/bin/repo init -u git://git.quicinc.com/platform/manifest.git -b refs/tags/' + au_tag + ' -m versioned.xml --repo-url=git://git.quicinc.com/tools/repo.git --repo-branch=qc/stable'
                elif 'LE' in au_tag:
                    repo_command = '/usr/bin/repo init -u git://git.quicinc.com/mdm/manifest.git -b refs/tags/' + au_tag + ' -m versioned.xml --repo-url=git://git.quicinc.com/tools/repo.git --repo-branch=qc/stable'
            else:
                #print('Unknown AU TAG')
                self.logger.log('repo_init_and_sync', {
                    'status': 'Unknown AU TAG'
                })
                return False
            self.logger.log('repo_init_and_sync', {
                'repo_command': repo_command
            })
            #print(repo_command)
            proc = subprocess.Popen(repo_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            self.logger.log('repo_init_and_sync', {
                'repo_command': repo_sync
            })
            #print(repo_sync)
            proc2 = subprocess.Popen(repo_sync.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc2.communicate()
        except:
            return False
        return True
    def __p4_sync(self, apps_id):
        try:
            if(os.path.isdir(OPENGROK + '/src/' + apps_id)):
                #print('aleady exists')
                self.logger.log('p4_sync', {
                    'status': 'aleady exists'
                })
                return False
            path = SRC_TEMP_PATH+'/'+apps_id
            print(path)
            try:
                os.makedirs(path)
                #print('mkdir')
                self.logger.log('p4_sync', {
                    'status': 'new'
                })
            except:
                #print('aleady exists')
                self.logger.log('p4_sync', {
                    'status': 'aleady exists'
                })
                return False
            os.chdir(path)
            #print('cd')
            if(os.path.isdir('qnx_ap')):
                self.logger.log('p4_sync', {
                    'status': 'aleady exists'
                })
                return False
            proc = subprocess.Popen(['bash', P4_SCRIPT, apps_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            #print('p4')
            self.logger.log('p4_sync', {
                'p4_command': 'bash ' + P4_SCRIPT + ' '+ apps_id
            })
        except:
            return False
        return True
    def work(self):
        build_list = self.__check_list()
        build_list.sort(reverse=True)
        iterator = ''
        count = 0
        for build in build_list:
            if 'LV_LE' in build or (not 'LV.' in build and not 'QX.' in build and not 'LA.' in build and not 'LE.' in build) or ('Mizar' in build or 'early' in build or 'ethcam' in build):
                continue
            isNew = True
            isNew2 = False
            #print('build : ', build)
            apps_id = self.__check_APPS_ID(build)
            self.logger.log('check_APPS_ID', {
                'build_id': build,
                'apps_id': apps_id
            })
            print('apps id : ', apps_id)
            if apps_id == "":
                continue
            #print 'count : ', count
            if(iterator != build.split('-')[0]):
                iterator = build.split('-')[0]
                count = 1
            if count > 3:
                continue
            if 'HQX' in build:
                gvm_id = self.__check_GVM_ID(build)
                au_tag = self.__check_AU_TAG(build)
                isNew2 = self.__repo_init_and_sync(gvm_id, au_tag)
            if 'QXA' in apps_id:
                isNew = self.__p4_sync(apps_id)
            elif 'LE' in apps_id:
                au_tag = self.__check_AU_TAG(build)
                isNew = self.__repo_init_and_sync(apps_id, au_tag)
            else:
                au_tag = self.__check_AU_TAG(build)
                isNew = self.__repo_init_and_sync(apps_id, au_tag)
            if isNew:
                src_full_path = os.path.join(SRC_TEMP_PATH, apps_id)
                if 'LV.' in build or 'QX.' in build:
                    dst_full_path = os.path.join(OPENGROK+'/src', apps_id)
                elif 'LA.' in build or 'LE.' in build:
                    dst_full_path = os.path.join(OPENGROK+'/src', apps_id)
                if os.path.isdir(dst_full_path):
                    continue
                #print 'src full path: ', src_full_path
                #print 'dst full path: ', dst_full_path
                #print 'chmod 777 -R ', apps_id
                self.logger.log('remove .repo and .git', {
                    'src': src_full_path,
                    'status': 'start'
                })
                remove_repo_and_git(src_full_path)
                self.logger.log('remove .repo and .git', {
                    'src': src_full_path,
                    'status': 'done'
                })
                self.logger.log('chmod_and_move', {
                    'src': src_full_path,
                    'dst': dst_full_path,
                    'status': 'chmod start'
                })
                chmod(SRC_TEMP_PATH + '/' + apps_id)
                self.logger.log('chmod_and_move', {
                    'status': 'chmod done, move start'
                })
                #print 'Done'
                #print 'mv ', src_full_path, ' ', dst_full_path
                move(src_full_path, dst_full_path)
                self.logger.log('chmod_and_move', {
                    'status': 'Done'
                })
                #print 'Done'
            if isNew2:
                src_full_path = os.path.join(SRC_TEMP_PATH, gvm_id)
                if 'LV.' in gvm_id:
                    dst_full_path = os.path.join(OPENGROK+'/src', gvm_id)
                elif 'LA.' in gvm_id:
                    dst_full_path = os.path.join(OPENGROK+'/src', gvm_id)
                if os.path.isdir(dst_full_path):
                    continue
                self.logger.log('chmod_and_move', {
                    'src': src_full_path,
                    'dst': dst_full_path,
                    'status': 'chmod start'
                })
                chmod(SRC_TEMP_PATH + '/' + gvm_id)
                self.logger.log('chmod_and_move', {
                    'status': 'chmod done, move start'
                })
                move(src_full_path, dst_full_path)
                self.logger.log('chmod_and_move', {
                    'status': 'Done'
                })
            count += 1
    def main(self):
        self.logger.log('start', {
            'pid': os.getpid()
        })
        random.seed(os.getpid())
        while not self.__stop and not os.path.isfile('/var/log/auto_repo/auto_repo.log'):
            now_hour = datetime.now(tz=self.tz).hour
            if now_hour == START_TIME or now_hour == END_TIME:
       		self.logger.log('message', 'It\'s time to start')
       		self.work()
            time.sleep(600)
        self.logger.log('stop', {
            'pid': os.getpid()
        })
        return 0
    def stop(self):
        self.__stop = True

def remove_repo_and_git(dir):
    cmd = 'find ' + dir +' -name .git -exec rm -rf {} ;'
    cmd2 = 'find ' + dir + ' -name .repo -exec rm -rf {} ;'
    proc = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc2 = subprocess.Popen(cmd2.split(), stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    proc2.communicate()
def chmod(dir):
    cmd = 'chmod 777 -R '+ dir
    proc = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
def move(src, dst):
    if os.path.isdir(dst) :
        return False
    cmd = 'mv ' + src + ' ' + dst
    proc = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return True

