## Overview
This program implements a distributed leader election algorithm in an asynchronous ring network using sockets, where each node exchanges messages to determine a unique leader based on UUIDs. Here, server and client run on same node. 
## Setup
### Start the process

```commandline
python myleprocess.py
```
The process is run on three different terminals to simulate distinct nodes, each with a server and client running on separate threads. The server listens for incoming connections, while the client connects to the next node in the ring. Once connected, nodes exchange messages containing a UUID and a flag. Upon receiving a message, a node compares the incoming UUID with its own: it relays the message if the incoming UUID is greater, ignores it if it's lesser, and if the UUID matches its own, it identifies itself as the leader. It then sends a new message with flag = 1 to inform other nodes and prints the leader announcement to the console.

## Examples

### Example 1
_Process1 Output_
```
Connection refused, retrying...
Client connected:  ('localhost', 12002)
Leader is d51e4824-f1d9-4347-9ebd-d805eea17c5a

```

_Process2 Output_
```
Connection refused, retrying...
Client connected:  ('localhost', 12003)
I am the Leader with id: d51e4824-f1d9-4347-9ebd-d805eea17c5a


```

_Process3 Output_
```
Client connected:  ('localhost', 12001)
Leader is d51e4824-f1d9-4347-9ebd-d805eea17c5a

```

## Log file Screenshots

### For Node1:

![Screenshot 2025-07-08 at 11.55.00 PM.png](Screenshot%202025-07-08%20at%2011.55.00%E2%80%AFPM.png)

### For Node2:

![Screenshot 2025-07-08 at 11.56.05 PM.png](Screenshot%202025-07-08%20at%2011.56.05%E2%80%AFPM.png)

### For Node3:

![Screenshot 2025-07-08 at 11.56.48 PM.png](Screenshot%202025-07-08%20at%2011.56.48%E2%80%AFPM.png)