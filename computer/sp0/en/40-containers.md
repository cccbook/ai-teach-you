# 40. Container Technology——namespace and cgroup

## 40.1 Containers vs Virtual Machines

| Feature | Container | Virtual Machine |
|---------|-----------|-----------------|
| Isolation level | Operating system | Hardware |
| Startup speed | Seconds | Minutes |
| Performance | Near native | More overhead |
| Resource isolation | namespace, cgroup | Full virtualization |

## 40.2 Linux Namespace

Namespace isolates system resources.

| Namespace | Isolates |
|-----------|----------|
| PID | Process IDs |
| Network | Network devices |
| Mount | Mount points |
| IPC | Signals, shared memory |
| UTS | Hostname |
| User | User IDs |

### 40.2.1 API

```c
// Create namespace
int unshare(int flags);
int setns(int fd, int nstype);

// /proc/PID/ns directory
ls /proc/self/ns/
```

### 40.2.2 Example

```c
unshare(CLONE_NEWPID | CLONE_NEWUTS);
execlp("bash", "bash", NULL);
```

## 40.3 cgroup

cgroup controls resource usage.

### 40.3.1 Subsystems

| Controller | Controls |
|------------|----------|
| cpu | CPU time distribution |
| memory | Memory limits |
| blkio | I/O bandwidth |
| cpuset | CPU core allocation |

### 40.3.2 Set Limits

```bash
# Create cgroup
mkdir /sys/fs/cgroup/memory/mylimit

# Set memory limit (100MB)
echo 104857600 > /sys/fs/cgroup/memory/mylimit/memory.limit_in_bytes

# Add process to group
echo $PID > /sys/fs/cgroup/memory/mylimit/tasks
```

## 40.4 Docker Basics

### 40.4.1 Basic Operations

```bash
# Run container
docker run -it ubuntu bash

# Build image
docker build -t myapp .

# List containers
docker ps -a
```

### 40.4.2 Dockerfile

```dockerfile
FROM ubuntu:latest
COPY . /app
WORKDIR /app
RUN make
CMD ["./app"]
```

## 40.5 Summary

In this chapter we learned:
- Containers vs VM comparison
- Linux Namespace concepts
- cgroup resource control
- Docker basics

## 40.6 Exercises

1. Use unshare to create isolated environment
2. Research containerd and runc
3. Compare Docker and Kubernetes
