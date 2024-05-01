import sqlite3
from flask import request, jsonify
import datetime
import traceback
# import math
import MtSystem


class MtCalendar:
	
	mt = None
	dbMgrPath = './res/database/manager.sqlite'
	dbCldPath = './res/database/calendar.sqlite'

	def __init__(self, _mt):
		self.mt = _mt

	def register(self):

		@self.mt.app.route("/api/calendar/get")
		def api_calendar_get():
			return self.api_get()
		
		@self.mt.app.route("/api/calendar/gen", methods=['POST'])
		def api_calendar_gen():
			return self.api_gen()

	def api_get(self):

		# Get Params
		p_type = request.args.get('type')
		p_year = int(request.args.get('year'))
		p_month = int(request.args.get('month'))

		rows = []
		if p_type == 'month':

			# Lịch hiển thị dư các ngày của tháng trước và tháng sau, tìm các ngày đó
			bMonthDate = datetime.date(p_year, p_month, 1)
			eMonthDate = datetime.date(p_year, p_month, MtSolar.getMaxDayOfMonth(p_month, p_year))
			bDeltaDay = MtSolar.getDayInWeek(bMonthDate)
			eDeltaDay = 6 - MtSolar.getDayInWeek(eMonthDate)
			bDayCalendar = bMonthDate - datetime.timedelta(days=bDeltaDay) # Ngày đầu lịch
			eDayCalendar = eMonthDate + datetime.timedelta(days=eDeltaDay) # Ngày cuối lịch

			# Build SQL
			sql = "SELECT * FROM calendar WHERE (year = ? AND month = ?)"
			param = [p_year, p_month]

			if bDeltaDay > 0:
				sql += " OR (year = ? AND month = ? AND day >= ?)"
				param.extend([bDayCalendar.year, bDayCalendar.month, bDayCalendar.day])

			if eDeltaDay > 0:
				sql += " OR (year = ? AND month = ? AND day <= ?)"
				param.extend([eDayCalendar.year, eDayCalendar.month, eDayCalendar.day])

			# Query
			conn = sqlite3.connect(self.dbCldPath)
			conn.row_factory = MtSystem.sql_dict_factory
			rows = conn.execute(sql, param).fetchall()
			conn.close()
		
		return jsonify(rows), 200

	def api_gen(self):
		result_code = 200
		result = {}
		try:
			# lấy params
			year = request.args.get('year')
			if year is None:
				raise Exception("Chưa truyền năm để gen (year)")
			year = int(year)
			
			# print(year)
			# print(type(year))

			# Mở kết nối
			conn = sqlite3.connect(self.dbCldPath)
			conn.row_factory = MtSystem.sql_dict_factory

			# Kiểm tra đã gen năm này chưa
			sql = "SELECT count(1) AS 'count' FROM calendar c WHERE c.'year' = ?;"
			params = [year]
			res = conn.execute(sql, params).fetchall()
			if res[0]['count'] > 0:
				result['msg'] = "Đã tạo sự kiện cho năm {0}".format(year)
			else:
				# Lấy danh sách event để gen
				sql = """
					SELECT * FROM event_loop
					"""
				param = []
				lstCld = conn.execute(sql, param).fetchall()
				
				# Tách lịch âm / dương
				lstSolar = []
				for cld in lstCld:
					if cld['is_lunar'] == 1:
						day = cld['day']
						month = cld['month']
						solarDate = MtLunar.Lunar2Solar(day, month, year, False)
						if solarDate[0] == year: # nếu thuộc năm nay
							cld['month'] = solarDate[1]
							cld['day'] = solarDate[2]
							lstSolar.append(cld)
						
						# Sự kiện âm lịch Cuối năm trước
						if cld['month'] == 12:
							solarDate = MtLunar.Lunar2Solar(day, month, year-1, False)
							if solarDate[0] == year: # nếu thuộc năm nay
								cld['month'] = solarDate[1]
								cld['day'] = solarDate[2]
								lstSolar.append(cld)
					else:
						lstSolar.append(cld)
					del cld['is_lunar']

				# Insert into table calender
				sql = """
					INSERT INTO calendar(name,day,month,year,tag,origin)
					VALUES(?,?,?,?,?,?)
					"""
				for cld in lstSolar:
					params = [
						cld['name'],
						cld['day'],
						cld['month'],
						year,
						cld['tag'],
						'LOOP'
					]
					conn.execute(sql, params)
					conn.commit()
					
				result['msg'] = "Thêm thành công {0} sự kiện cho năm {1}".format(len(lstSolar), year)
			conn.close()
		except Exception as e:
			traceback.print_exc()
			result['msg'] = str(e)
			result_code = 500
		return jsonify(result), result_code

	def getAllRawEvent(self):
		pass


class MtSolar:

	def getMaxDayOfMonth(month, year):
		if month == 2:
			if MtSolar.isLeapYear(year):
				return 29
			else:
				return 28
		elif month == 4 or month == 6 or month == 9 or month == 11:
			return 30
		else:
			return 31

	def isLeapYear(y):
		return ((y % 400 == 0) or (y % 100 != 0) and (y % 4 == 0))

	def getDayInWeek(date):
		return (date.weekday()) % 7 # Start is Monday


class MtLunar:

	lunar_month_days = [1887, 0x1694, 0x16aa, 0x4ad5, 0xab6, 0xc4b7, 0x4ae, 0xa56, 0xb52a,
						0x1d2a, 0xd54, 0x75aa, 0x156a, 0x1096d, 0x95c, 0x14ae, 0xaa4d, 0x1a4c, 0x1b2a, 0x8d55,
						0xad4, 0x135a, 0x495d,
						0x95c, 0xd49b, 0x149a, 0x1a4a, 0xbaa5, 0x16a8, 0x1ad4, 0x52da, 0x12b6, 0xe937, 0x92e,
						0x1496, 0xb64b, 0xd4a,
						0xda8, 0x95b5, 0x56c, 0x12ae, 0x492f, 0x92e, 0xcc96, 0x1a94, 0x1d4a, 0xada9, 0xb5a, 0x56c,
						0x726e, 0x125c,
						0xf92d, 0x192a, 0x1a94, 0xdb4a, 0x16aa, 0xad4, 0x955b, 0x4ba, 0x125a, 0x592b, 0x152a,
						0xf695, 0xd94, 0x16aa,
						0xaab5, 0x9b4, 0x14b6, 0x6a57, 0xa56, 0x1152a, 0x1d2a, 0xd54, 0xd5aa, 0x156a, 0x96c,
						0x94ae, 0x14ae, 0xa4c,
						0x7d26, 0x1b2a, 0xeb55, 0xad4, 0x12da, 0xa95d, 0x95a, 0x149a, 0x9a4d, 0x1a4a, 0x11aa5,
						0x16a8, 0x16d4,
						0xd2da, 0x12b6, 0x936, 0x9497, 0x1496, 0x1564b, 0xd4a, 0xda8, 0xd5b4, 0x156c, 0x12ae,
						0xa92f, 0x92e, 0xc96,
						0x6d4a, 0x1d4a, 0x10d65, 0xb58, 0x156c, 0xb26d, 0x125c, 0x192c, 0x9a95, 0x1a94, 0x1b4a,
						0x4b55, 0xad4,
						0xf55b, 0x4ba, 0x125a, 0xb92b, 0x152a, 0x1694, 0x96aa, 0x15aa, 0x12ab5, 0x974, 0x14b6,
						0xca57, 0xa56, 0x1526,
						0x8e95, 0xd54, 0x15aa, 0x49b5, 0x96c, 0xd4ae, 0x149c, 0x1a4c, 0xbd26, 0x1aa6, 0xb54,
						0x6d6a, 0x12da, 0x1695d,
						0x95a, 0x149a, 0xda4b, 0x1a4a, 0x1aa4, 0xbb54, 0x16b4, 0xada, 0x495b, 0x936, 0xf497,
						0x1496, 0x154a, 0xb6a5,
						0xda4, 0x15b4, 0x6ab6, 0x126e, 0x1092f, 0x92e, 0xc96, 0xcd4a, 0x1d4a, 0xd64, 0x956c,
						0x155c, 0x125c, 0x792e,
						0x192c, 0xfa95, 0x1a94, 0x1b4a, 0xab55, 0xad4, 0x14da, 0x8a5d, 0xa5a, 0x1152b, 0x152a,
						0x1694, 0xd6aa,
						0x15aa, 0xab4, 0x94ba, 0x14b6, 0xa56, 0x7527, 0xd26, 0xee53, 0xd54, 0x15aa, 0xa9b5, 0x96c,
						0x14ae, 0x8a4e,
						0x1a4c, 0x11d26, 0x1aa4, 0x1b54, 0xcd6a, 0xada, 0x95c, 0x949d, 0x149a, 0x1a2a, 0x5b25,
						0x1aa4, 0xfb52,
						0x16b4, 0xaba, 0xa95b, 0x936, 0x1496, 0x9a4b, 0x154a, 0x136a5, 0xda4, 0x15ac]
	solar_1_1 = [1887, 0xec04c, 0xec23f, 0xec435, 0xec649, 0xec83e, 0xeca51, 0xecc46, 0xece3a,
				 0xed04d, 0xed242, 0xed436, 0xed64a, 0xed83f, 0xeda53, 0xedc48, 0xede3d, 0xee050, 0xee244, 0xee439,
				 0xee64d,
				 0xee842, 0xeea36, 0xeec4a, 0xeee3e, 0xef052, 0xef246, 0xef43a, 0xef64e, 0xef843, 0xefa37, 0xefc4b,
				 0xefe41,
				 0xf0054, 0xf0248, 0xf043c, 0xf0650, 0xf0845, 0xf0a38, 0xf0c4d, 0xf0e42, 0xf1037, 0xf124a, 0xf143e,
				 0xf1651,
				 0xf1846, 0xf1a3a, 0xf1c4e, 0xf1e44, 0xf2038, 0xf224b, 0xf243f, 0xf2653, 0xf2848, 0xf2a3b, 0xf2c4f,
				 0xf2e45,
				 0xf3039, 0xf324d, 0xf3442, 0xf3636, 0xf384a, 0xf3a3d, 0xf3c51, 0xf3e46, 0xf403b, 0xf424e, 0xf4443,
				 0xf4638,
				 0xf484c, 0xf4a3f, 0xf4c52, 0xf4e48, 0xf503c, 0xf524f, 0xf5445, 0xf5639, 0xf584d, 0xf5a42, 0xf5c35,
				 0xf5e49,
				 0xf603e, 0xf6251, 0xf6446, 0xf663b, 0xf684f, 0xf6a43, 0xf6c37, 0xf6e4b, 0xf703f, 0xf7252, 0xf7447,
				 0xf763c,
				 0xf7850, 0xf7a45, 0xf7c39, 0xf7e4d, 0xf8042, 0xf8254, 0xf8449, 0xf863d, 0xf8851, 0xf8a46, 0xf8c3b,
				 0xf8e4f,
				 0xf9044, 0xf9237, 0xf944a, 0xf963f, 0xf9853, 0xf9a47, 0xf9c3c, 0xf9e50, 0xfa045, 0xfa238, 0xfa44c,
				 0xfa641,
				 0xfa836, 0xfaa49, 0xfac3d, 0xfae52, 0xfb047, 0xfb23a, 0xfb44e, 0xfb643, 0xfb837, 0xfba4a, 0xfbc3f,
				 0xfbe53,
				 0xfc048, 0xfc23c, 0xfc450, 0xfc645, 0xfc839, 0xfca4c, 0xfcc41, 0xfce36, 0xfd04a, 0xfd23d, 0xfd451,
				 0xfd646,
				 0xfd83a, 0xfda4d, 0xfdc43, 0xfde37, 0xfe04b, 0xfe23f, 0xfe453, 0xfe648, 0xfe83c, 0xfea4f, 0xfec44,
				 0xfee38,
				 0xff04c, 0xff241, 0xff436, 0xff64a, 0xff83e, 0xffa51, 0xffc46, 0xffe3a, 0x10004e, 0x100242,
				 0x100437,
				 0x10064b, 0x100841, 0x100a53, 0x100c48, 0x100e3c, 0x10104f, 0x101244, 0x101438, 0x10164c,
				 0x101842, 0x101a35,
				 0x101c49, 0x101e3d, 0x102051, 0x102245, 0x10243a, 0x10264e, 0x102843, 0x102a37, 0x102c4b,
				 0x102e3f, 0x103053,
				 0x103247, 0x10343b, 0x10364f, 0x103845, 0x103a38, 0x103c4c, 0x103e42, 0x104036, 0x104249,
				 0x10443d, 0x104651,
				 0x104846, 0x104a3a, 0x104c4e, 0x104e43, 0x105038, 0x10524a, 0x10543e, 0x105652, 0x105847,
				 0x105a3b, 0x105c4f,
				 0x105e45, 0x106039, 0x10624c, 0x106441, 0x106635, 0x106849, 0x106a3d, 0x106c51, 0x106e47,
				 0x10703c, 0x10724f,
				 0x107444, 0x107638, 0x10784c, 0x107a3f, 0x107c53, 0x107e48]

	def GetBitInt(data, length, shift):
		return (data & (((1 << length) - 1) << shift)) >> shift
	
	def SolarToInt(y, m, d):
		m = (m + 9) % 12
		y -= m // 10
		return 365 * y + y // 4 - y // 100 + y // 400 + (m * 306 + 5) // 10 + (d - 1)
	
	def SolarFromInt(g):
		y = (10000 * g + 14780) // 3652425
		ddd = g - (365 * y + y // 4 - y // 100 + y // 400)
		if ddd < 0:
			y -= 1
			ddd = g - (365 * y + y // 4 - y // 100 + y // 400)
		mi = (100 * ddd + 52) // 3060
		mm = (mi + 2) % 12 + 1
		y += (mi + 2) // 12
		dd = ddd - (mi * 306 + 5) // 10 + 1
		return [y, mm, dd]
	
	def Lunar2Solar(lunarDay, lunarMonth, lunarYear, isleap):
		days = MtLunar.lunar_month_days[lunarYear - MtLunar.lunar_month_days[0]]
		leap = MtLunar.GetBitInt(days, 4, 13)
		offset = 0
		loopend = leap
		if not isleap:

			if lunarMonth <= leap or leap == 0:

				loopend = lunarMonth - 1

			else:

				loopend = lunarMonth

		for i in range(0, loopend):
			offset += MtLunar.GetBitInt(days, 1, 12 - i) == 1 and 30 or 29

		offset += lunarDay

		solar11 = MtLunar.solar_1_1[lunarYear - MtLunar.solar_1_1[0]]

		y = MtLunar.GetBitInt(solar11, 12, 9)
		m = MtLunar.GetBitInt(solar11, 4, 5)
		d = MtLunar.GetBitInt(solar11, 5, 0)

		return MtLunar.SolarFromInt(MtLunar.SolarToInt(y, m, d) + offset - 1)

	def Solar2Lunar(solarDay, solarMonth, solarYear):

		index = solarYear - MtLunar.solar_1_1[0]
		data = (solarYear << 9) | (solarMonth << 5) | solarDay
		if MtLunar.solar_1_1[index] > data:
			index -= 1

		solar11 = MtLunar.solar_1_1[index]
		y = MtLunar.GetBitInt(solar11, 12, 9)
		m = MtLunar.GetBitInt(solar11, 4, 5)
		d = MtLunar.GetBitInt(solar11, 5, 0)
		offset = MtLunar.SolarToInt(solarYear, solarMonth, solarDay) - MtLunar.SolarToInt(y, m, d)

		days = MtLunar.lunar_month_days[index]
		leap = MtLunar.GetBitInt(days, 4, 13)

		lunarY = index + MtLunar.solar_1_1[0]
		lunarM = 1
		offset += 1

		for i in range(0, 13):

			dm = MtLunar.GetBitInt(days, 1, 12 - i) == 1 and 30 or 29
			if offset > dm:

				lunarM += 1
				offset -= dm

			else:

				break

		lunarDay = int(offset)
		lunarMonth = lunarM
		lunarYear = lunarY
		isleap = False

		if leap != 0 and lunarM > leap:
			lunarMonth = lunarM - 1
			if lunarM == leap + 1:
				isleap = True

		return [lunarDay, lunarMonth, lunarYear, isleap]


# class MtLunar:

# 	CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ",
# 		"Canh", "Tân", "Nhâm", "Quý"]
# 	CHI = ["Tí", "Sửu", "Dần", "Mão", "Thìn", "Tị", "Ngọ",
# 		"Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
# 	CHI_MONTH = ["", "Dần", "Mão", "Thìn", "Tị", "Ngọ", "Mùi",
# 		"Thân", "Dậu", "Tuất", "Hợi", "Tí", "Sửu"]
	
# 	def julian_day_from_date(dd, mm, yy):
# 		temp_a = int((14 - mm) / 12.)
# 		temp_year = yy + 4800 - temp_a
# 		temp_month = mm + 12 * temp_a - 3
# 		julian_day = (dd + int((153*temp_month + 2) / 5.) +
# 					365 * temp_year + int(temp_year / 4.) -
# 					int(temp_year/100.) + int(temp_year/400)
# 					- 32045)
# 		if julian_day < 2299161:
# 			julian_day = dd + int((153*temp_month + 2)/5.) \
# 				+ 365*temp_year + int(temp_year/4.) - 32083
# 		return julian_day

# 	def julian_day_to_date(julian_day):
# 		if julian_day > 2299160:
# 			# After 5/10/1582, Gregorian calendar
# 			temp_a = julian_day + 32044
# 			temp_b = int((4 * temp_a + 3) / 146097.)
# 			temp_c = temp_a - int((temp_b * 146097) / 4.)
# 		else:
# 			temp_b = 0
# 			temp_c = julian_day + 32082
# 		temp_d = int((4 * temp_c + 3) / 1461.)
# 		temp_e = temp_c - int((1461 * temp_d) / 4.)
# 		temp_m = int((5 * temp_e + 2) / 153.)
# 		_day = temp_e - int((153 * temp_m + 2) / 5.) + 1
# 		_month = temp_m + 3 - 12 * int(temp_m / 10.)
# 		_year = temp_b * 100 + temp_d - 4800 + int(temp_m / 10.)
# 		return [_day, _month, _year]

# 	def new_moon(k_th):
# 		# Time in Julian centuries from 1900 January 0.5
# 		time_julian = k_th / 1236.85
# 		time_julian_2 = time_julian * time_julian
# 		time_julian_3 = time_julian_2 * time_julian
# 		degree_to_radian = math.pi / 180
# 		julian_day_1 = (2415020.75933 + 29.53058868 * k_th +
# 						0.0001178 * time_julian_2 -
# 						0.000000155 * time_julian_3)
# 		julian_day_1 = (julian_day_1 +
# 						0.00033*math.sin((166.56 + 132.87*time_julian -
# 										0.009173 * time_julian_2) *
# 										degree_to_radian))
# 		# Mean new moon
# 		mean_new_moon = (359.2242 + 29.10535608*k_th -
# 						0.0000333*time_julian_2 - 0.00000347*time_julian_3)
# 		# Sun's mean anomaly
# 		sun_mean_anomaly = (306.0253 + 385.81691806*k_th +
# 							0.0107306*time_julian_2 + 0.00001236*time_julian_3)
# 		# Moon's mean anomaly
# 		moon_mean_anomaly = (21.2964 + 390.67050646*k_th -
# 							0.0016528*time_julian_2 - 0.00000239*time_julian_3)
# 		# Moon's argument of latitude
# 		moon_arg_lat = ((0.1734 - 0.000393*time_julian) *
# 						math.sin(mean_new_moon*degree_to_radian) +
# 						0.0021*math.sin(2*degree_to_radian*mean_new_moon))
# 		moon_arg_lat = (moon_arg_lat -
# 						0.4068*math.sin(sun_mean_anomaly*degree_to_radian)
# 						+ 0.0161*math.sin(degree_to_radian*2*sun_mean_anomaly))
# 		moon_arg_lat = (moon_arg_lat -
# 						0.0004*math.sin(degree_to_radian*3*sun_mean_anomaly))
# 		moon_arg_lat = (moon_arg_lat +
# 						0.0104*math.sin(degree_to_radian*2*moon_mean_anomaly)
# 						- 0.0051 * math.sin(degree_to_radian *
# 											(mean_new_moon + sun_mean_anomaly)))
# 		moon_arg_lat = (moon_arg_lat -
# 						0.0074*math.sin(degree_to_radian *
# 										(mean_new_moon - sun_mean_anomaly))
# 						+ 0.0004*math.sin(degree_to_radian *
# 										(2*moon_mean_anomaly + mean_new_moon)))
# 		moon_arg_lat = (moon_arg_lat - 0.0004*math.sin(degree_to_radian *
# 													(2*moon_mean_anomaly -
# 														mean_new_moon))
# 						- 0.0006 * math.sin(degree_to_radian *
# 											(2*moon_mean_anomaly
# 											+ sun_mean_anomaly)))
# 		moon_arg_lat = (moon_arg_lat + 0.0010*math.sin(degree_to_radian *
# 													(2*moon_mean_anomaly -
# 														sun_mean_anomaly))
# 						+ 0.0005*math.sin(degree_to_radian *
# 										(2*sun_mean_anomaly + mean_new_moon))
# 						)
# 		if time_julian < -11:
# 			deltat = (0.001 + 0.000839*time_julian + 0.0002261*time_julian_2
# 					- 0.00000845*time_julian_3 -
# 					0.000000081*time_julian*time_julian_3)
# 		else:
# 			deltat = -0.000278 + 0.000265*time_julian + 0.000262*time_julian_2
# 		new_julian_day = julian_day_1 + moon_arg_lat - deltat
# 		return new_julian_day

# 	def sun_longitude(jdn):
# 		time_in_julian = (jdn - 2451545.0) / 36525.
# 		# Time in Julian centuries
# 		# from 2000-01-01 12:00:00 GMT
# 		time_in_julian_2 = time_in_julian * time_in_julian
# 		degree_to_radian = math.pi / 180.  # degree to radian
# 		mean_time = (357.52910 + 35999.05030*time_in_julian
# 					- 0.0001559*time_in_julian_2 -
# 					0.00000048 * time_in_julian*time_in_julian_2)
# 		# mean anomaly, degree
# 		mean_degree = (280.46645 + 36000.76983*time_in_julian +
# 					0.0003032*time_in_julian_2)
# 		# mean longitude, degree
# 		mean_long_degree = ((1.914600 - 0.004817*time_in_julian -
# 							0.000014*time_in_julian_2)
# 							* math.sin(degree_to_radian*mean_time))
# 		mean_long_degree += ((0.019993 - 0.000101*time_in_julian) *
# 							math.sin(degree_to_radian*2*mean_time) +
# 							0.000290*math.sin(degree_to_radian*3*mean_time))
# 		long_degree = mean_degree + mean_long_degree  # true longitude, degree
# 		long_degree = long_degree * degree_to_radian
# 		long_degree = long_degree - math.pi*2*(int(long_degree / (math.pi*2)))
# 		# Normalize to (0, 2*math.pi)
# 		return long_degree

# 	def get_sun_longitude(dayNumber, timeZone):
# 		return int(MtLunar.sun_longitude(dayNumber - 0.5 - timeZone / 24)
# 				/ math.pi*6)

# 	def get_new_moon_day(k, timeZone):
# 		return int(MtLunar.new_moon(k) + 0.5 + timeZone / 24.)

# 	def get_lunar_month_11(yy, timeZone):
# 		off = MtLunar.julian_day_from_date(31, 12, yy) - 2415021.
# 		k = int(off / 29.530588853)
# 		lunar_month = MtLunar.get_new_moon_day(k, timeZone)
# 		sun_long = MtLunar.get_sun_longitude(lunar_month, timeZone)
# 		# sun longitude at local midnight
# 		if sun_long >= 9:
# 			lunar_month = MtLunar.get_new_moon_day(k - 1, timeZone)
# 		return lunar_month

# 	def get_leap_month_offset(a11, timeZone):
# 		k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
# 		last = 0
# 		i = 1  # start with month following lunar month 11
# 		arc = MtLunar.get_sun_longitude(MtLunar.get_new_moon_day(k + i, timeZone),
# 								timeZone)
# 		while True:
# 			last = arc
# 			i += 1
# 			arc = MtLunar.get_sun_longitude(MtLunar.get_new_moon_day(k + i, timeZone),
# 									timeZone)
# 			if not (arc != last and i < 14):
# 				break
# 		return i - 1

# 	def solar_to_lunar(solar_dd, solar_mm, solar_yy, time_zone=7):
# 		time_zone = 7
# 		day_number = MtLunar.julian_day_from_date(solar_dd, solar_mm, solar_yy)
# 		k = int((day_number - 2415021.076998695) / 29.530588853)
# 		month_start = MtLunar.get_new_moon_day(k + 1, time_zone)
# 		if month_start > day_number:
# 			month_start = MtLunar.get_new_moon_day(k, time_zone)
# 		# alert(dayNumber + " -> " + monthStart)
# 		a11 = MtLunar.get_lunar_month_11(solar_yy, time_zone)
# 		b11 = a11
# 		if a11 >= month_start:
# 			lunar_year = solar_yy
# 			a11 = MtLunar.get_lunar_month_11(solar_yy - 1, time_zone)
# 		else:
# 			lunar_year = solar_yy + 1
# 			b11 = MtLunar.get_lunar_month_11(solar_yy + 1, time_zone)
# 		lunar_day = day_number - month_start + 1
# 		diff = int((month_start - a11) / 29.)
# 		lunar_leap = 0
# 		lunar_month = diff + 11
# 		if b11 - a11 > 365:
# 			leap_month_diff = \
# 				MtLunar.get_leap_month_offset(a11, time_zone)
# 			if diff >= leap_month_diff:
# 				lunar_month = diff + 10
# 			if diff == leap_month_diff:
# 				lunar_leap = 1
# 		if lunar_month > 12:
# 			lunar_month = lunar_month - 12
# 		if lunar_month >= 11 and diff < 4:
# 			lunar_year -= 1
# 		return [lunar_day, lunar_month, lunar_year, lunar_leap]

# 	def lunar_to_solar(lunar_day, lunar_month, lunar_year, lunar_leap_month, time_zone=7):
# 		if lunar_month < 11:
# 			a11 = MtLunar.get_lunar_month_11(lunar_year - 1, time_zone)
# 			b11 = MtLunar.get_lunar_month_11(lunar_year, time_zone)
# 		else:
# 			a11 = MtLunar.get_lunar_month_11(lunar_year, time_zone)
# 			b11 = MtLunar.get_lunar_month_11(lunar_year + 1, time_zone)
# 		k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
# 		off = lunar_month - 11
# 		if off < 0:
# 			off += 12
# 		if b11 - a11 > 365:
# 			leap_off = MtLunar.get_leap_month_offset(a11, time_zone)
# 			leap_month = leap_off - 2
# 			if leap_month < 0:
# 				leap_month += 12
# 			if lunar_leap_month != 0 and lunar_month != leap_month:
# 				return [0, 0, 0]
# 			elif lunar_leap_month != 0 or off >= leap_off:
# 				off += 1
# 		month_start = MtLunar.get_new_moon_day(k + off, time_zone)
# 		return MtLunar.julian_day_to_date(month_start + lunar_day - 1)

# 	def day_in_week(solar_dd, solar_mm, solar_yy, viet_language=1):
# 		julian_day = MtLunar.julian_day_from_date(solar_dd, solar_mm, solar_yy)
# 		date_index = julian_day % 7
# 		if viet_language:
# 			_day_in_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5",
# 							"Thứ 6", "Thứ 7", "Chủ nhật"]
# 		else:
# 			_day_in_week = ["Mon", "Tue", "Wed", "Thu",
# 							"Fri", "Sat", "Sun"]
# 		return _day_in_week[date_index]

# 	def zodiac_year(year):
# 		can_index = (year + 6) % 10
# 		chi_index = (year + 8) % 12
# 		return "{} {}".format(MtLunar.CAN[can_index], MtLunar.CHI[chi_index])

# 	def zodiac_day(solar_dd, solar_mm, solar_yy):
# 		julian_day = MtLunar.julian_day_from_date(solar_dd, solar_mm, solar_yy)
# 		can_index = (julian_day + 9) % 10
# 		chi_index = (julian_day + 1) % 12
# 		return "{} {}".format(MtLunar.CAN[can_index], MtLunar.CHI[chi_index])

# 	def lunar_leap(yy):
# 		if yy % 19 in [0, 3, 6, 9, 11, 14, 17]:
# 			return 1
# 		else:
# 			return 0

# 	def zodiac_month(month, year):
# 		can_index = (year * 12 + month + 3) % 10
# 		return "{} {}".format(MtLunar.CAN[can_index], MtLunar.CHI_MONTH[month])

# 	def solar_to_lunar_string(solar_dd, solar_mm, solar_yy, time_zone=7):
# 		lunar_day = MtLunar.solar_to_lunar(solar_dd, solar_mm, solar_yy, time_zone)
# 		_day_in_week = MtLunar.day_in_week(solar_dd, solar_mm, solar_yy)
# 		_zodiac_year = MtLunar.zodiac_year(solar_yy)
# 		_zodiac_month = MtLunar.zodiac_month(lunar_day[1], lunar_day[3])
# 		_zodiac_day = MtLunar.zodiac_day(solar_dd, solar_mm, solar_yy)
# 		if lunar_day[3]:
# 			return "{} - {}/{}/{} AL {}; ngày :{} tháng: {} năm: {}".\
# 					format(_day_in_week, lunar_day[0], lunar_day[1],
# 						lunar_day[2], "", _zodiac_day, _zodiac_month,
# 						_zodiac_year)
# 		else:
# 			return "{} - {}/{}/{} AL{}; ngày: {} - tháng: {} - năm: {}".\
# 					format(_day_in_week, lunar_day[0], lunar_day[1],
# 						lunar_day[2], "", _zodiac_day, _zodiac_month,
# 						_zodiac_year)

