from flask import Flask, render_template, request, redirect
import os
import csv
import json

app = Flask(__name__)
#ANNO_FOLDER = r'C:\Users\srip_face\PycharmProjects\review_reject\static\list'
# ANNO_FOLDER = r'C:\Users\srip_face\PycharmProjects\review_reject\static\list'
ANNO_FOLDER = '/data3/srip_face/diving/code/Label_review/reject_file/csv/' #for server
VID_HTTP_BASE = "http://svcl.ucsd.edu/~yingwei/internal/diving_share/firstphase/video_first10/"
VID_HTTP_BASE_ = "http://svcl.ucsd.edu/~yingwei/internal/diving_share/firstphase/vid_A/"


def _load_anno(video_id):
    anno_path = os.path.join(ANNO_FOLDER, video_id+'.csv')
    if os.path.exists(anno_path):
        data_ = []
        with open(anno_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data_.append(row)
        return data_
    return []


def generate_reject_file(file_name, data, lst):
    file_header = ["HITId", "HITTypeId", "Title", "Description", "Keywords", "Reward",
                   "CreationTime", "MaxAssignments", "RequesterAnnotation",
                   "AssignmentDurationInSeconds", "AutoApprovalDelayInSeconds", "Expiration",
                   "NumberOfSimilarHITs", "LifetimeInSeconds", "AssignmentId", "WorkerId",
                   "AssignmentStatus", "AcceptTime", "SubmitTime", "AutoApprovalTime",
                   "ApprovalTime", "RejectionTime", "RequesterFeedback", "WorkTimeInSeconds",
                   "LifetimeApprovalRate", "Last30DaysApprovalRate", "Last7DaysApprovalRate",
                   "Input.vid_url", "Answer.answer", "Approve", "Reject"]
    anno_path = os.path.join(ANNO_FOLDER, file_name + '.csv')
    with open(anno_path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=file_header)
        writer.writeheader()
        for idx, row in enumerate(data):
            if idx not in lst:
                writer.writerow(row)
                continue
            if row["Approve"] == 'x':
                row["Approve"] = None
                if len(file_name) == 15:
                    row["Reject"] = 'You only label one or less instance which doesn\'t meet our demand.'
                else:
                    row["Reject"] = 'Your submission doesn\'t meet our demand.'
            else:
                row["Approve"] = 'x'
                row["Reject"] = None
            writer.writerow(row)


@app.route('/')
def form():
    entry_list = []
    video_dir = ANNO_FOLDER
    for file_ in os.listdir(video_dir):
        if file_.endswith(".csv"):
            video_id = os.path.splitext(os.path.basename(file_))[0]

            anno = _load_anno(video_id)
            entry = dict(video_id=video_id, n_annotation=len(anno))
            entry_list.append(entry)
    print('render index page')
    return render_template("index.html", entry_list=entry_list)


@app.route('/transform', methods=["GET", "POST"])
def transform_view():
    video_id = request.args.get('id', None)
    anno = _load_anno(video_id)
    return render_template('review_list.html', entry_list=anno, f_id=video_id)


@app.route('/tool', methods=['GET', 'POST'])
def naive_tool():
    assignment_id = request.args.get('id', None)
    f_id = request.args.get('fid', None)
    anno = _load_anno(f_id)
    # test = [i['Input.vid_url'].split('/')[-1].split('.')[0] for i in anno]
    test = [i['AssignmentId'] for i in anno]
    idx = test.index(assignment_id)
    video_url = anno[idx]['Input.vid_url']
    tmp_data = json.loads(anno[idx]['Answer.answer'])
    if isinstance(tmp_data, dict):
        data_ = []
    else:
        data_ = tmp_data[0]
    if f_id[0:3] == 'seg':
        return render_template('seg.html', vid_url=video_url, data=data_, comment=anno[idx]['Reject'])
    else:
        return render_template('trans.html', vid_url=video_url, data=data_, comment=anno[idx]['Reject'])


@app.route('/load_ajax', methods=['POST'])
def load_ajax():
    f_id = request.args.get('id', None)
    print(f_id)
    save_flag = int(request.args.get('flag', None))
    print(save_flag)
    if request.method == "POST":
        print('post!!')
        js_data = request.json
        print(js_data)
        anno = _load_anno(f_id)
        if len(js_data) != 0:
            if f_id[0:3] == 'seg':
                generate_reject_file(f_id[0:7]+'_revised', anno, js_data)
                print('redirecting')
            else:
                generate_reject_file(f_id[0:9] + '_revised', anno, js_data)
                print('redirecting')
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
