from flask import Flask, render_template
import hashlib
import time
import requests
import threading

app = Flask(__name__)

mining = True  # Control flag for the mining process
difficulty = 4  # Starting difficulty
target_time = 10  # Target time in seconds for mining a block

def get_latest_block():
    response = requests.get('https://blockchain.info/latestblock')
    return response.json()

def mine(block, difficulty):
    global mining
    prefix = '0' * difficulty
    nonce = 0
    start_time = time.time()
    
    while mining:
        text = block['hash'] + str(nonce)
        new_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        if new_hash.startswith(prefix):
            end_time = time.time()
            duration = end_time - start_time
            print(f"Block mined! Nonce: {nonce}")
            print(f"Hash: {new_hash}")
            print(f"Time taken: {duration} seconds")
            adjust_difficulty(duration)
            return nonce, new_hash, duration
        nonce += 1

def adjust_difficulty(duration):
    global difficulty
    if duration < target_time:
        difficulty += 1
    elif duration > target_time:
        difficulty -= 1
    print(f"New difficulty: {difficulty}")

def start_mining():
    while True:
        block = get_latest_block()
        print(f"Mining new block after: {block['hash']}")
        mine(block, difficulty)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    global mining
    mining = True
    threading.Thread(target=start_mining).start()
    return "Mining started!"

@app.route('/stop')
def stop():
    global mining
    mining = False
    return "Mining stopped!"

if __name__ == "__main__":
    app.run(debug=True)
