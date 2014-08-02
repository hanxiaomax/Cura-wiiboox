#-*- coding: utf-8 -*-
from __future__ import absolute_import

import optparse 
import sys
import os
import threading
#ugly hack:add makerbot_driver to sys.path to import
driver_path=os.path.dirname(__file__)
sys.path.append(driver_path)
import makerbot_driver
#from Cura.util import resources#获取profile

reload(sys)
sys.setdefaultencoding( "utf-8" )
def Convert_Gcode_to_x3g(dest,gcode_path):
    #get filename
    filename = os.path.basename(gcode_path)#获取主文件名，包括后缀
    filename = os.path.splitext(filename)[0]#分离文件名和后缀，返回一个list，list[0]为文件名

    # filename = os.path.basename('C:\Users\asus\Desktop\cura\shell.gcode')
    # filename = os.path.splitext(filename)[0]
    # #TODO:应该从wildcard传递
    f=open('@@@@@@@@@@','w')
    print >>f,dest,gcode_path

    f.close()


    condition = threading.Condition()
    
    #程序只能运行
    parser = makerbot_driver.Gcode.GcodeParser()

    parser.state = makerbot_driver.Gcode.GcodeStates()#getProfile4Gcode2X3g(profile)
    qqqqqq=open('!!!!!!','w')
    qqqqqq.close()
    #parser.state.profile = makerbot_driver.Profile(resources.getProfile4Gcode2X3g('Replicator2.json'))##
    parser.state.profile = makerbot_driver.Profile('D:\localgit\\resources\jsonprofiles\ReplicatorDual.json')
    parser.state.values['build_name'] = filename
    parser.s3g = makerbot_driver.s3g()
    
    
    parser.s3g.writer = makerbot_driver.Writer.FileWriter(open(dest, 'wb'), condition)
    
    with open(gcode_path) as f:
        for line in f:
            parser.execute_line(line)
    parser.s3g.writer.file.close()
