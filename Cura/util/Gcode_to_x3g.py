# coding=utf-8
from __future__ import absolute_import
__author__ = ['Bob Zhuo','Lingfeng Ai']
__copyright__ = "Copyright (C) 2014 Bob Zhuo,Lingfeng Ai - Released under terms of the AGPLv3 License"
#import optparse 
import sys
import os
import threading
import wx
import resources
from Cura.util import profile
#ugly hack:add makerbot_driver to sys.path to import
driver_path=os.path.dirname(__file__)
sys.path.append(driver_path)
import makerbot_driver
#ugly hack:处理中文路径
reload(sys)
sys.setdefaultencoding( "utf-8" )
def Convert_Gcode_to_x3g(dest,gcode_path,machine=profile.getMachineSetting('machine_type').encode('utf-8')):
	filename = os.path.basename(gcode_path)
	filename = os.path.splitext(filename)[0]
	condition = threading.Condition()
	parser = makerbot_driver.Gcode.GcodeParser()
	parser.state = makerbot_driver.Gcode.GcodeStates()
	parser.state.profile = makerbot_driver.Profile(machine)
	parser.state.values['build_name'] = unicode(filename).encode("utf-8")
	#INFO :必须使用Unicode.encode("utf-8")否则会出错
	parser.s3g = makerbot_driver.s3g()
	destfile=open(dest,'wb')# 创建destfile用来关闭文件
	parser.s3g.writer = makerbot_driver.Writer.FileWriter(destfile, condition)
	keepgoing=True# 进度条是否继续进行
	maxline = len(open(gcode_path, "rU").readlines())# 计算文件文件行数
	pos=0
	dlg = wx.ProgressDialog(_("Saving..."),_("Saving..."),
	                               maximum =maxline,
	                               parent=None,
	                               style = wx.PD_CAN_ABORT
	                                | wx.PD_APP_MODAL
	                                | wx.PD_ELAPSED_TIME
	                                # | wx.PD_ESTIMATED_TIME
	                                | wx.PD_REMAINING_TIME
		                           |wx.PD_AUTO_HIDE
	                                )
	with open(gcode_path,'r') as f:
		for line in f:
			parser.execute_line(line)
			pos+=1
			if pos>maxline/2:
				(keepgoing,skip)=dlg.Update(pos,_('Please wait...'))
			else:
				(keepgoing,skip)=dlg.Update(pos)
			if not keepgoing:
				break
	dlg.Destroy()
	if keepgoing:
		message_dlg = wx.MessageDialog(None,filename+_("has been saved to:\n")+dest,_('Finished'),
		                               wx.OK|wx.ICON_INFORMATION)
		message_dlg.ShowModal()
		message_dlg.Destroy()
	else:
		destfile.close()# 首先关闭文件然后才能remove
		os.remove(unicode(dest).encode('GBK'))
