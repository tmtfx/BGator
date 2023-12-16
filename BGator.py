from Be import BApplication, BWindow, BView, BMenu,BMenuBar, BMenuItem, BSeparatorItem, BMessage, window_type, B_NOT_RESIZABLE, B_QUIT_ON_WINDOW_CLOSE
from Be import BButton, BTextView, BTextControl, BAlert, BListItem, BListView, BScrollView, BRect, BBox, BFont,InterfaceDefs
from Be.GraphicsDefs import *
from Be.View import B_FOLLOW_NONE,set_font_mask
from Be.Alert import alert_type
from Be.InterfaceDefs import border_style
from Be.ListView import list_view_type
from Be.AppDefs import *
from Be.Font import be_plain_font, be_bold_font
from Be import AppDefs

from Be import Entry
from Be.Entry import entry_ref, get_ref_for_path

class ScrollViewItems(BListItem):
	nocolor = (0, 0, 0, 0)

	def __init__(self, name,color,type):
		self.name = name
		self.color=color
		self.type=type
		BListItem.__init__(self)
		self.newnews=false

	def DrawItem(self, owner, frame, complete):
		if self.IsSelected() or complete:
			#color = (200,200,200,255)
			if type == True:
				owner.SetHighColor(0,180,0,255)
				owner.SetLowColor(200,200,200,255)
			else:
				owner.SetHighColor(0,0,180,255)
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
		owner.MovePenTo(5,frame.Height()-2)
		if self.newnews:
			owner.DrawString("▶ "+self.name,None)
		else:
			owner.DrawString(self.name,None)

class ScrollView:
	HiWhat = 32 #Doppioclick
	def __init__(self, rect, name):
		self.lv = BListView(rect, name, list_view_type.B_SINGLE_SELECTION_LIST)
		self.sv = BScrollView('ScrollView', self.lv)#, 0x0202,0,False,False, border_style.B_FANCY_BORDER)#|0x1030

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
		self.Paperlist = ScrollView(BRect(8 , 56, boxboundsw / 3 , boxboundsh - 8 ), 'NewsPapersScrollView')
		self.box.AddChild(self.Paperlist.sv, None)
		self.NewsList = ScrollView(BRect(8 + boxboundsw / 3 , 56, boxboundsw -8 , boxboundsh / 1.8 ), 'NewsListScrollView')
		self.box.AddChild(self.NewsList.sv,None)
		txtRect=BRect(8 + boxboundsw / 3, boxboundsh / 1.8 + 8,boxboundsw -8,boxboundsh - 8)
		self.outbox_preview=BBox(txtRect,"previewframe",0x0202|0x0404,border_style.B_FANCY_BORDER)
		self.box.AddChild(self.outbox_preview,None)
		innerRect= BRect(8,8,txtRect.Width()-8,txtRect.Height())
		self.NewsPreView = BTextView(BRect(2,2, self.outbox_preview.Bounds().Width()-2,self.outbox_preview.Bounds().Height()-2), 'NewsTxTView', innerRect , B_FOLLOW_NONE,2000000)
		#fon=BFont()
		#sameProperties=0
		#colore=rgb_color()
		#sameColor=True
		#self.NewsTextView.GetFontAndColor(fon,sameProperties,colore,sameColor)
		#print("Rosso:",colore.red,"Verde:",colore.green,"Blu:",colore.blue,"Alfa:",colore.alpha)
		#colore.set_to(255,255,255,255)
		#print("Rosso:",colore.red,"Verde:",colore.green,"Blu:",colore.blue,"Alfa:",colore.alpha)
		#self.NewsTextView.SetFontAndColor(fon,set_font_mask.B_FONT_ALL, colore)
		self.outbox_preview.AddChild(self.NewsPreView,None)
		
		
		self.bckgnd.AddChild(self.bar, None)
		self.bckgnd.AddChild(self.box, None)

		

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
    print('so said dolphins...')
 
if __name__ == "__main__":
    main()
