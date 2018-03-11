from flask import Flask, render_template, request, redirect, url_for
import os
import json
from os import listdir
from os.path import isfile, join
from shutil import copyfile

app = Flask(__name__)
#VID_FOLDER = '/data3/yingwei/vidDB/diving/vid_640'
VID_FOLDER = '/data4/srip_face/video/vid_24/'
ANNO_FOLDER = '/data4/srip_face/video/anno_24/'
#ANNO_FOLDER = '/data3/srip_face/diving/code/Web_page/diving_page/web/anno'
#ANNO_FOLDER = '/data3/yingwei/vidDB/diving/annotation_first20'
#ANNO_FOLDER = '/data3/srip_face/diving/code/board_json_file'
ANNO_BAK_FOLDER = '/data4/srip_face/video/anno_24_bak/'
#ANNO_BAK_FOLDER = '/data3/srip_face/diving/code/Web_page/diving_page/web/anno_bak'
#ANNO_BAK_FOLDER = '/data3/yingwei/vidDB/diving/annotation_first20_bak'
#ANNO_BAK_FOLDER = '/data3/srip_face/diving/code/board_json_file_bak'
#VID_HTTP_BASE = "http://svcl.ucsd.edu/~yingwei/internal/diving/"
VID_HTTP_BASE = 'http://svcl.ucsd.edu/~yingwei/internal/diving_share/firstphase/video_24/'
INFO_FOLDER = '/data3/jason/diving_videos'

@app.route('/', methods=['POST'])
def index_post():

    filter_tag = request.form['filter_tag']

    return redirect(url_for('index', filter_tag_str=filter_tag))

def _load_youtube_info(video_id):
    info_path = os.path.join(INFO_FOLDER, video_id + '.info.json')
    if not os.path.exists(info_path):
        return {}
    else:
        with open(info_path, 'r') as f:
            info = json.load(f)
        return info

def _filter_tag(video_id, filter_tag_str=''):
    info_path = os.path.join(INFO_FOLDER, video_id + '.info.json')
    if not os.path.exists(info_path):
        return True

    with open(info_path, 'r') as f:
        info = json.load(f)
        tags = info['tags']
        if len(tags) == 0:
            pass
        for label in tags:
            if filter_tag_str in label:
                return True

    return False

def _load_anno(video_id):
    anno_path = os.path.join(ANNO_FOLDER, video_id+'.json')
    if os.path.exists(anno_path):
        with open(anno_path, 'r') as f:
            anno = json.load(f)
        return anno
    return []
# @app.route("/", defaults={'filter_tag_str': ''})
# @app.route("/<string:filter_tag_str>")
# def index(filter_tag_str):
#
#     entry_list = []
#     video_dir = VID_FOLDER
#     for file in os.listdir(video_dir):
#         if file.endswith(".mp4"):
#             video_id = os.path.splitext(os.path.basename(file))[0]
#             # filter logic
#             if _filter_tag(video_id, filter_tag_str=filter_tag_str):
#                 # TODO: add read json logic
#                 anno = _load_anno(video_id)
#                 entry = dict(video_id=video_id, n_annotation=len(anno))
#
#                 entry_list.append(entry)
#
#     return render_template("index.html", entry_list=entry_list, filter_tag_str=filter_tag_str)

@app.route("/", defaults={'filter_tag_str': ''})
@app.route("/<string:filter_tag_str>")
def index(filter_tag_str):

    entry_list = []
    video_dir = ANNO_FOLDER
    for file in os.listdir(video_dir):
        if file.endswith(".json"):
            video_id = os.path.splitext(os.path.basename(file))[0]
            ## filter logic
            #if _filter_tag(video_id, filter_tag_str=filter_tag_str):
            # TODO: add read json logic
            anno = _load_anno(video_id)
            entry = dict(video_id=video_id, n_annotation=len(anno))

            entry_list.append(entry)

    return render_template("index.html", entry_list=entry_list, filter_tag_str=filter_tag_str)



# this is deprecated
# @app.route('/', methods=['GET', 'POST'])
# def yang_index():
#     # json_path = app.static_folder
#     # json_files = [f for f in listdir(json_path) if isfile(join(json_path, f))]
#     video_path = VID_FOLDER
#     video_files = [f for f in listdir(video_path) if isfile(join(video_path, f))]
#     list_video = []
#     for v in video_files:
#         tmp = v.split('.')
#         list_video.append({'id': tmp[0]})
#
#     return render_template('list.html', list_video=list_video)


@app.route('/tool', methods=['GET', 'POST'])
def naive_tool():
    video_id = request.args.get('id', None)
    video_uri = VID_HTTP_BASE + video_id + ".mp4"
    json_uri = os.path.join(ANNO_FOLDER, video_id + ".json")
    youtube_info = _load_youtube_info(video_id)

    if os.path.exists(json_uri):
        with open(json_uri) as f:
            data = json.load(f)
        return render_template('tool.html', video_source=video_uri, data=data, video_id=video_id, title='',
                               description='', tags='')
    else:
        return render_template('tool.html', video_source=video_uri, data=[], video_id=video_id, title='',
                               description='', tags='')


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

            # backup logic
            bak_json_path = os.path.join(ANNO_BAK_FOLDER, json_name)
            if os.path.exists(json_path):
                copyfile(json_path, bak_json_path)

            with open(json_path, 'w') as f:
                json.dump(js_data, f)
                print('save data')
            return 'ok'
        else:
            return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=6080)
