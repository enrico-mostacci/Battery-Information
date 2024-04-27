import wx
import psutil
import winsound

class BatteryInfoPopup(wx.Frame):
    def __init__(self, parent, title):
        super(BatteryInfoPopup, self).__init__(parent, title=title, size=(350, 200))
        self.initUI()
        self.update(None)
        self.Show()
        
    def initUI(self):
        self.panel = wx.Panel(self)  # Create a panel
        self.button = wx.ToggleButton(self.panel, label="Stop quacking, Sir")
        self.button2 = wx.Button(self.panel, label="Enter")
        self.button.SetValue(True)
        self.button.Bind(wx.EVT_TOGGLEBUTTON, self.on_button_toggle)
        self.button2.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.SetMinSize((350, 200)) # Set the minimum size of the frame
        self.SetMaxSize((350, 200)) # Set the maximum size of the frame
        self.percent_label = wx.StaticText(self.panel, label="Percentage of battery: ")
        self.secsleft_label = wx.StaticText(self.panel, label="Approx time remaining: ")
        self.power_plugged_label = wx.StaticText(self.panel, label="Is power cable connected: ")
        self.input_user = wx.StaticText(self.panel, label = "Enter the min % of battery to monitor: ")
        self.input_user_percent = wx.TextCtrl(self.panel, value="30", size=(35, -1))
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # Create a font object
        font.SetFaceName("Helvetica")  # Set the font face to Helvetica
        self.percent_label.SetFont(font)  # Set the font for the percent label
        self.secsleft_label.SetFont(font)  # Set the font for the secsleft label
        self.power_plugged_label.SetFont(font)  # Set the font for the power_plugged label
        self.input_user.SetFont(font) # Set the font for the input_user label
        self.button.SetFont(font) # Set the font for the button
        self.button2.SetFont(font) # Set the font for the button2  
        vbox = wx.BoxSizer(wx.VERTICAL)  # Create a vertical box sizer
        vbox.Add(self.percent_label, wx.ALIGN_LEFT)  
        vbox.Add(self.secsleft_label, wx.ALIGN_LEFT)
        vbox.Add(self.power_plugged_label, wx.ALIGN_LEFT) 
        vbox.Add((-1, 10))
        hbox = wx.BoxSizer(wx.HORIZONTAL)  # Create a horizontal box sizer for input
        hbox.Add(self.input_user, wx.ALIGN_LEFT)
        hbox.Add(self.input_user_percent, wx.ALIGN_LEFT) 
        hbox.Add(self.button2, wx.ALIGN_LEFT)
        vbox.Add(hbox, 0, wx.EXPAND, 20) 
        vbox.Add((-1, 10)) 
        vbox.Add(self.button, 0, wx.EXPAND, 20)  
        self.panel.SetSizer(vbox) 
         
    def update(self, event=None):
            self.timer = wx.Timer(self)  # Create a timer
            self.Bind(wx.EVT_TIMER, self.update, self.timer)  # Bind the timer event
            self.timer.Start(2500)  # Start the timer with an interval
            self.update_battery_status()
            self.on_button_click()
            self.on_button_toggle()

    def on_button_toggle(self, event=None):
        label = "WARNING: QUACK MUTED!" if not self.button.GetValue() == True else "Stop quacking, Sir"
        self.button.SetLabel(label)
 
    def update_battery_status(self, event=None):
        battery_status = psutil.sensors_battery()
        self.percent_label.SetLabel("Percentage of battery: %s%%" % battery_status.percent)
        remaining_time = battery_status.secsleft
        hours = remaining_time // 3600
        minutes = (remaining_time % 3600) // 60
        seconds = remaining_time % 60
        if not battery_status.power_plugged:
            self.secsleft_label.SetLabel("Approx remaining: %s hours, %s minutes, %s seconds" % (hours, minutes, seconds))
        else:
            self.secsleft_label.SetLabel("Charging...")
        self.power_plugged_label.SetLabel("Is power cable connected: %s" % ("Yes" if battery_status.power_plugged else "No"))

    def on_button_click(self, event=None):
        battery_status = psutil.sensors_battery()
        is_unplugged = not battery_status.power_plugged
        is_button_checked = self.button.GetValue()
        if event is not None and event.GetEventObject() == self.button2:  
            threshold = int(self.input_user_percent.GetValue()) if self.input_user_percent.GetValue() else self.input_user_percent.GetValue() == 20
        else:
            threshold = int(self.input_user_percent.GetValue())  # Get the threshold value from the input field

        is_below = int(battery_status.percent) < threshold

        if is_below and is_unplugged and is_button_checked:
            winsound.PlaySound("C:/Users/Enrico/Desktop/quack_5.wav", winsound.SND_ASYNC)
            self.percent_label.SetForegroundColour(wx.Colour(255, 0, 0))
        elif (is_below and is_unplugged and not is_button_checked) or battery_status.power_plugged:
            winsound.PlaySound(None, winsound.SND_PURGE)
            self.percent_label.SetForegroundColour(wx.Colour(0, 0, 0))

if __name__ == '__main__':
    app = wx.App()
    BatteryInfoPopup(None, title="Battery Information")
    app.MainLoop()
