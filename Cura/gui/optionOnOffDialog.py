# coding=utf-8
__author__ = 'Lingfeng Ai'
import wx
from Cura.gui import configWizard
from Cura.gui import configBase
from Cura.util import machineCom
from Cura.util import profile
from Cura.util import pluginInfo
from Cura.util import resources
Filter=list(profile.getPreference('filter').encode('utf-8').split(','))#返回的字符串转换为列表
#print "list to filter:",Filter
class optionOnOffDialog(wx.Dialog):
	def __init__(self, parent):
		super(optionOnOffDialog, self).__init__(None, title=_("Option filter for expert settings"),size=(200,350),
		style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
		wx.EVT_CLOSE(self, self.OnClose)
		self.parent = parent
		self.panel = configBase.configPanelBase(self)
		left, right, main = self.panel.CreateConfigPanel(self)
		wx.StaticText(self,-1,_("please uncheck the settings you do not want to see"),style=wx.ALIGN_CENTER)
		self.y=35
		self.id_name_dic={}
		for name in profile.getSubCategoriesFor('expert'):
			id=wx.NewId()
			self.id_name_dic[id]=name
			i = wx.CheckBox(self, id, label=name,pos=(20,self.y),style=wx.ALIGN_LEFT)
			self.y+=25
			if name not in Filter:
				i.SetValue(True)
			else:
				i.SetValue(False)
			i.Bind(wx.EVT_CHECKBOX, self.Oncheck,i)
		main.Fit()

	def OnClose(self, e):
		_filterSave=','.join(Filter)
		#print "OnClose:",_filterSave
		profile.putPreference('filter', _filterSave)
		self.Destroy()
	def Oncheck(self,e):
		checkbox=e.GetEventObject()#INFO:使事件处理函数获取事件对象
		if checkbox.GetValue():
			Filter.remove(self.id_name_dic[checkbox.GetId()])
		else:
			Filter.append(self.id_name_dic[checkbox.GetId()])