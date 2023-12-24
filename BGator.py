from Be import BApplication, BWindow, BView, BMenu,BMenuBar, BMenuItem, BSeparatorItem, BMessage, window_type, B_NOT_RESIZABLE, B_QUIT_ON_WINDOW_CLOSE
from Be import BButton, BTextView, BTextControl, BAlert, BListItem, BListView, BScrollView, BRect, BBox, BFont, InterfaceDefs, BPath, BDirectory, BEntry
from Be import BNode, BStringItem, BFile, BPoint, BLooper, BHandler, BTextControl, TypeConstants, BScrollBar, BStatusBar, BStringView
from Be.GraphicsDefs import *
from Be.Menu import menu_info,get_menu_info
from Be.FindDirectory import *
from Be.View import B_FOLLOW_NONE,set_font_mask
from Be.Alert import alert_type
from Be.InterfaceDefs import border_style,orientation
from Be.ListView import list_view_type
from Be.AppDefs import *
from Be.Font import be_plain_font, be_bold_font
from Be import AppDefs
#from Be.fs_attr import attr_info

from Be import Entry
from Be.Entry import entry_ref, get_ref_for_path

import configparser,re,webbrowser, feedparser, struct, datetime
from threading import Thread

Config=configparser.ConfigParser()
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

def openlink(link):
	global tab,name
	webbrowser.get(name).open(link,tab,False)


def attr(node):
	al = []
	while 1:
		an = node.GetNextAttrName()
		#print("Risultato di GetNextAttrName",an[1],"valore",an[0])
		if not an[1]:
			a = an[0]
		else:
			a = None
		if a is None:
			node.RewindAttrs()
			break
		else:
			pnfo = node.GetAttrInfo(a)
			if not pnfo[1]:
				nfo = pnfo[0]#node.GetAttrInfo(a)[0]
			type_string = get_type_string(nfo.type)
			#print(nfo.size)
			ritorno=node.ReadAttr(a, nfo.type, 0, None,nfo.size)
			#print("Ritorno",ritorno)
			#print("Attr_name:",a,"Type:",type_string,"Size:", nfo.size,"Value:",node.ReadAttr(a, nfo.type, 0, None,nfo.size))
			al.append((a,("Type:",type_string,"Size:",nfo.size),node.ReadAttr(a, nfo.type, 0, None,nfo.size)))
			#node.RemoveAttr("Media:Width") <- works
	return al

def get_type_string(value):
	#type_string = ''.join([chr((value >> (8*i)) & 0xFF) for i in range(4)]) #<--- this works better if the binary representation of the integer contains bytes that are not valid for UTF-8 encoding
	type_string = struct.pack('>I', value).decode('utf-8')
	return type_string


class NewsItem(BListItem):
	def __init__(self, title, entry, link, unread,consist):
		self.name=title
		self.consistent=consist
		self.entry = entry
		self.link = link
		self.unread = unread
		fon=BFont()
		self.font_height_value=font_height()
		fon.GetHeight(self.font_height_value)
		BListItem.__init__(self)
		
	def DrawItem(self, owner, frame, complete):
		if self.IsSelected() or complete:
			owner.SetHighColor(200,200,200,255)
			owner.SetLowColor(200,200,200,255)
			owner.FillRect(frame)
		owner.SetHighColor(0,0,0,0)
		owner.MovePenTo(5,frame.bottom-self.font_height_value.descent)#frame.bottom-5)
		if self.unread:
			owner.SetFont(be_bold_font)
		else:
			owner.SetFont(be_plain_font)
		owner.DrawString(self.name,None)
		if not self.consistent:
			sp=BPoint(3,frame.bottom-((frame.bottom-frame.top)/2))
			ep=BPoint(frame.right-3,frame.bottom-(frame.bottom-frame.top)/2)
			owner.StrokeLine(sp,ep)
		owner.SetLowColor(255,255,255,255)

		

from Be.Font import font_height

class PaperItem(BListItem):
	nocolor = (0, 0, 0, 0)

	def __init__(self, path,address):
		self.name = path.Leaf()
		self.path = path
		self.address = address
		self.color=self.nocolor
		self.newnews=False
		self.datapath=BDirectory(path.Path())
		self.newscount=self.datapath.CountEntries()
		fon=BFont()
		self.font_height_value=font_height()
		fon.GetHeight(self.font_height_value)
		#print(value.ascent,value.descent,value.leading,"is descending the useful value to place the string?")


		BListItem.__init__(self)
		

	def DrawItem(self, owner, frame, complete):
		self.newnews=False
		perc=BPath()
		self.newscount=self.datapath.CountEntries()
		if self.newscount > 0:
			self.datapath.Rewind()
			ret=False
			while not ret:
				evalent=BEntry()
				ret=self.datapath.GetNextEntry(evalent)
				if not ret:
					evalent.GetPath(perc)
					nf=BNode(perc.Path())
					attributes=attr(nf)
					for element in attributes:
						if element[0] == "Unread":
							unr=element[2][0]
							if unr:
								ret=True
								self.newnews=True
								break
		if self.IsSelected() or complete:
			#color = (200,200,200,255)
			if self.newnews == True:
				owner.SetHighColor(250,80,80,255)
				owner.SetLowColor(200,200,200,255)
			else:
				owner.SetHighColor(250,230,0,255) # 230,230,0,255
				owner.SetLowColor(200,200,200,255)
			owner.FillRect(frame)
			owner.SetHighColor(0,0,0,255)
			owner.SetLowColor(255,255,255,255)
		owner.MovePenTo(5,frame.bottom-self.font_height_value.descent)#2
		if self.newnews:
			owner.SetFont(be_bold_font)
			owner.DrawString(self.name,None)#"▶ "+
		else:
			owner.SetFont(be_plain_font)
			owner.DrawString(self.name,None)


class NewsScrollView:
	HiWhat = 32 #Doppioclick
	NewsSelection = 102
	def __init__(self, rect, name):
		self.lv = BListView(rect, name, list_view_type.B_SINGLE_SELECTION_LIST)
		self.lv.SetSelectionMessage(BMessage(self.NewsSelection))
		self.lv.SetInvocationMessage(BMessage(self.HiWhat))
		self.sv = BScrollView(name, self.lv,B_FOLLOW_NONE,0,False,True,border_style.B_FANCY_BORDER)
		#'NewsScrollView'
	def topview(self):
		return self.sv

	def listview(self):
		return self.lv

class PapersScrollView:
	HiWhat = 33 #Doppioclick
	PaperSelection = 101

	def __init__(self, rect, name):
		self.lv = BListView(rect, name, list_view_type.B_SINGLE_SELECTION_LIST)
		self.lv.SetSelectionMessage(BMessage(self.PaperSelection))
		self.lv.SetInvocationMessage(BMessage(self.HiWhat))
		self.sv = BScrollView(name, self.lv,B_FOLLOW_NONE,0,True,True,border_style.B_FANCY_BORDER)
		#'PapersScrollView'
	def topview(self):
		return self.sv

	def listview(self):
		return self.lv
		
class AddFeedWindow(BWindow):
	def __init__(self):
		BWindow.__init__(self, BRect(150,150,500,300), "Add Feed Address", window_type.B_FLOATING_WINDOW,  B_NOT_RESIZABLE | B_QUIT_ON_WINDOW_CLOSE)#B_BORDERED_WINDOW B_FLOATING_WINDOW
		self.bckgnd = BView(self.Bounds(), "background_View", 8, 20000000)
		bckgnd_bounds=self.bckgnd.Bounds()
		self.AddChild(self.bckgnd,None)
		self.box = BBox(bckgnd_bounds,"Underbox",0x0202|0x0404,border_style.B_FANCY_BORDER)
		self.bckgnd.AddChild(self.box,None)
		a=BFont()
		wid=a.StringWidth("Feed address:")
		self.feedaddress = BTextControl(BRect(10,30,bckgnd_bounds.Width()-10,60),'TxTCtrl', "Feed address:",None,BMessage(1),0x0202|0x0404)
		self.feedaddress.SetDivider(wid+5)
		self.box.AddChild(self.feedaddress,None)
		self.cancelBtn = BButton(BRect(10,80,bckgnd_bounds.Width()/2-5,110),'GetNewsButton','Cancel',BMessage(6))
		self.addfeedBtn = BButton(BRect(bckgnd_bounds.Width()/2+5,80,bckgnd_bounds.Width()-10,110),'GetNewsButton','Add Feed',BMessage(7))
		self.box.AddChild(self.cancelBtn,None)
		self.box.AddChild(self.addfeedBtn,None)

	def MessageReceived(self, msg):
		if msg.what == 6:
			self.Hide()
		elif msg.what == 7:
			msg=BMessage(245)
			msg.AddString("feed",self.feedaddress.Text())
			be_app.WindowAt(0).PostMessage(msg)
			self.Hide()
		
		BWindow.MessageReceived(self, msg)

	def FrameResized(self,x,y):
		self.ResizeTo(350,150)
	def QuitRequested(self):
		self.Hide()
		#self.Quit()
		#return BWindow.QuitRequested(self)

class GatorWindow(BWindow):
	global tmpNitm,tmpPitm
	tmpPitm=[]
	tmpNitm=[]
	tmpWind=[]
	Menus = (
		('File', ((1, 'Add Paper'),(2, 'Remove Paper'),(None, None),(int(AppDefs.B_QUIT_REQUESTED), 'Quit'))),('News', ((6, 'Get News'),(4, 'Mark all as read'),(5, '(Clear news)'))),('(Sort)', ((40, 'By Name'),(41, 'By Unread'),(42, 'By Date'))),
		('Help', ((8, 'Help'),(3, 'About')))
		)
	def __init__(self):
		global tab,name
		BWindow.__init__(self, BRect(50,100,1024,750), "BGator is back", window_type.B_TITLED_WINDOW,  B_NOT_RESIZABLE | B_QUIT_ON_WINDOW_CLOSE)#B_MODAL_WINDOW
		bounds=self.Bounds()
		self.bckgnd = BView(self.Bounds(), "background_View", 8, 20000000)
		bckgnd_bounds=self.bckgnd.Bounds()
		self.AddChild(self.bckgnd,None)
		self.bar = BMenuBar(bckgnd_bounds, 'Bar')
		x, barheight = self.bar.GetPreferredSize()
		self.box = BBox(BRect(0,barheight,bckgnd_bounds.Width(),bckgnd_bounds.Height()),"Underbox",0x0202|0x0404,border_style.B_FANCY_BORDER)
		
		perc=BPath()
		find_directory(directory_which.B_USER_NONPACKAGED_DATA_DIRECTORY,perc,False,None)
		perc.Path()
		datapath=BDirectory(perc.Path()+"/BGator2")
		ent=BEntry(datapath,perc.Path()+"/BGator2")
		if not ent.Exists():
			datapath.CreateDirectory(perc.Path()+"/BGator2", datapath)
		ent.GetPath(perc)
		confile=BPath(perc.Path()+'/config.ini',None,False)
		ent=BEntry(confile.Path())
		if ent.Exists():
			Config.read(confile.Path())
			try:
				sort=ConfigSectionMap("General")['sort']
			except:
				print("no sezione, scrivo sort 1")
				cfgfile = open(confile.Path(),'w')
				Config.add_section('General')
				Config.set('General','sort', "1")
				sort="1"
				Config.write(cfgfile)
				cfgfile.close()
				Config.read(confile.Path())
		else:
			print("no file, scrivo sort 1")
			cfgfile = open(confile.Path(),'w')
			Config.add_section('General')
			Config.set('General','sort', "1")
			sort="1"
			Config.write(cfgfile)
			cfgfile.close()
			Config.read(confile.Path())
		for menu, items in self.Menus:
			if menu == "Sort":
				savemenu = True
			else:
				savemenu = False
			menu = BMenu(menu)
			for k, name in items:
				if k is None:
						menu.AddItem(BSeparatorItem())
				else:
						mitm=BMenuItem(name, BMessage(k),name[1],0)
						if name == "By Name" and sort == "1":
							mitm.SetMarked(True)
						elif name == "By Unread" and sort == "2":
							mitm.SetMarked(True)
						elif name == "By Date" and sort == "3":
							mitm.SetMarked(True)
						menu.AddItem(mitm)
			if savemenu:
				self.savemenu = menu
				self.bar.AddItem(menu)
			else:	
				self.bar.AddItem(menu)
		bf=BFont()
		bf.PrintToStream()
		oldSize=bf.Size()
		bf.SetSize(32)
		#self.box.SetFont(bf)
		self.addBtn = BButton(BRect(8,8,58,48),'AddButton','⊕',BMessage(1))
		self.addBtn.SetFont(bf)
		self.box.AddChild(self.addBtn,None)
		self.remBtn = BButton(BRect(62,8,112,48),'RemoveButton','⊖',BMessage(2))
		self.remBtn.SetFont(bf)
		self.box.AddChild(self.remBtn,None)
		boxboundsw=self.box.Bounds().Width()
		boxboundsh=self.box.Bounds().Height()
		self.getBtn = BButton(BRect(116,8,boxboundsw / 3,48),'GetNewsButton','⇩',BMessage(6))
		self.getBtn.SetFont(bf)
		self.progress = BStatusBar(BRect(boxboundsw / 3+6,8, boxboundsw - 12, 48),'progress',None, None)
		#self.progress.SetMaxValue(self.list.lv.CountItems())#-2.0)
		self.infostring= BStringView(BRect(boxboundsw/3+6,8,boxboundsw-12,28),"info","")
		self.box.AddChild(self.progress,None)
		self.box.AddChild(self.infostring,None)
		self.box.AddChild(self.getBtn,None)
		#bf.SetSize(oldSize)
		self.box.SetFont(bf)
		self.Paperlist = PapersScrollView(BRect(8 , 56, boxboundsw / 3 -20, boxboundsh - 28 ), 'NewsPapersScrollView')
		self.box.AddChild(self.Paperlist.topview(), None)
		self.NewsList = NewsScrollView(BRect(8 + boxboundsw / 3 , 56, boxboundsw -28 , boxboundsh / 1.8 ), 'NewsListScrollView')
		self.box.AddChild(self.NewsList.sv,None)
		PSframe=self.Paperlist.sv.Frame()
		txtRect=BRect(8 + boxboundsw / 3, boxboundsh / 1.8 + 8,boxboundsw -8,boxboundsh - 38)
		self.outbox_preview=BBox(txtRect,"previewframe",0x0202|0x0404,border_style.B_FANCY_BORDER)
		self.box.AddChild(self.outbox_preview,None)
		innerRect= BRect(8,8,txtRect.Width()-30,txtRect.Height())
		self.NewsPreView = BTextView(BRect(2,2, self.outbox_preview.Bounds().Width()-20,self.outbox_preview.Bounds().Height()-2), 'NewsTxTView', innerRect , B_FOLLOW_NONE,2000000)
		self.NewsPreView.MakeEditable(False)
		NewsPreView_bounds=self.outbox_preview.Bounds()
		self.scroller=BScrollBar(BRect(NewsPreView_bounds.right-21,NewsPreView_bounds.top+1.2,NewsPreView_bounds.right-1.4,NewsPreView_bounds.bottom-1.6),'NewsPreView_ScrollBar',self.NewsPreView,0.0,0.0,orientation.B_VERTICAL)
		self.outbox_preview.AddChild(self.scroller,None)
		perc=BPath()
		find_directory(directory_which.B_USER_NONPACKAGED_DATA_DIRECTORY,perc,False,None)
		perc.Path()
		datapath=BDirectory(perc.Path()+"/BGator2")
		ent=BEntry(datapath,perc.Path()+"/BGator2")
		#if not ent.Exists():
		#	datapath.CreateDirectory(perc.Path()+"/BGator2", datapath)
		ent.GetPath(perc)
		confile=BPath(perc.Path()+'/config.ini',None,False)
		ent=BEntry(confile.Path())
		if ent.Exists():
			Config.read(confile.Path())
			try:
				path=ConfigSectionMap("Browser")['path']
				name=ConfigSectionMap("Browser")['name']
				type=ConfigSectionMap("Browser")['type']
				buleano=ConfigSectionMap("Browser")['newtab']
				if buleano:
					tab=2
				else:
					tab=1
				tmpent=BEntry(path,False)
				if tmpent.Exists():
					if type=='Generic':
						webbrowser.register(name,None,webbrowser.GenericBrowser(path))
					elif type=='Mozilla':
						webbrowser.register(name,None,webbrowser.Mozilla(path))
					elif type=='Konqueror':
						webbrowser.register(name,None,webbrowser.Konqueror(path)) # no pass path
					elif type=='Opera':
						webbrowser.register(name,None,webbrowser.Opera(path)) # no pass path
			except:
				find_directory(directory_which.B_SYSTEM_APPS_DIRECTORY,perc,False,None)
				ent=BEntry(perc.Path()+"/WebPositive")
				if ent.Exists():
					cfgfile = open(confile.Path(),'w')
					Config.add_section('Browser')
					Config.set('Browser','path', perc.Path()+"/WebPositive")
					Config.set('Browser','name', "WebPositive")
					Config.set('Browser','type', "Generic")
					Config.set('Browser','newtab', "True")
					name="WebPositive"
					tab=2
					Config.write(cfgfile)
					cfgfile.close()
					Config.read(confile.Path())
					webbrowser.register( "WebPositive",None,webbrowser.GenericBrowser(perc.Path()+"/WebPositive"))
		else:
			find_directory(directory_which.B_SYSTEM_APPS_DIRECTORY,perc,False,None)
			ent=BEntry(perc.Path()+"/WebPositive")
			if ent.Exists():
				cfgfile = open(confile.Path(),'w')
				Config.add_section('Browser')
				Config.set('Browser','path', perc.Path()+"/WebPositive")
				Config.set('Browser','name', "WebPositive")
				Config.set('Browser','type', "Generic")
				Config.set('Browser','newtab', "True")
				name="WebPositive"
				tab=2
				Config.write(cfgfile)
				cfgfile.close()
				Config.read(confile.Path())
				webbrowser.register( "WebPositive",None,webbrowser.GenericBrowser(perc.Path()+"/WebPositive"))
		#fon=BFont()
		#sameProperties=0
		#colore=rgb_color()
		#sameColor=True
		#self.NewsTextView.GetFontAndColor(fon,sameProperties,colore,sameColor)
		#print("Rosso:",colore.red,"Verde:",colore.green,"Blu:",colore.blue,"Alfa:",colore.alpha)
		#colore.set_to(255,255,255,255)
		#print("Rosso:",colore.red,"Verde:",colore.green,"Blu:",colore.blue,"Alfa:",colore.alpha)
		#self.NewsTextView.SetFontAndColor(fon,set_font_mask.B_FONT_ALL, colore)
		
		btnswidth=round((boxboundsw - 8 - (8 + boxboundsw / 3) -8 - 8)/3,2)
		markBounds=BRect(round(8 + boxboundsw / 3, 2),round(boxboundsh - 36, 2),round(8 + boxboundsw / 3 + btnswidth, 2) ,round(boxboundsh - 8,2))
		self.markUnreadBtn = BButton(markBounds,'markUnreadButton','Mark as Unread',BMessage(9))
		self.openBtn = BButton(BRect(round(boxboundsw-8-btnswidth, 2),round( boxboundsh - 36, 2),round(boxboundsw-8, 2),round(boxboundsh-8, 2)),'openButton','Open with browser',BMessage(self.NewsList.HiWhat))
		self.markReadBtn = BButton(BRect(round(8 + boxboundsw / 3 + btnswidth + 8, 2),round( boxboundsh - 36, 2),round(boxboundsw-16-btnswidth, 2),round(boxboundsh-8, 2)),'markReadButton','Mark as Read',BMessage(10))
		self.outbox_preview.AddChild(self.NewsPreView,None)
		self.box.AddChild(self.markUnreadBtn,None)
		markUnreadBtn_bounds=self.markUnreadBtn.Frame()
		if markUnreadBtn_bounds != markBounds:
			hdelta=markUnreadBtn_bounds.Height()-markBounds.Height()
			self.markUnreadBtn.MoveBy(0.0,-hdelta)
			self.openBtn.MoveBy(0.0,-hdelta)
			self.markReadBtn.MoveBy(0.0,-hdelta)
			self.NewsPreView.ResizeBy(0.0,-hdelta)
			self.scroller.ResizeBy(0.0,-hdelta)
			self.outbox_preview.ResizeBy(0.0,-hdelta)
		self.box.AddChild(self.openBtn,None)
		self.box.AddChild(self.markReadBtn,None)

		self.bckgnd.AddChild(self.bar, None)
		self.bckgnd.AddChild(self.box, None)
		
		self.UpdatePapers()
		
	def ClearNewsList(self):
			self.NewsList.lv.DeselectAll()
			self.NewsList.lv.MakeEmpty()
			if len(tmpNitm)>0:
				for item in tmpNitm:
					del item
				tmpNitm.clear()

	def ClearPaperlist(self):
		if self.Paperlist.lv.CountItems()>0:
			self.Paperlist.lv.DeselectAll()
			i=0
			while i>self.Paperlist.lv.CountItems():
				self.Paperlist.lv.RemoveItem(i)
			self.NewsList.lv.MakeEmpty()
			if len(tmpPitm)>0:
				for item in tmpPitm:
					del item
				tmpPitm.clear()

	def UpdatePapers(self):
		self.ClearPaperlist()
		
		perc=BPath()
		find_directory(directory_which.B_USER_NONPACKAGED_DATA_DIRECTORY,perc,False,None)
		perc.Path()
		datapath=BDirectory(perc.Path()+"/BGator2/Papers")
		ent=BEntry(datapath,perc.Path()+"/BGator2/Papers")
		if not ent.Exists():
			datapath.CreateDirectory(perc.Path()+"/BGator2/Papers", datapath)
		ent.GetPath(perc)
		if datapath.CountEntries() > 0:
			datapath.Rewind()
			ret=False
			while not ret:
				evalent=BEntry()
				ret=datapath.GetNextEntry(evalent)
				if not ret:
					porc=BPath()
					evalent.GetPath(porc)
					self.PaperItemConstructor(porc)
					
					
	def PaperItemConstructor(self, perc):
		nf=BNode(perc.Path())
		attributes=attr(nf)
		for element in attributes:
			if element[0] == "address":
				tmpPitm.append(PaperItem(perc,element[2][0]))
				self.Paperlist.lv.AddItem(tmpPitm[-1])

	def gjornaaltolet(self):
			self.NewsPreView.SetText("",None)
			self.NewsList.lv.DeselectAll()
			self.NewsList.lv.RemoveItems(0,self.NewsList.lv.CountItems()) #azzera newslist
			self.NewsList.lv.ScrollToSelection()
			#### check sort type
			marked=self.savemenu.FindMarked().Label()
			
			curpaper=self.Paperlist.lv.ItemAt(self.Paperlist.lv.CurrentSelection())
			x=curpaper.datapath.CountEntries()
			if x>0:
				curpaper.datapath.Rewind()
				rit = False
				while not rit:
					itmEntry=BEntry()
					rit=curpaper.datapath.GetNextEntry(itmEntry)
					if not rit:
						if marked == "By Name":
							self.NewsItemConstructor(itmEntry)
						if marked == "By Unread": #TODO
							self.NewsItemConstructor(itmEntry)
						if marked == "By Date": #TODO
							self.NewsItemConstructor(itmEntry)

	def NewsItemConstructor(self,entry):
		nf = BNode(entry)
		attributes = attr(nf)
		addnews = False
		blink = False
		bunread = False
		btitle = False
		for element in attributes:
			if element[0] == "link":
					link = element[2][0]
					blink = True
			if element[0] == "Unread":
					unread = element[2][0]
					bunread = True
			if element[0] == "title":
					title = element[2][0]
					btitle = True

		try:
			type(link)
			type(unread)
			type(title)
			
			addnews=True
		except:
			print("unconsistent news")
			
		
		if addnews:
			consist=True
			tmpNitm.append(NewsItem(title,entry,link,unread,consist))
			self.NewsList.lv.AddItem(tmpNitm[-1])
		else:
			consist=False
			if not blink:
				link = ""
			if not bunread:
				unread = False
			if not btitle:
				if link == "":
					title = "No Title and no link"
				else:
					title = link
			tmpNitm.append(NewsItem(title,entry,link,unread,consist))
			self.NewsList.lv.AddItem(tmpNitm[-1])
			
	def MessageReceived(self, msg):
		if msg.what == 8:
			ask = BAlert('Whoa!', 'Are you sure you need help?', 'Yes','No', None, InterfaceDefs.B_WIDTH_AS_USUAL, alert_type.B_IDEA_ALERT)
			answ=ask.Go()
			if answ==0:
				risp = BAlert('lol', 'Well there\'s no help manual here', 'Bummer', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_INFO_ALERT)
				risp.Go()
			else:
				risp = BAlert('lol', 'If you think so...', 'Poor me', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_WARNING_ALERT)
				risp.Go()
		elif msg.what == 3:
			about = BAlert('awin', 'BGator v. 1.9.0 alpha preview by TmTFx', 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_INFO_ALERT)
			about.Go()
		elif msg.what == 2:
			#remove feed and relative files and dir
			cursel=self.Paperlist.lv.CurrentSelection()
			if cursel>-1:
				self.Paperlist.lv.Select(-1)
				dirname=self.Paperlist.lv.ItemAt(cursel).path.Path()
				datapath = BDirectory(dirname)
				if datapath.CountEntries() > 0:
					datapath.Rewind()
					ret=False
					while not ret:
						evalent=BEntry()
						ret=datapath.GetNextEntry(evalent)
						if not ret:
							ret_status=evalent.Remove()
				if datapath.CountEntries() == 0:
					ent=BEntry(dirname)
					ent.Remove()
				x=len(tmpPitm)
				i=0
				remarray=False
				while i<x:
					if tmpPitm[i].path.Path() == dirname:
						remarray=True
						break
					i+=1
				self.Paperlist.lv.RemoveItem(cursel)
				if remarray:
					del tmpPitm[i]
		
		elif msg.what == 40:
			#TODO snellire Sort By Name
			perc=BPath()
			find_directory(directory_which.B_USER_NONPACKAGED_DATA_DIRECTORY,perc,False,None)
			datapath=BDirectory(perc.Path()+"/BGator2")
			ent=BEntry(datapath,perc.Path()+"/BGator2")
			if not ent.Exists():
				datapath.CreateDirectory(perc.Path()+"/BGator2", datapath)
			ent.GetPath(perc)
			confile=BPath(perc.Path()+'/config.ini',None,False)
			ent=BEntry(confile.Path())
			if ent.Exists():
				cfgfile = open(confile.Path(),'w')
				Config.set('General','sort', "1")
				Config.write(cfgfile)
				cfgfile.close()
				Config.read(confile.Path())
			menuitm=self.savemenu.FindItem(40)
			menuitm.SetMarked(1)
			menuitm=self.savemenu.FindItem(41)
			menuitm.SetMarked(0)
			menuitm=self.savemenu.FindItem(42)
			menuitm.SetMarked(0)
		elif msg.what == 41:
			#TODO snellire Sort By Unread
			perc=BPath()
			find_directory(directory_which.B_USER_NONPACKAGED_DATA_DIRECTORY,perc,False,None)
			datapath=BDirectory(perc.Path()+"/BGator2")
			ent=BEntry(datapath,perc.Path()+"/BGator2")
			if not ent.Exists():
				datapath.CreateDirectory(perc.Path()+"/BGator2", datapath)
			ent.GetPath(perc)
			confile=BPath(perc.Path()+'/config.ini',None,False)
			ent=BEntry(confile.Path())
			if ent.Exists():
				cfgfile = open(confile.Path(),'w')
				Config.set('General','sort', "2")
				Config.write(cfgfile)
				cfgfile.close()
				Config.read(confile.Path())
			menuitm=self.savemenu.FindItem(40)
			menuitm.SetMarked(0)
			menuitm=self.savemenu.FindItem(41)
			menuitm.SetMarked(1)
			menuitm=self.savemenu.FindItem(42)
			menuitm.SetMarked(0)
		elif msg.what == 42:
			#TODO snellire Sort By Date
			perc=BPath()
			find_directory(directory_which.B_USER_NONPACKAGED_DATA_DIRECTORY,perc,False,None)
			datapath=BDirectory(perc.Path()+"/BGator2")
			ent=BEntry(datapath,perc.Path()+"/BGator2")
			if not ent.Exists():
				datapath.CreateDirectory(perc.Path()+"/BGator2", datapath)
			ent.GetPath(perc)
			confile=BPath(perc.Path()+'/config.ini',None,False)
			ent=BEntry(confile.Path())
			if ent.Exists():
				cfgfile = open(confile.Path(),'w')
				Config.set('General','sort', "3")
				Config.write(cfgfile)
				cfgfile.close()
				Config.read(confile.Path())
			menuitm=self.savemenu.FindItem(40)
			menuitm.SetMarked(0)
			menuitm=self.savemenu.FindItem(41)
			menuitm.SetMarked(0)
			menuitm=self.savemenu.FindItem(42)
			menuitm.SetMarked(1)
		elif msg.what == self.Paperlist.PaperSelection:
			#Paper selection
			self.NewsList.lv.MakeEmpty()
			self.NewsPreView.SelectAll()
			self.NewsPreView.Clear()
			if len(tmpNitm)>0:
				for item in tmpNitm:
					del item
				tmpNitm.clear()
			if self.Paperlist.lv.CurrentSelection()>-1:
				self.gjornaaltolet()

		elif msg.what == self.NewsList.NewsSelection:
			#News selection
			curit = self.NewsList.lv.CurrentSelection()
			if curit>-1:
				Nitm = self.NewsList.lv.ItemAt(curit)
				if Nitm.unread:
					Nitm.unread=False
					msg=BMessage(83)
					pth=BPath()
					Nitm.entry.GetPath(pth)
					msg.AddString("path",pth.Path())
					msg.AddBool("unreadValue",False)
					msg.AddInt32("selected",curit)
					msg.AddInt32("selectedP",self.Paperlist.lv.CurrentSelection())
					be_app.WindowAt(0).PostMessage(msg)
				NFile=BFile(Nitm.entry,0)
				r,s=NFile.GetSize()
				if not r:
					self.NewsPreView.SetText(NFile,0,s,None)
				else:
					self.NewsPreView.SetText("There\'s no preview here",None)
			else:
				#self.NewsPreView.Delete()
				self.NewsPreView.SelectAll()
				self.NewsPreView.Clear()

		elif msg.what == 4:
			if self.NewsList.lv.CountItems()>0:
				for item in self.NewsList.lv.Items():
					item.unread = False
					msg=BMessage(83)
					pth=BPath()
					item.entry.GetPath(pth)
					msg.AddString("path",pth.Path())
					msg.AddBool("unreadValue",False)
					msg.AddInt32("selected",self.NewsList.lv.IndexOf(item))
					msg.AddInt32("selectedP",self.Paperlist.lv.CurrentSelection())
					be_app.WindowAt(0).PostMessage(msg)

		elif msg.what == 9:
			#mark unread btn
			curit = self.NewsList.lv.CurrentSelection()
			if curit>-1:
				Nitm = self.NewsList.lv.ItemAt(curit)
				if not Nitm.unread:
					Nitm.unread = True
					msg=BMessage(83)
					pth=BPath()
					Nitm.entry.GetPath(pth)
					msg.AddString("path",pth.Path())
					msg.AddBool("unreadValue",True)
					msg.AddInt32("selected",curit)
					msg.AddInt32("selectedP",self.Paperlist.lv.CurrentSelection())
					be_app.WindowAt(0).PostMessage(msg)

		elif msg.what == 10:
			#mark read btn
			curit = self.NewsList.lv.CurrentSelection()
			if curit>-1:
				Nitm = self.NewsList.lv.ItemAt(curit)
				if Nitm.unread:
					Nitm.unread = True
					msg=BMessage(83)
					pth=BPath()
					Nitm.entry.GetPath(pth)
					msg.AddString("path",pth.Path())
					msg.AddBool("unreadValue",False)
					msg.AddInt32("selected",curit)
					msg.AddInt32("selectedP",self.Paperlist.lv.CurrentSelection())
					be_app.WindowAt(0).PostMessage(msg)

		elif msg.what == 83: # Mark Read/unread
			e = msg.FindString("path")
			unrVal = msg.FindBool("unreadValue")
			nd=BNode(e)
			ninfo,ret=nd.GetAttrInfo("Unread")
			if not ret:
				if unrVal:
					givevalue=bytearray(b'\x01')
				else:
					givevalue=bytearray(b'\x00')
				nd.WriteAttr("Unread",ninfo.type,0,givevalue)
				itto=self.NewsList.lv.ItemAt(msg.FindInt32("selected"))
				itto.DrawItem(self.NewsList.lv,self.NewsList.lv.ItemFrame(msg.FindInt32("selected")),True)
				
				itto=self.Paperlist.lv.ItemAt(msg.FindInt32("selectedP"))
				itto.DrawItem(self.Paperlist.lv,self.Paperlist.lv.ItemFrame(msg.FindInt32("selectedP")),False)
			self.NewsList.lv.Hide()
			self.NewsList.lv.Show()

		elif msg.what == self.NewsList.HiWhat:
			#open link
			curit=self.NewsList.lv.CurrentSelection()
			if curit>-1:
				itto=self.NewsList.lv.ItemAt(curit)
				if itto.link != "":
					t = Thread(target=openlink,args=(itto.link,))
					t.run()
			
		elif msg.what == self.Paperlist.HiWhat: #TODO
			curit=self.Paperlist.lv.CurrentSelection()
			if curit>-1:
				ittp=self.Paperlist.lv.ItemAt(curit)
				print(ittp.address)
			print("window with details and eventually per paper settings or open tracker at its path") #like pulse specified update 
		
		elif msg.what == 1:
			#open add feed window
			self.tmpWind.append(AddFeedWindow())
			self.tmpWind[-1].Show()

		elif msg.what == 245:
			# ADD FEED
			#be_app.WindowAt(0).PostMessage(BMessage(1992))
			feedaddr=msg.FindString("feed")
			#TODO: externalize on a "def" and threadize this, Show() progress on a BStringView and on a BStatusBar then Hide() them
			d=feedparser.parse(feedaddr)
			if d.feed.has_key('title'):
				dirname=d.feed.title
				perc=BPath()
				find_directory(directory_which.B_USER_NONPACKAGED_DATA_DIRECTORY,perc,False,None)
				folder=perc.Path()+"/BGator2/Papers/"+dirname
				datapath=BDirectory(folder)
				entr=BEntry(folder)
				if entr.Exists():
					saytxt="The folder "+folder+" is present, please remove it and add the feed again"
					about = BAlert('Ops', saytxt, 'Ok', None,None,InterfaceDefs.B_WIDTH_AS_USUAL,alert_type.B_WARNING_ALERT)
					about.Go()
				else:
					datapath.CreateDirectory(perc.Path()+"/BGator2/Papers/"+dirname,datapath)
					del perc
					nd=BNode(entr)
					givevalue=feedaddr.encode('utf-8')#bytes(feedaddr,'utf-8')
					nd.WriteAttr("address",TypeConstants.B_STRING_TYPE,0,givevalue)
					attributes=attr(nd)
					pirc=BPath()
					entr.GetPath(pirc)
					for element in attributes:
						if element[0] == "address":
							tmpPitm.append(PaperItem(pirc,element[2][0]))
							self.Paperlist.lv.AddItem(tmpPitm[-1])
							be_app.WindowAt(0).PostMessage(6)
				#controlla se esiste cartella chiamata titul&
				#se esiste ma gli attributi non corrispondono, chiedere cosa fare
				#se esiste ma non ha tutti gli attributi scrivili
				
		elif msg.what == 6:
			#be_app.WindowAt(0).PostMessage(BMessage(1992))
			self.infostring.SetText("Updating news, please wait...")
			self.progress.SetMaxValue(self.Paperlist.lv.CountItems()*100+self.Paperlist.lv.CountItems())
			#parallel=[]
			#Download Papers News, and eventually update NewsList.lv
			for item in self.Paperlist.lv.Items():
				Thread(target=self.DownloadNews,args=(item,)).start()

				#item.DrawItem(self.Paperlist.lv,self.Paperlist.lv.ItemFrame(self.Paperlist.lv.IndexOf(item)),False)
			self.Paperlist.lv.Hide()
			self.Paperlist.lv.Show()

		elif msg.what == 542:
			# eventually remove this
			#self.UpdatePapers()
			self.Paperlist.lv.Hide()
			self.Paperlist.lv.Show()
		elif msg.what == 1990:
			d = msg.FindFloat("delta")
			self.progress.Update(d,None,None)
		elif msg.what == 1991:
			self.progress.Reset(None,None)
			emptystring = ""
			self.infostring.SetText(emptystring)
		#elif msg.what == 1992:
		#	self.progress.Reset(None,None)
		#	self.progress.Show()
		#	self.infostring.Show()
			
		BWindow.MessageReceived(self, msg)

	def remove_html_tags(self,data):
		p = re.compile(r'<.*?>')
		return p.sub('', data)
		
	def DownloadNews(self,item):
				# TODO inserire un lock per non sballare i valori di progress
				#self.progress.Reset(None,None)
				perc=BPath()
				find_directory(directory_which.B_USER_NONPACKAGED_DATA_DIRECTORY,perc,False,None)
				dirpath=BPath(perc.Path()+"/BGator2/Papers/"+item.name,None,False)
				datapath=BDirectory(dirpath.Path())
				stringa=item.address.encode('utf-8')
				rss = feedparser.parse(stringa.decode('utf-8'))
				valueperentry=100/(len(rss.entries)+1)
				mxg=BMessage(1990)
				mxg.AddFloat("delta",valueperentry)
				be_app.WindowAt(0).PostMessage(mxg)
				del stringa
				y=len(rss['entries'])
				for x in range (y):
					filename=rss.entries[x].title
					newfile=BFile()
					if datapath.CreateFile(dirpath.Path()+"/"+filename,newfile,True):
						pass
					else:
						nd=BNode(dirpath.Path()+"/"+filename)
						try:
							givevalue=bytes(rss.entries[x].title,'utf-8')
						except:
							givevalue=bytes("No title",'utf-8')
						finally:
							nd.WriteAttr("title",TypeConstants.B_STRING_TYPE,0,givevalue)
						try:
							givevalue=bytes(rss.entries[x].link,'utf-8')
						except:
							givevalue=bytes("no link",'utf-8')
						else:
							nd.WriteAttr("link",TypeConstants.B_STRING_TYPE,0,givevalue)
						givevalue=bytearray(b'\x01')
						nd.WriteAttr("Unread",TypeConstants.B_BOOL_TYPE,0,givevalue)
						try:
							givevalue=bytes(rss.entries[x].author,'utf-8')
						except:
							givevalue=bytes("No author",'utf-8')
						finally:
							nd.WriteAttr("author",TypeConstants.B_STRING_TYPE,0,givevalue)
						try:
							published = rss.entries[x].published_parsed
						except:
							published = None
						else:
						#if published != None:
							#print(published)# TODO There's a difference of 1 hour between time parsed from feedrss and what is written and read in the filesystem attribute
							################## does this means I didn't care of timezone? or something else? legal hour?
							asd=datetime.datetime(published.tm_year,published.tm_mon,published.tm_mday,published.tm_hour,published.tm_min,published.tm_sec)
							#print(rss.entries[x].title,asd)
							asd_sec = round((asd - datetime.datetime(1970, 1, 1,0,0,0)).total_seconds()) 
							pass_time = struct.pack('q',asd_sec)
							nd.WriteAttr("published",TypeConstants.B_TIME_TYPE,0,pass_time)
#							try:
#									rssdate=rss.entries[x].date
#									date,timeall= rssdate.split('T')
#									time,all= timeall.split('+')
#									zornade=(date+' '+time)
#							except:
#									now=datetime.datetime.now()
#									zornade=(str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second))
						try:
							texttowrite=bytes(self.remove_html_tags(rss.entries[x].summary_detail.value),'utf-8')
						except:
							Texttowrite=bytes("No summary available",'utf-8')
						finally:
							newfile.Write(texttowrite)
					be_app.WindowAt(0).PostMessage(mxg)
				be_app.WindowAt(0).PostMessage(542)
				be_app.WindowAt(0).PostMessage(1991)
				
	
	def FrameResized(self,x,y):
		#self.ResizeToPreferred()
		self.ResizeTo(974,650)


	def QuitRequested(self):
		wnum = be_app.CountWindows()
		if wnum>1:
			for wind in self.tmpWind:
				wind.Lock()
				wind.Quit()
		return BWindow.QuitRequested(self)
		
class App(BApplication):
    def __init__(self):
        BApplication.__init__(self, "application/x-python-BGator2")
    def ReadyToRun(self):
        self.window = GatorWindow()
        self.window.Show()

def main():
    global be_app
    be_app = App()
    be_app.Run()
 
if __name__ == "__main__":
    main()
