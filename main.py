# -*- coding: utf-8 -*-
"""
Created on 11 Jul 2020 18:34:14
@author: jiahuei
"""

import os
import json
import platform
from coco_caption.eval import evaluate_caption_json

assert platform.python_version().startswith("3.6")
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DIR = os.path.join(CURR_DIR, "tests")
SCORE_DIR = os.path.join(CURR_DIR, "scores")


def save_results():
    res_a = evaluate_caption_json(
        res_file=os.path.join(TEST_DIR, "test_a.json"), ann_file="captions_val2014.json"
    )
    res_b = evaluate_caption_json(
        res_file=os.path.join(TEST_DIR, "test_b.json"), ann_file="captions_val2014.json"
    )
    if not os.path.isdir(os.path.join(CURR_DIR, "scores")):
        os.makedirs(os.path.join(CURR_DIR, "scores"))

    for i, out_file in enumerate(("res_{}.json", "res_detailed_{}.json")):
        with open(os.path.join(SCORE_DIR, out_file.format("a")), "w") as f:
            json.dump(res_a[i], f)

    for i, out_file in enumerate(("res_{}", "res_detailed_{}")):
        with open(os.path.join(SCORE_DIR, out_file.format("b")), "w") as f:
            json.dump(res_b[i], f)


def check_overall_score():
    res_a = []
    with open(os.path.join(TEST_DIR, "scores_py2", "res_a.json"), "r") as f:
        res_a.append(json.load(f))
    with open(os.path.join(SCORE_DIR, "res_a.json"), "r") as f:
        res_a.append(json.load(f))
    res_b = []
    with open(os.path.join(TEST_DIR, "scores_py2", "res_b.json"), "r") as f:
        res_b.append(json.load(f))
    with open(os.path.join(SCORE_DIR, "res_b.json"), "r") as f:
        res_b.append(json.load(f))

    assert res_a[0] == res_a[1] and res_b[0] == res_b[1], "Python 2 and 3 overall results mismatch."


def check_detailed_score():
    res_a = []
    with open(os.path.join(TEST_DIR, "scores_py2", "res_a_detailed.json"), "r") as f:
        res_a.append(json.load(f))
    with open(os.path.join(SCORE_DIR, "res_a_detailed.json"), "r") as f:
        res_a.append(json.load(f))
    res_b = []
    with open(os.path.join(TEST_DIR, "scores_py2", "res_b_detailed.json"), "r") as f:
        res_b.append(json.load(f))
    with open(os.path.join(SCORE_DIR, "res_b_detailed.json"), "r") as f:
        res_b.append(json.load(f))

    assert res_a[0] == res_a[1] and res_b[0] == res_b[1], "Python 2 and 3 detailed results mismatch."


if __name__ == "__main__":
    save_results()
    check_overall_score()
    check_detailed_score()
