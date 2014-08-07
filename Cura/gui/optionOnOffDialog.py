# coding=utf-8
__author__ = 'Lingfeng Ai'
import wx
from Cura.gui import configWizard
from Cura.gui import configBase
from Cura.util import machineCom
from Cura.util import profile
from Cura.util import pluginInfo
from Cura.util import resources
Fliter=list(profile.getPreference('filter'))
class optionOnOffDialog(wx.Dialog):
	def __init__(self, parent):
		super(optionOnOffDialog, self).__init__(None, title=_(u"高级设置面板过滤器"),size=(200,300),
		style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
		wx.EVT_CLOSE(self, self.OnClose)
		self.parent = parent
		self.panel = configBase.configPanelBase(self)
		left, right, main = self.panel.CreateConfigPanel(self)
		wx.StaticText(self,-1,_("请勾选您需要保留的选项"),style=wx.ALIGN_CENTER)
		self.y=35
		self.id_name_dic={}
		for name in profile.getSubCategoriesFor('expert'):
			id=wx.NewId()
			self.id_name_dic[id]=name
			i = wx.CheckBox(self, id, label=name,pos=(20,self.y),style=wx.ALIGN_LEFT)
			self.y+=25
			if name not in Fliter:
				i.SetValue(True)
			else:
				i.SetValue(False)
			i.Bind(wx.EVT_CHECKBOX, self.Oncheck,i)
		main.Fit()

	def OnClose(self, e):
		for i in Fliter:
			if i in ['\'']:
				Fliter.remove(i)
		profile.putPreference('filter', Fliter)
		self.Destroy()
	def Oncheck(self,e):
		checkbox=e.GetEventObject()#INFO:使事件处理函数获取事件对象
		if checkbox.GetValue():
			Fliter.remove(self.id_name_dic[checkbox.GetId()])
		else:
			Fliter.append(self.id_name_dic[checkbox.GetId()])
		print Fliter