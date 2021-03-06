#!/usr/bin/python

import os, subprocess, time, errno, glob, sys, logging, signal, argparse, random, pytz
from threading import Thread, Event
from Logger import *
from filelock import FileLock

from datetime import datetime
from dateutil.tz import tzlocal

META_WATCH = '/local2/mnt/watch'
OPENGROK_SRC = '/local2/mnt/opengrok/src'
OPENGROK_IDX = '/local2/mnt/opengrok/data/index'
GROK_UPDATE_LOG=META_WATCH+'/grok_update.log'
GROK_URL = 'https://automotive-linux:7070/source'
START_TIME = 3
END_TIME = 4
class Grok_Update:
    def __init__(self, log_file=GROK_UPDATE_LOG):
        self.log_file = log_file
        self.__stop = False
        self.logger = Logger('worker-{0}'.format(os.getpid()), self.log_file)
        self.child = 0
        self.tz = tzlocal()
    
    def __check_list(self):
        update_list = []
	dirs_src = []
	dirs_idx = []
        dirs_src_tmp = os.listdir(OPENGROK_SRC)
        for entry_src in dirs_src_tmp:
	    if os.path.isdir(os.path.join(OPENGROK_SRC,entry_src)):
		dirs_src.append(entry_src)
	dirs_idx_tmp = os.listdir(OPENGROK_IDX)
        
	for entry_idx in dirs_idx_tmp:
            if os.path.isdir(os.path.join(OPENGROK_IDX,entry_idx)):
                dirs_idx.append(entry_idx)

        for src in dirs_src:
            if src not in dirs_idx:
                update_list.append(src)
                
        return update_list
        
    def work(self):
        self.logger.log('work', 'OpenGrok_LV_LA_QXA_MDM update - run')
        update_list = self.__check_list()
        if len(update_list) == 0:
            self.logger.log('work','latest index status, no update')
            return 0
        self.logger.log('update_list : ',update_list)
        for update_src in update_list:
            idx_cmd = 'java -Djava.util.logging.config.file=/local2/mnt/opengrok/etc/logging.properties -jar /local2/mnt/opengrok/dist/lib/opengrok.jar -s /local2/mnt/opengrok/src -d /local2/mnt/opengrok/data -c /usr/local/bin/ctags -W /local2/mnt/opengrok/etc/configuration.xml -U '+GROK_URL+' '+update_src
            try:
                self.logger.log('now update ',update_src)
                update_idx = subprocess.Popen(idx_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                (stdout,stderr)=update_idx.communicate()
		print(stdout)
            except Exception as ex:
                self.logger.log('update failed ',update_src,{'err' : str(ex)})
            self.logger.log('finish update ',update_src)
            
        self.logger.log('work', 'OpenGrok_LV_LA_QXA_MDM update - done')

    def main(self):
        self.logger.log('start', {
            'pid': os.getpid()
        })
        random.seed(os.getpid())
        while not self.__stop and not os.path.isfile('/var/log/opengrok_auto/grok_update.log'):
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
