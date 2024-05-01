import datetime
import calendar


def createDate(year, month, day):
	return datetime.datetime(year, month, day)

def getCurrentDate():
	return datetime.date.today()

def getCurrentDateTime():
	return datetime.datetime.now()

def getDateInWeek(date):
	return (date.weekday()) % 7 # Start is Monday
	# return (date.weekday() + 1) % 7 # Start is Sunday

def main():
	curDate = getCurrentDate()
	print(curDate.day)
	print(curDate.month)
	print(curDate.year)
 

main()
