import os
import json


def single_file_process(f_path):
    r_dict = dict()
    with open(f_path, 'r') as fr:
        js = json.load(fr)
    for a in js:
        if a['id'] not in r_dict.keys():
            r_dict[a['id']] = a
    return r_dict


if __name__ == '__main__':
    remain_id = int(input('remain_id: '))
    path = os.path.join(os.getcwd(), 'result', 'remain_%d' % remain_id)
    file_list = os.listdir(path)
    result_dict = dict()
    for n, file in enumerate(file_list):
        print('%d: %d/%d %s' % (remain_id, n, len(file_list), file))
        file_path = os.path.join(path, file)
        current_dict = single_file_process(file_path)
        for k, v in current_dict.items():
            if k not in result_dict.keys():
                result_dict[k] = v

    print('merge result is %d' % len(result_dict))
    result_dir = os.path.join(os.getcwd(), 'merged_result')
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    result_path = os.path.join(result_dir, 'remain_merge_%d.json' % remain_id)
    with open(result_path, 'w') as fw:
        json.dump(result_dict, fw)
