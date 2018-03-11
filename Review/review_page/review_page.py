from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)
ANNO_FOLDER = '/data3/srip_face/diving/code/find_board/board_location/'
VID_HTTP_BASE = "http://svcl.ucsd.edu/~yingwei/internal/diving/"


def _load_anno(video_id):
    anno_path = os.path.join(ANNO_FOLDER, video_id+'.json')
    if os.path.exists(anno_path):
        with open(anno_path, 'r') as f:
            anno = json.load(f)
        return anno
    return []


def _load_senet_only():
    with open("/data3/srip_face/diving/code/video_select/video_A.json", 'r') as f:
        data = json.load(f)
    gn = []
    for itm in data:
        if itm['game_name'][0:5] == 'Senet':
            gn.append(itm['video_name'])
    return gn


def len2(ann):
    c = 0
    for i in ann:
        if i[1]==0:
            c+=1
    return c


@app.route('/')
def index():
    entry_list = []
    count_instance = 0
    video_dir = ANNO_FOLDER
    gn = _load_senet_only()
    for file in os.listdir(video_dir):
        if file.endswith(".json"):
            video_id = os.path.splitext(os.path.basename(file))[0]

            anno = _load_anno(video_id)
            if len(anno)>1:
                count_instance += len2(anno)
                entry = dict(video_id=video_id, n_annotation=len2(anno))
                entry_list.append(entry)

    return render_template("index.html", entry_list=entry_list, count_instance=count_instance )


@app.route('/tool', methods=['GET', 'POST'])
def naive_tool():
    video_id = request.args.get('id', None)
    if 'part' not in video_id:
        video_uri = VID_HTTP_BASE + video_id + ".mp4"
    else:
        video_uri = 'http://svcl.ucsd.edu/~yingwei/internal/diving_share/firstphase/video_24/' + video_id + ".mp4"
    json_uri = os.path.join(ANNO_FOLDER, video_id + ".json")

    if os.path.exists(json_uri):
        with open(json_uri) as f:
            data = json.load(f)
        return render_template('tool.html', video_source=video_uri, data=data, video_id=video_id)
    else:
        return render_template('tool.html', video_source=video_uri, data=[], video_id=video_id)


@app.route('/load_ajax', methods=['POST'])
def load_ajax():
    video_id = request.args.get('id', None)
    save_flag = int(request.args.get('flag', None))
    if request.method == "POST":
        print('post!!')
        if save_flag == 1:
            print('save_flage is 1')
            js_data = request.json
            json_name = video_id + '.json'

            json_path = os.path.join(ANNO_FOLDER, json_name)
            # check if dup
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    old_js_data = json.load(f)
                if js_data == old_js_data:
                    return 'ok'

            with open(json_path, 'w') as f:
                json.dump(js_data, f)
                print('save data')
            return 'ok'
        else:
            return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=6070)
