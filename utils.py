# -*- coding: utf-8 -*-

import os
import sys
import json
import re
import stat
import shutil
from PySide.QtCore import Qt

import fbx
import FbxCommon

__all__ = [
    'pattern_exp',
    'pattern_rpl',
    'file_convert',
    'item_height',
    'item_color',
    'item_background',
    'convert',
]


pattern_exp = Qt.UserRole + 1
pattern_rpl = Qt.UserRole + 2
file_convert = Qt.UserRole + 3
item_height = Qt.UserRole + 4
item_color = Qt.UserRole + 5
item_background = Qt.UserRole + 6

basic_patterns = {
    '(?i)_qte_': '_QTE_',
    '(?i)_stp_': '_STP_',
    '(?i)_fulb_': '_FulB_',
    '(?i)_addfacial_': '_AddFacial_',
    '(?i)_miniqte_': '_MiniQTE_',
    '(?i)^[a-z]|_[a-z]': lambda m: m.group(0).upper()
}

node_patterns = {
    ': "[a-z]': lambda m: m.group(0).upper()
}


def convert(patterns, text, node=False):
    patterns = json.loads(patterns)
    for pattern in patterns:
        text = re.sub(pattern, patterns[pattern], text, flags=re.IGNORECASE)

    for pattern in basic_patterns:
        text = re.sub(pattern, basic_patterns[pattern], text)

    if node:
        text = re.sub(': "[a-z]', lambda m: m.group(0).upper(), text)

    return text


def execute(path, skeleton=None, path_new=None, patterns=None):
    message = {'path': path, 'path_new': path_new, 'takes': []}
    os.chmod(path, stat.S_IWRITE)
    (fbx_manager, fbx_scene) = FbxCommon.InitializeSdkObjects()
    status = FbxCommon.LoadScene(fbx_manager, fbx_scene, path)

    if status:
        stack_class_id = fbx.FbxAnimStack.ClassId
        stack_object_type = fbx.FbxCriteria.ObjectType(stack_class_id)
        stack_count = fbx_scene.GetSrcObjectCount(stack_object_type)
        for i in range(stack_count):
            stack = fbx_scene.GetSrcObject(stack_object_type, i)
            message['takes'].append(stack.GetName())

        if patterns:
            patterns = patterns.replace('\'', '"')
            basename = os.path.basename(path)
            path_new = os.path.join(path_new, convert(patterns, basename)).replace('\\', '/')
            message['path_new'] = path_new
            for i in range(stack_count):
                stack = fbx_scene.GetSrcObject(stack_object_type, i)
                stack.SetName(convert(patterns, stack.GetName()))
            fbx_format = fbx_manager.GetIOPluginRegistry().GetNativeWriterFormat()
            FbxCommon.SaveScene(fbx_manager, fbx_scene, path_new, fbx_format, True)
            # if path.lower() != message['path_new'].lower():
            #     os.remove(path)

            node_path = re.sub('(?i)fbx$', 'nodes', path)
            node_path_new = re.sub('(?i)fbx$', 'nodes', path_new)
            if os.path.isfile(node_path):
                os.chmod(node_path, stat.S_IWRITE)
                with open(node_path) as node:
                    node_data = json.dumps(json.load(node))
                skeleton = skeleton.replace('\\', '\\\\\\\\')
                name_replacer = lambda m: convert(patterns, m.group(0), True)
                node_data_new = re.sub('"name": "(.*?)"', name_replacer, node_data)
                node_data_new = re.sub('"take": "(.*?)"', name_replacer, node_data_new)
                node_data_new = re.sub('"path": "(.*?)"', '"path": "%s"' % skeleton, node_data_new)
                node_data_new = json.loads(node_data_new)
                # os.remove(node_path)
                with open(node_path_new, 'w') as node:
                    json.dump(node_data_new, node, indent=4, sort_keys=True)

    fbm_path = re.sub('(?i)fbx$', 'fbm', path)
    if os.path.isdir(fbm_path):
        shutil.rmtree(fbm_path)
    elif os.path.isfile(fbm_path):
        os.remove(fbm_path)

    return json.dumps(message)


if __name__ == '__main__':
    print(execute(*sys.argv[1:]))
    sys.exit()
