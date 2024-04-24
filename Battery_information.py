import wx
import psutil
import winsound

class BatteryInfoPopup(wx.Frame):
    def __init__(self, parent, title):
        super(BatteryInfoPopup, self).__init__(parent, title=title, size=(350, 150))
        self.panel = wx.Panel(self)
        self.create_widgets()
        self.timer = wx.Timer(self)  # Create a timer
        self.Bind(wx.EVT_TIMER, self.update_battery_status, self.timer)  # Bind the timer event
        self.timer.Start(1000)  # Start the timer with an interval
        self.SetMinSize((350, 150)) # Set the minimum size of the frame
        self.SetMaxSize((350, 150)) # Set the maximum size of the frame
        self.Show()

    def create_widgets(self):
        self.percent_label = wx.StaticText(self.panel, label="Percentage of battery: ")
        self.secsleft_label = wx.StaticText(self.panel, label="Approx time remaining: ")
        self.power_plugged_label = wx.StaticText(self.panel, label="Is power cable connected: ")

        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  
        font.SetFaceName("Helvetica") 
        self.percent_label.SetFont(font) 
        self.secsleft_label.SetFont(font) 
        self.power_plugged_label.SetFont(font)  

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.percent_label, 0, wx.ALL, 5)
        sizer.Add(self.secsleft_label, 0, wx.ALL, 5)
        sizer.Add(self.power_plugged_label, 0, wx.ALL, 5)

        self.panel.SetSizer(sizer)


    def update_battery_status(self, event):
        battery_status = psutil.sensors_battery()
        self.percent_label.SetLabel("Percentage of battery: %s %%" % battery_status.percent)
        if int(battery_status.percent) < 30 and not battery_status.power_plugged:
            winsound.PlaySound("C:/Users/Enrico/Desktop/quack_5.wav", winsound.SND_ALIAS)
            self.percent_label.SetForegroundColour(wx.Colour(255, 0, 0))
        remaining_time = battery_status.secsleft
        hours = remaining_time // 3600
        minutes = (remaining_time % 3600) // 60
        seconds = remaining_time % 60
        if not battery_status.power_plugged:
            self.secsleft_label.SetLabel("Approx remaining: %s hours, %s minutes, %s seconds" % (hours, minutes, seconds))
        else:
            self.secsleft_label.SetLabel("Charging...")
        self.power_plugged_label.SetLabel("Is power cable connected: %s" % ("Yes" if battery_status.power_plugged else "No"))

if __name__ == '__main__':
    app = wx.App()
    BatteryInfoPopup(None, title="Battery Information")
    app.MainLoop()
