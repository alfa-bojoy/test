# coding: utf-8

"""Train tickets query via command-line.

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options: 
    -h,--help        显示帮助菜单
    -g               高铁
    -d               动车
    -t               特快
    -k               快速
    -z               直达

Example:
    tickets 南京 北京 2016-07-01
    tickets -dg 南京 北京 2016-07-01
"""


# 车次 				    出发车站 			到达车站 		发车时间 	商务 	特等 	一等 	二等 	高级软卧 	软卧 	硬卧 	软座 	硬座 	无座
# station_train_code	from_station_name	to_station_name	start_time	swz_num	tz_num	zy_num	ze_num	gr_num		rw_num	yw_num	rz_num	yz_num	wz_num
from docopt import docopt
from stations import stations
import requests
import json
from pylsy import pylsytable
import sys
reload(sys)
sys.setdefaultencoding('utf8')

dict_keys=[['station_train_code','from_station_name','to_station_name','start_time','swz_num',
    'tz_num','zy_num','ze_num','gr_num','rw_num','yw_num','rz_num','yz_num','wz_num'],
    [u'车次',u'出发地',u'目的地',u'发车时间',u'商务',u'特等',u'一等',u'二等',u'高级软卧',u'软卧',u'硬卧',u'软座',u'硬座',u'无座']]

def get_data(date,from_station,to_station):
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT'%(date,from_station,to_station)
    r = requests.get(url, verify=False)
    return r


def data_pro(source_data):
    des_data=[]
    data_row={}
    keys=dict_keys[0]
    r=source_data.json()['data']
    data_len=len(r)
    for i in range(data_len):
        data_row={}
        for j in keys:
            data_row[j]=r[i]['queryLeftNewDTO'][j]
        des_data.append(data_row)
    return des_data

def format_print(data):
    attributes=dict_keys[1]
    table=pylsytable(attributes)
    for temp in data:
        for i in range(len(temp)):
            table.append_data(dict_keys[1][i],temp[dict_keys[0][i]])
    print table
    



def cli():
    arguments = docopt(__doc__)
    from_staion = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    r = get_data(date,from_staion,to_station)
    rows = data_pro(r)
    format_print(rows)
#    print json.dumps(rows, encoding="UTF-8", ensure_ascii=False)
#字典、列表、元组中有中文是打印的方法

if __name__ == '__main__': 
    cli()

