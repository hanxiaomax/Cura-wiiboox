#coding:utf-8
__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import wx

from Cura.util import profile

class simpleModePanel(wx.Panel):
	"Main user interface window for Quickprint mode"
	def __init__(self, parent, callback):
		super(simpleModePanel, self).__init__(parent)
		self._callback = callback

		#toolsMenu = wx.Menu()
		#i = toolsMenu.Append(-1, 'Switch to Normal mode...')
		#self.Bind(wx.EVT_MENU, self.OnNormalSwitch, i)
		#self.menubar.Insert(1, toolsMenu, 'Normal mode')

		printTypePanel = wx.Panel(self)
		self.printTypeHigh = wx.RadioButton(printTypePanel, -1, _("High quality print"), style=wx.RB_GROUP)
		self.printTypeNormal = wx.RadioButton(printTypePanel, -1, _("Normal quality print"))
		self.printTypeLow = wx.RadioButton(printTypePanel, -1, _("Fast low quality print"))
		self.printTypeJoris = wx.RadioButton(printTypePanel, -1, _("Thin walled cup or vase"))
		self.printTypeJoris.Hide()


		printMaterialPanel = wx.Panel(self)
		self.printMaterialPLA_Pro = wx.RadioButton(printMaterialPanel, -1, 'PLA Pro', style=wx.RB_GROUP)
		self.printMaterialPLA = wx.RadioButton(printMaterialPanel, -1, 'PLA')
		self.printMaterialABS = wx.RadioButton(printMaterialPanel, -1, 'ABS')
		# self.printMaterialDiameter = wx.TextCtrl(printMaterialPanel, -1, profile.getProfileSetting('filament_diameter'))
		if profile.getMachineSetting('gcode_flavor') == 'UltiGCode':
			printMaterialPanel.Show(False)
		
		self.printSupport = wx.CheckBox(self, -1, _("Print support structure"))

		sizer = wx.GridBagSizer()
		self.SetSizer(sizer)

		sb = wx.StaticBox(printTypePanel, label=_("Select a quickprint profile:"))
		boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
		boxsizer.Add(self.printTypeHigh)
		boxsizer.Add(self.printTypeNormal)
		boxsizer.Add(self.printTypeLow)
		boxsizer.Add(self.printTypeJoris, border=5, flag=wx.TOP)
		printTypePanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
		printTypePanel.GetSizer().Add(boxsizer, flag=wx.EXPAND)
		sizer.Add(printTypePanel, (0,0), flag=wx.EXPAND)

		sb = wx.StaticBox(printMaterialPanel, label=_("Material:"))
		boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
		boxsizer.Add(self.printMaterialPLA_Pro)
		boxsizer.Add(self.printMaterialPLA)
		boxsizer.Add(self.printMaterialABS)
		#boxsizer.Add(wx.StaticText(printMaterialPanel, -1, _("Diameter:")))
		# boxsizer.Add(self.printMaterialDiameter)
		printMaterialPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
		printMaterialPanel.GetSizer().Add(boxsizer, flag=wx.EXPAND)
		sizer.Add(printMaterialPanel, (1,0), flag=wx.EXPAND)

		sb = wx.StaticBox(self, label=_("Other:"))
		boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
		boxsizer.Add(self.printSupport)
		sizer.Add(boxsizer, (2,0), flag=wx.EXPAND)

		self.printTypeNormal.SetValue(True)
		self.printMaterialPLA_Pro.SetValue(True)

		self.printTypeHigh.Bind(wx.EVT_RADIOBUTTON, lambda e: self._callback())
		self.printTypeNormal.Bind(wx.EVT_RADIOBUTTON, lambda e: self._callback())
		self.printTypeLow.Bind(wx.EVT_RADIOBUTTON, lambda e: self._callback())
		#self.printTypeJoris.Bind(wx.EVT_RADIOBUTTON, lambda e: self._callback())

		self.printMaterialPLA.Bind(wx.EVT_RADIOBUTTON, lambda e: self._callback())
		self.printMaterialABS.Bind(wx.EVT_RADIOBUTTON, lambda e: self._callback())
		self.printMaterialPLA_Pro.Bind(wx.EVT_RADIOBUTTON, lambda e: self._callback())
		# self.printMaterialDiameter.Bind(wx.EVT_TEXT, lambda e: self._callback())

		self.printSupport.Bind(wx.EVT_CHECKBOX, lambda e: self._callback())

	def setupSlice(self):
		put = profile.setTempOverride
		get = profile.getProfileSetting
		for setting in profile.settingsList:
			if not setting.isProfile():
				continue
			profile.setTempOverride(setting.getName(), setting.getDefault())

		if self.printSupport.GetValue():
			put('support', _("Exterior Only"))

		nozzle_size = float(get('nozzle_size'))
		if self.printTypeNormal.GetValue():
			put('layer_height', '0.15')
			put('layer_height', '0.15')
			put('fill_density', '20')
		elif self.printTypeLow.GetValue():
			put('wall_thickness',"0.4")
			put('layer_height', '0.20')
			put('fill_density', '15')
			put('print_speed', '60')
			put('inset0_speed','30')
			put('insetx_speed','35')
			put('cool_min_layer_time', '3')
			put('bottom_layer_speed', '30')
		elif self.printTypeHigh.GetValue():
			put('layer_height', '0.1')
			put('fill_density', '20')
			put('bottom_layer_speed', '15')
			put('inset0_speed','15')
			put('insetx_speed','25')

		elif self.printTypeJoris.GetValue():
			put('wall_thickness', nozzle_size * 1.5)

		put('filament_diameter', "1.75")
		if self.printMaterialPLA.GetValue():
			pass
		if self.printMaterialPLA_Pro.GetValue():
			put('bottom_layer_speed','8')
			put('support_angle', "60")
		if self.printMaterialABS.GetValue():
			put('print_bed_temperature', '100')
			put('platform_adhesion', 'Brim')
			put('filament_flow', '107')
			put('print_temperature', '245')
		put('plugin_config', '')

	def updateProfileToControls(self):
		pass
