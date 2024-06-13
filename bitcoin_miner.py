import hashlib
import time
import requests
import threading

def get_latest_block():
    response = requests.get('https://blockchain.info/latestblock')
    return response.json()

def mine(block, difficulty, start_nonce, step):
    prefix = '0' * difficulty
    nonce = start_nonce
    start_time = time.time()
    
    while True:
        text = block['hash'] + str(nonce)
        new_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        if new_hash.startswith(prefix):
            end_time = time.time()
            print(f"Block mined! Nonce: {nonce}")
            print(f"Hash: {new_hash}")
            print(f"Time taken: {end_time - start_time} seconds")
            break
        nonce += step

def main():
    difficulty = 4  # Adjust difficulty as needed
    block = get_latest_block()
    print(f"Mining new block after: {block['hash']}")
    
    num_threads = 4  # Number of threads
    threads = []
    
    for i in range(num_threads):
        thread = threading.Thread(target=mine, args=(block, difficulty, i, num_threads))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
