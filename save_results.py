# -*- coding: utf-8 -*-
"""
Created on 11 Jul 2020 18:34:14
@author: jiahuei
"""

import os
import json
from coco_caption_py2.eval import evaluate_caption_json

res_a = evaluate_caption_json(res_file="test_a.json", ann_file="captions_val2014.json")
res_b = evaluate_caption_json(res_file="test_b.json", ann_file="captions_val2014.json")

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
if not os.path.isdir(os.path.join(CURR_DIR, "scores")):
    os.makedirs(os.path.join(CURR_DIR, "scores"))

for i, out_file in enumerate(("res_{}", "res_detailed_{}")):
    with open(os.path.join(CURR_DIR, "scores", out_file.format("a")), "w") as f:
        json.dump(res_a[i], f)

for i, out_file in enumerate(("res_{}", "res_detailed_{}")):
    with open(os.path.join(CURR_DIR, "scores", out_file.format("b")), "w") as f:
        json.dump(res_b[i], f)
