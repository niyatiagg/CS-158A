## Overview
This program implements a distributed leader election algorithm in an asynchronous ring network using sockets, where each node exchanges messages to determine a unique leader based on UUIDs. Here, server and client run on same node. 
## Setup
### Start the process

```commandline
python myleprocess.py 1
```

```commandline
python myleprocess.py 2
```

```commandline
python myleprocess.py 3
```
The process is executed on three separate terminals to simulate distinct nodes in the system, with each node running both a server and a client on separate threads. As part of the simulation, I have created three configuration and log files. The command-line arguments 1, 2, and 3 (above) specify which configuration and log files each node should use. Each server thread listens for incoming connections, while the corresponding client thread connects to the next node in the ring topology. Once connections are established, nodes exchange messages containing a universally unique identifier (UUID) and a flag indicating the state of leader election. Upon receiving a message, a node compares the incoming UUID with its own: if the incoming UUID is greater, it forwards the message; if it is lesser, the message is ignored. If a node receives a message containing its own UUID, it declares itself the leader, updates the flag to 1. It then sends the message to its neighbor to inform the rest of the nodes of the decision, and lastly, prints the leader announcement to the console along with the rest of the nodes.
## Examples

### Example 1
_Node1 Output_
```
Connection refused, retrying...
Client connected:  ('localhost', 12002)
Leader is d51e4824-f1d9-4347-9ebd-d805eea17c5a

```

_Node2 Output_
```
Connection refused, retrying...
Client connected:  ('localhost', 12003)
I am the Leader with id: d51e4824-f1d9-4347-9ebd-d805eea17c5a


```

_Node3 Output_
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