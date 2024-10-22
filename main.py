import pandas as pd
import time
import random
import datetime
from DrissionPage import Chromium
import re
import logging

# Configure logging at the beginning of the file
logging.basicConfig(filename='course_calendar.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Course:
	def __init__(self, term, day, period, name, room):
		logging.info(f"Creating course: {name}, Term: {term}, Day: {day}, Period: {period}, Room: {room}")
		self.term = term
		self.day = day
		self.period = period
		self.name = name
		self.room = room if room else "Online"

	def format(self):
		logging.info(f"Formatting course: {self.name}")
		if len(self.period) == 1:
			self.add_to_calendar()
		elif len(self.day) >= 8:  
			self.handle_multiple_days()
		elif len(self.day) < 6:  
			self.handle_intensive_course()

	def add_to_calendar(self):
		day = self.convert_day()
		term = self.convert_term()
		if term == 3:
			calendar(1, day, self.period, self.name, self.room, fq, sq)
			calendar(2, day, self.period, self.name, self.room, fq, sq)
		else:
			calendar(term, day, self.period, self.name, self.room, fq, sq)

	def handle_multiple_days(self):
		days = self.day.split()
		periods = self.period.split()
		for day, period in zip(days, periods):
			Course(self.term, day, period, self.name, self.room).format()

	def handle_intensive_course(self):
		Course(self.term, self.day, self.period[0], self.name, self.room).format()
		Course(self.term, self.day, self.period[-1], self.name, self.room).format()

	def convert_day(self):
		days_dict = {"Mon.": 1, "Tues.": 2, "Wed.": 3, "Thur.": 4, "Fri.": 5}
		return days_dict.get(self.day, self.day)

	def convert_term(self):
		terms_dict = {
			"fall semester": 3, "spring semester": 3,
			"fall quarter": 1, "winter quarter": 2,
			"spring quarter": 1, "summer quarter": 2
		}
		return terms_dict.get(self.term, self.term)

def hex(digits):
	return "".join([random.choice("0123456789ABCDEF") for i in range(digits)])

def uid():
	return hex(8) + "-" + hex(4) + "-" + hex(4) + "-" + hex(4) + "-" + hex(12)

def calendar(day,period,name,room,start_date,end_date):
	no = start_date.weekday() + 1
	gap = (7 + day - no) % 7
	firstclass = start_date + datetime.timedelta(days=gap)
	#find the time 
	time_list = ["08:50-10:30","10:40-12:20","13:10-14:50","15:05-16:45","17:00-18:40","18:55-20:35","20:45-21:35"]
	coursetime = time_list[int(period) - 1]
	begin = time_list[int(period) - 1].split("-")[0].replace(":","")
	end = time_list[int(period) - 1].split("-")[1].replace(":","")
	firstclassstr = firstclass.__str__().replace("-","")
	lastclassstr = end_date.__str__().replace("-","")
	#read the ics file
	try:
		with open('course.ics', 'r') as f:# if the file exists
			text = f.readlines()
		logging.info("Successfully read existing course.ics file")
	except FileNotFoundError:
		logging.info("course.ics file does not exist, creating new file")
		text = ['BEGIN:VCALENDAR\n', 'PRODID:Waseda\n', 'VERSION:2.0\n', 'X-WR-CALNAME:Waseda\n','END:VCALENDAR']
	# insert the new event
	text.insert(-1,f"BEGIN:VEVENT\nDTEND;TZID=Asia/Tokyo:{firstclassstr}T{end}00\nDTSTART;TZID=Asia/Tokyo:{firstclassstr}T{begin}00\nLOCATION:{room}\nRRULE:FREQ=WEEKLY;UNTIL={lastclassstr}\nSEQUENCE:0\nSUMMARY:{name}\nUID:{uid()}\nEND:VEVENT\n")
	# write the ics file
	try:
		with open('course.ics', 'w') as f:
			f.writelines(text)
		logging.info(f"Successfully wrote course {name} to course.ics file")
	except Exception as e:
		logging.error(f"Error writing to course.ics file: {str(e)}")


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
		calendar(1,day,period,name,room,fq,sq)
		calendar(2,day,period,name,room,fq,sq)
	else:
		calendar(term,day,period,name,room,fq,sq)

def get_course_info(row, column):
	xpath = f"/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table[2]/tbody/tr/td/table[3]/tbody/tr[{row+1}]/td[{column}]"
	try:
		info = tab3.ele(xpath).text.strip()
		logging.info(f"Retrieved course info: Row {row}, Column {column}, Content: {info}")
		return info
	except Exception as e:
		logging.error(f"Failed to get course info: Row {row}, Column {column}, Error: {str(e)}")
		raise
def extract_and_convert_to_date(date_str):
    match = re.search(r'(\w+)\s+(\d+)', date_str)
    if match:
        month = match.group(1)
        day = int(match.group(2))
        month_num = datetime.datetime.strptime(month, "%B").month
        return datetime.date(academic_year, month_num, day)
    else:
        return None

if __name__ == "__main__":
	tab = Chromium().latest_tab
	tab.get('https://my.waseda.jp/login/login')
	tab2 = tab.ele('registration').click.for_new_tab()
	tab2.wait.eles_loaded('Course Registration')
	tab3 = tab2.ele('x:/html/body/p/table[1]/tbody/tr[3]/td[2]/a/font').click.for_new_tab()
	eles = tab3.eles('@@class=decisionboxf') 
	texts = []
	for ele in eles.filter.displayed():
		texts.append(ele.text)
	columns = texts[:12]
	data = [texts[i:i+12] for i in range(12, len(texts), 12)]
	df = pd.DataFrame(data, columns=columns)
	#remove on-demand courses
	df = df[~df['Period'].str.contains('On demand')]
	tab.get('https://www.waseda.jp/top/en/about/work/organizations/academic-affairs-division/academic-calendar')
	academic_year = tab.ele('@@class=mod-title').text[:4]
	spring_quarter_begin, fall_quarter_begin = tab.eles('Classes begin').get.texts()
	spring_quarter_end, fall_quarter_end= tab.eles('First term ends').get.texts()
	summer_quarter_begin, winter_quarter_begin = tab.eles('Second term begins').get.texts()
	summer_quarter_end, winter_quarter_end = tab.eles('Classes end').get.texts()
	spring_quarter_begin = extract_and_convert_to_date(spring_quarter_begin)
	spring_quarter_end = extract_and_convert_to_date(spring_quarter_end)
	summer_quarter_begin = extract_and_convert_to_date(summer_quarter_begin)
	summer_quarter_end = extract_and_convert_to_date(summer_quarter_end)
	winter_quarter_begin = extract_and_convert_to_date(winter_quarter_begin)
	winter_quarter_end = extract_and_convert_to_date(winter_quarter_end)
	fall_quarter_begin = extract_and_convert_to_date(fall_quarter_begin)
	fall_quarter_end = extract_and_convert_to_date(fall_quarter_end)
	def calendar(day,period,name,room,start_date,end_date)
	for i in range(len(df)):
		if df.loc[i, 'Term'] == 'spring quarter':
			calendar(df.loc[i, 'Day'],df.loc[i, 'Period'],df.loc[i, 'Course Title'],df.loc[i, 'Classroom'],spring_quarter_begin,spring_quarter_end)
		elif df.loc[i, 'Term'] == 'summer quarter':
			calendar(df.loc[i, 'Day'],df.loc[i, 'Period'],df.loc[i, 'Course Title'],df.loc[i, 'Classroom'],summer_quarter_begin,summer_quarter_end)
		elif df.loc[i, 'Term'] == 'winter quarter':
			calendar(df.loc[i, 'Day'],df.loc[i, 'Period'],df.loc[i, 'Course Title'],df.loc[i, 'Classroom'],winter_quarter_begin,winter_quarter_end)
		elif df.loc[i, 'Term'] == 'fall quarter':
			calendar(df.loc[i, 'Day'],df.loc[i, 'Period'],df.loc[i, 'Course Title'],df.loc[i, 'Classroom'],fall_quarter_begin,fall_quarter_end)
		elif df.loc[i, 'Term'] == 'spring semester':
			calendar(df.loc[i, 'Day'],df.loc[i, 'Period'],df.loc[i, 'Course Title'],df.loc[i, 'Classroom'],spring_quarter_begin,summer_quarter_end)
		elif df.loc[i, 'Term'] == 'fall semester':
			calendar(df.loc[i, 'Day'],df.loc[i, 'Period'],df.loc[i, 'Course Title'],df.loc[i, 'Classroom'],fall_quarter_begin,winter_quarter_end)
		

