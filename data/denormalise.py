import csv

def fileToList(filePath):
	with open(filePath, "rb") as f:
		listed = list(csv.reader(f))
	f.close()
	return listed

transactions = fileToList("transactions.csv")
gasstations = fileToList("gasstations.csv")
products = fileToList("products.csv")
customers = fileToList("customers.csv")