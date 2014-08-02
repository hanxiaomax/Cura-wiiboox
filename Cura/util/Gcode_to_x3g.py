#-*- coding: utf-8 -*-
#from __future__ import absolute_import
import optparse 
import sys
import os
import threading

import makerbot_driver
from Cura.util import resources#获取profile

def Convert_Gcode_to_x3g(dest,gcode_file_path):
    #get filename
    #filename = os.path.basename(gcode_file_path)#获取主文件名，包括后缀
    #filename = os.path.splitext(filename)[0]#分离文件名和后缀，返回一个list，list[0]为文件名
    #x3g_path=os.path.split(gcode_file_path)[0]#获取gcode相同的路径储存x3g

    filename = os.path.basename('C:\Users\asus\Desktop\cura\shell.gcode')
    filename = os.path.splitext(filename)[0]
    #TODO:应该从wildcard传递
    f=open('@@@@@@@@@@','w')
    print >>f,filename

    f.close()


    condition = threading.Condition()
    qqqqqq=open('!!!!!!','w')
    #程序只能运行到这里
    parser = makerbot_driver.Gcode.GcodeParser()

    parser.state = makerbot_driver.Gcode.GcodeStates()#getProfile4Gcode2X3g(profile)
    
    qqqqqq.close()
    #parser.state.profile = makerbot_driver.Profile(resources.getProfile4Gcode2X3g('Replicator2.json'))##
    parser.state.profile = makerbot_driver.Profile('D:\localgit\\resources\jsonprofiles\ReplicatorDual.json')
    parser.state.values['build_name'] = filename
    parser.s3g = makerbot_driver.s3g()
    
    
    parser.s3g.writer = makerbot_driver.Writer.FileWriter(open(r'C:\Users\asus\Desktop\cura\xxx.x3g', 'wb'), condition)
    
    with open(gcode_file_path) as f:
        for line in f:
            parser.execute_line(line)
    parser.s3g.writer.file.close()

