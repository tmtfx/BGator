#!/boot/system/bin/python

#   A Simple news aggregator for Haiku.
#   Copyright (C) 2021  Fabio Tomat
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>

import os,sys,re,datetime,time,struct,thread,webbrowser,ConfigParser

def openlink(link):
	global iltab,name
	webbrowser.get(name).open(link,iltab,False)

Config=ConfigParser.ConfigParser()
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def checkbrowser():
	global iltab,name
	try:
		confile=os.path.join(sys.path[0],'config.ini')
		Config.read(confile)
		path=ConfigSectionMap("Browser")['path']
		name=ConfigSectionMap("Browser")['name']
		type=ConfigSectionMap("Browser")['type']
		buleano=ConfigSectionMap("Browser")['newtab']
		if buleano:
			iltab=2
		else:
			iltab=1
		if os.path.exists(path):
			if type=='Generic':
				webbrowser.register(name,None,webbrowser.GenericBrowser(path))
			elif type=='Mozilla':
				webbrowser.register(name,None,webbrowser.Mozilla(path))
			elif type=='Konqueror':
				webbrowser.register(name,None,webbrowser.Konqueror(path)) # no pass path
			elif type=='Opera':
				webbrowser.register(name,None,webbrowser.Opera(path)) # no pass path
	except:
		confile=os.path.join(sys.path[0],'config.ini')
		cfgfile = open(confile,'w')

		Config.add_section('Browser')
		Config.set('Browser','path', "/boot/system/apps/WebPositive")
		Config.set('Browser','name', "WebPositive")
		Config.set('Browser','type', "Generic")
		Config.set('Browser','newtab', True)
		Config.write(cfgfile)
		cfgfile.close()
		Config.read(confile)
		
		iltab=2
		print "fallback mode"
		path="/boot/system/apps/WebPositive"
		if os.path.exists(path):
			webbrowser.register(os.path.basename(path),None,webbrowser.GenericBrowser(path))#,-1)
		else:
			print ("could not find WebPositive in "+path)
			sys.exit(1)
checkbrowser()
ies=False
try:
	import feedparser
except:
	print "your system lacks of Universal Feed Parser module"
	pothpath=os.path.join(sys.path[0],'help/index.html')
	thread.start_new_thread(openlink,(pothpath,))
	ies=True

	pothpath="http://code.google.com/p/feedparser/downloads/list"
	thread.start_new_thread(openlink,(pothpath,))
try:
	import sqlite3
except:
	print "your system lacks of SQLite3 module"
	if not ies:
		pothpath=os.path.join(sys.path[0],'help/index.html')
		thread.start_new_thread(openlink,(pothpath,))
	ies=True
	#pothpath="http://code.google.com/p/pysqlite/downloads/list"
	#thread.start_new_thread(openlink,(pothpath,))
try:
	import BApplication,SupportKit
	from BStringItem import BStringItem
	from BListView import BListView
	from BScrollView import BScrollView
	from BWindow import BWindow
	from BMessage import BMessage
	from BMenuItem import BMenuItem
	from BMenu import BMenu
	from BBox import BBox
	from BButton import BButton
	from BMenuBar import BMenuBar
	from BPopUpMenu import BPopUpMenu
	from BSeparatorItem import BSeparatorItem
	from BStringView import BStringView
	from BSlider import BSlider
	from BTextView import BTextView
	from BFont import be_plain_font, be_bold_font
	from BTextControl import BTextControl
	from BAlert import BAlert
	from BListItem import BListItem
	from BStatusBar import BStatusBar
	from StorageKit import *
	from BTranslationUtils import *
	from BFile import BFile
	from BBitmap import BBitmap
	from BCheckBox import BCheckBox
	from BView import BView
	from InterfaceKit import B_VERTICAL,B_FOLLOW_ALL,B_FOLLOW_TOP,B_FOLLOW_LEFT,B_FOLLOW_RIGHT,B_TRIANGLE_THUMB,B_BLOCK_THUMB,B_FLOATING_WINDOW,B_TITLED_WINDOW,B_WILL_DRAW,B_NAVIGABLE,B_FRAME_EVENTS,B_ALIGN_CENTER,B_FOLLOW_ALL_SIDES,B_MODAL_WINDOW,B_FOLLOW_TOP_BOTTOM,B_FOLLOW_BOTTOM,B_FOLLOW_LEFT_RIGHT,B_SINGLE_SELECTION_LIST,B_NOT_RESIZABLE,B_NOT_ZOOMABLE,B_PLAIN_BORDER,B_FANCY_BORDER,B_NO_BORDER,B_ITEMS_IN_COLUMN
	from AppKit import B_QUIT_REQUESTED,B_KEY_UP,B_KEY_DOWN,B_MODIFIERS_CHANGED,B_UNMAPPED_KEY_DOWN
except:
	print "your system lacks of Bethon modules"
	if not ies:
		pothpath=os.path.join(sys.path[0],'help/index.html')
		thread.start_new_thread(openlink,(pothpath,))
	ies = True
	pothpath="http://www.bebits.com/download/1564"
	thread.start_new_thread(openlink,(pothpath,))
if ies:
	sys.exit(1)
	
	
	
	
from threading import Event, Thread


class timerLoop(Thread):
	def __init__(self,interval):
		Thread.__init__(self)
		self.finished = Event()
		self.interval = interval
		
	def run(self):
		global loopenable,valor
		while not self.finished.is_set():
			self.finished.wait(self.interval)
			if not self.finished.is_set():
				if loopenable:
					BApplication.be_app.WindowAt(0).PostMessage(29)
					self.interval=valor*60

	def cancel(self):
		self.finished.set()

class PView(BView):
	def __init__(self,frame,name,immagine):
		self.immagine=immagine
		self.frame=frame
		BView.__init__(self,self.frame,name,B_FOLLOW_ALL_SIDES,B_WILL_DRAW)

	def Draw(self,rect):
		BView.Draw(self,rect)
		a,b,c,d=self.frame
		rect=(0,0,c-a,d-b)
		self.DrawBitmap(self.immagine,rect)

class TimerSettings(BWindow):
	kWindowFrame = (250, 150, 555, 290)
	kWindowName = "Timer Settings"
	kButtonFrame = (205, 105, 295, 125)
	kButtonName = "Revert"
	
	def __init__(self):
		BWindow.__init__(self, self.kWindowFrame, self.kWindowName, B_FLOATING_WINDOW, B_NOT_RESIZABLE|B_WILL_DRAW)
		bounds=self.Bounds()
		self.underframe= BBox(bounds, 'underframe', B_FOLLOW_ALL, B_WILL_DRAW|B_NAVIGABLE, B_NO_BORDER)
		self.AddChild(self.underframe)
		
		self.slidetime=BSlider((10,10,265,30),'timeselect','minutes',BMessage(610), 1, 180)
		self.slidevalue = BStringView((240,7,268,30), 'slidevalue','1')
		self.underframe.AddChild(self.slidetime)
		self.underframe.AddChild(self.slidevalue)
		
		self.revertBtn=BButton(self.kButtonFrame, self.kButtonName, self.kButtonName, BMessage(611))
		self.incBtn=BButton((270,10,295,25), 'up', '+', BMessage(613))
		self.decBtn=BButton((270,40,295,55), 'down', '-', BMessage(614))
		self.underframe.AddChild(self.revertBtn)
		self.underframe.AddChild(self.incBtn)
		self.underframe.AddChild(self.decBtn)
		
		
		self.startimer= BCheckBox((10,70,290,90),'Starttimer','Enable timer? (Experimental)',BMessage(612))
		self.underframe.AddChild(self.startimer)
		
		self.getsettings()



	def getsettings(self):
		global valor
		try:
			confile=os.path.join(sys.path[0],'config.ini')
			Config.read(confile)
			timer=ConfigSectionMap("Timer")['value']
			valor=int(timer)
			self.slidevalue.SetText(str(timer))
			self.slidetime.SetPosition((float(timer))/180.0)
			tabvalue=Config.getboolean("Timer", "enable")
			if tabvalue:
				self.startimer.SetValue(1)
			else:
				self.startimer.SetValue(0)
		except:
			confile=os.path.join(sys.path[0],'config.ini')
			cfgfile = open(confile,'w')
			Config.add_section('Timer')
			valor=1
			Config.set('Timer','value', 1)
			Config.set('Timer','enable', False)
			Config.write(cfgfile)
			cfgfile.close()
		
		
	def MessageReceived(self, msg):
		global valor
		if msg.what==610:
			a = msg.FindInt32('be:value')
			self.slidevalue.SetText(str(a))#'%.2f' % (a/100.0))
			valor=a
		elif msg.what==611:
			self.getsettings()
		elif msg.what==612:
			global loopenable
			loopenable=self.startimer.Value()
		elif msg.what==613:
			a=int(self.slidevalue.Text())
			self.slidevalue.SetText(str(a+1))
			self.slidetime.SetPosition((float(a+1))/180.0)
			valor=a
		elif msg.what==614:
			a=int(self.slidevalue.Text())
			self.slidevalue.SetText(str(a-1))
			self.slidetime.SetPosition((float(a-1))/180.0)
			valor=a

	def QuitRequested(self):
		confile=os.path.join(sys.path[0],'config.ini')
		cfgfile = open(confile,'w')
		Config.set('Timer','value',int(self.slidevalue.Text()))
		if self.startimer.Value():
			Config.set('Timer','enable',True)
		else:
			Config.set('Timer','enable',False)
		Config.write(cfgfile)
		cfgfile.close()
		
		self.Hide()
		return 0


class BrowserSettings(BWindow):
	kWindowFrame = (150, 150, 455, 355)
	kWindowName = "Browser Settings"
	kButtonFrame = (205, 170, 295, 180)
	kButtonName = "Revert"
	
	def __init__(self):
		BWindow.__init__(self, self.kWindowFrame, self.kWindowName, B_FLOATING_WINDOW, B_NOT_RESIZABLE|B_WILL_DRAW)
		bounds=self.Bounds()
		self.underframe= BBox(bounds, 'underframe', B_FOLLOW_ALL, B_WILL_DRAW|B_NAVIGABLE, B_NO_BORDER)
		self.AddChild(self.underframe)
		msg=BMessage(600)
		self.stringpath= BTextControl((10,10,295,30),'percorso', "Path:",None,msg,B_FOLLOW_LEFT_RIGHT)
		self.stringpath.SetDivider(50.0)
		self.stringpath.SetModificationMessage(msg)
		self.underframe.AddChild(self.stringpath)
		msg=BMessage(601)
		self.stringname= BTextControl((10,40,295,60),'ProgramName', "Name:",None,msg,B_FOLLOW_LEFT_RIGHT)
		self.stringname.SetDivider(50.0)
		self.underframe.AddChild(self.stringname)
		self.popoop = BPopUpMenu('Browser Type')
		type=ConfigSectionMap("Browser")['type']
		item=BMenuItem('Mozilla', BMessage(605))
		if type=='Mozilla':
			item.SetMarked(1)
		self.popoop.AddItem(item)
		item=BMenuItem('Konqueror', BMessage(606))
		if type=='Konqueror':
			item.SetMarked(1)
		self.popoop.AddItem(item)
		item=BMenuItem('Opera', BMessage(607))
		if type=='Opera':
			item.SetMarked(1)
		self.popoop.AddItem(item)
		item=BMenuItem('Generic', BMessage(608))
		if type=='Generic':
			item.SetMarked(1)
		self.popoop.AddItem(item)
		
		self.whaaaat= BStringView((10,70,100,90),"Label","Browser type:")
		self.underframe.AddChild(self.whaaaat)
		self.tbar = BMenuBar((110.0, 70.0, 200.0, 90.0), 'pop1',B_FOLLOW_TOP, B_ITEMS_IN_COLUMN)
		self.tbar.AddItem(self.popoop)
		self.underframe.AddChild(self.tbar)
		
		msg=BMessage(602)
		self.newtab= BCheckBox((10,100,290,120),'NewTabQuestion','Open in new tab (May not work)',msg)
		self.underframe.AddChild(self.newtab)
		
		self.revertBtn=BButton(self.kButtonFrame, self.kButtonName, self.kButtonName, BMessage(603))
		self.underframe.AddChild(self.revertBtn)
		
		self.getsettings()
		
	def getsettings(self):
		path=ConfigSectionMap("Browser")['path']
		self.stringpath.SetText(path)
		name=ConfigSectionMap("Browser")['name']
		self.stringname.SetText(name)
		tabvalue=Config.getboolean("Browser", "newtab")
		if tabvalue:
			self.newtab.SetValue(1)
		else:
			self.newtab.SetValue(0)
			
	def MessageReceived(self, msg):
		global iltab
		if msg.what == 603:
			self.getsettings()
		elif msg.what == 602:
			if self.newtab.Value():
				iltab=2
			else:
				iltab=1
		elif msg.what == 600:
			path=self.stringpath.Text()
			if os.path.exists(path):
				self.stringname.SetText(os.path.basename(path))
				item=self.popoop.FindMarked()
				if item.Label()=='Mozilla':
					webbrowser.register(self.stringname.Text(),None,webbrowser.Mozilla(path))
				elif item.Label()=='Konqueror':
					webbrowser.register(self.stringname.Text(),None,webbrowser.Konqueror(path))#no path here
				elif item.Label()=='Opera':
					webbrowser.register(self.stringname.Text(),None,webbrowser.Opera(path))#no path here
				elif item.Label()=='Generic':
					webbrowser.register(self.stringname.Text(),None,webbrowser.GenericBrowser(path))
		elif msg.what == 601:
			path=self.stringpath.Text()
			if os.path.exists(path):
				item=self.popoop.FindMarked()
				if item.Label()=='Mozilla':
					webbrowser.register(self.stringname.Text(),None,webbrowser.Mozilla(path))
				elif item.Label()=='Konqueror':
					webbrowser.register(self.stringname.Text(),None,webbrowser.Konqueror(path))#no path here
				elif item.Label()=='Opera':
					webbrowser.register(self.stringname.Text(),None,webbrowser.Opera(path))#no path here
				elif item.Label()=='Generic':
					webbrowser.register(self.stringname.Text(),None,webbrowser.GenericBrowser(path))
		elif msg.what == 605:
			path=self.stringpath.Text()
			webbrowser.register(self.stringname.Text(),None,webbrowser.Mozilla(path))
		elif msg.what == 606:
			path=self.stringpath.Text()
			webbrowser.register(self.stringname.Text(),None,webbrowser.Konqueror(path))
		elif msg.what == 607:
			path=self.stringpath.Text()
			webbrowser.register(self.stringname.Text(),None,webbrowser.Opera(path))
		elif msg.what == 608:
			path=self.stringpath.Text()
			webbrowser.register(self.stringname.Text(),None,webbrowser.GenericBrowser(path))
		
		else:
			return
	
	def QuitRequested(self):
		confile=os.path.join(sys.path[0],'config.ini')
		cfgfile = open(confile,'w')
		Config.set('Browser','path',self.stringpath.Text())
		Config.set('Browser','name',self.stringname.Text())
		if self.newtab.Value():
			Config.set('Browser','newtab',True)
		else:
			Config.set('Browser','newtab',False)
		item=self.popoop.FindMarked()
		Config.set('Browser','type', item.Label())
		Config.write(cfgfile)
		cfgfile.close()
		self.Hide()
		return 0

class AboutWindow(BWindow):
	kWindowFrame = (150, 150, 650, 620)
	kButtonFrame = (395, 425, 490, 460)
	kWindowName = "About"
	kButtonName = "Close"
	BUTTON_MSG = struct.unpack('!l', 'PRES')[0]

	def __init__(self):							
		BWindow.__init__(self, self.kWindowFrame, self.kWindowName, B_MODAL_WINDOW, B_NOT_RESIZABLE|B_WILL_DRAW)
		self.CloseButton = BButton(self.kButtonFrame, self.kButtonName, self.kButtonName, BMessage(self.BUTTON_MSG))		
		cise=(10,4,485,420)
		cjamput=(0,0,475,420)
		self.messagjio= BTextView(cise, 'TxTView', cjamput, B_FOLLOW_ALL, B_WILL_DRAW)
		self.messagjio.SetStylable(1)
		self.messagjio.MakeSelectable(0)
		self.messagjio.MakeEditable(0)
		stuff = '\n\t\t\t\t\t\t\tBulletin Gator\n\n\t\t\t\t\t\t\t\t\t\t\tA simple feed aggregator\n\t\t\t\t\t\t\t\t\t\t\tfor Haiku, version 0.8.3\n\t\t\t\t\t\t\t\t\t\t\tcodename "Hully Gully"\n\n\t\t\t\t\t\t\t\t\t\t\tby Fabio Tomat aka TmTFx\n\t\t\t\t\t\t\t\t\t\t\te-mail:\n\t\t\t\t\t\t\t\t\t\t\tf.t.public@gmail.com\n\n\t\t\t\t\t\t\t\t\t\t\tspecial thanks to:\n\t\t\t\t\t\t\t\t\t\t\tVanessa W. x translations\n\nGNU GENERAL PUBLIC LICENSE:\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with this program.  If not, see \n<http://www.gnu.org/licenses/>'
		n = stuff.find('Bulletin Gator')
		m = stuff.find('This')
		self.messagjio.SetText(stuff, [(0, be_plain_font, (0, 0, 0, 0)), (n, be_bold_font, (0, 150, 0, 0)), (n + 14, be_plain_font, (0, 0, 0, 0)),(m,be_plain_font,(100,150,0,0))])
		self.AddChild(self.messagjio)
		self.AddChild(self.CloseButton)
		self.CloseButton.MakeFocus(1)
		link=sys.path[0]+"/help/bgator5.png"
		self.img=BTranslationUtils.GetBitmap(link)
		#self.img.Bounds()
		self.photoframe=PView((0,50,315,185),"photoframe",self.img)
		self.AddChild(self.photoframe)

	def MessageReceived(self, msg):
		if msg.what == self.BUTTON_MSG:
			self.Quit()
		else:
			return


class NewsItem(BListItem):
	nocolor = (0, 0, 0, 0)

	def __init__(self, name,color):
		self.name = name
		self.color=color
		BListItem.__init__(self)

	def DrawItem(self, owner, frame, complete):
		if self.IsSelected() or complete:
			color = (200,200,200,255)
			owner.SetHighColor(color)
			owner.SetLowColor(color)
			owner.FillRect(frame)
			self.color=self.nocolor
		owner.SetHighColor(self.color)
		#if self.color == (200,0,0,0):
		#	self.font = be_bold_font
		#	owner.SetFont(self.font)
		#else:	
		#	self.font = be_plain_font
		#	owner.SetFont(self.font)
		owner.MovePenTo(frame[0],frame[3]-2)
		owner.DrawString(self.name)
		owner.SetLowColor((255,255,255,255))

	def Text(self):
		return self.name
		
class PaperItem(BListItem):
	nocolor = (0, 0, 0, 0)

	def __init__(self, name, nunus):
		self.name = name
		self.nunus=nunus
		self.color=self.nocolor
		self.frame=(0,0,0,0)
		BListItem.__init__(self)

	def DrawItem(self, owner, frame, complete):
		self.frame=frame
		if self.IsSelected() or complete:
			color = (200,200,200,255)
			owner.SetHighColor(color)
			owner.SetLowColor(color)
			owner.FillRect(frame)
			self.color=self.nocolor
		owner.SetHighColor(self.color)
		#if self.color == (200,0,0,0):
		#	self.font = be_bold_font
		#	owner.SetFont(self.font)
		#else:
		#	self.font = be_plain_font
		#	owner.SetFont(self.font)
		owner.MovePenTo(frame[0],frame[3]-2)
		if self.nunus==0:
			owner.SetHighColor((0,0,0,0))
			owner.DrawString(self.name)
		else:
			owner.SetHighColor((0,0,255,0))
			owner.DrawString(self.name+" ("+str(self.nunus)+")")
		owner.SetLowColor((255,255,255,255))
		
	def Text(self):
		return self.name

class PBut(BButton):

	def __init__(self,frame,name,caption,msg,immagine,immaginedown):
		self.immagine=immagine
		self.imgdown=immaginedown
		self.frame=frame
		BButton.__init__(self, frame, name, caption, msg)

	def Draw(self,rect):
		BButton.Draw(self, rect)
		x,y,l,a=self.frame
		inset = (4, 4, l-x-4, a-y-4)
		if self.Value():
			self.DrawBitmap(self.immagine, inset)
		else:
			self.DrawBitmap(self.imgdown, inset)

		
class ScrollView:
	HiWhat = 32 #Doppioclick
	SelezioneGiornale = 101
	SelezioneNotizia = 102
	path=os.path.join(sys.path[0],'xdiefga')

	def __init__(self, rect, name, OPTION, type):
		self.lv = BListView(rect, name, B_SINGLE_SELECTION_LIST,OPTION)
		self.type=type
		con = sqlite3.connect(self.path)
		cur = con.cursor()
		if type:
			item = PaperItem("Status",0)
			self.lv.AddItem(item)
			msg=BMessage(self.SelezioneGiornale)
			self.lv.SetSelectionMessage(msg)
			cix = con.cursor()
			cur.execute('select * from papers')
			for row in cur:
				x=row[1]
				command='select * from a'+str(row[0])
				cix.execute(command)
				cont=0
				for azz in cix:
					if azz[6]==1:
						cont=cont+1
				item = PaperItem(x.encode("utf-8"),cont)
				#item = BStringItem(x.encode("utf-8"))
				self.lv.AddItem(item)
			cix.close()
			cur.execute('select * from news')
			cont=0
			for row in cur:
				if row[6]==1:
					cont=cont+1
			item = PaperItem("Trash",cont)
			self.lv.AddItem(item)
		else:
			msg=BMessage(self.SelezioneNotizia)
			self.lv.SetSelectionMessage(msg)	
			msg = BMessage(self.HiWhat)
			self.lv.SetInvocationMessage(msg)
		self.sv = BScrollView('ScrollView', self.lv, OPTION, B_WILL_DRAW, 1, 1, B_FANCY_BORDER)
		cur.close()
		con.close()

	def reload(self):
		if self.type:
			i=0
			while self.lv.CountItems()>i:
				self.lv.RemoveItem(self.lv.ItemAt(0))
			item = PaperItem("Status",0)
			self.lv.AddItem(item)
			con = sqlite3.connect(self.path)
			cur = con.cursor()
			cix = con.cursor()
			cur.execute('select * from papers')
			for row in cur:
				x=row[1]
				command='select * from a'+str(row[0])
				cix.execute(command)
				cont=0
				for azz in cix:
					if azz[6]==1:
						cont=cont+1
				item = PaperItem(x.encode("utf-8"),cont)
				self.lv.AddItem(item)
			cix.close()
			cur.execute('select * from news')
			cont=0
			for row in cur:
				if row[6]==1:
					cont=cont+1
			item = PaperItem("Trash",cont)
			self.lv.AddItem(item)
			self.lv.Select(0)
			cur.close()
			con.close()

	def topview(self):
		return self.sv

	def listview(self):
		return self.lv


class NuzWindow(BWindow):
	Menus = (
		('File', ((1, 'Add FeedRSS'), (2, 'Get News'), (5, 'Remove Feed'),(6,'Empty Trash'),(None, None),(B_QUIT_REQUESTED, 'Quit'))),
		('Sort by', ((71,'Downloaded'), (72, 'Date'),(73,'Title'),(74, 'Unread'),(75, 'Author'))),
		('Settings', ((41, 'Set Browser'), (42, 'Set Timer')	)),
		('About', ((3, 'Help'),(None, None),(4, 'About')))
		)
	path=os.path.join(sys.path[0],'xdiefga')
	
	def __init__(self, frame):
		global faas, selectionmenu,loopenable,valor
		selectionmenu=0
		faas = True
		BWindow.__init__(self, frame, 'Bulletin Gator a simple Haiku feed aggregator!', B_TITLED_WINDOW, B_WILL_DRAW)
		bounds = self.Bounds()
###### CHECK DATABASE Existence
		if os.path.exists(self.path):
			con=sqlite3.connect(self.path)
			cur=con.cursor()
			try:
				cur.execute('select * from papers')
				goon=True
			except:
				goon=False
				cur.execute("create table papers (idpaper NUMERIC, titlepaper TEXT, rsslink TEXT)")
				con.commit()
			if goon:
				cer=con.cursor()
				for row in cur:
					try:
						cer.execute("select * from a"+str(row[0]))
					except:
						command="create table a"+str(row[0])+" (titlepaper TEXT, entry TEXT, author TEXT, entrylink TEXT, summary TEXT, date DATE,newnews NUMERIC)" 
						cer.execute(command)
						con.commit()
				cer.close()
			cur.close()
			con.close()
		else:
			try:
				con=sqlite3.connect(self.path)
				cur=con.cursor()
				cur.execute("create table papers (idpaper NUMERIC, titlepaper TEXT, rsslink TEXT)")
				cur.execute('''create table news (titlepaper TEXT, entry TEXT, author TEXT, entrylink TEXT, summary TEXT, date DATE,newnews NUMERIC,idpaper NUMERIC)''')
				con.commit()
				cur.close()
				con.close()
			except:
				print "unable to create DB, disk full? readonly FileSystem?"
##### MENU
		self.bar = BMenuBar(bounds, 'Bar')
		x, barheight = self.bar.GetPreferredSize()
		self.mkey = {}
		for menu, items in self.Menus:
			if menu == 'Sort by':
				fullmetaljacket=True
			else:
				fullmetaljacket=False
			menu = BMenu(menu)
			for k, name in items:
				if fullmetaljacket:
					menu.SetRadioMode(1)
					msg = BMessage(k)
					zaza=BMenuItem(name, msg)
					if name == 'Downloaded':
							zaza.SetMarked(1)
					menu.AddItem(zaza)
				else:		
					if k is None:
						menu.AddItem(BSeparatorItem())
					else:
						msg = BMessage(k)
						menu.AddItem(BMenuItem(name, msg))
						self.mkey[k] = name
			self.bar.AddItem(menu)
		l, t, r, b = bounds
		self.AddChild(self.bar)
##### COLOR GRAY UNDER LISTS
		self.underlist = BBox((l, t + barheight, r, b), 'underlist', B_FOLLOW_ALL, B_WILL_DRAW|B_NAVIGABLE, B_NO_BORDER)
		self.AddChild(self.underlist)
##### SCROLLVIEW LEFT
		self.list = ScrollView((18 , barheight+36, r/3 - 18 , b - 53 ), 'ScrollView',B_FOLLOW_TOP_BOTTOM,1)
		starttx=r/3 + 18
		self.underlist.AddChild(self.list.topview())
		self.list.listview().MakeFocus(1)
##### SCROLLVIEW RIGHT
		self.newslist= ScrollView(( r/3 + 18, barheight+36, r - 36, b/2 -12 ), 'ScrollView',B_FOLLOW_TOP|B_FOLLOW_LEFT_RIGHT,0)
		startty=((b/2)+barheight)
		self.underlist.AddChild(self.newslist.topview())
		#self.list.lv.Select(self.list.lv.CountItems()-1,0)
		self.list.lv.Select(0)
##### TEXT for NEWS
		bounds=(starttx,startty,r-22,b-36)
		self.background = BBox(bounds, 'background', B_FOLLOW_ALL, B_WILL_DRAW|B_NAVIGABLE, B_FANCY_BORDER)
		recinto=(starttx+2,startty+2,(r-24),(b-38))
		boundos = (8.0, 8.0, (r-32) - (starttx+2), (b - 46) - (startty+2))
		self.anteprime= BTextView(recinto, 'TxTView', boundos , B_FOLLOW_ALL,B_WILL_DRAW)
		self.anteprime.SetStylable(1)
		self.anteprime.MakeEditable(0)
		stuff = 'Bulletin Gator\n\nSimple Feed Aggregator\n\nEnjoy!'
		n = stuff.find('Bulletin Gator')
		self.anteprime.SetText(stuff, [(0, be_plain_font, (0, 0, 0, 0)), (n, be_bold_font, (0, 150, 0, 0)), (n + 8, be_plain_font, (0, 0, 0, 0))])
		self.underlist.AddChild(self.background)
		self.underlist.AddChild(self.anteprime)
##### ADD FEED
		self.feedbox = BBox((18 , barheight , r/3  , 162), 'feedbox', B_FOLLOW_TOP_BOTTOM, B_WILL_DRAW|B_NAVIGABLE, B_FANCY_BORDER)
		self.underlist.AddChild(self.feedbox)
		msg=BMessage(888)
		self.Linkedit= BTextControl((5,54,r/3 - 23,36),'TxTView', None,None,msg)
		msg=BMessage(666)
		self.CloseButton = BButton((5, 99, 108, 129), "Cancel", "Cancel", msg)
		self.BUTTON_MSG = struct.unpack('!l', 'PRES')[0]
		self.AddButton = BButton((112, 99, 210, 129), "Add", "Add", BMessage(self.BUTTON_MSG))
		self.Labello= BStringView((5,18,r/3-23,36),"Label","Add feed link here:")
		self.feedbox.AddChild(self.CloseButton)
		self.feedbox.AddChild(self.AddButton)
		self.feedbox.AddChild(self.Linkedit)
		self.feedbox.AddChild(self.Labello)
		self.feedbox.Hide()
##### FILTER NEWS
		msg=BMessage(321)
		self.Findedit= BTextControl((r/3+18,barheight,r-22,18),'TxTView', "Find:",None,msg,B_FOLLOW_LEFT_RIGHT)
		self.Findedit.SetDivider(50.0)
		self.underlist.AddChild(self.Findedit)
###### PROGRESS BAR
		self.progressbox = BBox((16 , barheight , r/3-2, b-36), 'progressbox', B_FOLLOW_TOP_BOTTOM, B_WILL_DRAW|B_NAVIGABLE, B_FANCY_BORDER)
		self.underlist.AddChild(self.progressbox)
		self.progressbox.Hide()
		self.bar = BStatusBar((5,70,r/3-25,144), 'progress','0%', '100%')
		self.bar.SetMaxValue(self.list.lv.CountItems()-2.0)
		self.info= BStringView((5,20,r/3-25,110),"info","Updating news, please wait...")
		self.canceldownload=BButton((5,130,r/3-25,174), "cancdown", "Stop Downloading", BMessage(266))
		self.progressbox.AddChild(self.bar)
		self.progressbox.AddChild(self.info)
		self.progressbox.AddChild(self.canceldownload)
###### INFO BOX UPDATE
		self.infupdbox = BBox(( r/3 + 18, barheight, r-18-2, b-36), 'infoboxupdate', B_FOLLOW_TOP_BOTTOM|B_FOLLOW_LEFT_RIGHT, B_WILL_DRAW|B_NAVIGABLE, B_FANCY_BORDER)
		self.underlist.AddChild(self.infupdbox)
		self.infupdbox.Hide()
		u,i,o,p=self.infupdbox.Bounds()
		self.updinf= BStringView((u+2,p/2-9,o-2,p/2+9),"infupd","Now 0 new news", B_FOLLOW_TOP|B_FOLLOW_LEFT_RIGHT)#(5,,o-23,),"infupd","Now 0 new news")
		self.updinf.SetAlignment(B_ALIGN_CENTER)
		self.infupdbox.AddChild(self.updinf)
###### CONTROL BUTTONS
		self.BtnBox=BBox(( 18, 5, r/3-5, 49), 'buttonbox', B_FOLLOW_TOP, B_WILL_DRAW|B_NAVIGABLE, B_NO_BORDER)
		link=sys.path[0]+"/help/plusmine2.bmp"
		img=BTranslationUtils.GetBitmap(link)
		link2=sys.path[0]+"/help/plusmined.bmp"
		img2=BTranslationUtils.GetBitmap(link2)
		self.fadBtn = PBut((0, 5, 36, 41), "Add","+", BMessage(1),img2,img)
		link=sys.path[0]+"/help/minusmine.bmp"
		img=BTranslationUtils.GetBitmap(link)
		link2=sys.path[0]+"/help/minusmined.bmp"
		img2=BTranslationUtils.GetBitmap(link2)
		self.fremBtn = PBut((36, 5, 72, 41), "Frem", "-",BMessage(5),img2,img)
		link=sys.path[0]+"/help/downmine.bmp"
		img=BTranslationUtils.GetBitmap(link)
		link2=sys.path[0]+"/help/downmined.bmp"
		img2=BTranslationUtils.GetBitmap(link2)
		self.refBtn = PBut((80, 5, 116, 41), "Ref", "Get",BMessage(2),img2,img)
		self.RedBtn = BButton((124, 5, 210, 41), "Mark", "Mark Read", BMessage(210))
		self.underlist.AddChild(self.BtnBox)
		self.BtnBox.AddChild(self.fadBtn)
		self.BtnBox.AddChild(self.fremBtn)
		self.BtnBox.AddChild(self.refBtn)
		self.BtnBox.AddChild(self.RedBtn)
###### Sliders
		self.hsliz=BSlider((self.list.sv.Frame()[0],b-35,r-36,b),"hslide","",BMessage(870),0,1000,B_TRIANGLE_THUMB,B_FOLLOW_LEFT_RIGHT|B_FOLLOW_BOTTOM)
		self.hsliz.SetModificationMessage(BMessage(870))
		self.hsliz.SetPosition(0.34)
		self.vsliz=BSlider((r-20,self.newslist.sv.Frame()[1],r,b-36),"vslide","",BMessage(871),0,1000,B_TRIANGLE_THUMB,B_FOLLOW_TOP_BOTTOM|B_FOLLOW_RIGHT)
		self.vsliz.SetPosition(0.50)
		
		self.vsliz.SetOrientation(B_VERTICAL)
		self.vsliz.SetModificationMessage(BMessage(871))
		self.underlist.AddChild(self.hsliz)
		self.underlist.AddChild(self.vsliz)
		try:
			confile=os.path.join(sys.path[0],'config.ini')
			Config.read(confile)
			horiz=ConfigSectionMap("Size")['horizon']
			vertiz=ConfigSectionMap("Size")['vertic']
			self.hsliz.SetPosition(float(horiz))
			self.vsliz.SetPosition(float(vertiz))
			BApplication.be_app.WindowAt(0).PostMessage(870)
			BApplication.be_app.WindowAt(0).PostMessage(871)
		except:
			pass
		#start thread loop
		try:
			loopenable=Config.getboolean("Timer","enable")
			valor=int((ConfigSectionMap("Timer")['value']))
		except:
			confile=os.path.join(sys.path[0],'config.ini')
			cfgfile = open(confile,'w')
			Config.add_section('Timer')
			Config.set('Timer','value', 30)
			Config.set('Timer','enable', False)
			Config.write(cfgfile)
			cfgfile.close()
			Config.read(confile)
			valor=30
		BApplication.be_app.WindowAt(0).PostMessage(471)
		
		

	def remove_html_tags(self,data):
		p = re.compile(r'<.*?>')
		return p.sub('', data)

	def markread(self):
		#UPDATED to new database system
		self.anteprime.SetText("")
		try:
			if (self.list.lv.CurrentSelection()>-1):
				con = sqlite3.connect(self.path)
				cur = con.cursor()
				cox = con.cursor()
				if (((self.list.lv.CurrentSelection())==(self.list.lv.CountItems()-1)) or ((self.list.lv.CurrentSelection())== 0)):
					cox.execute('select * from papers')
					for row in cox:
						id=row[0]
						command='UPDATE a'+str(id)+' SET newnews=0'
						cur.execute(command)
						con.commit()
					cox.close()
					cur.close()
					con.close()
					BApplication.be_app.WindowAt(0).PostMessage(883)
				elif (self.list.lv.CurrentSelection()>0): #elif >0
					titlepapero=self.list.lv.ItemAt(self.list.lv.CurrentSelection()).Text()
					cur.execute('select * from papers')
					for row in cur:
						if row[1].encode("utf-8")==titlepapero:
							id=row[0]
							break
					command='UPDATE a'+str(id)+' SET newnews=0'
					#cur.execute('UPDATE news SET newnews=0 WHERE idpaper=%d;'% id)
					cur.execute(command)
					con.commit()
					cur.close()
					con.close()
					item= self.list.lv.ItemAt(self.list.lv.CurrentSelection())
					item.nunus=0
					self.list.sv.Hide()
					self.list.sv.Show()
				self.gjornaaltolet()
		except:
			print "Folk che ti trai"
			print "could not write db"
			try:
				con.rollback()
				cur.close()
				con.close()
			except:
				pass

	def gjornaaltolet(self):
			self.anteprime.SetText("")
			#funzion di selezion gjornaal
			#UPDATED for new database system
			try:
				self.newslist.lv.DeselectAll()
				self.newslist.lv.RemoveItems(0,self.newslist.lv.CountItems()) #azzera newslist
				self.newslist.lv.ScrollToSelection()

				con = sqlite3.connect(self.path)
				cur = con.cursor()
				
				if self.list.lv.CurrentSelection()>-1:
					if ((self.list.lv.CurrentSelection())==(self.list.lv.CountItems()-1)):
						if selectionmenu==0:
							cur.execute('select * from news')
						elif selectionmenu==1:
							cur.execute('select * from news order by entry')
						elif selectionmenu==2:
							cur.execute('select * from news order by date')
						elif selectionmenu==3:
							cur.execute('select * from news order by newnews')
						elif selectionmenu==4:
							cur.execute('select * from news order by author')
						#SEZIONE PER SELEZIONE "ALL" NELLA LISTA NEWSPAPERS 
						for row in cur:
							x=row[1]
							# IF CON FILTRO
							lowered=x.lower().encode("utf-8")
							if self.Findedit.Text() == "":
								if row[6] == 1:
									item = NewsItem(x.encode("utf-8"),(200,0,0,0))
									self.newslist.lv.AddItem(item)
								else:
									item = NewsItem(x.encode("utf-8"),(0,0,0,0))
									self.newslist.lv.AddItem(item)
#							elif self.Findedit.Text() == "&u":
#								if row[6] == 1:
#									#item = BStringItem(x.encode("utf-8"))
#									item = NewsItem(x.encode("utf-8"),(200,0,0,0))
#									self.newslist.lv.AddItem(item)									
							else:
								srclowered=self.Findedit.Text().lower()
								res=lowered.find(srclowered)
								if res>-1:
									if row[6] == 1:
										item = NewsItem(x.encode("utf-8"),(200,0,0,0))
										self.newslist.lv.AddItem(item)
									else:
										item = NewsItem(x.encode("utf-8"),(0,0,0,0))
										self.newslist.lv.AddItem(item)
					elif (self.list.lv.CurrentSelection()==0):
						numpa=0
						numnu=0
						numnunu=0
						trashbin=0
						cux=con.cursor()
						cur.execute('select * from news')
						for x in cur:
							trashbin=trashbin+1
							numnu=numnu+1
							if x[6]==1:
								numnunu=numnunu+1
						cur.execute('select * from papers')
						for x in cur:
							numpa=numpa+1
							command='select * from a'+str(x[0])
							cux.execute(command)
							for y in cux:
								numnu=numnu+1
								if y[6]==1:
									numnunu=numnunu+1
						cux.close()
						stuff= ("Database summary:\n\n\nNumber of papers: "+str(numpa)+"\n\nNew news: "+str(numnunu)+"\n\nNumber of news: "+str(numnu)+"\n\nNumber of news saved in trashbin: "+str(trashbin))
						txt0="Database summary"
						txt1="New news"
						txt2="Number of news saved in trashbin"
						
						m = stuff.find(txt0)
						n = stuff.find(txt1)
						a = stuff.find(txt2)
						
						self.anteprime.SetText(stuff, [(0, be_plain_font, (0, 0, 0, 0)), (m, be_bold_font, (0, 0, 0, 0)), ((m + len(txt0)),be_plain_font, (0, 0, 0, 0)),(n, be_bold_font, (200, 0, 0, 0)), ((n + len(txt1)),be_plain_font, (0, 0, 0, 0)), (a, be_bold_font, (100, 100, 0, 0)), ((a+len(txt2)),be_plain_font,(0,0,0,0))])
						
					else:
						#SELEZIONE IN BASE AL GIORNALE SCELTO
						newspaper=self.list.lv.ItemAt(self.list.lv.CurrentSelection()).Text()
						cur.execute('select * from papers')
						for row in cur:
							if row[1].encode("utf-8") == newspaper:
								idpapero=row[0]
								break
						command = ('select * from a'+str(idpapero))
						if selectionmenu==0:
							pass
						elif selectionmenu==1:
							command = command+' order by entry'
						elif selectionmenu==2:
							command = command+' order by date'
						elif selectionmenu==3:
							command = command+' order by newnews'
						elif selectionmenu==4:
							command = command+' order by author'
						cur.execute(command)
						for row in cur:
							x=row[0]
							if x.encode("utf-8") == newspaper:
								y=row[1]
								# IF CON FILTRO 
								lowered=y.lower().encode("utf-8")
								if self.Findedit.Text() == "":
									if row[6] == 1:
										item = NewsItem(y.encode("utf-8"),(200,0,0,0))
										self.newslist.lv.AddItem(item)
									else:
										self.newslist.lv.AddItem(NewsItem(y.encode("utf-8"),(0,0,0,0)))
#								elif self.Findedit.Text() == "&u":
#									if row[6] == 1:
#										self.newslist.lv.AddItem(NewsItem(y.encode("utf-8"),(0,0,0,0)))
								else:
									srclowered=self.Findedit.Text().lower()
									res=lowered.find(srclowered)
									if res>-1:
										self.newslist.lv.AddItem(NewsItem(y.encode("utf-8"),(0,0,0,0)))
				cur.close()
				con.close()
			except:
				try:
					cur.close()
					con.close()
				except:
					pass
			try:
				self.newslist.lv.DeselectAll()
				#self.newslist.lv.Select(0)
				#self.newslist.lv.Select(self.newslist.lv.CountItems()-1)
				self.newslist.lv.Select(self.newslist.lv.CountItems()-1)
				self.newslist.lv.ScrollToSelection()
			except:
				pass
			return

	def FrameResized(self,x,y):
		BApplication.be_app.WindowAt(0).PostMessage(870)
		BApplication.be_app.WindowAt(0).PostMessage(871)
#		l,t,r,b= self.anteprime.Bounds()
#		boundos = (8.0, 8.0, (r - 8.0), (b-8.0))
#		self.anteprime.SetTextRect(boundos)
#		l,t,r,b=self.infupdbox.Bounds()
#		self.updinf.ResizeTo(r-23,18)

	def tiriles_ju2(self,rsspass):
	### UPDATED for new database system
	##inserire check database consistency per ricreare le tabelle mancanti dai vecchi database
		global faas,godown
		BApplication.be_app.WindowAt(0).PostMessage(505)
		pth=os.path.join(sys.path[0],'xdiefga')
		try:
			con = sqlite3.connect(pth)
			if rsspass=="":
				cur = con.cursor()
				cur.execute('select * from papers')
				for row in cur:
					if godown:
						BApplication.be_app.WindowAt(0).PostMessage(515)
						cul = con.cursor()
						idpapero=row[0]
						rss = feedparser.parse(row[2])
						y=len(rss['entries'])
						for x in range (y):
							aggiunta=True
							command='select * from a'+str(idpapero)
							cul.execute(command)
							k=rss.entries[x].title
							for bobo in cul:
								z=bobo[1]
								if z.encode("utf-8") == k.encode("utf-8"):
									aggiunta = False
							if aggiunta:
								try:
									gjornaal=rss.feed.title
								except:
									gjornaal=""
								try:
									titul=rss.entries[x].title
								except:
									titul=""
								try:
									autoor=rss.entries[x].author
								except:
									autoor=""
								try:
									collegament=rss.entries[x].link
								except:
									collegament=""
								try:
									sommari=self.remove_html_tags(rss.entries[x].summary_detail.value)
								except:
									sommari=""
								try:
									rssdate=rss.entries[x].date
									date,timeall= rssdate.split('T')
									time,all= timeall.split('+')
									zornade=(date+' '+time)
								except:
									now=datetime.datetime.now()
									zornade=(str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second))
								new=1
								try:
									madone = con.cursor()
									command="insert into a"+str(idpapero)+" values(?,?,?,?,?,?,?);"
									madone.execute(command, (gjornaal,titul,autoor,collegament,sommari,zornade,new))
									con.commit()
									madone.close()
									BApplication.be_app.WindowAt(0).PostMessage(525)
								except:
									con.rollback()
									ask = BAlert('oops', 'Unable to update database. Try again later', 'Ok',None, None, None, 3)
									ask.Go()
						cul.close()
				cur.close()
			else:
				BApplication.be_app.WindowAt(0).PostMessage(535)
				rss = feedparser.parse(rsspass)
				y=len(rss['entries'])
				for x in range (y):
					aggiunta=True
					cul = con.cursor()
					cul.execute('select * from papers')
					for row in cul:
						if row[2] == rsspass:
							idpapero=row[0]
							break
					command='select * from a'+str(idpapero)
					cul.execute(command)
					#cul.execute('select * from news')
					for bobo in cul:
						z=bobo[1]
						k=rss.entries[x].title
						if z.encode("utf-8") == k.encode("utf-8"):
							aggiunta = False
					if aggiunta:
						try:
							gjornaal=rss.feed.title
						except:
							gjornaal=""
						try:
							titul=rss.entries[x].title
						except:
							titul=""
						try:
							autoor=rss.entries[x].author
						except:
							autoor=""
						try:
							collegament=rss.entries[x].link
						except:
							collegament=""
						try:
							sommari=self.remove_html_tags(rss.entries[x].summary_detail.value)
						except:
							sommari=""
						try:
							rssdate=rss.entries[x].date
							date,timeall= rssdate.split('T')
							time,all= timeall.split('+')
							zornade=(date+' '+time)
						except:
							now=datetime.datetime.now()
							zornade=(str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second))
						madone = con.cursor()
						madone.execute('select * from papers')
						new=1
						try:
							command=("insert into a"+str(idpapero)+" values(?,?,?,?,?,?,?);")
							madone.execute(command, (gjornaal,titul,autoor,collegament,sommari,zornade,new))
							con.commit()
							BApplication.be_app.WindowAt(0).PostMessage(525)
						except:
							con.rollback()
							ask = BAlert('oops', 'Unable to update database. Try again later', 'Ok',None,None, None, 3)
							ask.Go()
						madone.close()			
				cul.close()
			con.close()
		except:
			pass
		faas=True	
		BApplication.be_app.WindowAt(0).PostMessage(505)
		BApplication.be_app.WindowAt(0).PostMessage(883)
		#BApplication.be_app.WindowAt(0).PostMessage(101)#check if needed?
		

	def funcalfa(self,a,b):
		a=a.Text()
		b=b.Text()
		if a > self.b:
			return 1
		elif self.a==self.b:
			return 0
		else:
			return -1
	
	def enableloop(self):
		global loopenable
		if loopenable:
			loopenable=False
		else:
			loopenable=True

# MESSAGES 
	def MessageReceived(self, msg):
		global valor,faas,counter,selectionmenu,godown
		if faas:
			if msg.what == 71:
				selectionmenu=0
				self.gjornaaltolet()
				return
			elif msg.what == 72:
				selectionmenu=2
				self.gjornaaltolet()
				return
			elif msg.what == 73:
				selectionmenu=1
				self.gjornaaltolet()
				return
			elif msg.what == 74:
				selectionmenu=3
				self.gjornaaltolet()
				return
			elif msg.what == 75:
				selectionmenu=4
				self.gjornaaltolet()
				return
			if msg.what == 666:
				# Cancel add Feed box
				self.feedbox.Hide()
				self.list.sv.Show()
				self.BtnBox.Show()
				self.Findedit.Show()
				self.newslist.sv.Show()
				self.anteprime.Show()
				self.background.Show()
				return
			elif msg.what == 471:
				temp=valor*60
				self.r = timerLoop((int(temp)))
				self.r.start()
			elif (msg.what == self.BUTTON_MSG):
				try:
					# aggiungo notiziario nuovo
					#UPDATED to new database system
					con = sqlite3.connect(self.path)
					cur = con.cursor()
					link=self.Linkedit.Text()
					d=feedparser.parse(link)
					if d.feed.has_key('title'):
						titul=d.feed.title
						aggiungere=True
						cur.execute('select * from papers')
						for row in cur:
							x=row[1]
							if x.encode("utf-8")==titul.encode("utf-8"):
								aggiungere=False
								z=BAlert('Spud', "It\'s already in newspaper\'s list", 'OK',None,None, None, 1)
								z.Go()
						cur.close()
						if aggiungere:
								madone=con.cursor()
								madone.execute('select * from papers')
								cx=0
								try:
									for row in madone:
										if row[0] >= cx:
											cx=row[0]+1
								except:
									pass
								madone.close()
								cur = con.cursor()
								command="create table a"+str(cx)+" (titlepaper TEXT, entry TEXT, author TEXT, entrylink TEXT, summary TEXT, date DATE,newnews NUMERIC)"#,idpaper NUMERIC)"
								cur.execute(command)
								madone=con.cursor()
								madone.execute("insert into papers values(?,?,?);", (cx,d.feed.title,link))
								con.commit()
								madone.close()
								cur.close()
								self.list.reload()
								faas=False
								counter = 0
								thread.start_new_thread(self.tiriles_ju2,(link,))
						else:
							con.close()
						self.list.sv.Show()
						self.BtnBox.Show()
						self.Findedit.Show()
						self.newslist.sv.Show()
						self.anteprime.Show()
						self.background.Show()
						self.feedbox.Hide()
					else:
						z=BAlert('Spud', "It doesn\'t look like a feed", 'OK',None,None, None, 3)
						z.Go()
						self.feedbox.Hide()
						self.list.sv.Show()
						self.BtnBox.Show()
						self.Findedit.Show()
						self.newslist.sv.Show()
						self.anteprime.Show()
						self.background.Show()			
					self.bar.SetMaxValue(self.list.lv.CountItems()-2.0)
				except:
					try:
						con.rollback()
						cur.close()
						con.close()
					except:
						pass
				return
			elif msg.what == self.list.SelezioneGiornale:
				# SEZIONE PER VISUALIZZARE LE NEWS IN BASE AL GIORNALE SELEZIONATO
				self.gjornaaltolet()
				return
			elif msg.what == 1:
				# SEZIONE PER AGGIUNGI FEED
				if self.feedbox.IsHidden():
					self.list.sv.Hide()
					self.BtnBox.Hide()
					self.Findedit.Hide()
					self.newslist.sv.Hide()
					self.anteprime.Hide()
					self.background.Hide()
					self.Linkedit.SetText("")
					self.updinf.SetText("Now 0 new news")
					self.feedbox.Show()
					self.Linkedit.MakeFocus(1)
				return
			elif msg.what == 2:
			# SEZIONE PER AGGIORNARE LE NEWS
				godown=True
				counter=0
				self.updinf.SetText("Now 0 new news")

				if self.list.lv.CurrentSelection()>-1:
					faas=False
					if self.list.lv.IsItemSelected(self.list.lv.CountItems()-1) or self.list.lv.IsItemSelected(0):
						self.canceldownload.Show()
						thread.start_new_thread(self.tiriles_ju2,("",))
					else:
						try:
							newspaper=self.list.lv.ItemAt(self.list.lv.CurrentSelection()).Text()
							con = sqlite3.connect(self.path)
							cur = con.cursor()
							cur.execute('select * from papers')
							for row in cur:
								if row[1].encode("utf-8") == newspaper:
									tolaunch=row[2]
									break
							cur.close()
							con.close()
							self.canceldownload.Hide()
							thread.start_new_thread(self.tiriles_ju2,(tolaunch,))
						except:
							pass
				return
			elif msg.what == 29:
				godown=True
				counter=0
				self.updinf.SetText("Now 0 new news")
				faas=False
				self.canceldownload.Show()
				thread.start_new_thread(self.tiriles_ju2,("",))
				return
			elif msg.what == 5:
				# sezione per cancellare notiziari e notizie
				#UPDATED to new database system
				if ((self.list.lv.CurrentSelection()==self.list.lv.CountItems()-1)or (self.list.lv.CurrentSelection()==0)):
					return
				else:
					lookfor=self.list.lv.ItemAt(self.list.lv.CurrentSelection()).Text()
					ask = BAlert('whoa', 'Are you sure to remove '+lookfor+"?", 'Yes','No', None, None, 2)
					ans=ask.Go()
					if ans == 0:
						try:
							con = sqlite3.connect(self.path)
							cur = con.cursor()
							cur.execute('select * from papers')
							proceed=False
							for row in cur:
								if row[1].encode("utf-8") == lookfor:
									idpapero=row[0]
									proceed=True
									break
							if proceed:
								ask = BAlert('whoa', 'Do you want to save the '+lookfor+' news in the Trash section?', 'Yes','No', None, None, 2)
								answ=ask.Go()
								if answ==1:
									command="drop table a"+str(idpapero)
									cur.execute(command)
									con.commit()
								else:
									madone=con.cursor()
									command='select * from a'+str(idpapero)
									cur.execute(command)
									for culo in cur:
										madone.execute('select * from news')
										vamova=True
										for frico in madone:
											if ((frico[1].encode("utf-8")==culo[1].encode("utf-8")) and (frico[3]==culo[3])):
												vamova=False
												break
										if vamova:
											try:
												gjornaal=culo[0]
											except:
												gjornaal=""
											try:
												titul=culo[1]
											except:
												titul=""
											try:
												autoor=culo[2]
											except:
												autoor=""
											try:
												collegament=culo[3]
											except:
												collegament=""
											try:
												sommari=culo[4]
											except:
												sommari=""
											try:
												zornade=culo[5]
											except:
												now=datetime.datetime.now()
												zornade=(str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second))
											try:
												new=culo[6]
											except:
												new=1
											madone.execute("insert into news values(?,?,?,?,?,?,?,?);", (gjornaal,titul,autoor,collegament,sommari,zornade,new,idpapero))
											con.commit()
									command="drop table a"+str(idpapero)
									cur.execute(command)
									con.commit()
									madone.close()
								cur.execute('DELETE from papers WHERE idpaper=?', (idpapero,))
								con.commit()
								cur.close()
								con.close()
								self.list.reload()
						except:
							try:
								con.rollback()
								cur.close()
								con.close()
							except:
								pass
				return
			elif msg.what == 321:
				self.gjornaaltolet()
			elif msg.what == 4:
				#print "avvia schermata About"
				self.About = AboutWindow()
				self.About.Show()
				return
			elif msg.what==41:
				try:
					self.Browsettin.Show()
				except:
					self.Browsettin=BrowserSettings()
					self.Browsettin.Show()
				return
			elif msg.what==42:
				try:
					self.Timeset.Show()
				except:
					self.Timeset=TimerSettings()
					self.Timeset.Show()
				return
			elif msg.what == 3:
				#print "Avvia help"
				pothpath=os.path.join(sys.path[0],'help/index.html')
				thread.start_new_thread(openlink,(pothpath,))
				return
			elif msg.what == 6:
				con = sqlite3.connect(self.path)
				cur = con.cursor()
				cur.execute("drop table news")
				con.commit()
				cur.execute('''create table news (titlepaper TEXT, entry TEXT, author TEXT, entrylink TEXT, summary TEXT, date DATE,newnews NUMERIC,idpaper NUMERIC)''')
				con.commit()
				cur.close()
				con.close()
				self.list.reload()
				return
			elif msg.what == 210:
				self.markread()
				return
		if msg.what == 505:
				# Progress Bar for aggiornamenti
				if self.progressbox.IsHidden():
					self.Findedit.Hide()
					self.list.sv.Hide()
					self.newslist.sv.Hide()
					self.anteprime.Hide()
					self.background.Hide()
					self.BtnBox.Hide()
					self.progressbox.Show()
					self.infupdbox.Show()
					
				else:
					self.bar.Reset('0%','100%')
					self.bar.SetMaxValue(self.list.lv.CountItems()-2.0)
					self.progressbox.Hide()
					self.infupdbox.Hide()
					self.list.sv.Show()
					self.newslist.sv.Show()
					self.BtnBox.Show()
					self.anteprime.Show()
					self.background.Show()
					self.Findedit.Show()
					
				return
		elif msg.what == 515:
					self.bar.Update(1.0)
					return
		elif msg.what == 525:
					counter=counter+1
					self.updinf.SetText(("Now %d new news" % (counter)))
					print counter
					return
		elif msg.what == 535:
					self.bar.Update(self.bar.MaxValue())
					return
		elif msg.what == self.list.HiWhat:
			if ((self.list.lv.CurrentSelection())==(self.list.lv.CountItems()-1)):
				try:
					#print "Lancio il Browser"
					# UPDATED for new database system
					con = sqlite3.connect(self.path)
					cur = con.cursor()
					cur.execute('select * from news')
					article=self.newslist.lv.ItemAt(self.newslist.lv.CurrentSelection()).Text()
					k=article.decode("utf-8")
					for row in cur:
						if k==row[1]:
							thread.start_new_thread(openlink,(row[3],))
							break
					cur.close()
					con.close()
					return
				except:
					return
			else:
				try:
					#print "Lancio il Browser"
					# UPDATED for new database system
					con = sqlite3.connect(self.path)
					cur = con.cursor()
					cur.execute('select * from papers')
					lookfor=self.list.lv.ItemAt(self.list.lv.CurrentSelection()).Text()
					for row in cur:
						if row[1].encode("utf-8") == lookfor:
							idpapero=row[0]
					command='select * from a'+str(idpapero)
					cur.execute(command)
					article=self.newslist.lv.ItemAt(self.newslist.lv.CurrentSelection()).Text()
					k=article.decode("utf-8")
					for row in cur:
						if k==row[1]:
							thread.start_new_thread(openlink,(row[3],))
							break
					cur.close()
					con.close()
					return
				except:
					return
		elif msg.what==266:
			godown=False
		#resize by slider
		elif msg.what == 870:
			l, t, r, b=self.underlist.Bounds()
			a,s,d,f = self.hsliz.Bounds()
			lung=((d-16)*self.hsliz.Position())-24 #(d-16) cause 8px for distance from bounds and slider cursor
			z,x,c,v=self.list.sv.Bounds()
			self.list.sv.ResizeTo((self.list.sv.Frame()[0]+8+lung),(v))
			z,x,c,v=self.list.lv.Bounds()
			self.list.lv.ResizeTo((self.list.lv.Frame()[0]+8+lung-4),(v))

			z,x,c,v = self.newslist.sv.Frame()
			self.newslist.sv.MoveTo(self.list.sv.Frame()[0]+8+lung+36,x)
			g,h,j,k =self.newslist.sv.Frame()
			b,n,m,p = self.newslist.sv.Bounds()
			newsize=r-g-20
			self.newslist.sv.ResizeTo(newsize,p)
			self.newslist.lv.ResizeTo(newsize-18,p-18)
			
			z,x,c,v = self.anteprime.Frame()
			self.anteprime.MoveTo(self.list.sv.Frame()[0]+8+lung+39,x)
			g,h,j,k =self.anteprime.Frame()
			b,n,m,p = self.anteprime.Bounds()
			newsize=r-g-20
			self.anteprime.ResizeTo(newsize-3,p)
			
			u,i,o,y= self.anteprime.Bounds()
			boundos = (8.0, 8.0, (o - 8.0), (y-8.0))
			self.anteprime.SetTextRect(boundos)
			
			z,x,c,v = self.background.Frame()
			self.background.MoveTo(self.list.sv.Frame()[0]+8+lung+36,x)
			g,h,j,k =self.background.Frame()
			b,n,m,p = self.background.Bounds()
			newsize=r-g-20
			self.background.ResizeTo(newsize,p)
			
			
		elif msg.what == 871:
			l, t, r, b=self.underlist.Bounds()
			a,s,d,f = self.vsliz.Bounds()
			lung=f-(((f-16)*self.vsliz.Position()))
			z,x,c,v=self.newslist.sv.Bounds()
			self.newslist.sv.ResizeTo((c),(lung-16))
			z,x,c,v=self.newslist.lv.Bounds()
			self.newslist.lv.ResizeTo((c),(lung-34))
			
			z,x,c,v = self.anteprime.Frame()
			self.anteprime.MoveTo(self.background.Frame()[0]+3,lung+52)
			g,h,j,k =self.anteprime.Frame()
			b,n,m,p = self.anteprime.Bounds()
			fine= self.underlist.Frame()[3]-39
			inizio = self.anteprime.Frame()[1]
			delta=fine-inizio
			self.anteprime.ResizeTo(self.background.Bounds()[2]-6,delta)
			u,i,o,y= self.anteprime.Bounds()
			boundos = (8.0, 8.0, (o - 8.0), (y-8.0))
			self.anteprime.SetTextRect(boundos)
			
			z,x,c,v = self.background.Frame()
			self.background.MoveTo(z,lung+52)
			g,h,j,k =self.background.Frame()
			b,n,m,p = self.background.Bounds()
			fine= self.underlist.Frame()[3]-36
			inizio = self.anteprime.Frame()[1]
			delta=fine-inizio
			self.background.ResizeTo(m,delta)		
		elif msg.what == 883:
			con = sqlite3.connect(self.path)
			cur = con.cursor()
			cul = con.cursor()
			cur.execute('select * from papers')
			for row in cur:
				command='select * from a'+str(row[0])
				cul.execute(command)
				abaco=0
				for bighe in cul:
					if bighe[6] == 1:
						abaco = abaco+1
				for x in range(self.list.lv.CountItems()-2):
					item=self.list.lv.ItemAt(x+1)
					if item.Text() == row[1].encode("utf-8"):
						item.nunus=abaco
			self.list.sv.Hide()
			self.list.sv.Show()
			self.gjornaaltolet()
		elif msg.what == self.list.SelezioneNotizia:
		#sezione per visualizzare il sommario e rendere letta la news
		#UPDATED for the new database system
			if ((self.list.lv.CurrentSelection())==(self.list.lv.CountItems()-1)):
				try:
					con = sqlite3.connect(self.path)
					cur = con.cursor()
					cur.execute('select * from news')
					x=self.newslist.lv.ItemAt(self.newslist.lv.CurrentSelection()).Text()
					for row in cur:
						y=row[1]
						if x==y.encode("utf-8"):
							origin=row[0].encode("utf-8")
							if row[2] == "":
								dodad=False
							else:
								dodad=True
							autore=row[2].encode("utf-8")
							summary=row[4].encode("utf-8")
							if row[6] == 1:
								cur.execute('UPDATE news SET newnews=0 WHERE titlepaper=? AND entry=?',(row[0],row[1]))
								con.commit()
								item= self.list.lv.ItemAt(self.list.lv.CurrentSelection())
								item.nunus=item.nunus-1
								self.list.sv.Hide()
								self.list.sv.Show()
					if dodad:
						stuff= ("from: "+origin+"\n"+"by: "+autore+"\n\n"+summary)
						n = stuff.find(origin)
						a = stuff.find(autore)
						self.anteprime.SetText(stuff, [(0, be_plain_font, (0, 0, 0, 0)), (n, be_bold_font, (0, 150, 0, 0)), ((n + len(origin)),be_plain_font, (0, 0, 0, 0)), (a, be_bold_font, (0, 0, 150, 0)), ((a+len(autore)),be_plain_font,(0,0,0,0))])
					else:
						stuff= ("from: "+origin+"\n\n"+summary)
						n=stuff.find(origin)
						self.anteprime.SetText(stuff,[(0, be_plain_font, (0, 0, 0, 0)), (n, be_bold_font, (0, 150, 0, 0)), ((n + len(origin)),be_plain_font, (0, 0, 0, 0))])
					cur.close()
					con.close()
					return
				except:
					try:
						con.rollback()
						cur.close()
						con.close()
					except:
						pass
					return
			else:
				try:
					con = sqlite3.connect(self.path)
					cur = con.cursor()
					cur.execute('select * from papers')
					lookfor=self.list.lv.ItemAt(self.list.lv.CurrentSelection()).Text()
					for row in cur:
						if row[1].encode("utf-8") == lookfor:
							idpapero=row[0]
					command='select * from a'+str(idpapero)
					cur.execute(command)			
					x=self.newslist.lv.ItemAt(self.newslist.lv.CurrentSelection()).Text()
					for row in cur:
						y=row[1]
						if x==y.encode("utf-8"):
							origin=row[0].encode("utf-8")
							if row[2] == "":
								dodad=False
							else:
								dodad=True
							autore=row[2].encode("utf-8")
							summary=row[4].encode("utf-8")
							if row[6] == 1:
								command='UPDATE a'+str(idpapero)+' SET newnews=0 WHERE titlepaper=? AND entry=?'
								cur.execute(command,(row[0],row[1]))
								con.commit()
								item= self.list.lv.ItemAt(self.list.lv.CurrentSelection())
								item.nunus=item.nunus-1
								self.list.sv.Hide()
								self.list.sv.Show()
					if dodad:
						stuff= ("from: "+origin+"\n"+"by: "+autore+"\n\n"+summary)
						n = stuff.find(origin)
						a = stuff.find(autore)
						self.anteprime.SetText(stuff, [(0, be_plain_font, (0, 0, 0, 0)), (n, be_bold_font, (0, 150, 0, 0)), ((n + len(origin)),be_plain_font, (0, 0, 0, 0)), (a, be_bold_font, (0, 0, 150, 0)), ((a+len(autore)),be_plain_font,(0,0,0,0))])
					else:
						stuff= ("from: "+origin+"\n\n"+summary)
						n=stuff.find(origin)
						self.anteprime.SetText(stuff,[(0, be_plain_font, (0, 0, 0, 0)), (n, be_bold_font, (0, 150, 0, 0)), ((n + len(origin)),be_plain_font, (0, 0, 0, 0))])
					cur.close()
					con.close()
					return
				except:
					try:
						con.rollback()
						cur.close()
						con.close()
					except:
						pass
					return
		BWindow.MessageReceived(self, msg)

	def QuitRequested(self):
		global faas
		if faas:
			confile=os.path.join(sys.path[0],'config.ini')
			cfgfile = open(confile,'w')
			try:
				Config.add_section('Size')
				Config.write(cfgfile)
			except:
				pass
			Config.set('Size','horizon', self.hsliz.Position())
			Config.set('Size','vertic', self.vsliz.Position())
			Config.write(cfgfile)
			cfgfile.close()
			BApplication.be_app.PostMessage(B_QUIT_REQUESTED)
			print "So long and thanks for all the fish"
			self.r.cancel()
			return 1
		else:
			BApplication.be_app.WindowAt(0).PostMessage(B_QUIT_REQUESTED)
			time.sleep(0.1)
			return 0


class NuzRiderApplication(BApplication.BApplication):

	def __init__(self):
		BApplication.BApplication.__init__(self, "application/x-vnd.Haiku-Feed-Aggregator")

	def ReadyToRun(self):
		window((100,80,800,600))

	def QuitRequested(self):
		return 1
		



def window(rectangle):
	global faas
	faas=True
	window = NuzWindow(rectangle)
	window.Show()

NuzRider = NuzRiderApplication()
NuzRider.Run()
