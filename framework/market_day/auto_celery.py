#!usr/bin/ebv python
# -*- coding:utf-8 -*-
import threading
import os

class auto_celery(threading.Thread):
    def run(self):
        parent_path=os.path.dirname(os.path.dirname(__file__))
        p=parent_path[0:2]
        command='cd '+ parent_path+'&&'+p+'&&'+'celery -A conf worker --loglevel=info --pool=solo'
        os.system(command)
