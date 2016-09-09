#coding:utf-8
from pylsy import pylsytable
import sys 
reload(sys)
sys.setdefaultencoding('utf8')
attributes=[u"姓名","age","sex","id","time"]
table=pylsytable(attributes)
name=["sun","lsy","luna"]
table.add_data(u"姓名",name)
table.append_data(u"姓名",["leviathan"])
table.append_data(u"姓名",u"小明")
table.append_data('age',18)
table.add_data('id','1232312312312323014156465431456412348612346841654567897546941')
table.append_data('id','348612346841654567897546941')
table.add_data('id','146941')
print(table)
print(table.__str__())
