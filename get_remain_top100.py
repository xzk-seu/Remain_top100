import requests
import json
import random
from Logger import logger
import warnings
import time
import os
from multiprocessing import Pool
warnings.filterwarnings("ignore")

_MAXRETRY = 6
_ERRORMESSAGE = "id: {0} | Error: {1}"
_INFOMESSAGE = "id: {0} has done."
_RESULT_PATH = os.path.join(os.getcwd(), "result", "top100author")
_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'academic.microsoft.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235',
}

proxyHost = "http-proxy-sg2.dobel.cn"
proxyPort = "9180"
proxyUser = "DONGNANHTT1"
proxyPass = "T74B13bQ"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,

    "pass": proxyPass,
}
_PROXIES = {
    "http": proxyMeta,
    "https": proxyMeta,
}


_HOST = 'https://academic.microsoft.com/api/etap/author/TopAuthors'
_SESSION = requests.session()


def _get_request(url, param):
    resp = _SESSION.get(
        url,
        params=param,
        headers=_HEADERS,
        proxies=_PROXIES,
        # verify=False,
        timeout=random.choice(range(30, 100))
    )
    resp.encoding = "utf-8"
    if resp.status_code == 200:
        return resp.text
    else:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))


def get_top100_author(fos_id, p, remain_id):
    tries = 0
    js = dict()
    param = {'fosid': fos_id,
             'filter': p[0],
             'dateRange': p[1]}
    while tries < _MAXRETRY:
        tries += 1
        try:
            html = _get_request(_HOST, param)
            js = json.loads(html.strip())
            break
        except Exception as e:
            if tries < _MAXRETRY:
                logger.info(_ERRORMESSAGE.format(str(fos_id), str(e)) + " | tries: %d" % tries)
            else:
                logger.error(_ERRORMESSAGE.format(str(fos_id), str(e)) + " | tries: %d" % tries)
            time.sleep(tries)

    if not list(js):
        return js
    # res_list = list()
    # for d in js:
    #     res_list.append(d['id'])
    logger.info(str(fos_id))
    path = os.path.join(os.getcwd(), 'result', 'remain_%d' % remain_id, '%d_%d_%d' % (int(fos_id), p[0], p[1]))
    with open(path, 'w') as fw:
        json.dump(js, fw)
        # for r in res_list:
        #     fw.write(str(r)+'\n')


def get_fos_list(remain_id):
    path = os.path.join(os.getcwd(), 'remain_FOS', 'remain_fos%d' % remain_id)
    res_list = list()
    with open(path, 'r') as fr:
        js = json.load(fr)
    res_path = os.path.join(os.getcwd(), 'result', 'remain_%d' % remain_id)
    if not os.path.exists(res_path):
        os.makedirs(res_path)

    p1 = [1, 3, 4]
    p2 = [1, 4, 3]
    p_list = [(i, j) for i in p1 for j in p2]
    exsiting = os.listdir(res_path)
    logger.info('total is %d' % len(js))
    logger.info('existing is %d' % (len(exsiting)//9))
    for fos in js:
        for p in p_list:
            task_str = '%s_%d_%d' % (fos, p[0], p[1])
            if task_str not in exsiting:
                res_list.append(fos)
                break
    return res_list


def multiproc_run(f_list, remain_id):
    pool = Pool()
    p1 = [1, 3, 4]
    p2 = [1, 4, 3]
    p_list = [(i, j) for i in p1 for j in p2]
    for fos in f_list:
        for p in p_list:
            pool.apply_async(my_run, args=(fos, p, remain_id))
    pool.close()
    pool.join()


def my_run(fos_id, p, remain_id):
    try:
        get_top100_author(fos_id, p, remain_id)
    except Exception as e:
        logger.info(e)


if __name__ == '__main__':
    # i = int(input('input 0-10: '))
    # fos_list = get_fos_list(i)
    # logger.info(len(fos_list))
    # multiproc_run(fos_list, i)

    # fos_list = get_fos_list(0)
    get_top100_author('2776449238', (1, 1), 0)




