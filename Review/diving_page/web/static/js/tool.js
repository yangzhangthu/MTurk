/**
 * Created by yingwei on 5/23/17.
 */
//global handles


function current_time_fn(caller_name) {
    var char_time = parseFloat(video.currentTime).toFixed(2);
    document.getElementById("time").innerHTML = char_time;
    var dom = document.getElementById(caller_name);
    if (dom)
        dom.value = char_time;
}

function time_travel(delta_t) {
    video.currentTime = video.currentTime + delta_t;
    current_time_fn('')
}

function keycontrol(e) {
    // use shortcut 's' to pause the video
    if (document.activeElement.className != "form-control") {
    // if (document.activeElement.getAttribute('type') != "text") {
        switch (e.keyCode) {
            case 70: // f
                break;
            case 32: // space
                if (video.paused) {
                    video.play();
                }
                else {
                    video.pause();
                }
                break;
            case 37: // left
                if (e.ctrlKey) {
                    time_travel(-video_step2);
                }
                else {
                    time_travel(-video_step1);
                }
                break;
            case 39:// right
                if (e.ctrlKey) {
                    time_travel(video_step2);
                }
                else {
                    time_travel(video_step1);
                }
                break;
            case 38: // up
                break;
            case 40: // down
                break;
            case 83: // s
                current_time_fn('start_time');
                break;
            case 84: // t
                current_time_fn('stop_time');
                break;
            case 74: // j
                current_time_fn('info_time');
                break;
            case 75: // k
                current_time_fn('score_time');
                break;
            default:
                break;
        }
    }
}

function save_all(save_ind) {
    var entry = {
        action1: "", action2: "", action3: "", action4: "", athelete_name: "",
        cam_dist: "", cam_view: "", difficulty: "", exe_score: 0, game_name: "", game_type: "",
        info_time: -1, score_time: -1, sex: "", slow_motion: false, start_time: -1,
        stop_time: -1, sync_score: -1, trimmed: false, type: "", video_name: "", comment: ""
    };
    for (var key in entry) {
        var dom = document.getElementById(key);
        if (dom != null)
            switch (dom.type) {
                case "text":
                    entry[key] = dom.value;
                    break;
                case "number":
                    entry[key] = Number(dom.value);
                    break;
                case "select-one":
                    entry[key] = dom[dom.selectedIndex].value;
                    break;
                case "checkbox":
                    entry[key] = dom.checked;
                    break;
                default:
                    alert('attr type not implemented: ' + dom.type);
                    break;
            }
    }
    if (save_ind == total_label) {
        console.log('It will be saved as an new entry!');
        data_json.push(entry);
        total_label = total_label + 1;
        cur_anno_ind = total_label - 1;
        review_label(cur_anno_ind)
    }
    else {
        data_json[save_ind] = entry;
        review_label(cur_anno_ind)
    }
}

function show_label() {
    // clear
    var review_btns = document.getElementById('review_btns');
    while (review_btns.firstChild) {
        review_btns.removeChild(review_btns.firstChild);
    }

    for (var t_anno_ind = 0; t_anno_ind < total_label; t_anno_ind++) {
        var t_anno_ind_str = t_anno_ind.toString();
        var btn = document.createElement("BUTTON");
        btn.id = 'label_id_' + t_anno_ind_str;
        btn.name = 'label_id_' + t_anno_ind_str;
        btn.id_num = t_anno_ind.toString();
        btn.onclick = function () {
            var anno_num = Number(this.id_num);
            review_label(anno_num);
        };
        btn.innerHTML = 'annot-' + t_anno_ind_str;
        review_btns.appendChild(btn);
    }

}

function clear_time() {
    document.getElementById("start_time").value = 0;
    document.getElementById("stop_time").value = 0;
    document.getElementById("info_time").value = 0;
    document.getElementById("score_time").value = 0;
}

function set_time(caller_name) {
    var tt = document.getElementById(caller_name).value;
    if (video.played) {
        video.pause();
    }
    video.currentTime = Number(tt);
}

function set_focus_to_video() {
    document.getElementById("the_video").focus();
}

function delete_entry() {
    data_json.splice(cur_anno_ind, 1);
    total_label = total_label - 1;
    if (cur_anno_ind >= total_label) {
        cur_anno_ind = total_label;
    }
}

function review_label(review_anno_ind) {
    if (review_anno_ind == undefined)
        cur_anno_ind = 0;
    else
        cur_anno_ind = review_anno_ind;
    if (cur_anno_ind < 0)
        cur_anno_ind = 0;

    if (cur_anno_ind >= total_label)
        cur_anno_ind = total_label-1;

    document.getElementById('stat').innerHTML = 'Current clip is ' + (cur_anno_ind).toString() + ', ' + (total_label).toString() + ' in total.';
    var entry = data_json[cur_anno_ind];
    for (var key in entry) {
        var dom = document.getElementById(key);
        if (dom != null)
            switch (dom.type) {
                case "text":
                    dom.value = entry[key];
                    break;
                case "number":
                    dom.value = entry[key];
                    break;
                case "select-one":
                    dom.value = entry[key];
                    break;
                case "checkbox":
                    dom.checked = entry[key];
                    break;
                default:
                    alert('attr type not implemented: ' + dom.type);
                    break;
            }
        else
        {
            alert('attr name not found in html: ' + key)
        }

    }

    if (entry) {
        var video = document.getElementById("the_video");
        var pausing_function = function () {
            if (this.currentTime >= entry['stop_time']) {
                this.pause();
                // remove the event listener after you paused the playback
                this.ontimeupdate = null;
            }
        };
        video.currentTime = entry['start_time'];
        video.play();
        video.ontimeupdate = pausing_function;
    }


}
// function vidVolume(delta_v) {
//                     if (video.muted) {
//                         video.muted = false;
//                         video.volume = 0.0;
//                     }
//                     video.volume = video.volume + delta_v;
//                     if (video.volume <= 0.0) {
//                         video.muted = true;
//                         video.volumn = 0.0;
//                     }
//                 }