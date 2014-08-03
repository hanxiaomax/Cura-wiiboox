#-*- coding: utf-8 -*-
from __future__ import absolute_import

#import optparse 
import sys
import os
import threading
import wx
#TODO:添加保存完成提示
#ugly hack:add makerbot_driver to sys.path to import
driver_path=os.path.dirname(__file__)
sys.path.append(driver_path)

import makerbot_driver

#ugly hack:to handle path with chinese
reload(sys)
sys.setdefaultencoding( "utf-8" )
def Convert_Gcode_to_x3g(dest,gcode_path,machine='ReplicatorDual'):

    filename = os.path.basename(gcode_path)#获取主文件名，包括后缀
    filename = os.path.splitext(filename)[0]#分离文件名和后缀，返回一个list，list[0]为文件名
    condition = threading.Condition()
    parser = makerbot_driver.Gcode.GcodeParser()
    parser.state = makerbot_driver.Gcode.GcodeStates()
    parser.state.profile = makerbot_driver.Profile(machine)
    parser.state.values['build_name'] = filename
    parser.s3g = makerbot_driver.s3g()   
    parser.s3g.writer = makerbot_driver.Writer.FileWriter(open(dest, 'wb'), condition)
    with open(gcode_path) as f:
        for line in f:
            parser.execute_line(line)
    parser.s3g.writer.file.close()
    message_dlg = wx.MessageDialog(None, filename+u" 已经被保存至：\n"+dest,'Finished', wx.OK|wx.ICON_INFORMATION)
    message_dlg.ShowModal()
    message_dlg.Destroy()

