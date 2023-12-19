from Be import BApplication, BWindow, BView, BMenu,BMenuBar, BMenuItem, BSeparatorItem, BMessage, window_type, B_NOT_RESIZABLE, B_QUIT_ON_WINDOW_CLOSE
from Be import BButton, BTextView, BTextControl, BAlert, BListItem, BListView, BScrollView, BRect, BBox, BFont, InterfaceDefs, BPath, BDirectory, BEntry
from Be import BNode, BStringItem, BFile
from Be.GraphicsDefs import *
from Be.FindDirectory import *
from Be.View import B_FOLLOW_NONE,set_font_mask
from Be.Alert import alert_type
from Be.InterfaceDefs import border_style
from Be.ListView import list_view_type
from Be.AppDefs import *
from Be.Font import be_plain_font, be_bold_font
from Be import AppDefs
#from Be.fs_attr import attr_info

from Be import Entry
from Be.Entry import entry_ref, get_ref_for_path

import configparser,webbrowser, feedparser, struct

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
				nfo = node.GetAttrInfo(a)[0]	
			type_string = get_type_string(nfo.type)
			#print("Attr_name:",a,"Type:",type_string,"Size:", nfo.size,"Value:",node.ReadAttr(a, nfo.type, 0, None,nfo.size))
			al.append((a,("Type:",type_string,"Size:",nfo.size),node.ReadAttr(a, nfo.type, 0, None,nfo.size)))
			#node.RemoveAttr("Media:Width") <- works
	return al

def get_type_string(value):
	#type_string = ''.join([chr((value >> (8*i)) & 0xFF) for i in range(4)]) #<--- this works better if the binary representation of the integer contains bytes that are not valid for UTF-8 encoding
	type_string = struct.pack('>I', value).decode('utf-8')
	return type_string


class NewsItem(BListItem):
	def __init__(self, title, entry, link, unread):
		self.name=title
		print(title)
		self.entry = entry
		self.link = link
		self.unread = unread
		BListItem.__init__(self)
		
	def DrawItem(self, owner, frame, complete):
		if self.IsSelected() or complete:
			owner.SetHighColor(200,200,200,255)
			owner.SetLowColor(200,200,200,255)
			owner.FillRect(frame)
		owner.SetHighColor(0,0,0,0)
		#if self.color == (200,0,0,0):
		#	self.font = be_bold_font
		#	owner.SetFont(self.font)
		#else:	
		#	self.font = be_plain_font
		#	owner.SetFont(self.font)
		owner.MovePenTo(5,frame.Height()-5)
		if self.unread:
			owner.SetFont(be_bold_font)
		else:
			owner.SetFont(be_plain_font)
		owner.DrawString(self.name,None)
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
		print(fon.Size())
		value=font_height()
		fon.GetHeight(value)
		print(value.ascent,value.descent,value.leading,"is descending the useful value to place the string?")
		perc=BPath()
		if self.newscount > 0:
#			print("num entries:",datapath.CountEntries())
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

		BListItem.__init__(self)
		

	def DrawItem(self, owner, frame, complete):
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
			#self.color=self.nocolor
		#owner.SetHighColor(self.color)
		#if self.color == (200,0,0,0):
		#	self.font = be_bold_font
		#	owner.SetFont(self.font)
		#else:	
		#	self.font = be_plain_font
		#	owner.SetFont(self.font)
		#frame.PrintToStream()
		owner.MovePenTo(5,frame.Height()-5)#2
		if self.newnews:
			owner.SetFont(be_bold_font)
			owner.DrawString("▶ "+self.name,None)
		else:
			owner.SetFont(be_plain_font)
			owner.DrawString(self.name,None)


class NewsScrollView:
	HiWhat = 32 #Doppioclick
	NewsSelection = 102
	def __init__(self, rect, name):
		self.lv = BListView(rect, name, list_view_type.B_SINGLE_SELECTION_LIST)
		self.lv.SetSelectionMessage(BMessage(self.NewsSelection))
		self.sv = BScrollView(name, self.lv)#, 0x0202,0,False,False, border_style.B_FANCY_BORDER)#|0x1030
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
		self.sv = BScrollView(name, self.lv)#, 0x0202,0,False,False, border_style.B_FANCY_BORDER)#|0x1030
		#'PapersScrollView'
	def topview(self):
		return self.sv

	def listview(self):
		return self.lv


class GatorWindow(BWindow):
	Menus = (
		('File', ((1, 'Add Paper'),(2, 'Remove Paper'),(None, None),(int(AppDefs.B_QUIT_REQUESTED), 'Quit'))),('News', ((6, 'Get News'),(4, 'Mark all read'),(5, 'Clear news'))),
		('Help', ((8, 'Help'),(3, 'About')))
		)
	def __init__(self):
		global tab,name
		BWindow.__init__(self, BRect(100,100,900,750), "BGator is back", window_type.B_TITLED_WINDOW,  B_NOT_RESIZABLE | B_QUIT_ON_WINDOW_CLOSE)#B_MODAL_WINDOW
		bounds=self.Bounds()
		self.bckgnd = BView(self.Bounds(), "background_View", 8, 20000000)
		bckgnd_bounds=self.bckgnd.Bounds()
		self.AddChild(self.bckgnd,None)
		self.bar = BMenuBar(bckgnd_bounds, 'Bar')
		x, barheight = self.bar.GetPreferredSize()
		self.box = BBox(BRect(0,barheight,bckgnd_bounds.Width(),bckgnd_bounds.Height()),"Underbox",0x0202|0x0404,border_style.B_FANCY_BORDER)
		for menu, items in self.Menus:
			menu = BMenu(menu)
			for k, name in items:
				if k is None:
						menu.AddItem(BSeparatorItem())
				else:
						menu.AddItem(BMenuItem(name, BMessage(k),name[1],0))
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
		self.box.AddChild(self.getBtn,None)
		#bf.SetSize(oldSize)
		self.box.SetFont(bf)
		self.Paperlist = PapersScrollView(BRect(8 , 56, boxboundsw / 3 , boxboundsh - 8 ), 'NewsPapersScrollView')
		self.box.AddChild(self.Paperlist.topview(), None)
		self.NewsList = NewsScrollView(BRect(8 + boxboundsw / 3 , 56, boxboundsw -8 , boxboundsh / 1.8 ), 'NewsListScrollView')
		self.box.AddChild(self.NewsList.sv,None)
		txtRect=BRect(8 + boxboundsw / 3, boxboundsh / 1.8 + 8,boxboundsw -8,boxboundsh - 38)
		self.outbox_preview=BBox(txtRect,"previewframe",0x0202|0x0404,border_style.B_FANCY_BORDER)
		self.box.AddChild(self.outbox_preview,None)
		innerRect= BRect(8,8,txtRect.Width()-8,txtRect.Height())
		self.NewsPreView = BTextView(BRect(2,2, self.outbox_preview.Bounds().Width()-2,self.outbox_preview.Bounds().Height()-2), 'NewsTxTView', innerRect , B_FOLLOW_NONE,2000000)
		self.NewsPreView.MakeEditable(False)
		perc=BPath()
		find_directory(directory_which.B_USER_NONPACKAGED_DATA_DIRECTORY,perc,False,None)
		perc.Path()
		datapath=BDirectory(perc.Path()+"/BGator2")
		ent=BEntry(datapath,perc.Path()+"/BGator2")
		if not ent.Exists():
			datapath.CreateDirectory(perc.Path()+"/BGator2", datapath)
		ent.GetPath(perc)
		confile=BPath(perc.Path()+'/config.ini','',False)
		ent=BEntry(confile.Path())
		if ent.Exists():
			#print("il file esiste carico tutto")
			Config.read(confile.Path())
			path=ConfigSectionMap("Browser")['path']
			name=ConfigSectionMap("Browser")['name']
			type=ConfigSectionMap("Browser")['type']
			buleano=ConfigSectionMap("Browser")['newtab']
			if buleano:
				#print("tab is 2")
				tab=2
			else:
				#print("tab is 1")
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
		self.markUnreadBtn = BButton(BRect(round(8 + boxboundsw / 3, 2),round(boxboundsh - 36, 2),round(8 + boxboundsw / 3 + btnswidth, 2) ,round(boxboundsh - 8,2)),'markUnreadButton','Mark as Unread',BMessage(9))
		self.openBtn = BButton(BRect(round(boxboundsw-8-btnswidth, 2),round( boxboundsh - 36, 2),round(boxboundsw-8, 2),round(boxboundsh-8, 2)),'openButton','Open with browser',BMessage(1))
		self.markReadBtn = BButton(BRect(round(8 + boxboundsw / 3 + btnswidth + 8, 2),round( boxboundsh - 36, 2),round(boxboundsw-16-btnswidth, 2),round(boxboundsh-8, 2)),'markReadButton','Mark as Read',BMessage(1))
		self.outbox_preview.AddChild(self.NewsPreView,None)
		self.box.AddChild(self.markUnreadBtn,None)
		self.box.AddChild(self.openBtn,None)
		self.box.AddChild(self.markReadBtn,None)
		
		self.bckgnd.AddChild(self.bar, None)
		self.bckgnd.AddChild(self.box, None)
		
#		perc=BPath()
#		find_directory(directory_which.B_USER_NONPACKAGED_DATA_DIRECTORY,perc,False,None)
#		perc.Path()
#		datapath=BDirectory(perc.Path()+"/BGator2/Papers")
#		ent=BEntry(datapath,perc.Path()+"/BGator2/Papers")
#		if not ent.Exists():
#			datapath.CreateDirectory(perc.Path()+"/BGator2/Papers", datapath)
#		ent.GetPath(perc)
#		if datapath.CountEntries() > 0:
#			print("num entries:",datapath.CountEntries())
#			datapath.Rewind()
#			ret=False
#			while not ret:
#				evalent=BEntry()
#				ret=datapath.GetNextEntry(evalent)
#				if not ret:
#					evalent.GetPath(perc)
#					nf=BNode(perc.Path())
#					attributes=attr(nf)
#					for element in attributes:
#						if element[0] == "address":
#							
#							perc.Path()
#							dir=element[2][0]
#							global papero
#							papero=ScrollViewItem(perc,dir)
#							#self.Paperlist.lv.AddItem(BStringItem(perc.Leaf()))e
#							self.Paperlist.lv.AddItem(papero)
#					
		self.UpdatePapers()
		

		
	def UpdatePapers(self):
		if self.Paperlist.lv.CountItems()>0:
			print("azzero lista")
			self.Paperlist.lv.DeselectAll()
			i=0
			while i>self.Paperlist.lv.CountItems():
				self.Paperlist.lv.RemoveItem(i)
		
		perc=BPath()
		find_directory(directory_which.B_USER_NONPACKAGED_DATA_DIRECTORY,perc,False,None)
		perc.Path()
		datapath=BDirectory(perc.Path()+"/BGator2/Papers")
		ent=BEntry(datapath,perc.Path()+"/BGator2/Papers")
		if not ent.Exists():
			datapath.CreateDirectory(perc.Path()+"/BGator2/Papers", datapath)
		ent.GetPath(perc)
#		#print(perc.Path())
#		#datapath=BDirectory(perc.Path()+"/")
		if datapath.CountEntries() > 0:
#			print("num entries:",datapath.CountEntries())
			datapath.Rewind()
			ret=False
			while not ret:
				evalent=BEntry()
				ret=datapath.GetNextEntry(evalent)
				if not ret:
					evalent.GetPath(perc)
					self.PaperItemConstructor(perc)
					
					
	def PaperItemConstructor(self, perc):
		nf=BNode(perc.Path())
		attributes=attr(nf)
		for element in attributes:
			if element[0] == "address":
				global itm
				itm = PaperItem(perc,element[2][0])
				self.Paperlist.lv.AddItem(itm)

	def gjornaaltolet(self):
			self.NewsPreView.SetText("",None)
			self.NewsList.lv.DeselectAll()
			self.NewsList.lv.RemoveItems(0,self.NewsList.lv.CountItems()) #azzera newslist
			self.NewsList.lv.ScrollToSelection()
			
			curpaper=self.Paperlist.lv.ItemAt(self.Paperlist.lv.CurrentSelection())
			x=curpaper.datapath.CountEntries()
			if x>0:
				curpaper.datapath.Rewind()
				rit = False
				while not rit:
					itmEntry=BEntry()
					rit=curpaper.datapath.GetNextEntry(itmEntry)
					if not rit:
						self.NewsItemConstructor(itmEntry)
						print("aggiungo file")

	def NewsItemConstructor(self,entry):
	#def __init__(self, title, entry, link, unread):
		perc=BPath()
		entry.GetPath(perc)
		nf=BNode(perc.Path())
		attributes=attr(nf)
		addnews=False
		for element in attributes:
			if element[0] == "link":
					link = element[2][0]
			if element[0] == "Unread":
					unread = element[2][0]
			if element[0] == "title":
					title = element[2][0]

		try:
			type(link)
			type(unread)
			type(title)
			
			addnews=True
		except:
			print("unconsistent news")

		if addnews:
			print("Aggiungo la news")
			global tmpNitm
			tmpNitm=NewsItem(title,entry,link,unread)
			self.NewsList.lv.AddItem(tmpNitm)
			
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
		elif msg.what == self.Paperlist.PaperSelection:
			if self.Paperlist.lv.CurrentSelection()>-1:
				self.gjornaaltolet()
		elif msg.what == self.NewsList.NewsSelection:
			if self.NewsList.lv.CurrentSelection()>-1:
				curit = self.NewsList.lv.CurrentSelection()
				Nitm = self.NewsList.lv.ItemAt(curit)
				if Nitm.unread:
					Nitm.unread=False
					#TODO: writeattr
				NFile=BFile(Nitm.entry,0)
				r,s=NFile.GetSize()
				if not r:
					data=b""
					data,size=NFile.Read(s)
					###### scrivi testo su anteprima notizia ######
					self.NewsPreView.SetText(NFile,0,s,None)
				else:
					print("sembra che non ci sia anteprima qui")
					###### scrivi su anteprima notizia che non c'è alcun riassunto di questa notizia ##########
			else:
				#self.NewsPreView.Delete()#SetText("",None)
				self.NewsPreView.SelectAll()
				self.NewsPreView.Clear()
			
		BWindow.MessageReceived(self, msg)
		
	def FrameResized(self,x,y):
		#self.ResizeToPreferred()
		self.ResizeTo(800,650)


	def QuitRequested(self):
		return BWindow.QuitRequested(self)
		
class App(BApplication):
    def __init__(self):
        BApplication.__init__(self, "application/x-python")
    def ReadyToRun(self):
        self.window = GatorWindow()
        self.window.Show()

def main():
    global be_app
    be_app = App()
    be_app.Run()
 
if __name__ == "__main__":
    main()
