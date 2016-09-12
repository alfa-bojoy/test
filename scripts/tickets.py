# coding: utf-8

"""Train tickets query via command-line.

Usage:
    tickets <from> <to> <date> [ --s_code=<s_code> --s_time=<time> --zx=<zx> ]

Options: 
    -h,--help               显示帮助菜单
    --s_code <s_code>       车次,可以选择一个或多个(用,分割)
    --s_time <time>         发车时间
    --zx <zx>               坐席,可以选择一个或多个(用,分割),默认是全部
                            [sw:商务,tz:特等,zy:一等,ze:二等,gr:高级软卧,rw:软卧,yw:硬卧,rz:软座,yz:硬座,wz:无座]


Example:
    tickets 上海 长春 2016-07-01
    tickets 上海 长春 2016-07-01 --s_code='G1258,Z172' --s_time='18:00' --zx='yz,rz'
"""

# 车次 				    出发车站 			到达车站 		发车时间 	
# station_train_code	from_station_name	to_station_name	start_time	


#商务 	    特等 	一等 	二等 	高级软卧 	软卧 	硬卧 	软座 	硬座 	无座
#swz_num	tz_num	zy_num	ze_num	gr_num		rw_num	yw_num	rz_num	yz_num	wz_num




from docopt import docopt
from stations import stations
import requests
import json,time
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



def baidu_gaojing(s_id,s_key,content):
    url='http://gaojing.baidu.com/event/create'
    data={'service_id': s_id, 'description': content, 'event_type': 'trigger'}
    headers={'servicekey': s_key}
    requests.post('http://gaojing.baidu.com/event/create', json=data, headers=headers)
    
    






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
    #print json.dumps(rows, encoding="UTF-8", ensure_ascii=False)
    #字典、列表、元组中有中文是打印的方法
    

def monitor(data,cli_dict):
    pass
    
def filter(data,cli_dict):
    filter_data=[]
    if cli_dict['--s_time'] != None:
        for i in data:
            i_start_time=i['start_time']
            if i_start_time == u'24:00':
                i_start_time=u'23:59'
            if time.mktime(time.strptime(i_start_time,'%H:%M')) >= time.mktime(time.strptime(cli_dict['--s_time'],'%H:%M')):
                filter_data.append(i)
        if len(filter_data) == 0:
            return filter_data
    else:
        filter_data=data
    if cli_dict['--s_code'] != None:
            for i in range(len(filter_data)-1,-1,-1):
                if filter_data[i]['station_train_code'] not in cli_dict['--s_code'] :
                    filter_data.pop(i)
            if len(filter_data) == 0:
                return filter_data
    return filter_data
    
                
                
                
                
                



def cli():
    '''
    返回一个字典,并且对车站，时间格式进行检查
    {'--s_code': 'G123,',
     '--s_time': '18:00',
     '--zx': 'yz',
     '<date>': '2016-09-21',
     '<from>': '上海',
     '<to>': '南京'
    }
    '''
   
    arguments = docopt(__doc__)
    
    
    from_station = stations.get(arguments['<from>'])
    arguments['<from>']=from_station
    
        
    to_station = stations.get(arguments['<to>'])
    arguments['<to>']=to_station
    
    
    date = arguments['<date>']
    if from_station == None :
        print '出发地错误！'
        exit(1)
    if to_station == None :
        print '目的地错误！'
        exit(1)
    try:
        arguments['<date>']=time.strftime("%Y-%m-%d",time.strptime(date, "%Y-%m-%d"))
    except:
        print '查询日期格式错误！'
        exit(1)
    if arguments['--s_time'] != None:
        try:
            time.strptime(arguments['--s_time'], "%H:%M")
        except:
            print '过滤时间格式错误！'
            exit(1)
    return arguments
   



if __name__ == '__main__': 
    arguments=cli()
    from_station = arguments['<from>']
    to_station = arguments['<to>']
    date = arguments['<date>']
    r = get_data(date,from_station,to_station)
    rows = data_pro(r)
    rows2 = filter(rows,arguments)
    format_print(rows2)

