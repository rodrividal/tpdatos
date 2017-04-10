import csv
star_date_colum = 2
nombre = input("Ingrese nombre para csv parseado: ") + ".csv"
writer = csv.writer(open('C:\\Users\\Agustin\\Documents\\Python\\tp\\' + nombre , "w"))
with open('C:\\Users\\Agustin\\Documents\\Python\\tp\\trip.csv', newline='', encoding='utf-8') as f:
	reader = csv.reader(f)
	for row in reader:
		
		row[star_date_colum]=row[star_date_colum].replace("/","").replace(" ","").replace(":","")
		
		writer.writerow(row)
		

