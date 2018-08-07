# -*- coding: utf-8 -*-

import os
import sys
import json
import re
from PyQt5.QtCore import Qt

import fbx
import FbxCommon

__all__ = [
    'pattern_exp',
    'pattern_rpl',
    'file_convert',
    'item_height',
    'item_color',
    'item_background',
    'basic_patterns',
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
    '(?i)^[a-z]|_[a-z]': lambda m: m.group(0).upper()
}


def convert(patterns, text):
    patterns = json.loads(patterns)
    for pattern in patterns:
        text = re.sub(pattern, patterns[pattern], text, flags=re.IGNORECASE)

    for pattern in basic_patterns:
        text = re.sub(pattern, basic_patterns[pattern], text)

    return text


if __name__ == '__main__':
    message = {'path': sys.argv[1]}
    (fbx_manager, fbx_scene) = FbxCommon.InitializeSdkObjects()
    status = FbxCommon.LoadScene(fbx_manager, fbx_scene, message['path'])

    if status:
        stack_class_id = fbx.FbxAnimStack.ClassId
        stack_object_type = fbx.FbxCriteria.ObjectType(stack_class_id)
        stack_count = fbx_scene.GetSrcObjectCount(stack_object_type)

        try:
            pattern_list = sys.argv[2].replace('\'', '"')
            dirname = os.path.dirname(message['path'])
            basename = os.path.basename(message['path'])
            message['path_new'] = os.path.join(dirname, convert(pattern_list, basename))
            for i in range(stack_count):
                stack = fbx_scene.GetSrcObject(stack_object_type, i)
                stack.SetName(convert(pattern_list, stack.GetName()))
            fbx_format = fbx_manager.GetIOPluginRegistry().GetNativeWriterFormat()
            FbxCommon.SaveScene(fbx_manager, fbx_scene, message['path_new'], fbx_format, True)
            os.remove(message['path'])

        except IndexError:
            message['takes'] = []
            for i in range(stack_count):
                stack = fbx_scene.GetSrcObject(stack_object_type, i)
                message['takes'].append(stack.GetName())

    print(json.dumps(message))

    sys.exit()
