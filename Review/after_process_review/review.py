from flask import Flask, render_template, request
import os
import csv
import json

app = Flask(__name__)
ANNO_FOLDER = '/data3/srip_face/diving/code/Label_review/result/'
VID_HTTP_BASE = "http://svcl.ucsd.edu/~yingwei/internal/diving_share/firstphase/video_first10/"
VID_HTTP_BASE_ = "http://svcl.ucsd.edu/~yingwei/internal/diving_share/firstphase/vid_A/"


def _load_anno(video_id):
    anno_path = os.path.join(ANNO_FOLDER, video_id+'.json')
    if os.path.exists(anno_path):
        with open(anno_path, 'r') as f:
            anno = json.load(f)
        return anno
    return []


@app.route('/')
def form():
    entry_list = []
    video_dir = ANNO_FOLDER
    for file in os.listdir(video_dir):
        if file.endswith(".json") and file.startswith('seg'):
            video_id = os.path.splitext(os.path.basename(file))[0]

            anno = _load_anno(video_id)
            if len(anno)>1:
                entry = dict(video_id=video_id, n_annotation=len(anno))
                entry_list.append(entry)

    return render_template("index.html", entry_list=entry_list)


@app.route('/transform', methods=["GET", "POST"])
def transform_view():
    video_id = request.args.get('id', None)
    anno = _load_anno(video_id)
    return render_template('review_list.html', entry_list=anno, f_id=video_id)


@app.route('/tool', methods=['GET', 'POST'])
def naive_tool():
    video_id = request.args.get('id', None)
    f_id = request.args.get('fid', None)
    anno = _load_anno(f_id)
    test = [i[0] for i in anno]
    idx = test.index(video_id)
    anno2 = _load_anno('trans'+f_id[3:7])
    test_ = [i['video'] for i in anno2]
    idx_ = test_.index(video_id)
    if float(f_id[-3:])>10:
        return render_template('tool2.html', vid_url=VID_HTTP_BASE_+video_id+'.mp4', data=anno[idx][1], data_=anno2[idx_])
    return render_template('tool2.html', vid_url=VID_HTTP_BASE+video_id+'.mp4', data=anno[idx][1], data_=anno2[idx_])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
