# main.py

import time
import wx
from settings import *
from simulation import Simulation 

n=COUNT_SEARCHBOT
item=wx.GREEN

# list of n x item objects
COLORS = [
    item for i in range(n)
    ]

class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent)
        self.sim = Simulation(SIZE, SIZE, COUNT, OBSTACLE_COUNT)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
        self.timestamp = time.time()
        self.on_timer()
    def on_timer(self):
        now = time.time()
        dt = now - self.timestamp
        self.timestamp = now
        self.sim.update(dt)
        self.Refresh()
        wx.CallLater(10, self.on_timer)
    def on_left_down(self, event):
        self.sim.bots[0].target = event.GetPosition()
    def on_right_down(self, event):
        width, height = self.GetClientSize()
        self.sim = Simulation(SIZE, SIZE, COUNT, OBSTACLE_COUNT)
    def on_size(self, event):
        width, height = self.GetClientSize()
        self.sim = Simulation(SIZE, SIZE, COUNT, OBSTACLE_COUNT)
        event.Skip()
        self.Refresh()
    def on_paint(self, event):
        # n = len(COLORS)
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.WHITE_BRUSH)  
        dc.Clear()
        dc.SetPen(wx.WHITE_PEN)

        # Trail SearchBot
        # for index, bot in enumerate(self.sim.bots[:n]):
        #     dc.SetBrush(wx.Brush(wx.Colour(255 - COLORS[index].Red(), 255 - COLORS[index].Green(), 255 - COLORS[index].Blue())))  
        #     for x, y in bot.history:
        #         dc.DrawCircle(int(x), int(y), 3)

        # Target
        dc.SetBrush(wx.WHITE_BRUSH)  
        for index, bot in enumerate(self.sim.bots[:n]):
            dc.SetPen(wx.Pen(wx.Colour(255 - COLORS[index].Red(), 255 - COLORS[index].Green(), 255 - COLORS[index].Blue())))  
            x, y = bot.target
            dc.DrawCircle(int(x), int(y), 6)

        # Bots
        for index, bot in enumerate(self.sim.bots):
            dc.SetPen(wx.WHITE_PEN) 

            # SearchBot 
            if index < n:
                dc.SetBrush(wx.Brush(wx.Colour(255 - COLORS[index].Red(), 255 - COLORS[index].Green(), 255 - COLORS[index].Blue())))

            # FollowerBot  
            elif index >= COUNT - FOLLOWERS:
                dc.SetBrush(wx.WHITE_BRUSH)  
                dc.SetPen(wx.BLACK_PEN) 

            # ObstacleBot      
            else:
                dc.SetBrush(wx.BLACK_BRUSH) 

            x, y = bot.position
            dc.DrawCircle(int(x), int(y), 6)

        # Static Obstacles
        dc.SetBrush(wx.RED_BRUSH)  
        for obstacle in self.sim.obstacles:
            x, y = obstacle.position
            dc.DrawCircle(int(x), int(y), 6) 

class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None)
        self.SetTitle('Motion')
        self.SetClientSize((SIZE, SIZE))
        Panel(self)

def main():
    app = wx.App()
    frame = Frame()
    frame.Center()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()

