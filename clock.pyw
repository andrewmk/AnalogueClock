#!/usr/bin/env python

import wx
from wx.lib import analogclock as ac

import ConfigParser

class MyFrame(wx.Frame):
    def __init__(self, app, parent, id, title, style=wx.DEFAULT_FRAME_STYLE, width=400, height=350):
        if app.win:
            wx.Frame.__init__(self, parent, id, title, style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_TASKBAR)
        else:
            wx.Frame.__init__(self, parent, id, title, style=wx.FRAME_NO_TASKBAR)
        self.SetSize((width,height))
        self.delta = (0,0)

        clock = ac.AnalogClockWindow(self, hoursStyle=ac.TICKS_DECIMAL, minutesStyle=ac.TICKS_CIRCLE,
                                     clockStyle=ac.SHOW_HOURS_HAND|ac.SHOW_MINUTES_HAND|ac.SHOW_SECONDS_HAND| \
                                     ac.SHOW_HOURS_TICKS|ac.SHOW_MINUTES_TICKS|ac.OVERLAP_TICKS)
        ##clock.SetBackgroundColour(wx.Colour(0,118,163))
        ##clock.SetFaceFillColour(wx.Colour(0,118,163))
        clock.SetBackgroundColour(wx.Colour(0,0,0))
        clock.SetFaceFillColour(wx.Colour(0,0,0))
        clock.SetHandColours('yellow')
        clock.SetTickColours('yellow')
        clock.SetTickSizes(h=25, m=5)

        clock.Bind(wx.EVT_LEFT_DCLICK,   app.OnDoubleClick)
        clock.Bind(wx.EVT_LEFT_DOWN,     self.OnLeftDown)
        clock.Bind(wx.EVT_LEFT_UP,       self.OnLeftUp)
        clock.Bind(wx.EVT_MOTION,        self.OnMouseMove)
        clock.Bind(wx.EVT_MIDDLE_UP,      self.OnExit)

        clock.myframe = self

        self.clock = clock
        width, height = self.GetClientSize()
        clock.SetSize((width, height))
        
        if wx.Platform == "__WXGTK__":
            # wxGTK requires that the window be created before you can
            # set its shape, so delay the call to SetWindowShape until
            # this event.
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)
        else:
            # On wxMSW and wxMac the window has already been created, so go for it.
            self.SetWindowShape()

    def SetWindowShape(self, *evt):
        pass
        ##r = wx.Region()
        ##self.hasShape = self.SetShape(r)

    def OnLeftDown(self, evt):
        self.clock.CaptureMouse()
        x, y = self.ClientToScreen(evt.GetPosition())
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ((dx, dy))

    def OnLeftUp(self, evt):
        if self.clock.HasCapture():
            config = ConfigParser.ConfigParser()
            self.clock.ReleaseMouse()
            f = open("AnalogClock.ini", "w")
            config.add_section("Basic")
            config.set("Basic", "no_cap", str(self.no_cap))
            wid, hei = self.GetSize()
            config.set("Basic", "width", wid)
            config.set("Basic", "height", hei)
            x, y = self.GetPosition()
            config.set("Basic", "x", x)
            config.set("Basic", "y", y)
            config.write(f)
            f.close()

    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)

    def OnExit(self, evt):
        config = ConfigParser.ConfigParser()
        f = open("AnalogClock.ini", "w")
        config.add_section("Basic")
        config.set("Basic", "no_cap", str(self.no_cap))
        wid, hei = self.GetSize()
        config.set("Basic", "width", wid)
        config.set("Basic", "height", hei)
        x, y = self.GetPosition()
        config.set("Basic", "x", x)
        config.set("Basic", "y", y)
        config.write(f)
        self.Close()

class MyApp(wx.App):
    def OnInit(self):
        self.win = True
        self.frame = MyFrame(self, None, -1, '', wx.DEFAULT_FRAME_STYLE)
        self.frame.no_cap = False
        x = y = 0
        config = ConfigParser.ConfigParser()
        try:
            f = open("AnalogClock.ini", "r")
        except:
            print "Can't open AnalogClock.ini for reading"
        try:
            config.readfp(f)
        except:
            print "Can't read ini file"
        try:
            self.frame.no_cap = config.getboolean("Basic", "no_cap")
            self.win = not self.frame.no_cap
        except:
            print "Can't read window options"
        try:
            wid = config.getint("Basic", "width")
            hei = config.getint("Basic", "height")
            self.frame.SetSize((wid, hei))
        except:
            print "Can't read size options"
        try:
            x = config.getint("Basic", "x")
            y = config.getint("Basic", "y")
            self.frame.Move((x, y))
        except:
            print "Can't read position options"

        if self.frame.no_cap:
            self.frame.SetWindowStyle(wx.FRAME_NO_TASKBAR)

        self.frame.Show(True)
        return True
    
    def OnDoubleClick(self, evt):
        self.win = not self.win
        self.frame.no_cap = not self.frame.no_cap
        wid, hei = self.frame.GetClientSize()
##        width, height = self.frame.GetSize()
##        dw = width - wid
##        dh = height - hei
##        print "dw=%d, dh=%d" % (dw, dh)
##        x, y = self.frame.GetPosition()
##        print "x=%d, y=%d" % (x, y)

        if self.win:
            self.frame.SetWindowStyle(wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_TASKBAR)
        else:
            self.frame.SetWindowStyle(wx.FRAME_NO_TASKBAR)
            self.frame.SetSize((wid, hei))
##            self.frame.Refresh()
##            x = x + dw
##            y = y + dh
##            print "new x=%d, y=%d" % (x, y)
##            self.frame.MoveXY(x, y)

app = MyApp(0)
app.MainLoop()
