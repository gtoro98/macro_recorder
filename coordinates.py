from pynput import mouse
from pynput import keyboard
import PySimpleGUI as sg

position_x = 0
position_y = 0

def on_move(x, y):
    window['x'].update(x)
    window['y'].update(y)


mouse_listener = mouse.Listener(on_move=on_move)


sg.theme('DarkAmber')   # Add a touch of color

# All the stuff inside your window.
layout = [  [sg.Text('Position of mouse')],
            [sg.Text('X position:'), sg.Text('X', key = 'x')],
            [sg.Text("Y position:"), sg.Text('Y', key = 'y')],
            [sg.Button('Close')] ]

# Create the Window
window = sg.Window('Mouse coordinates', layout)
# Event Loop to process "events" and get the "values" of the inputs


mouse_listener.start()
while True:
    event, values = window.read()
    
    if event == None:
        window['x'].update(position_x)
        window['y'].update(position_y)

    if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
        break

window.close()