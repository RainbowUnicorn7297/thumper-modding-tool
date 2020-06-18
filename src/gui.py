import configparser
import psutil
import traceback
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from levels import *
from savedata import *

def read_config():
    global config
    config.read('config.ini')
    if 'default' not in config:
        config['default'] = {}
        default = config['default']
        while True:
            game_dir = filedialog.askdirectory(
                title='Select Thumper folder',
                initialdir='C:/Program Files (x86)/Steam/steamapps/common/Thumper')
            if len(game_dir) > 7 and game_dir[-7:] == 'Thumper':
                break
        default['game_dir'] = game_dir
        default['mod_mode'] = 'OFF'
        write_config()

def write_config():
    global config
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def get_config(key):
    global config
    return config['default'][key]

def set_config(key, value):
    global config
    config['default'][key] = value
    write_config()

def change_game_dir():
    while True:
        game_dir = filedialog.askdirectory(
            title='Select Thumper folder',
            initialdir=get_config('game_dir'))
        if len(game_dir) > 7 and game_dir[-7:] == 'Thumper':
            break
    set_config('game_dir', game_dir)

def thumper_running():
    for process in psutil.process_iter():
        try:
            process_name = process.name()
        except:
            continue
        if process_name in ('THUMPER_dx9.exe', 'THUMPER_win8.exe',
                            'THUMPER_win10.exe'):
            messagebox.showwarning(title='Warning',
                                   message='Please fully exit Thumper before switching Mod Mode.')
            return True
    return False

def update_level():
    global update_level_button
    try:
        update_level_button.config(text='Please wait...', state=DISABLED)
        
        make_custom_levels(get_config('game_dir'))
        make_custom_savedata(get_config('game_dir'))
    except:
        messagebox.showerror(title='Error',message=traceback.format_exc())
    finally:
        update_level_button.config(text='Update Custom Levels', state=NORMAL)

def mod_on():
    global mod_mode_label, mod_on_button, mod_off_button, update_level_button
    try:
        mod_on_button.config(text='Please wait...', state=DISABLED)
        
        if thumper_running():
            return
        backup_savedata(get_config('game_dir'))
        make_custom_levels(get_config('game_dir'))
        make_custom_savedata(get_config('game_dir'))
        
        mod_mode_label.config(text='Mod Mode: ON', fg='green')
        mod_on_button.grid_forget()
        mod_off_button.grid(row=0)
        set_config('mod_mode', 'ON')
    except:
        messagebox.showerror(title='Error',message=traceback.format_exc())
        try:
            mod_off(skip_check=True)
        except:
            pass
    finally:
        mod_on_button.config(text='Turn ON Mod Mode', state=NORMAL)
        if get_config('mod_mode') == 'OFF':
            update_level_button.config(state=DISABLED)
        else:
            update_level_button.config(state=NORMAL)

def mod_off(skip_check=False):
    global mod_mode_label, mod_off_button, mod_on_button, update_level_button
    try:
        mod_off_button.config(text='Please wait...', state=DISABLED)
        update_level_button.config(state=DISABLED)
        
        if not skip_check and thumper_running():
            return
        restore_levels(get_config('game_dir'))
        restore_savedata(get_config('game_dir'))
        
        mod_mode_label.config(text='Mod Mode: OFF', fg='red')
        mod_off_button.grid_forget()
        mod_on_button.grid(row=0)
        set_config('mod_mode', 'OFF')
    except:
        messagebox.showerror(title='Error',message=traceback.format_exc())
    finally:
        mod_off_button.config(text='Turn OFF Mod Mode', state=NORMAL)
        if get_config('mod_mode') == 'OFF':
            update_level_button.config(state=DISABLED)
        else:
            update_level_button.config(state=NORMAL)

root = Tk()
root.title('Thumper Modding Tool v1.0.0')
root.resizable(False, False)

menubar = Menu(root)
options_menu = Menu(menubar, tearoff=0)
options_menu.add_command(label='Change game folder...', command=change_game_dir)
menubar.add_cascade(label='Options', menu=options_menu)
root.config(menu=menubar)

left_frame = Frame(root)
left_frame.grid(padx=(10, 10), pady=(10, 10))
right_frame = Frame(root)
right_frame.grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
mod_mode_label = Label(left_frame, text='Mod Mode: OFF', fg='red',
                       font=(None, 20), width=15)
mod_mode_label.grid(row=0)
mod_on_button = Button(right_frame, text='Turn ON Mod Mode', bg='lightgreen',
                       width=20, command=mod_on)
mod_on_button.grid(row=0)
mod_off_button = Button(right_frame, text='Turn OFF Mod Mode', bg='pink',
                        width=20, command=mod_off)
update_level_button = Button(right_frame, text='Update Custom Levels', width=20,
                             command=update_level, state=DISABLED)
update_level_button.grid(row=1)

config = configparser.ConfigParser()
read_config()
if config['default']['mod_mode'] == 'ON':
    mod_mode_label.config(text='Mod Mode: ON', fg='green')
    mod_on_button.grid_forget()
    mod_off_button.grid(row=0)
    update_level_button.config(state=NORMAL)

root.mainloop()
