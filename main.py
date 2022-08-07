import requests
import time
import bitcoinaddress
from multiprocessing import Process, Queue
import hashlib
import os
from config import *

def worker(treasure: Queue, tasks: Queue, worker_id: int):
    while not tasks.empty(): 
        tasks_block = list()
        for i in range(20):
            tasks_block.append(tasks.get())
            if tasks.empty():
                break
                
        wallets = list()
        for task in tasks_block:     
            wallets.append(bitcoinaddress.Wallet(task))

        addresses = ''
        for wallet in wallets:
            addresses+=wallet.address.__dict__['mainnet'].__dict__['pubaddr1']+'|'
        balances = requests.get('https://blockchain.info/balance?active='+addresses[:-1]).json()
        for address in addresses[:-1].split('|'):
            WIF = str(wallets[addresses[:-1].split('|').index(address)].key).split('\n')[2]
            WIF = WIF[WIF.index(':')+1:].rstrip()
            
            if balances[address]['n_tx'] != 0 and GET_NUMBER_OF_TRANSACTION:
                print(f'[W] worker id:{worker_id} | number of transactions:{ balances[address]["n_tx"]} | address:{address} | WIF:{WIF}')
            if balances[address]['final_balance'] != 0:
                print(f'[W] worker id:{worker_id} | balance (satoshi):{balances[address]["final_balance"]} | address:{address} | WIF:{WIF}')
                treasure.put(wallet)

def main():
    start = time.time()
    
    treasure = Queue()
    tasks = Queue()

    for i in range(startr, stopr):
        tasks.put("0"*(64-len(str(i)))+str(i))
    print('[INFO] Tasks is ready')

    workers = []
    for i in range(WORKERS_AMOUNT):
        w = Process(target=worker, args=(treasure, tasks, i))
        w.start()
        workers.append(w)
    print("[INFO] Workers is ready")
    
    for w in workers:
        w.join()
    print("[INFO] Workers is joined")
    
    print('[INFO]', round(time.time()-start, 2), 'sec spent from start')

    wif_list = list()

    if treasure.empty():
        print('[INFO] Wallet with bitcoins not found')
        return 0
    
    while not treasure.empty():
        wif_list.append(str(treasure.get().key).split('\n')[2])

    with open('treasure.txt', 'w') as f:
        for wif in wif_list:
            f.write(wif+'\n')
    print('[INFO] Treasure written in file')
    

if __name__ == "__main__":
    main()