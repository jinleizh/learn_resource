#!/bin/env python
# coding=utf-8

import json
import random
import re
import string
import time
import traceback
import urllib
import urllib2

import pytesseract
from PIL import Image, ImageEnhance


def echo_success():
    print "download success\n"


def echo_fail():
    print "download fail\n"


"""
初始化请求头, 返回相应结果
"""


def init_req(req):
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    req.add_header("Accept-Encoding", "gzip, deflate")
    req.add_header("Cache-Control", "max-age=0")
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    req.add_header('Cookie', cookie)


"""
保存二进制流到文件
"""


def save_binary_to_file(response, filename):
    with open(filename, "wb") as file:
        file.write(response.read())


"""
保存文本到文件(html或者json)
"""


def save_txt_to_file(response, filename):
    with open(filename, "w+") as file:
        file.write(response.read())


"""
下载,支持单个和批量
"""


def download(url, doc, total_loop_time, total_retry_time):
    loop_time = 0
    retry_time = 0
    while loop_time < total_loop_time:
        params = {
            'conditions': '',
            'docIds': doc,
            'keyCode': ''
        }

        data = urllib.urlencode(params)
        req = urllib2.Request(url, data)
        init_req(req)
        response = urllib2.urlopen(req, timeout=10)
        content_type = response.headers['Content-Type']
        if content_type == "text/html" and retry_time < total_retry_time:
            print "sleep 5s \n"
            time.sleep(5)
            retry_time += 1
            continue

        if debug:
            print response.headers

        name = response.headers['Content-Disposition']
        m = re.match("(.*)filename=(.*)", name)
        filename = urllib.unquote(m.group(2)).decode('utf8')
        save_binary_to_file(response, filename)
        loop_time += 1
        print '=' * 60 + "\n"
        print "download==>%s.\n" % filename


"""
搜索框中搜索结果页
"""


def search(key_word):
    url = home_url + urllib.quote(key_word)
    if debug:
        print url

    req = urllib2.Request(url)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    req.add_header('Cookie', cookie)

    response = urllib2.urlopen(req, timeout=30)
    if debug:
        print response.headers

    filename = "test.html"
    save_txt_to_file(response, filename)
    print '=' * 60 + "\n"
    print "download==>%s.\n" % filename


"""
分页搜索并批量下载
"""


def searchAndDownload(url, values):
    print "download begin\n"
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36")
    req.add_header("Accept", "*/*")
    req.add_header("Connection", "keep-alive")
    req.add_header('Cookie', cookie)
    response = urllib2.urlopen(req, timeout=download_timeout)
    if debug:
        print response.headers

    retStr = response.read()
    result = json.loads(retStr)
    result = eval(result)

    if debug:
        print type(result)
        print len(result)

    first = True
    docIds = ""
    for i in xrange(len(result)):
        if result[i].get("裁判要旨段原文") is not None:
            if (first):
                docIds = "|".join((result[i]["文书ID"], result[i]["案件名称"], result[i]["裁判日期"]))
                first = False
            else:
                docIds += ","
                docIds += "|".join((result[i]["文书ID"], result[i]["案件名称"], result[i]["裁判日期"]))

    if debug:
        print docIds, '\n'

    download(download_url, docIds, 1, 1)


"""
生成guid
"""


def genGuid():
    f1 = ''.join(random.sample(string.ascii_lowercase + string.octdigits, 8))
    f2 = ''.join(random.sample(string.ascii_lowercase + string.octdigits, 4))
    f3 = ''.join(random.sample(string.ascii_lowercase + string.octdigits, 8))
    f4 = ''.join(random.sample(string.ascii_lowercase + string.octdigits, 12))
    return '-'.join([f1, f2, f3, f4])


"""
下载验证码图片
"""


def downloadYZM(url):
    print "download yzm begin ..."
    guid = genGuid()
    url = url + guid
    if debug:
        print url

    req = urllib2.Request(url)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/Png, */*;q=0.8")
    req.add_header('Cookie', cookie)

    response = urllib2.urlopen(req, timeout=5)
    if debug:
        print response.headers

    # save_binary_to_file(response, "png/" + guid + ".png")
    save_binary_to_file(response, guid + ".png")
    print "download yzm end ..."
    return guid


"""
二值化图片
"""


def get_bin_table(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table


"""
解析验证码
"""


def parseYZM(guid, psm, factor, enhance=0):
    picName = guid + ".png"
    im = Image.open(picName)
    threshold = factor
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    im = im.convert('L')
    im = im.point(table, '1')

    if enhance == 1:
        try:
            # 先变为黑白
            im = ImageEnhance.Color(im).enhance(1.0)
            im = ImageEnhance.Brightness(im).enhance(1.0)
            im = ImageEnhance.Contrast(im).enhance(2.0)
            im = ImageEnhance.Sharpness(im).enhance(0.0)
        except:
            pass

    code = pytesseract.image_to_string(im, lang="eng", config="-psm " + psm)
    return code, im


"""
非训练方式的解决方案
评估识别效果 + 出错重试
默认重试10次, 从测试数据看，10次中能正确识别一次的概率比较高
"""


def preOp(yzm_url, max_retry_time=10):
    try:
        championCode = ""
        guid = ""
        retry_time = 0
        while not championCode and retry_time < max_retry_time:
            if (retry_time < 6):
                time.sleep(0.5)
            else:
                time.sleep(1)

            print "retry time %d get yzm begin ..." % (retry_time)
            codeMap = {}
            guid = downloadYZM(yzm_url)
            print "guid=" + guid
            im = Image.open(guid + ".png")
            if debug:
                im.show()
            show_cnt = 0
            for mode in range(14):
                if 0 == mode or 2 == mode:
                    continue

                code, newIm = parseYZM(guid, str(mode), 140, 0)
                ret, new_code = isValid(code)
                if not ret:
                    continue

                print str(mode) + "===" + code + "====after parse new_code=" + new_code
                if 0 == show_cnt:
                    if debug:
                        newIm.show()
                    show_cnt = 1

                if codeMap and new_code in codeMap:
                    codeMap[new_code] = codeMap[new_code] + 1
                else:
                    codeMap.setdefault(new_code, 1)

            maxCnt = 0
            for key in codeMap:
                if maxCnt < codeMap[key]:
                    maxCnt = codeMap[key]
                    championCode = key

            print "retry time %d get yzm end ..." % (retry_time)

            retry_time = retry_time + 1

            print codeMap

        codeList = []
        adjust(codeList, championCode)
        return guid, codeList
    except :
        traceback.print_exc()

"""
矫正验证码
5 - s
s - 5
"""
def adjust(codeList, code):
    codeList.append(code)
    for c in code:
        if c == '5':
            codeList.append(code.replace("5", "s"))
        if c == 's':
            codeList.append(code.replace("s", "5"))
        if c == 'Q':
            codeList.append(code.replace("Q", "9"))
        if c == '7':
            codeList.append(code.replace("7", "j"))

"""
 校验code合法
"""
def isValid(code):
    print code
    len = 0
    retCharSet = []
    for c in code:
        if (c >= '0' and c <= '9') or (c >= 'a' and c <= 'z') or (c >= 'A' and c <='Z'):
            len = len + 1
            retCharSet.append(c)

    if 4 == len:
        return True, ''.join(retCharSet)

    return False, ""

if __name__ == "__main__":
    # 是否打印调试信息
    debug = True

    # 超时时间, 如果下载的文件较多, 可以调大该参数，不建议太大，防止网站发现批量下载
    download_timeout = 30

    # 失败后最多重试次数, 默认重试3次，重试的时间间隔为3s
    max_retry_time = 3

    # Cookie 网站cookie只在一段时间内有效，当cookie失效时，只需要手动打开浏览器，访问下网站，通过chrome浏览器查看到cookie值，将cookie
    # 拷贝到此处即可继续访问网站
    cookie = 'FSSBBIl1UgzbN7N80S=O3TNSgYcV9WFLzlXB0tsPPRdMVLwXQOdxDdsas9yirdjlHB.rngwjkvhmUmdABT8; ASP.NET_SessionId=yevnk4hl4sv0430gj25d12pf; Hm_lvt_3f1a54c5a86d62407544d433f6418ef5=1483454076,1483628071; Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5=1483630318; _gsref_2116842793=http://wenshu.court.gov.cn/; _gscu_2116842793=83454076gg0viy14; _gscs_2116842793=t836303187qi7th55|pv:1; _gscbrs_2116842793=1; FSSBBIl1UgzbN7N80T=1.CHRm_n8brhw0o9um0aJuPyaHikYK3yHsCqg8VU5YwshyuwaR405wcmD9bPoWfayth8JrPXlbX8NsRb0RaXc_M2HWw72L1UXqtsuSRR.3.z3E9VxESDGF3EdTdOXCRuOO7jM4Ns_vxVn0R3e0jYbHz0wFVbM_pRxujJ3C2aqwsQaiWXAS0caTTjUzgrUAsycfNuthAdkGHhgZKNAx7sncyBD2BtR_RySd8IguxZmPfI.ic8UOEcPDgw09TU5kXYV9SiXAAqgIoyCYVKKxBb.OoOwlZWMhuYKK3lIfX55T5pN0XJIzT4CC6gE64LfMMkfBq'

    # 下载url
    download_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateListDocZip.aspx?action=1"

    # 主页-全文搜索框url
    home_url = "http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+QWJS+++"

    # 分页搜索url
    page_url = "http://wenshu.court.gov.cn/List/ListContent?MmEwMD=1cQYd7ALgH.p4wz5Y78j.FEOKb9RudnON_QF865J3Z6xzARoKapX30LIGJWgf2hjIOfl.LE0PHllH_uZ1aF09sSZW0t_BrFqaMNj81QZfg.PbQ1LFG7HfPiF8A0DBjGIhpM91lFOMnJQJAmC1xRSsyVJSQIkzi639fv7TZvtM7cDCvU.WlJB7CBEcl1683S4E.JvSGEFqKY42vY.UhoUbAsOa9fibHIBnmpldRGP2NL1_yCj6WBxNV9zcQ_pEQt9ExCXNCzItugvIJBkwMX3PlNs85rBTLNipTlkUasObyhzDKptjyX985sCNFdn9VLL4KGT0gWkMDIugztjtjpjb8MaJonKnVRzLMY4aqcPlRiV7gO3Aj2Jum5TSPcIqeOsnS6"

    # 验证码url
    yzm_url = "http://wenshu.court.gov.cn/ValiCode/CreateCode/?guid="

    # Param:搜索的关键字
    # Index:第几页
    # Page: 每页有几条结果
    # Order: 按哪个层级排序
    # Direction: 升序asc 降序desc
    values = {
        'Param': '全文检索:医药',
        'Index': 1,
        'Page': 5,
        'Order': '法院层级',
        'Direction': 'asc'
    }

    """
    retry_time = 0
    success = False
    while retry_time < max_retry_time:
        try:
            searchAndDownload(page_url, values)
            success = True
        except socket.timeout, e:
            retry_time += 1
            print "begin the No.%d retry" % retry_time
            time.sleep(3)
            continue
        except Exception, e:
            traceback.print_exc()
            exit()
        else:
            echo_success()
            exit()

    if success:
        echo_success()
    else:
        echo_fail()
    """
    guid, codeList = preOp(yzm_url)
    print guid, codeList
