import time
import random
import datetime
def hex(digits):
	return "".join([random.choice("0123456789ABCDEF") for i in range(digits)])

def uid():
	return hex(8) + "-" + hex(4) + "-" + hex(4) + "-" + hex(4) + "-" + hex(12) + "@Waseda"

def calendar(term,day,period,name,room,fq="2021-09-28",sq="2021-11-28"):
	print(f'called: {term},{day},{period},{name},{room}')
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
			lastclass = datetime.date(f"{firstclass.year + 1},1,31")
		else:
			lastclass = datetime.date(f"{firstclass.year},7,31")
	# find the time
	if time.gmtime().tm_year >= 2023 and time.gmtime().tm_mon >= 2:
		time_list = ["8:50-10:30","10:40-12:20","Lunch Break","13:10-14:50","15:05-16:45","17:00-18:40","18:55-20:35","20:45-21:35"]
	else:
		time_list = ["9:00-10:30","10:40-12:10","Lunch Break","13:00-14:30","14:45-16:15","16:30-18:00","18:15-19:45","19:55-21:25"]
	begin = time_list[period - 1].split("-")[0].replace(":","")
	end = time_list[period - 1].split("-")[1].replace(":","")
	firstclass = firstclass.__str__().replace("-","")
	lastclass = lastclass.__str__().replace("-","")
	#read the ics file
	try:
		with open('course.ics', 'r') as f:# if the file exists
			text = f.readlines()
			text.insert(-1,f"BEGIN:VEVENT\nDTEND;TZID=Asia/Tokyo:{firstclass}T{begin}Z\nDTSTART;TZID=Asia/Tokyo:{firstclass}T{end}Z\nSUMMARY:{name}\nUID:{uid()}\nLOCATION:{room}\nRRULE:FREQ=WEEKLY;UNTIL={lastclass}\nEND:VEVENT\n")
	except FileNotFoundError:
			text = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:Waseda\nEND:VCALENDAR"
	# add the event
	# write the ics file
	with open('course.ics', 'w') as f:
		f.writelines(text)

if __name__ == '__main__':
	calendar(1,1,1,"time","room")