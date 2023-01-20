from pynput import mouse
from pynput import keyboard
import PySimpleGUI as sg
import time
import json
import sys
import os
import play

storage = []
count = 0
message = ''

def on_press(key):
    try:
        json_object = {'action':'pressed_key', 'key':key.char, '_time': time.time()}
    except AttributeError:
        if key == keyboard.Key.esc:
            mouse_listener.stop()
            with open('data/{}.txt'.format(name_of_recording), 'w') as outfile:
                json.dump(storage, outfile)
            return False
        json_object = {'action':'pressed_key', 'key':str(key), '_time': time.time()}
    storage.append(json_object)

def on_release(key):
    try:
        json_object = {'action':'released_key', 'key':key.char, '_time': time.time()}
    except AttributeError:
        json_object = {'action':'released_key', 'key':str(key), '_time': time.time()}
    storage.append(json_object)
        

def on_move(x, y):
    if (record_all) == True:
        if len(storage) >= 1:
            if storage[-1]['action'] != "moved":
                json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time()}
                storage.append(json_object)
            elif storage[-1]['action'] == "moved" and time.time() - storage[-1]['_time'] > 0.02:
                json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time()}
                storage.append(json_object)
        else:
            json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time()}
            storage.append(json_object)
    else:
        if len(storage) >= 1:
            if (storage[-1]['action'] == "pressed" and storage[-1]['button'] == 'Button.left') or (storage[-1]['action'] == "moved" and time.time() - storage[-1]['_time'] > 0.02):
                json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time()}
                storage.append(json_object)

def on_click(x, y, button, pressed):
    json_object = {'action':'pressed' if pressed else 'released', 'button':str(button), 'x':x, 'y':y, '_time':time.time()}
    storage.append(json_object)
    if len(storage) > 1:
        if storage[-1]['action'] == 'released' and storage[-1]['button'] == 'Button.right' and storage[-1]['_time'] - storage[-2]['_time'] > 2:
            with open('data/{}.txt'.format(name_of_recording), 'w') as outfile:
                json.dump(storage, outfile)
            return False


def on_scroll(x, y, dx, dy):
    json_object = {'action': 'scroll', 'vertical_direction': int(dy), 'horizontal_direction': int(dx), 'x':x, 'y':y, '_time': time.time()}
    storage.append(json_object)


# Collect events from keyboard until esc
# Collect events from mouse until scroll
keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

mouse_listener = mouse.Listener(
        on_click=on_click,
        on_scroll=on_scroll,
        on_move=on_move)


sg.theme('DarkAmber')   # Add a touch of color

recordings = os.listdir('./data')
print(recordings)
# All the stuff inside your window.
layout = [  [sg.Text(f'Some text on Row 1 {message}', key="title")],
            [sg.Text('Ingrese el nombre de la grabacion'), sg.InputText(key="input")],
            [sg.Text('Seleccionar grabacion'), sg.Combo(recordings, key="combo"), sg.Button('Play')],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs

recording = False
while True:
    event, values = window.read()
    recordings = os.listdir('./data')
    window['combo'].update(values=recordings)

    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Ok':
        window['combo'].update(values=recordings)
        name_of_recording = window['input'].get()
        record_all = True

        if not values['input']:
            message = 'Please enter a name for the recording'
            window['title'].update(message)
            continue
        if not recording:
            recording = True
            print("Hold right click for more than 2 seconds (and then release) to end the recording for mouse and click 'esc' to end the recording for keyboard (both are needed to finish recording)")
            keyboard_listener.start()
            mouse_listener.start()
            #keyboard_listener.join()
            #mouse_listener.join()
            window['title'].update('Please enter a name for the recording' + values['input'] + "!")
        else:
            recording = False
            with open('data/{}.txt'.format(name_of_recording), 'w') as outfile:
                json.dump(storage, outfile)
            mouse_listener.stop()
            keyboard_listener.stop()
    
    if event == 'Play':
        print("Playing")
        print(values['combo'])
        play.play_recording(values['combo'], 5)

window.close()

# 
