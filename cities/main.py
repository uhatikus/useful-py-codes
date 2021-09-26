import vk_api
import json
import time
import pymysql

connection = pymysql.connect(host='localhost',
                             user='user',
                             password='pw',
                             db='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
	with connection.cursor() as cursor:
		# remove table
		sql = "DROP TABLE IF EXISTS cities_T;"
		cursor.execute(sql)

	with connection.cursor() as cursor:
		# create table
		sql = "CREATE TABLE IF NOT EXISTS cities_T ( id INTEGER, title VARCHAR(255), region VARCHAR(255), area VARCHAR(255), country VARCHAR(255), PRIMARY KEY (id) );"
		cursor.execute(sql)
	# connection is not autocommit by default. So you must commit to save
	# your changes.
	connection.commit()
 
finally:
	connection.close()
	# with connection.cursor() as cursor:
	# 	# Create a new record
	# 	sql = "INSERT INTO cities_T (id, title, region, country) VALUES (%s, %s, %s, %s)"
	# 	cursor.execute(sql, (4, 'Мурсманск', 'Мурманская область', 'Россия'))


vk_session = vk_api.vk_api.VkApi('+79000000000', 'pw')
vk_session.auth()

vk = vk_session.get_api()

max_num_of_cities = 1000
country_ids = [1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18]
n = 1.0*len(country_ids)

countries = vk.database.getCountriesById(country_ids=country_ids)
print("cities")
c = 1.0
cities = []
for country in countries: 
	print("__________ new coutry ___________")
	print(c/n)
	c += 1
	response = (vk.database.getCities(country_id=country['id'], need_all=1, count=max_num_of_cities, offset=0))
	first_count = response['count']
	count = first_count - max_num_of_cities
	cities = cities + response['items']
	iteration = 1
	while count > 0:
		print(max_num_of_cities*iteration/first_count)
		response = (vk.database.getCities(country_id=country['id'], need_all=1, count=max_num_of_cities, offset=iteration*max_num_of_cities))
		cities = cities + response['items']
		count = count - max_num_of_cities
		iteration += 1
	connection = pymysql.connect(host='localhost', user='root', password='root', db='cities', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
	print("Write to mysql table")
	try:
		for city in cities:
			with connection.cursor() as cursor:
				# Create a new record
				if ('area' in city) and ('region' in city):
					sql = "INSERT INTO cities_T (id, title, region, area, country) VALUES (%s, %s, %s, %s, %s)"
					cursor.execute(sql, (city['id'], city['title'], city['region'], city['area'], country['title']))
				elif ('region' in city):
					sql = "INSERT INTO cities_T (id, title, region, country) VALUES (%s, %s, %s, %s)"
					cursor.execute(sql, (city['id'], city['title'], city['region'], country['title']))
				elif ('area' in city):
					sql = "INSERT INTO cities_T (id, title, area, country) VALUES (%s, %s, %s, %s)"
					cursor.execute(sql, (city['id'], city['title'], city['are'], country['title']))
				else:
					sql = "INSERT INTO cities_T (id, title, country) VALUES (%s, %s, %s)"
					cursor.execute(sql, (city['id'], city['title'], country['title']))

		# connection is not autocommit by default. So you must commit to save
		# your changes.
		connection.commit()
	finally:
		connection.close()
	cities = []


# f = open("cities_test.txt","w")
# f.write(str(cities))
# f.close()



















# countries = vk.database.getCountriesById(country_ids=country_ids)
# print("cities in regions")
# count = 1.0
# for country in countries:
# 	print("__________ new coutry ___________")
# 	print(count/n)
# 	count += 1
# 	country['regions'] = (vk.database.getRegions(country_id=country['id'],count=1000))['items']
# 	count2 = 1.0
# 	n2 = 1.0*len(country['regions'])
# 	for region in country['regions']:
# 		print(count2/n2)
# 		count2 += 1
# 		region['cities'] = (vk.database.getCities(country_id=country['id'], region_id=region['id'], need_all=1, count=1000))['items']
# f = open("cities_in_regions.txt","w")
# f.write(str(countries))
# f.close()

# print("schools in cities in regions")
# count = 1.0
# for country in countries:
# 	print("__________ new coutry ___________")
# 	print(count/n)
# 	count += 1
# 	count2 = 1.0
# 	n2 = 1.0*len(country['regions'])
# 	for region in country['regions']:
# 		print(count2/n2)
# 		count2 += 1
# 		for city in region['cities']:
# 			city['schools'] = (vk.database.getSchools(city_id=city['id'], count=10000))['items']
# f = open("schools_in_cities_in_regions.txt","w")
# f.write(str(countries))
# f.close()

# countries = vk.database.getCountriesById(country_ids=country_ids)
# print("cities")
# count = 1.0
# for country in countries: 
# 	print("__________ new coutry ___________")
# 	print(count/n)
# 	count += 1
# 	country['cities'] = (vk.database.getCities(country_id=country['id'], need_all=1, count=1000))['items']
# f = open("cities.txt","w")
# f.write(str(countries))
# f.close()

# print("schools in cities")
# count = 1.0
# for country in countries:
# 	print("__________ new coutry ___________")
# 	print(count/n)
# 	count += 1
# 	count2 = 1.0
# 	n2 = 1.0*len(country['cities'])
# 	for city in country['cities']:
# 		print(count2/n2)
# 		count2 += 1
# 		city['schools'] = (vk.database.getSchools(city_id=city['id'], count=10000))['items']
# f = open("schools_in_cities.txt","w")
# f.write(str(countries))
# f.close()