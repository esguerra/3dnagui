#
# Name:     3DNA Pymol Plugin
# Author:   Mauricio Esguerra
# Date:     September 14, 2012
# Version:  0.1
# 
'''
Described at: http://www.pymolwiki.org/index.php/3dna_plugin

Plugin contributed by Mauricio Esguerra (mauricio.esguerra@gmail.com)
'''
 
import Tkinter
import Pmw
import os, sys, subprocess, math, re

try:
    import pymol
    REAL_PYMOL = True
except ImportError:
    REAL_PYMOL = False
    class pymol:
        class cmd:
            def fetch(*args):
                print "fetch", args
            def png(*args,**kwargs):
                print "png",args,kwargs
            fetch = staticmethod(fetch)
            png = staticmethod(png)
 
def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command',
                             'Launch 3DNA Plugin',
                             label='3DNA...',
                             command = lambda s=self: x3DNA(s))
class x3DNA:
 
    def __init__(self,app):
        self.parent = app.root
        self.dialog = Pmw.Dialog(self.parent,
                                 buttons = ('Fetch', 'Findpair','Analyze','Exit'),
                                 title = '3DNA plugin',
                                 command = self.execute)
        self.dialog.withdraw()
        Pmw.setbusycursorattributes(self.dialog.component('hull'))
# buttonbox_hull_relief
        w = Tkinter.Label(self.dialog.interior(),
                                text = 'PyMOL 3DNA Plugin v0.1\nMauricio Esguerra, 2012\n http://mesguerra.net',
                                background = 'black',
                                foreground = 'white',
                                )
        w.pack(expand = 1, fill = 'both', padx = 4, pady = 4)
 
 
        # Set up the Main page
        group = Pmw.Group(self.dialog.interior())

        group.pack(fill = 'both', expand = 1, padx = 10, pady = 5)
        self.filename = Pmw.EntryField(group.interior(),
                                        labelpos='w',
                                        label_text='PDB ID:',
                                        value='1ehz',
                                        )
        self.width =    Pmw.EntryField(group.interior(),
                                       labelpos='w',
                                       label_text = 'Width:',
                                       value = str(4.0),
                                       validate = {'validator' : 'real',
                                               'min':0,}
                                   )
        self.units = Pmw.OptionMenu(group.interior(), labelpos='w',
                                   label_text = 'Units',
                                   items = ('s','1',),
                                   )
        entries = (self.width, self.units, self.filename)
        
        for entry in entries:
            entry.pack(fill='x',expand=1,padx=4,pady=1) # vertical
        self.showAppModal()
 
    def showAppModal(self):
        self.dialog.show()
 
    def execute(self, result):
        if result == 'Fetch':
            pymol.cmd.fetch(self.filename.getvalue())
        if result == 'Findpair':
            os.system("find_pair %s.pdb stdout" % (self.filename.getvalue()))
            os.system("find_pair %s.pdb %s.inp 2> /dev/null" % (self.filename.getvalue(), self.filename.getvalue()))
        elif result == 'Analyze':
            os.system("analyze  %s.inp" % (self.filename.getvalue()))
            os.system("x3dna_utils dcmnfile")
        else:
            #
            # Doing it this way takes care of clicking on the x in the top of the
            # window, which as result set to None.
            #
            if __name__ == '__main__':
                #
                # dies with traceback, but who cares
                #
                self.parent.destroy()
            else:
                self.dialog.withdraw()
 
 