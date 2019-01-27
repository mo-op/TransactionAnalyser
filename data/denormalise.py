import csv, json
'''
This script combines the files to a 
'''

def fileToList(filePath):
	with open(filePath, "rb") as f:
		listed = list(csv.reader(f))
	f.close()
	return listed

def returnCustomerDetails(c_ID):
	'''
	To return product details matching the customer ID. Structure:
	CustomerID	Segment	Currency
	'''
	global customers
	found = False
	for customer in customers:
		if customer[0] == c_ID:
			found = True
			return customer[1], customer[2]

	if found == False:
		# fabricating details if customer not found
		segment = "SME" 
		currency = "CZK"
		customer = [c_ID, segment, currency]
		return customer[1], customer[2]

def returnProductDescription(p_ID):
	'''
	To return customer details matching the customer ID. Structure:
	CustomerID	Segment	Currency
	'''
	global products
	found = False 
	for product in products:
		if product[0] == p_ID:
			found = True
			return product[1]

	if found == False:
		# fabricating details if product not found
		desc = "Product Description Unavailable"
		return desc

def returnGasStationDetails(gs_ID):
	'''
	To return gas station details matching the ID. Structure:
	GasStationID	ChainID	Country	Segment
	'''
	global gasstations
	found = False 
	for gasstation in gasstations:
		if gasstation[0] == gs_ID:
			found = True
			return gasstation[1], gasstation[2], gasstation[3]

	if found == False:
		# fabricating details if product not found
		chain = random.randint(1,290)
		country = "CZE"
		segment = "Other" 
		return chain, country, segment 

transactions = fileToList("transactions.csv")[1:]
gasstations = fileToList("gasstations.csv")[1:]
products = fileToList("products.csv")[1:]
customers = fileToList("customers.csv")[1:]

combined_transactions = []

for transaction in transactions:
	
	'''
	TransactionID	Date	Time	CustomerID	CardID	GasStationID	ProductID	Amount	Price
	'''
	c_segment, c_currency = returnCustomerDetails(transaction[3])
	#print (c_segment, c_currency)

	p_description = returnProductDescription(transaction[6])
	#print (p_description)

	g_chainID, g_country, g_segment = returnGasStationDetails(transaction[5])
	#print (g_chainID, g_country, g_segment)
	combined_transaction = {	
	'ID': transaction[0],
	'Date': transaction[1],
	'Time': transaction[2],
	'Amount': transaction[7],
	'Price': float(transaction[8]),
	'Customer':{
		'ID': transaction[3],
		'Segment': c_segment,
		'Currency': c_currency,
		'Card_ID': transaction[4]
		},
	'GasStation':{
		'ID': transaction[5],
		'ChainID': g_chainID,
		'Country': g_country,
		'Segment': g_segment
		},
	'Product':{
		'ID': transaction[6],
		'Description': p_description
		}
	}

	combined_transactions.append(dict(combined_transaction))
	#print combined_transaction

print ("Combining files ....")
print(str(len(combined_transactions))+" combined")
#print combined_transactions

with open('denormalisedData.json', 'w') as outfile:  
    json.dump(combined_transactions, outfile)

print ("Testing ...")

filePath = "denormalisedData.json"
with open(filePath) as f:
	transactions_ = json.load(f)
print(str(len(transactions_))+" in json file!")