import sys
import os
import glob2

input_basedir = '/data3/jason/diving_videos'


output_basedir = '/data3/yingwei/vidDB/diving/vid_640/'
n_job = 16
vid_name_list = map(lambda t: os.path.splitext(os.path.basename(t))[0], sorted(glob2.glob(os.path.join(input_basedir, '*.mp4'))))
def chunkify(lst, n):
    return [lst[i::n] for i in xrange(n)]

def extract_job(vid_inds, vid_names, input_basedir, output_basedir):
    import os
    for vid_ind, vid_name in zip(vid_inds, vid_names):
        print('converting video: {}'.format(vid_ind, vid_name))
        cmd = 'ffmpeg -y -i {} -c:v libx264 -crf 22 ' \
              ' -movflags faststart -s 640x480 {}'.format(
            os.path.join(input_basedir, vid_name + '.mp4'),
            os.path.join(output_basedir, vid_name + '.mp4')
        )
        os.system(cmd)
    return 0

def main():
    from ipyparallel import Client
    rc = Client(profile='mpi')
    workers = rc.load_balanced_view()
    jobs = []
    batches = chunkify(vid_name_list, n_job)
    batch_inds = chunkify(range(len(vid_name_list)), n_job)
    for i in range(n_job):
        print(i)
        jobs.append(workers.apply_async(extract_job, *(batch_inds[i], batches[i], input_basedir, output_basedir)))

    for i in range(n_job):
        print(jobs[i].get(), i, len(jobs))

main()