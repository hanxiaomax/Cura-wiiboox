# coding=utf-8
__author__ = 'Lingfeng Ai'
import wx
from Cura.gui import configWizard
from Cura.gui import configBase
from Cura.util import machineCom
from Cura.util import profile
from Cura.util import pluginInfo
from Cura.util import resources

class optionOnOffDialog(wx.Dialog):
	def __init__(self, parent):
		super(optionOnOffDialog, self).__init__(None, title=_(u"高级设置面板过滤器"),style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
		wx.EVT_CLOSE(self, self.OnClose)
		self.parent = parent
		self.panel = configBase.configPanelBase(self)
		left, right, main = self.panel.CreateConfigPanel(self)
		self.y=0
		for name in profile.getSubCategoriesFor('expert'):
			print name
			self.y+=25
			i = wx.CheckBox(self, -1, label=name,pos=(20,self.y),style=wx.ALIGN_LEFT)
			#self.SetValue(self.setting.getValue(self.settingIndex))
			#i.Bind(wx.EVT_CHECKBOX, self.OnSettingChange)

		main.Fit()
		self.Fit()

	def OnClose(self, e):
		#self.parent.reloadSettingPanels()
		self.Destroy()

class machineSettingsDialog(wx.Dialog):
	def __init__(self, parent):
		super(machineSettingsDialog, self).__init__(None, title=_("Machine settings"))
		wx.EVT_CLOSE(self, self.OnClose)

		self.parent = parent

		self.panel = configBase.configPanelBase(self)
		self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
		self.GetSizer().Add(self.panel, 1, wx.EXPAND)
		self.nb = wx.Notebook(self.panel)
		self.panel.SetSizer(wx.BoxSizer(wx.VERTICAL))
		self.panel.GetSizer().Add(self.nb, 1, wx.EXPAND)

		for idx in xrange(0, profile.getMachineCount()):
			extruderCount = int(profile.getMachineSetting('extruder_amount', idx))
			left, right, main = self.panel.CreateConfigPanel(self.nb)
			configBase.TitleRow(left, _("Machine settings"))
			configBase.SettingRow(left, 'steps_per_e', index=idx)
			configBase.SettingRow(left, 'machine_width', index=idx)
			configBase.SettingRow(left, 'machine_depth', index=idx)
			configBase.SettingRow(left, 'machine_height', index=idx)
			configBase.SettingRow(left, 'extruder_amount', index=idx)
			configBase.SettingRow(left, 'has_heated_bed', index=idx)
			configBase.SettingRow(left, 'machine_center_is_zero', index=idx)
			configBase.SettingRow(left, 'machine_shape', index=idx)
			configBase.SettingRow(left, 'gcode_flavor', index=idx)

			configBase.TitleRow(right, _("Printer head size"))
			configBase.SettingRow(right, 'extruder_head_size_min_x', index=idx)
			configBase.SettingRow(right, 'extruder_head_size_min_y', index=idx)
			configBase.SettingRow(right, 'extruder_head_size_max_x', index=idx)
			configBase.SettingRow(right, 'extruder_head_size_max_y', index=idx)
			configBase.SettingRow(right, 'extruder_head_size_height', index=idx)

			for i in xrange(1, extruderCount):
				configBase.TitleRow(left, _("Extruder %d") % (i+1))
				configBase.SettingRow(left, 'extruder_offset_x%d' % (i), index=idx)
				configBase.SettingRow(left, 'extruder_offset_y%d' % (i), index=idx)

			configBase.TitleRow(right, _("Communication settings"))
			configBase.SettingRow(right, 'serial_port', ['AUTO'] + machineCom.serialList(), index=idx)
			configBase.SettingRow(right, 'serial_baud', ['AUTO'] + map(str, machineCom.baudrateList()), index=idx)

			self.nb.AddPage(main, profile.getMachineSetting('machine_name', idx).title())

		self.nb.SetSelection(int(profile.getPreferenceFloat('active_machine')))

		self.buttonPanel = wx.Panel(self.panel)
		self.panel.GetSizer().Add(self.buttonPanel)

		self.buttonPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
		self.okButton = wx.Button(self.buttonPanel, -1, 'Ok')
		self.okButton.Bind(wx.EVT_BUTTON, lambda e: self.Close())
		self.buttonPanel.GetSizer().Add(self.okButton, flag=wx.ALL, border=5)


		self.addButton = wx.Button(self.buttonPanel, -1, _('Add new machine'))
		self.addButton.Bind(wx.EVT_BUTTON, self.OnAddMachine)
		self.buttonPanel.GetSizer().Add(self.addButton, flag=wx.ALL, border=5)

		self.remButton = wx.Button(self.buttonPanel, -1, _('Remove machine'))
		self.remButton.Bind(wx.EVT_BUTTON, self.OnRemoveMachine)
		self.buttonPanel.GetSizer().Add(self.remButton, flag=wx.ALL, border=5)

		self.renButton = wx.Button(self.buttonPanel, -1, _('Change machine name'))
		self.renButton.Bind(wx.EVT_BUTTON, self.OnRenameMachine)
		self.buttonPanel.GetSizer().Add(self.renButton, flag=wx.ALL, border=5)


		main.Fit()
		self.Fit()

	def OnAddMachine(self, e):
		self.Hide()
		self.parent.Hide()
		profile.setActiveMachine(profile.getMachineCount())
		configWizard.configWizard(True)
		self.parent.Show()
		self.parent.reloadSettingPanels()
		self.parent.updateMachineMenu()

		prefDialog = machineSettingsDialog(self.parent)
		prefDialog.Centre()
		prefDialog.Show()
		wx.CallAfter(self.Close)

	def OnRemoveMachine(self, e):
		if profile.getMachineCount() < 2:
			wx.MessageBox(_("Cannot remove the last machine configuration in Cura"), _("Machine remove error"), wx.OK | wx.ICON_ERROR)
			return

		self.Hide()
		profile.removeMachine(self.nb.GetSelection())
		self.parent.reloadSettingPanels()
		self.parent.updateMachineMenu()

		prefDialog = machineSettingsDialog(self.parent)
		prefDialog.Centre()
		prefDialog.Show()
		wx.CallAfter(self.Close)


	def OnRenameMachine(self, e):
		dialog = wx.TextEntryDialog(self, _("Enter the new name:"), _("Change machine name"), self.nb.GetPageText(self.nb.GetSelection()))
		if dialog.ShowModal() != wx.ID_OK:
			return
		self.nb.SetPageText(self.nb.GetSelection(), dialog.GetValue())
		profile.putMachineSetting('machine_name', dialog.GetValue(), self.nb.GetSelection())
		self.parent.updateMachineMenu()

	def OnClose(self, e):
		self.parent.reloadSettingPanels()
		self.Destroy()
