import ast
import os
import shutil
from common import *

trait_types = ['kTraitInt',
               'kTraitBool',
               'kTraitFloat',
               'kTraitColor',
               'kTraitObj',
               'kTraitVec3',
               'kTraitPath',
               'kTraitEnum',
               'kTraitAction',
               'kTraitObjVec',
               'kTraitString',
               'kTraitCue',
               'kTraitEvent',
               'kTraitSym',
               'kTraitList',
               'kTraitTraitPath',
               'kTraitQuat',
               'kTraitChildLib',
               'kTraitComponent',
               'kNumTraitTypes']
obj_types = ['SequinLeaf',
             'SequinLevel',
             'SequinGate',
             'SequinMaster',
             'EntitySpawner',
             'Sample',
             'Xfmer']

def write_param_path(f, param_path, param_path_hash = None):
    if param_path:
        param_path_list = param_path.split(':')
    else:
        param_path_list = param_path_hash.split(':')
    write_int(f, len(param_path_list))
    for j in range(len(param_path_list)):
        if ',' in param_path_list[j]:
            param_name, param_idx = param_path_list[j].split(',')
        else:
            param_name, param_idx = param_path_list[j], '-1'
        if param_path:
            write_hash(f, param_name)
        else:
            write_hex_reverse(f, param_name)
        write_int(f, int(param_idx))

def write_data_point_value(f, val, trait_type):
    if trait_type == 'kTraitInt':
        write_int(f, val)
    elif trait_type == 'kTraitBool' or trait_type == 'kTraitAction':
        write_bool(f, val)
    elif trait_type == 'kTraitFloat':
        write_float(f, val)
    elif trait_type == 'kTraitColor':
        write_color(f, val)
    elif trait_type == 'kTraitVec3':
        write_vec3(f, val)
    elif trait_type == 'kTraitString':
        write_string(f, val)

def write_sequencer_objects(f, obj):
    global trait_types
    beat_cnt = obj['beat_cnt'] if 'beat_cnt' in obj else 0
    seq_objs = obj['seq_objs']
    
    write_int(f, len(seq_objs))
    for obj in seq_objs:
        #header
        write_string(f, obj['obj_name'])
        write_param_path(f, obj.get('param_path'), obj.get('param_path_hash'))
        write_int(f, trait_types.index(obj['trait_type']))

        #data points
        interp = obj['default_interp'] if 'default_interp' in obj else 'kTraitInterpLinear'
        ease = obj['default_ease'] if 'default_ease' in obj else 'kEaseInOut'
        if obj['step']:
            write_int(f, beat_cnt)
            for i in range(beat_cnt):
                write_float(f, i)
                if i in obj['data_points']:
                    write_data_point_value(f, obj['data_points'][i], obj['trait_type'])
                else:
                    write_data_point_value(f, obj['default'], obj['trait_type'])
                write_string(f, interp)
                write_string(f, ease)
        else:
            write_int(f, len(obj['data_points']))
            for i in obj['data_points']:
                write_float(f, i)
                write_data_point_value(f, obj['data_points'][i], obj['trait_type'])
                write_string(f, interp)
                write_string(f, ease)
        write_int(f, 0)

        #footer
        write_int(f, obj['footer'][0])
        write_int(f, obj['footer'][1])
        write_int(f, obj['footer'][2])
        write_int(f, obj['footer'][3])
        write_int(f, obj['footer'][4])
        write_string(f, obj['footer'][5])
        write_string(f, obj['footer'][6])
        write_bool(f, obj['footer'][7])
        write_bool(f, obj['footer'][8])
        write_int(f, obj['footer'][9])
        write_float(f, obj['footer'][10])
        write_float(f, obj['footer'][11])
        write_float(f, obj['footer'][12])
        write_float(f, obj['footer'][13])
        write_float(f, obj['footer'][14])
        write_bool(f, obj['footer'][15])
        write_bool(f, obj['footer'][16])
        write_bool(f, obj['footer'][17])

def write_anim_comp(f):
    write_hash(f, 'AnimComp')
    write_int(f, 1)
    write_float(f, 0)
    write_string(f, 'kTimeBeats')

def write_approach_anim_comp(f, obj):
    write_hash(f, 'ApproachAnimComp')
    write_int(f, 1)
    write_float(f, 0)
    write_string(f, 'kTimeBeats')
    write_int(f, 0)
    write_int(f, obj['approach_beats'])

def write_xfm_comp(f, obj):
    write_hash(f, 'XfmComp')
    write_int(f, 1)
    write_string(f, obj['xfm_name'])
    write_string(f, obj['constraint'])
    write_vec3(f, obj['pos'])
    write_vec3(f, obj['rot_x'])
    write_vec3(f, obj['rot_y'])
    write_vec3(f, obj['rot_z'])
    write_vec3(f, obj['scale'])

def write_leaf_header(f):
    write_int(f, 34)
    write_int(f, 33)
    write_int(f, 4)
    write_int(f, 2)

def write_leaf_comp(f, obj):
    write_hash(f, 'EditStateComp')
    write_sequencer_objects(f, obj)

def write_leaf_footer(f, obj):
    beat_cnt = obj['beat_cnt']
    write_int(f, 0)
    write_int(f, beat_cnt)
    for i in range(beat_cnt*3):
        write_int(f, 0)
    write_int(f, 0)
    write_int(f, 0)
    write_int(f, 0)

def write_lvl_header(f):
    write_int(f, 51)
    write_int(f, 33)
    write_int(f, 4)
    write_int(f, 2)

def write_lvl_comp(f, obj):
    write_hash(f, 'EditStateComp')
    write_sequencer_objects(f, obj)

    #.leaf sequence
    write_int(f, 0)
    write_string(f, 'kMovePhaseRepeatChild')
    write_int(f, 0)
    last_beat_cnt = 0
    for leaf in obj['leaf_seq']:
        write_bool(f, True)
        write_int(f, 0)
        write_int(f, leaf['beat_cnt'])
        write_bool(f, False)
        write_string(f, leaf['leaf_name'])
        write_string(f, leaf['main_path'])
        write_int(f, len(leaf['sub_paths']))
        for sub_path in leaf['sub_paths']:
            write_string(f, sub_path)
            write_int(f, 0)
        write_string(f, 'kStepGameplay')
        write_int(f, last_beat_cnt)
        write_vec3(f, leaf['pos'])
        write_vec3(f, leaf['rot_x'])
        write_vec3(f, leaf['rot_y'])
        write_vec3(f, leaf['rot_z'])
        write_vec3(f, leaf['scale'])
        write_hex(f, '0000')
        last_beat_cnt = leaf['beat_cnt']
    write_bool(f, False)

    #loops
    write_int(f, len(obj['loops']))
    for loop in obj['loops']:
        write_string(f, loop['samp_name'])
        write_int(f, loop['beats_per_loop'])
        write_int(f, 0)

def write_lvl_footer(f, obj):
    write_bool(f, False)
    write_float(f, obj['volume'])
    write_int(f, 0)
    write_int(f, 0)
    write_string(f, 'kNumTraitTypes')
    write_bool(f, obj['input_allowed'])
    write_string(f, obj['tutorial_type'])
    write_vec3(f, obj['start_angle_fracs'])

def write_gate_header(f):
    write_int(f, 26)
    write_int(f, 4)
    write_int(f, 1)

def write_gate_comp(f, obj):
    write_hash(f, 'EditStateComp')
    write_string(f, obj['spn_name'])
    write_param_path(f, obj.get('param_path'), obj.get('param_path_hash'))
    
    write_int(len(obj['boss_patterns']))
    for boss_pattern in obj['boss_patterns']:
        if 'node_name' in boss_pattern:
            write_hash(f, boss_pattern['node_name'])
        else:
            write_hex(f, boss_pattern['node_name_hash'])
        write_string(f, boss_pattern['lvl_name'])
        write_bool(f, True)
        write_string(f, boss_pattern['sentry_type'])
        write_hex(f, '00000000')
        write_int(f, boss_pattern['bucket_num'])

def write_gate_footer(f, obj):
    write_string(f, obj['pre_lvl_name'])
    write_string(f, obj['post_lvl_name'])
    write_string(f, obj['restart_lvl_name'])
    write_int(f, 0)
    write_string(f, obj['section_type'])
    write_float(f, 9)
    write_string(f, obj['random_type'])

def write_master_header(f):
    write_int(f, 33)
    write_int(f, 33)
    write_int(f, 4)
    write_int(f, 2)

def write_master_comp(f, obj):
    write_hash(f, 'EditStateComp')
    write_int(f, 0)
    write_float(f, 300)
    write_string(f, obj['skybox_name'])
    write_string(f, obj['intro_lvl_name'])

    #.lvl/.gate groupings
    write_int(f, len(obj['groupings']))
    for grouping in obj['groupings']:
        write_string(f, grouping['lvl_name'])
        write_string(f, grouping['gate_name'])
        write_bool(f, grouping['checkpoint'])
        write_string(f, grouping['checkpoint_leader_lvl_name'])
        write_string(f, grouping['rest_lvl_name'])
        write_hex(f, '01000100000001')
        write_bool(f, grouping['play_plus'])

def write_master_footer(f, obj):
    write_bool(f, False)
    write_bool(f, True)
    write_int(f, 3)
    write_int(f, 50)
    write_int(f, 8)
    write_int(f, 1)
    write_float(f, 0.6)
    write_float(f, 0.5)
    write_float(f, 0.5)
    write_string(f, obj['checkpoint_lvl_name'])
    write_string(f, 'path.gameplay')

def write_spn_header(f):
    write_int(f, 1)
    write_int(f, 4)
    write_int(f, 2)

def write_spn_comp(f):
    write_hash(f, 'EditStateComp')

def write_spn_footer(f, obj):
    write_int(f, 0)
    write_string(f, obj['objlib_path'])
    write_string(f, obj['bucket'])

def write_samp_header(f):
    write_int(f, 12)
    write_int(f, 4)
    write_int(f, 1)

def write_samp_comp(f, obj):
    write_hash(f, 'EditStateComp')
    write_string(f, obj['mode'])
    write_int(f, 0)
    write_string(f, obj['path'])
    write_hex(f, '0000000000')
    write_float(f, obj['volume'])
    write_float(f, obj['pitch'])
    write_float(f, obj['pan'])
    write_float(f, obj['offset'])
    write_string(f, obj['channel_group'])

def write_xfm_header(f):
    write_int(f, 4)
    write_int(f, 4)
    write_int(f, 1)

def make_custom_levels(game_dir):
    src_filenames = ['lib/2e7b0500.pc',
                     'lib/e0c51024.pc',
                     'lib/f78b7d78.pc']
    
    for level_name in level_names:
        level_config = {}
        objs = []
        obj_count = 0
        
        for filename in os.listdir('levels/'+level_name):
            obj_file = os.path.join(os.getcwd(), 'levels/'+level_name, filename)
            with open(obj_file, 'r') as fin:
                try:
                    new_objs = ast.literal_eval(fin.read())
                except Exception as e:
                    raise type(e)('Error reading file '+filename) from e
                objs += new_objs

        for obj in objs:
            if obj['obj_type'] == 'LevelLib':
                level_config = obj
            elif obj['obj_type'] in obj_types:
                obj_count += 1

        cache_filename = 'out/'+level_name+'/'+level_config['cache_filename']
        with open(cache_filename, 'wb') as f:
            with open('lib/header.objlib', 'rb') as fin:
                f.write(fin.read())

            write_string(f, level_config['objlib_path'])

            with open('lib/obj_list_1.objlib', 'rb') as fin:
                f.write(fin.read())
            write_int(f, 63 + obj_count)
            with open('lib/obj_list_2.objlib', 'rb') as fin:
                f.write(fin.read())
            for obj in objs:
                if obj['obj_type'] in obj_types:
                    write_hash(f, obj['obj_type'])
                    write_string(f, obj['obj_name'])

            with open('lib/obj_def_'+level_name+'.objlib', 'rb') as fin:
                f.write(fin.read())
            for obj in objs:
                if obj['obj_type'] == 'SequinLeaf':
                    write_leaf_header(f)
                    write_anim_comp(f)
                    write_leaf_comp(f, obj)
                    write_leaf_footer(f, obj)
                elif obj['obj_type'] == 'SequinLevel':
                    write_lvl_header(f)
                    write_approach_anim_comp(f, obj)
                    write_lvl_comp(f, obj)
                    write_lvl_footer(f, obj)
                elif obj['obj_type'] == 'SequinGate':
                    write_gate_header(f)
                    write_gate_comp(f, obj)
                    write_gate_footer(f, obj)
                elif obj['obj_type'] == 'SequinMaster':
                    write_master_header(f)
                    write_anim_comp(f)
                    write_master_comp(f, obj)
                    write_master_footer(f, obj)
                elif obj['obj_type'] == 'EntitySpawner':
                    write_spn_header(f)
                    write_spn_comp(f)
                    write_xfm_comp(f, obj)
                    write_spn_footer(f, obj)
                elif obj['obj_type'] == 'Sample':
                    write_samp_header(f)
                    write_samp_comp(f, obj)
                elif obj['obj_type'] == 'Xfmer':
                    write_xfm_header(f)
                    write_xfm_comp(f, obj)

            with open('lib/footer_1.objlib', 'rb') as fin:
                f.write(fin.read())
            write_float(f, level_config['bpm'])
            with open('lib/footer_2.objlib', 'rb') as fin:
                f.write(fin.read())

            src_filenames.append(cache_filename)

        config_cache_filename = 'out/'+level_name+'/'+level_config['config_cache_filename']
        with open(config_cache_filename, 'wb') as f:
            write_int(f, 9)
            write_int(f, len(level_config['level_sections']))
            for level_section in level_config['level_sections']:
                write_string(f, level_section)
            write_color(f, level_config['rails_color'])
            write_color(f, level_config['rails_glow_color'])
            write_color(f, level_config['path_color'])
            write_color(f, level_config['joy_color'])

            src_filenames.append(config_cache_filename)

    for src_filename in src_filenames:
        shutil.copy(src_filename, game_dir+'/cache')

def restore_levels(game_dir):
    src_filenames = ['lib/original/2e7b0500.pc',
                     'lib/original/e0c51024.pc',
                     'lib/original/f78b7d78.pc']
    custom_filenames = []

    for level_name in level_names:
        for filename in os.listdir('out/'+level_name):
            custom_filenames.append(filename)
    
    for src_filename in src_filenames:
        shutil.copy(src_filename, game_dir+'/cache')
    for custom_filename in custom_filenames:
        dst_filename = game_dir+'/cache/'+custom_filename
        if os.path.exists(dst_filename):
            os.remove(dst_filename)
