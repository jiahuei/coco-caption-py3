# -*- coding: utf-8 -*-
"""
Created on 11 Jul 2020 18:34:14
@author: jiahuei
"""

from coco_caption_py2.eval import evaluate_caption_json


res_a = evaluate_caption_json(res_file="test_a.json", ann_file="captions_val2014.json")
res_b = evaluate_caption_json(res_file="test_b.json", ann_file="captions_val2014.json")

pass
