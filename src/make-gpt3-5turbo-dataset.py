import os
import copy
from itertools import count
import json
import pickle
import numpy as np
import jsonlines
import matplotlib.pyplot as plt
import csv
CSV_FILE_PATH = './evogym-design-tool/exported/caption-v2.csv'
JSONL_FILE_PATH = './dataset/gpt3-5turbo-dataset-v4.jsonl'

def get_caption_by_index(CSV_FILE_PATH, target_index):
    with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for idx, row in enumerate(csv_reader, start=1):
            if idx == target_index:
                caption_en = row['caption-en-v2']
                return caption_en
    return None  

# open json file
path = './evogym-design-tool/exported/'
for i in range(104, 217):  # a104.json から a216.json までループ(100*20sizeのデータセットのみ)
    print("count:",i)
    index = i
    file_name = f'a{i}.json'
    env_file = os.path.join(path, file_name)

    with open(env_file) as f:
        env_json = json.load(f)
    
    width, height = env_json['grid_width'], env_json['grid_height']
    text = np.full((height,width),'-')
    for platform in env_json['objects'].values():
        for idx, t in zip(platform['indices'],platform['types']):
            x = idx % width
            y = idx // width

            if t==2: 
                color = [0.7,0.7,0.7]
                text[y,x] = 'S'
            else:
                color = 'k'
                text[y,x] = 'H'
    text1 = np.flipud(text)

    Text = []
    for i in text1:
        t = "".join(i)
        Text.append(t)

    caption = get_caption_by_index(CSV_FILE_PATH, index)
    caption = f"{width}*{height} size " + caption
    system_text = "The environment in reinforcement learning, where the agent progresses from left to right, is represented by a list of strings, one character per block. The following conditions are applied: '-' is a blank block, 'H' is a hard block, and 'S' is a soft block. The agent can walk on the 'H' and 'S' blocks and can exist in the '-' area. If there is no 'H' or 'S' block under the agent, it will fall. Please return a list that predicts what kind of environment it is from a prompt that describes the given environment. Please make all elements in the list have the same length. Also, only allow '-' , 'H', and 'S' characters in the elements. Please return with the specified character length. Do not output anything other than a list."

    # JSONLファイルに保存するためのデータ作成
    data = {
        "messages": [
            {"role":"system","content":str(system_text)},
            {"role":"user","content":str(caption)},
            {"role":"assistant","content":str(Text)}
        ]}

    with jsonlines.open(JSONL_FILE_PATH, mode='a') as writer:  # 'a'モードで追記
        writer.write(data)

print(f"データが{JSONL_FILE_PATH}に追加されました。")
