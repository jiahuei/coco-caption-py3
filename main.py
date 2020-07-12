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

    for i, out_file in enumerate(("res_{}.json", "res_detailed_{}.json")):
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

    for k in res_a[0].keys():
        assert abs(res_a[0][k] - res_a[1][k]) < 0.00001, \
            f"`res_a` overall {k} mismatch: {res_a[0][k]} (py2)    {res_a[1][k]} (py3)"
        assert abs(res_b[0][k] - res_b[1][k]) < 0.00001, \
            f"`res_b` overall {k} mismatch: {res_a[0][k]} (py2)    {res_a[1][k]} (py3)"


def check_detailed_score():
    def load_json_to_dict(fp):
        data = {}
        with open(fp, "r") as ff:
            sc = json.load(ff)
        for _ in sc:
            data[_["image_id"]] = _
        return data

    good_ids = [151842, 275015, 413043, 112608, 315976, 365711]
    res_a = [
        load_json_to_dict(os.path.join(TEST_DIR, "scores_py2", "res_detailed_a.json")),
        load_json_to_dict(os.path.join(SCORE_DIR, "res_detailed_a.json"))
    ]
    res_b = [
        load_json_to_dict(os.path.join(TEST_DIR, "scores_py2", "res_detailed_b.json")),
        load_json_to_dict(os.path.join(SCORE_DIR, "res_detailed_b.json"))
    ]

    for imgid in res_a[0].keys():
        for k in res_a[0][imgid].keys():
            if k == "image_id":
                continue
            elif k == "SPICE":
                py2, py3 = res_a[0][imgid][k]['All']['f'], res_a[1][imgid][k]['All']['f']
                if py3 > 0.01:
                    assert imgid in good_ids
            else:
                py2, py3 = res_a[0][imgid][k], res_a[1][imgid][k]
                if py3 > 0.5:
                    assert imgid in good_ids
            assert abs(py2 - py3) < 0.00001, \
                f"`res_detailed_a` {k} mismatch: {py2} (py2)    {py3} (py3)"

    for imgid in res_b[0].keys():
        for k in res_b[0][imgid].keys():
            if k == "image_id":
                continue
            elif k == "SPICE":
                py2, py3 = res_b[0][imgid][k]['All']['f'], res_b[1][imgid][k]['All']['f']
            else:
                py2, py3 = res_b[0][imgid][k], res_b[1][imgid][k]
            assert abs(py2 - py3) < 0.00001, \
                f"`res_detailed_a` {k} mismatch: {py2} (py2)    {py3} (py3)"


if __name__ == "__main__":
    if not (
            os.path.isfile(os.path.join(SCORE_DIR, "res_detailed_a.json")) and
            os.path.isfile(os.path.join(SCORE_DIR, "res_detailed_b.json"))
    ):
        save_results()
    check_overall_score()
    check_detailed_score()
