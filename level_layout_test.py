from csv import reader


with open("stages.csv") as file:
	csv_reader = reader(file, delimiter=";")
	data = list(csv_reader)
	
for line in data:
    print(line)