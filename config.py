WORKERS_AMOUNT = 4 
startr = 1   #int from workers start generate secret key (0 is Error value)
stopr  = 10000 #int to workers stop generate secret key
#amount checked wallet equal stopr-startr
GET_NUMBER_OF_TRANSACTION = True # if True , workers print (but don't put in file) wallets with 0 balance and nonzero number of transactions
