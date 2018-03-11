from flask import Flask, render_template, request
import io
import csv
import json

app = Flask(__name__)


vid_ = []
data_ = []


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route('/')
def form():
    return render_template("upload_file.html")
    # return """
    #     <html>
    #         <body>
    #             <h1>Transform a file demo</h1>
    #
    #             <form action="/transform" method="post" enctype="multipart/form-data">
    #                 <input type="file" name="data_file" />
    #                 <input type="submit" />
    #             </form>
    #         </body>
    #     </html>
    # """


@app.route('/transform', methods=["POST"])
def transform_view():
    f = request.files['data_file']
    if not f:
        return "No file"

    vid_[:] = []
    data_[:] = []
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    # print("file contents: ", file_contents)
    # print(type(file_contents))
    # print(csv_input)
    count = -1
    for row in csv_input:
        if count == -1:
            count += 1
            continue
        temp = {"video_dir": "", "video_name": "", "index": 0, "worker_name": "", "number_of_labels": 0}
        data_.append(json.loads(row[28]))
        temp["video_dir"] = row[27]
        t_vid = row[27].split('/')
        temp["video_name"] = t_vid[-1]
        temp["index"] = count
        temp["worker_name"] = row[15]
        if 'instances' in data_[count][0]:
            temp["number_of_labels"] = len(data_[count][0]["instances"])
        else:
            temp["number_of_labels"] = -1
        vid_.append(temp)
        count += 1

    # stream.seek(0)
    # result = transform(stream.read())

    # response = make_response(result)
    # response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return render_template('review_list.html', entry_list=vid_)


@app.route('/tool', methods=['GET', 'POST'])
def naive_tool():
    video_id = request.args.get('id', None)
    # video_uri = VID_HTTP_BASE + video_id + ".mp4"
    if 'instances' not in data_[int(video_id)][0]:
        return render_template('tool.html', vid_url=vid_[int(video_id)]["video_dir"], data=data_[int(video_id)])
    else:
        return render_template('tool2.html', vid_url=vid_[int(video_id)]["video_dir"], data=data_[int(video_id)])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
