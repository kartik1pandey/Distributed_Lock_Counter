# REST-based Distributed Counter (Concurrency Control Demo)

## 🎯 Project Description
A distributed counter system demonstrating the **lost update problem** in concurrent environments. The system shows how race conditions occur without proper locking and how thread-safe mechanisms prevent data inconsistency.

## 🏗️ Architecture
```
Client (Multiple Threads)
    ↓ (Concurrent HTTP Requests)
REST API Server (Flask)
    ├─ /increment (NO LOCK) → Demonstrates lost updates
    └─ /increment-safe (WITH LOCK) → Prevents race conditions
    ↓
Shared Counter (In-Memory)
```

The server maintains two counters: one without synchronization (unsafe) and one with mutex lock (safe). Concurrent requests expose the race condition in the unsafe version.

## 👥 Group Details
**Group Number:** 6 
**Project Title:** REST-based Distributed Counter

## 📋 Prerequisites
- Python 3.8 or higher
- pip package manager

## 🚀 How to Run

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server (Terminal 1)
```bash
python server.py
```
You should see:
```
🚀 Starting Distributed Counter Server...
✅ Server running on http://localhost:5000
```

### Step 3: Run the Client (Terminal 2)
```bash
python client.py
```

The client will automatically:
1. Test concurrent increments WITHOUT lock
2. Show lost updates
3. Test concurrent increments WITH lock
4. Show correct behavior

## 📊 Expected Output

**Without Lock (Unsafe):**
```
Expected value: 100
Actual value:   87
Lost updates:   13
⚠ LOST UPDATE PROBLEM DETECTED!
```

**With Lock (Safe):**
```
Expected value: 100
Actual value:   100
Lost updates:   0
✓ SUCCESS! Lock prevented race conditions
```

## 🔍 Key Concepts Demonstrated

1. **Race Condition**: Multiple threads reading and writing shared data simultaneously
2. **Lost Update Problem**: Updates are overwritten due to concurrent access
3. **Mutex Lock**: Ensures only one thread accesses critical section at a time
4. **Thread Safety**: Proper synchronization prevents data corruption

## 📁 Project Structure
```
Group_XX_DistributedCounter/
├── server.py           # REST API server with safe/unsafe endpoints
├── client.py           # Test client simulating concurrent requests
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── demo_video.mp4     # 5-minute demonstration video
└── group_details.txt  # Group member information
```

## 🎥 Demo Video Contents
1. **Introduction (0:00-0:20)**: Team introduction and project name
2. **System Overview (0:20-1:20)**: What the counter system does
3. **Architecture (1:20-2:20)**: Diagram explanation
4. **Live Demo (2:20-4:20)**: Running both tests showing the difference
5. **Takeaway (4:20-5:00)**: Key learning about concurrency control

## 🛠️ Technical Details

**Server:**
- Framework: Flask (Python)
- Port: 5000
- Threading: Multi-threaded request handling
- Synchronization: `threading.Lock()`

**Client:**
- Concurrent Requests: 100 threads
- Library: `requests` + `threading`
- Visual Output: Colored console using `colorama`

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/increment` | POST | Increment without lock (unsafe) |
| `/increment-safe` | POST | Increment with lock (safe) |
| `/reset` | POST | Reset both counters to 0 |
| `/status` | GET | Get current counter values |

## 💡 What We Learned

1. **Concurrency is hard**: Even simple increment operations can fail without proper synchronization
2. **Locks ensure consistency**: Mutex locks guarantee data integrity in concurrent environments
3. **Trade-offs exist**: Locking adds overhead but ensures correctness
4. **Testing is crucial**: Race conditions may not appear in sequential testing

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Module not found:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Connection refused:**
- Ensure server is running before starting client
- Check firewall settings for port 5000

## 📚 References
- Flask Documentation: https://flask.palletsprojects.com/
- Python Threading: https://docs.python.org/3/library/threading.html
- Concurrency Control: Database Systems Concepts

---