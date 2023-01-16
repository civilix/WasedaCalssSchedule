#####################################################
id = "example@xxxx.waseda.jp"
pw = "password"
start_date_of_the_first_quarter = "2022-09-28"
start_date_of_the_second_quarter = "2022-11-28"
#####################################################
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import xlsxwriter
import time
import random
import datetime
def hex(digits):
	return "".join([random.choice("0123456789ABCDEF") for i in range(digits)])

def uid():
	return hex(8) + "-" + hex(4) + "-" + hex(4) + "-" + hex(4) + "-" + hex(12)

def calendar(term,day,period,name,room,fq,sq):
	# find the first class of the semester
	if term == 1:
		first = datetime.date.fromisoformat(fq)
	else:
		first = datetime.date.fromisoformat(sq)
	no = first.weekday() + 1
	gap = (7 + day - no) % 7
	firstclass = first + datetime.timedelta(days=gap)
	# find the end of the semester
	if term == 1:
		lastclass = datetime.date.fromisoformat(sq) - datetime.timedelta(days=1)
	else:
		if firstclass.month >= 8:
			lastclassyear = firstclass.year + 1
			lastclass = datetime.date(lastclassyear,1,31)
		else:
			lastclassyear = firstclass.year
			lastclass = datetime.date(lastclassyear,7,31)
	#find the time 
	if time.gmtime().tm_year >= 2023 and time.gmtime().tm_mon >= 2:
		time_list = ["08:50-10:30","10:40-12:20","13:10-14:50","15:05-16:45","17:00-18:40","18:55-20:35","20:45-21:35"]
	else:
		time_list = ["09:00-10:30","10:40-12:10","13:00-14:30","14:45-16:15","16:30-18:00","18:15-19:45","19:55-21:25"]
	coursetime = time_list[int(period) - 1]
	begin = time_list[int(period) - 1].split("-")[0].replace(":","")
	end = time_list[int(period) - 1].split("-")[1].replace(":","")
	firstclassstr = firstclass.__str__().replace("-","")
	lastclassstr = lastclass.__str__().replace("-","")
	#read the ics file
	try:
		with open('course.ics', 'r') as f:# if the file exists
			text = f.readlines()
	except FileNotFoundError:
			text = ['BEGIN:VCALENDAR\n', 'PRODID:Waseda\n', 'VERSION:2.0\n', 'X-WR-CALNAME:Waseda\n','END:VCALENDAR']
	# insert the new event
	text.insert(-1,f"BEGIN:VEVENT\nDTEND;TZID=Asia/Tokyo:{firstclassstr}T{end}00\nDTSTART;TZID=Asia/Tokyo:{firstclassstr}T{begin}00\nLOCATION:{room}\nRRULE:FREQ=WEEKLY;UNTIL={lastclassstr}\nSEQUENCE:0\nSUMMARY:{name}\nUID:{uid()}\nEND:VEVENT\n")
	# write the ics file
	with open('course.ics', 'w') as f:
		f.writelines(text)
def get(a,b):
	xpath = "/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table[2]/tbody/tr/td/table[3]/tbody/tr[x]/td[z]"
	xpath = xpath.replace("x",str(a+1))
	xpath = xpath.replace("z",str(b))
	text = driver.find_element(By.XPATH, xpath).text.strip()
	return(text)
def format(term,day,period,name,room):
	if len(period) == 1:
		num(term,day,period,name,room)
	elif len(day) >= 8:#Multiple days
		sday = day.split()
		speriod = period.split()
		for i in range(len(sday)):
			format(term,sday[i],speriod[i],name,room)
	elif len(day) < 6:#Intensive
		format(term,day,period[0],name,room)
		format(term,day,period[-1],name,room)
def num(term,day,period,name,room):
	days_dict={"Mon.":1,"Tues.":2,"Wed.":3,"Thur.":4,"Fri.":5}
	if day in days_dict:
		day = days_dict[day]				
	terms_dict={"fall semester":3,"spring semester":3,"fall quarter":1,"winter quarter":2,"spring quarter":1,"summer quarter":2}
	if term in terms_dict:
		term = terms_dict[term]	
	if term == 3:
		excel(1,day,period,name)
		calendar(1,day,period,name,room,fq,sq)
		excel(2,day,period,name)
		calendar(2,day,period,name,room,fq,sq)
	else:
		excel(term,day,period,name)
		calendar(term,day,period,name,room,fq,sq)
def excel(term,day,period,name):
	period = int(period)
	x = day
	if period <= 2:
		y = period
	else:
		y = period + 1
	if term == 1:
		worksheet1.write(y,x,name,cell_format)
	else:
		worksheet2.write(y,x,name,cell_format)
	
if __name__ == "__main__":
	workbook = xlsxwriter.Workbook("course.xlsx",{'in_memory': True})
	worksheet1 = workbook.add_worksheet("First Quarter")     
	worksheet2 = workbook.add_worksheet("Second Quarter")
	cell_format = workbook.add_format()
	cell_format.set_text_wrap()
	cell_format.set_bg_color('yellow')
	if time.gmtime().tm_year >= 2023 and time.gmtime().tm_mon >= 2:
		time_list = ["08:50-10:30","10:40-12:20","Lunch Break","13:10-14:50","15:05-16:45","17:00-18:40","18:55-20:35","20:45-21:35"]
	else:
		time_list = ["09:00-10:30","10:40-12:10","Lunch Break","13:00-14:30","14:45-16:15","16:30-18:00","18:15-19:45","19:55-21:25"]
	for r in range(8):
		worksheet1.write(r+1,0,time_list[r])
		worksheet1.set_row(r+1,60)
		worksheet2.write(r+1,0,time_list[r])
		worksheet2.set_row(r+1,60)
	days_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
	for c in range(7):
		worksheet1.write(0,c+1,days_list[c])
		worksheet1.set_column(chr(65+c)+":"+chr(65+c),20)
		worksheet2.write(0,c+1,days_list[c])
		worksheet2.set_column(chr(65+c)+":"+chr(65+c),20)
	coptions = webdriver.ChromeOptions()
	coptions.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
	driver = webdriver.Chrome(options=coptions)
	driver.get('https://my.waseda.jp/login/login')
	driver.find_element(By.ID, 'infoUrl2').click()
	handles = driver.window_handles
	driver.switch_to.window(handles[1])
	driver.find_element(By.NAME, 'loginfmt').send_keys(id)
	driver.find_element(By.ID, 'idSIButton9').click()
	driver.find_element(By.NAME, 'passwd').send_keys(pw)
	time.sleep(2)
	driver.find_element(By.ID, 'idSIButton9').click()
	driver.find_element(By.LINK_TEXT, 'Course Registration').click()
	handles = driver.window_handles
	driver.switch_to.window(handles[2])
	time.sleep(2)
	fq = start_date_of_the_first_quarter
	sq = start_date_of_the_second_quarter
	courseno = 1
	while courseno:
		try:
			term = get(courseno,1)
			day = get(courseno,2)
			period = get(courseno,3)
			name = get(courseno,6)
			room = get(courseno,9)
			if not room:
				room = "Online"
			format(term,day,period,name,room)
			courseno += 1
		except:
			break
	workbook.close()
	driver.quit()
