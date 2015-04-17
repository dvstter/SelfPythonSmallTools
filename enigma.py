#_*_ coding:utf-8 _*_
import wx

#######################################################
# Constants
#######################################################
mappingList = [[18,13,7,5,2,1,22,9,3,25,12,24,0,19,20,21,16,17,23,10,11,8,15,14,6,4],
		    [25,18,12,16,23,20,8,1,14,10,22,15,3,0,9,4,17,13,21,5,19,7,11,24,2,6],
		    [11,9,15,16,8,10,19,20,5,7,22,14,21,18,3,1,6,4,12,25,23,13,17,24,2,0],
		    [24,9,4,19,12,23,11,10,8,3,14,5,0,21,6,7,2,1,15,22,25,13,18,16,20,17],
		    [25,17,6,24,22,8,20,18,14,12,16,10,2,11,13,1,15,19,0,21,9,23,5,3,7,4]]
class EnigmaModel:
	def __init__(self):
		self.InitCipherEngine([0,1,2])
	def InitCipherEngine(self, rotatorsList, cursorsList = [0,0,0], linksInList=[-1,-1,-1], linksOutList=[-1,-1,-1]):
		self.rotatorsList = rotatorsList # choose the rotators
		self.cursorsList = cursorsList # get the initial cursor position
		self.linksInList = linksInList
		self.linksOutList = linksOutList

	# getter and setter
	def SetCursor(self, idx, number):
		if number not in range(26):
			return
		else:
			self.cursorsList[idx] = number
	def GetCursor(self, idx):
		return self.cursorsList[idx]
	def SetLink(self, idx, num):
		if idx in range(3):
			self.linksInList[idx] = num
		else:
			self.linksOutList[idx%3] = num

	# increase cursor
	def Rotate(self):
		increment = 1
		for idx in range(3):
			num = self.cursorsList[idx] + increment
			if num >= 26:
				increment = 1
				num = 0
			else:
				increment = 0
			self.cursorsList[idx] = num

	def ChangeLinks(self, keycode):
		if keycode in self.linksInList:
			return self.linksOutList[self.linksInList.index(keycode)]
		if keycode in self.linksOutList:
			return self.linksInList[self.linksOutList.index(keycode)]
		return keycode

	# keycode will be a offset value 0--a 1--b etc..
	def CipherText(self, keycode):
		# the linking board
		keycode = self.ChangeLinks(keycode)
		# forward
		next = keycode
		for idx in range(3):
			next = mappingList[self.rotatorsList[idx]][(next + self.cursorsList[idx])%26]
		# backward
		index = 25 - mappingList[self.rotatorsList[2]].index(next)
		index = (mappingList[self.rotatorsList[1]].index(index)-self.cursorsList[1]+26)%26
		index = (mappingList[self.rotatorsList[0]].index(index)-self.cursorsList[0]+26)%26
		# rotate the links
		self.Rotate()
		# the linking board
		index = self.ChangeLinks(index)
		return chr(index+0x41)


# Enigma view and Enigma controller class
# actualy I don't know how to separate the view and controller
# so I have to put them into one class
# God, help me.
class EnigmaView(wx.Panel):
	def __init__(self, window):
		wx.Panel.__init__(self, window)

		# init view
		self.InitWindows()
		# init model
		self.model = EnigmaModel()
		# init some extra things
		self.typeSound = wx.Sound('type.wav')

	# init window functions
	def InitOutputWindow(self):
		# create output text ctrl
		self.stdout = wx.TextCtrl(self, -1, style=wx.TE_READONLY | wx.TE_RIGHT)
		promptStaticText = wx.StaticText(self, -1, 'CIPHER TEXT')
		clearButton = wx.Button(self, label='C', size=(30, 30))
		# create sizer and return
		stdout_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# bind clear text button
		self.Bind(wx.EVT_BUTTON, self.OnClearText, clearButton)
		# layout the output TextCtrl
		stdout_sizer.Add((30, 30), 0, wx.EXPAND | wx.ALIGN_CENTER)
		stdout_sizer.Add(promptStaticText, 0, wx.ALIGN_CENTER)
		stdout_sizer.Add((10, 10), 0, wx.EXPAND | wx.ALIGN_CENTER)
		stdout_sizer.Add(self.stdout, 1, wx.ALIGN_CENTER)
		stdout_sizer.Add((30, 30), 0, wx.EXPAND | wx.ALIGN_CENTER)
		stdout_sizer.Add(clearButton, 0, wx.ALIGN_CENTER)
		stdout_sizer.Add((30, 30), 0, wx.EXPAND | wx.ALIGN_CENTER)
		return stdout_sizer

	def InitCipherCoreWindow(self):
		# init all the widgets
		rotatorsStaticText = wx.StaticText(self, -1, 'ROTATORS')
		linksStaticText = [wx.StaticText(self, -1, '->') for x in range(3)]
		self.rotators = [wx.Button(self, label='A', size=(20, 20)) for x in range(3)]
		increaseButtons = [wx.Button(self, label='+', size=(20, 20)) for x in range(3)]
		decreaseButtons = [wx.Button(self, label='-', size=(20, 20)) for x in range(3)]
		self.plugs_in = [wx.TextCtrl(self, style=wx.TE_CENTER, size=(20,20), ) for x in range(3)]
		self.plugs_out = [wx.TextCtrl(self, style=wx.TE_CENTER, size=(20, 20)) for x in range(3)]
		for eachPlug in self.plugs_out+self.plugs_in:
			eachPlug.SetMaxLength(1)
		# bind all the events
		for idx, eachPlug in enumerate(self.plugs_in+self.plugs_out):
			self.Bind(wx.EVT_TEXT, lambda evt, idx=idx:self.OnChangePlug(evt, idx), eachPlug)
			self.Bind(wx.EVT_CHAR, lambda evt, idx=idx:self.OnChangePlug(evt, idx), eachPlug)
		for x in range(3):
			self.Bind(wx.EVT_BUTTON, lambda evt, idx=x:self.OnClickIncrease(evt, idx), increaseButtons[x])
			self.Bind(wx.EVT_BUTTON, lambda evt, idx=x:self.OnClickDecrease(evt, idx), decreaseButtons[x])
			self.Bind(wx.EVT_BUTTON, lambda evt, idx=x:self.OnClearRotator(evt, idx), self.rotators[x])
		# layout all the widgets
		pair_sizer = [wx.BoxSizer(wx.VERTICAL) for x in range(3)]
		sizer = wx.BoxSizer(wx.HORIZONTAL) # main sizer
		for each in range(3): # init increase and decrease buttons pair
			pair_sizer[each].Add(increaseButtons[each], 0, wx.ALIGN_CENTER)
			pair_sizer[each].Add(decreaseButtons[each], 0, wx.ALIGN_CENTER)

		sizer.Add(rotatorsStaticText, 0, wx.ALIGN_CENTER)
		sizer.Add((40, 40), 1, wx.ALIGN_CENTER) # add some space
		for idx, eachRotator in enumerate(self.rotators):
			sizer.Add(eachRotator, 0, wx.ALIGN_CENTER)
			sizer.Add(pair_sizer[idx], 0, wx.ALIGN_CENTER)
			sizer.Add((40, 40), 1, wx.EXPAND | wx.ALIGN_CENTER) # add some space
		pair_sizer = [wx.BoxSizer(wx.HORIZONTAL) for x in range(3)]
		for each in range(3):
			pair_sizer[each].Add(self.plugs_in[each], 0, wx.ALIGN_CENTER)
			pair_sizer[each].Add(linksStaticText[each], 0, wx.ALIGN_CENTER)
			pair_sizer[each].Add(self.plugs_out[each], 0, wx.ALIGN_CENTER)
		plugs_sizer = wx.BoxSizer(wx.VERTICAL)
		for each in range(3):
			plugs_sizer.Add(pair_sizer[each], 1, wx.EXPAND | wx.ALIGN_CENTER)
		sizer.Add(plugs_sizer, 0, wx.ALIGN_CENTER)
		return sizer

	def InitInputWindow(self):
		# create all sizers
		keyboard_sizer = wx.BoxSizer(wx.VERTICAL)
		first_sizer = wx.BoxSizer(wx.HORIZONTAL)
		second_sizer = wx.BoxSizer(wx.HORIZONTAL)
		third_sizer = wx.BoxSizer(wx.HORIZONTAL)
		# create keyboard
		first_buttons = [wx.Button(self, label=x, size=(40,40)) for x in 'QWERTYUIOP']
		second_buttons = [wx.Button(self, label=x, size=(40,40)) for x in 'ASDFGHJKL']
		third_buttons = [wx.Button(self, label=x, size=(40,40)) for x in 'ZXCVBNM']
		# bind events
		for button in first_buttons + second_buttons + third_buttons:
			self.Bind(wx.EVT_BUTTON, self.OnClick, button)
		# layout the buttons
		second_sizer.Add((40, 40), 1, wx.EXPAND | wx.ALIGN_CENTER)
		third_sizer.Add((40, 40), 1, wx.EXPAND | wx.ALIGN_CENTER)
		third_sizer.Add((40, 40), 1, wx.EXPAND | wx.ALIGN_CENTER)
		for button in first_buttons:
			first_sizer.Add(button, 1, wx.EXPAND | wx.ALIGN_CENTER)
		for button in second_buttons:
			second_sizer.Add(button, 1, wx.EXPAND | wx.ALIGN_CENTER)
		for button in third_buttons:
			third_sizer.Add(button, 1, wx.EXPAND | wx.ALIGN_CENTER)
		second_sizer.Add((40, 40), 1, wx.EXPAND | wx.ALIGN_CENTER)
		third_sizer.Add((40, 40), 1, wx.EXPAND | wx.ALIGN_CENTER)
		third_sizer.Add((40, 40), 1, wx.EXPAND | wx.ALIGN_CENTER)
		# all the sizers into one
		keyboard_sizer.Add(first_sizer, 0, wx.ALIGN_CENTER)
		keyboard_sizer.Add(second_sizer, 0, wx.ALIGN_CENTER)
		keyboard_sizer.Add(third_sizer, 0, wx.ALIGN_CENTER)
		return keyboard_sizer

	def InitWindows(self):
		# call all the function above
		main_sizer = wx.BoxSizer(wx.VERTICAL)
		# layout all the window
		main_sizer.Add((10, 10), 1, wx.EXPAND | wx.ALIGN_CENTER) # add some space
		main_sizer.Add(self.InitOutputWindow(), 0, wx.EXPAND | wx.ALIGN_CENTER)
		main_sizer.Add((10, 10), 1, wx.EXPAND | wx.ALIGN_CENTER) # add some space
		main_sizer.Add(self.InitCipherCoreWindow(), 0, wx.ALIGN_CENTER)
		main_sizer.Add((10, 10), 1, wx.EXPAND | wx.ALIGN_CENTER) # add some space
		main_sizer.Add(self.InitInputWindow(), 0, wx.EXPAND | wx.ALIGN_CENTER)
		main_sizer.Add((10, 10), 1, wx.EXPAND | wx.ALIGN_CENTER) # add some space
		self.SetSizer(main_sizer)

	# event callback functions
	def OnClick(self, event):
		self.typeSound.Play(wx.SOUND_ASYNC)
		cipher_char = self.model.CipherText(ord(event.GetEventObject().GetLabel())-0x41)
		self.stdout.AppendText(cipher_char)
		# update the rotators
		for idx in range(3):
			text = chr(self.model.GetCursor(idx)+0x41)
			self.rotators[idx].SetLabelText(text)
	def OnChangePlug(self, event, idx):
		obj = event.GetEventObject()
		try:
			# null text
			if obj.GetValue() == u'':
				self.model.SetLink(idx, -1)
				return
			num = ord(str(obj.GetValue()))-0x61
			if num not in range(26):
				obj.Clear()
			else:
				self.model.SetLink(idx, num)
		except TypeError, UnboundLocalError:
			pass

	def OnClickIncrease(self, event, idx):
		self.model.SetCursor(idx, self.model.GetCursor(idx)+1)
		text = chr(self.model.GetCursor(idx)+0x41)
		self.rotators[idx].SetLabelText(text)

	def OnClickDecrease(self, event, idx):
		self.model.SetCursor(idx, self.model.GetCursor(idx)-1)
		text = chr(self.model.GetCursor(idx)+0x41)
		self.rotators[idx].SetLabelText(text)

	def OnClearRotator(self, event, idx):
		self.model.SetCursor(idx, 0)
		self.rotators[idx].SetLabelText('A')

	def OnClearText(self, event):
		self.stdout.Clear()

class MainFrame(wx.Frame):
	def __init__(self, title):
		wx.Frame.__init__(self, None, wx.ID_ANY, size=(500,300), title=title)
		panel = EnigmaView(self)
		self.Show(True)

if __name__ == '__main__':
	enigma = wx.App()
	frame = MainFrame('Enigma')
	frame.Show()
	enigma.MainLoop()