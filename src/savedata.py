import datetime
import os
import shutil
from common import *

max_backup_count = 50

def backup_savedata(game_dir):
    global max_backup_count
    backup_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    shutil.copytree(game_dir+'/savedata', 'backup/'+backup_time)
    all_backup_dirs = os.listdir('backup')
    while len(all_backup_dirs) > max_backup_count:
        first_backup_time = min(all_backup_dirs)
        shutil.rmtree('backup/'+first_backup_time)
        all_backup_dirs.remove(first_backup_time)

def make_custom_savedata(game_dir):
    last_backup_time = max(os.listdir('backup'))
    for root, dirs, files in os.walk('backup/'+last_backup_time):
        for filename in files:
            if filename == 'data.index':
                with open(os.path.join(root, filename), 'rb') as f:
                    data = f.read()
                    src_filename = 'data_' + str(read_int(data, 8)) + '.sav'
    for root, dirs, files in os.walk('backup/'+last_backup_time):
        for filename in files:
            if filename == src_filename:
                with open(os.path.join(root, filename), 'rb') as f:
                    src_data = f.read()

    for root, dirs, files in os.walk(game_dir+'/savedata'):
        for filename in files:
            if filename == 'data.index':
                with open(os.path.join(root, filename), 'wb') as f:
                    write_int(f, 0)
                    write_int(f, 12)
                    write_int(f, 0)
            elif filename == 'data_0.sav':
                with open(os.path.join(root, filename), 'wb') as f:
                    write_savedata(f, src_data)
            elif filename == 'data_1.sav':
                os.remove(os.path.join(root, filename))

def seek_savedata_pos(src_data):
    pos = 12
    num_levels = read_int(src_data, 8)
    for i in range(num_levels):
        pos += 4 + read_int(src_data, pos)
        pos += 4 + read_int(src_data, pos)
        pos += 4
        pos += 4 + read_int(src_data, pos)
        pos += 13
        pos += 4 + read_int(src_data, pos)
        pos += 4 + read_int(src_data, pos)
        pos += 8
        num_sublevels = read_int(src_data, pos)
        pos += 4
        for j in range(num_sublevels):
            pos += 4 + read_int(src_data, pos)
    pos += 4 + read_int(src_data, pos)
    pos += 4 + read_int(src_data, pos)
    return pos

def write_savedata(f, src_data):
    dst_data_len = 12
    all_level_names = level_names[:]
    all_level_names.append('level4')
    for level_name in all_level_names:
        dst_data_len += 95 + len(level_name)
    dst_data_len += 8 + len(all_level_names[0])*2
    src_pos = seek_savedata_pos(src_data)
    dst_data_len += len(src_data[src_pos:])
    
    write_int(f, 57)
    write_int(f, dst_data_len)
    write_int(f, len(all_level_names))
    for level_name in all_level_names:
        write_string(f, level_name)
        write_string(f, 'RANK_C')
        write_int(f, 0)
        write_string(f, 'RANK_NONE')
        write_bool(f, True)
        write_hex(f, '00'*12)
        write_string(f, 'RANK_NONE')
        write_string(f, 'RANK_NONE')
        write_int(f, -1)
        write_int(f, 0)
        write_int(f, 1)
        write_string(f, 'RANK_NONE')
    write_string(f, all_level_names[0])
    write_string(f, all_level_names[0])
    f.write(src_data[src_pos:])

def restore_savedata(game_dir):
    last_backup_time = max(os.listdir('backup'))
    shutil.copytree('backup/'+last_backup_time, game_dir+'/savedata',
                    dirs_exist_ok=True)
