## OS X FS Events and `isdaemon`



## Outline
* Rationale
* Overview of `isdaemon`
* IPC between `isdaemon` and Insync
* Installation and launching the `isdaemon` process



## Goals:
Receive notifications of filesystem events



## Option 1: `FSEvents` API
* Available in OS X 10.5+
* Register for notification of changes in a directory hierarchy
* Can be notified of offline changes


## Option 1: `FSEvents` API
* Coalesces multiple notifications
* Directory-level granularity: doesn't contain _what_ changed
  * So there's a need to keep state snapshots and perform diffs
* Not intended to be fine-grained and real-time


## Option 1: `FSEvents` API
* Since 10.7, file-level notifications have become available, but we haven't revisited this API
* 10.5 and 10.6 support


## Option 2: `kqueue`
* Event notification interface introduced in FreeBSD 4.1
* Supports monitoring file descriptors, processes, signals, asynchronous I/O, VNODEs


## Option 2: `kqueue`
* Can't be used recursively to watch an entire directory tree
* Needs to open a file descriptor to watch a file
* Will not scale well with increasing number of watched files


## Option 3: `/dev/fsevents`
* Read `/dev/fsevents` directly -- special device file used by Spotlight and `FSEvents` API


## Option 3: `/dev/fsevents`
* Granular, per-file, real-time notifications
* Depending on implementation, can be faster than `FSEvents` API
* More efficient that using `kqueue`


## Option 3: `/dev/fsevents`
* Requires root access
* The raw feed will include ALL FS events
* Undocumented and unsupported



## `isdaemon`
* `isdaemon` is the daemon (i.e., background process) with root access that reads `/dev/fsevents`
* Insync client's `MacFSWatcher` connects to `isdaemon` to retrieve FS events


### Threads
* Main thread
* `prepareEventMessage` thread
* `runServer` thread



### Digression: kernel mode, user mode, and `ioctl`


## The kernel
* Core of the operating system
* Has complete control over and access to entire system
* Connects application software to the hardware and manages:
  * System startup
  * I/O requests from applications
  * Memory
  * Devices/peripherals
* On OS X, it's called Darwin
  * Built on top of Mach and BSD
  * Open source


## Kernel mode vs user mode
* _kernel mode_: executing code has complete and unrestricted access to hardware
* _user mode_: executing code can't directly access hardware or memory
* Program crashes in _user mode_ are recoverable
* These modes are enforced by the CPU hardware


## Kernel space vs user space
* Memory also gets divided similarly into _kernel space_ and _user space_
* The kernel can access user space, but user processes can't access kernel space


### Making requests to the kernel from userspace
* System calls are provided by the kernel, e.g.,
  * File management (`open`, `close`, `read`, `write`, etc.)
  * Process management (`load`, `execute`, etc.)
  * Device management (request/release device, read/write, attach/detach)


## `ioctl`
* System call for device-specific operations
* Allows userspace to communicate with device drivers
* e.g., `/dev/fsevents`



## `isdaemon` main thread
* The main loop just reads from `/dev/fsevents` until the daemon is terminated


### Reading from `/dev/fsevents`
`isdaemon/FSLogger.m`:
```objective-c
fd = open('/dev/fsevents', O_RDONLY); // get a read-only file descriptor

// retrieve_ioctl is a struct of the message/args for the ioctl call:
// * event_list - action (report/ignore) to take for each event type (e.g.,
//   create/delete/modify/stat change)
// * num_events - length of event_list
// * event_queue_depth - unsure, undocumented, related to event buffering
// * fd - pointer to file descriptor which will hold the cloned fsevents
//   descriptor to read from
retrieve_ioctl.event_list = event_list;
retrieve_ioctl.num_events = sizeof(event_list);
retrieve_ioctl.event_queue_depth = EVENT_QUEUE_SIZE;
retrieve_ioctl.fd = &newfd;

// FSEVENTS_CLONE is a command number for `ioctl`
// generated in `fsevents.h`
if (ioctl(fd, FSEVENTS_CLONE, &retrieve_ioctl) < 0) {
  die(1);
};

close(fd);

while (!_terminateServer)
{
  n = read(newfd, large_buf, sizeof(large_buf));
  if (!_terminateServer && n > 0)
  {
    [self processEventNotification:n];
  }
}
```


### Parsing the read event data
* `processEventNotification` reads from `large_buf` and parses the ff. event info:
  * action - add/delete/modify/move
  * path - path to the changed item, OR the original path for moves
  * destPath - destination for moves
* The events are added to `_eventList`
* It signals the `prepareEventMessage` thread that new events are available



## `prepareEventMessage` thread
* Continuously waits for main thread's signal
* Gets the events retrieved by the main thread, then:
  * Filters the events based on paths to watch registered by the Insync client
  * Adds the filtered events to the queue which is made accessible to the Insync client



## `isdaemon` `runServer` thread
* Sets up an `NSConnection` making the `isdaemon` object available via Cocoa's Distributed Objects API



### IPC between `isdaemon` and Insync: Distributed Objects
* Cocoa API for IPC built on automatic proxying of messages
* Remote objects look and act (mostly) like local objects
* Remote object can be in different thread/process/machine
* Very simple interface using `NSConnection`


## Distributed Objects
Setting up an object to be vended (just on the same machine):
```objective-c
NSConnection *conn = [[NSConnection alloc] init];
[conn setRootObject:theObject];
[conn registerName:@"com.example.name"];
```


## Distributed Objects
Accessing a remote object (on the same machine):
```objective-c
id theObject = (id)[NSConnection
  rootProxyForConnectionWithRegisteredName:@"com.example.name"];
[theObject someMethod];
```



## IPC between `isdaemon` and Insync
* Insync clients register with the `isdaemon` using `registerClient:`
* Multiple clients (i.e., different users) can register
* A queue for FS events is created for each registered client


## In the Insync client
`isyncd/mac/ipclistener.IPCListener.getDaemonConnection`:
```python
daemon_object = (Foundation.NSConnection
                 .rootProxyForConnectionWithRegisteredName_host_(IPC_DAEMON_NAME, None))
if daemon_object is None:
  logging.info("Daemon is not alive, retrying after 1 second.")
  time.sleep(1)
  continue
daemon_object.retain()
daemon_object.registerClient_(self._serverString)
self._daemon = daemon_object
```


### IPC between `isdaemon` and Insync
`isyncd/mac/fswatcher.py`:
```python
while self.is_running:
  try:
    with sub_auto_release():
      daemon_object = self._ipc_listener.getDaemonConnection()
      eventsList = daemon_object.getEventsList_(self._ipc_listener.get_server_string())
      if eventsList is None:
        continue
      eventsList.retain()
      for eventDict in eventsList:
        // Process the retrieved events...
  except:
    logging.exception("Events harvesting failed!")
    time.sleep(1)
```



## `isdaemon`: Installation and launching
* Needs to be run with root access
* Would be good to run automatically


## `isdaemon`: Using `launchd`
* `launchd` is a service-management framework
* On OS X, it boots the system as well as loading and maintaining services
* `launchctl` is the corresponding command-line application


## `isdaemon`: `launchd`
* `daemon`: run as root, config files in `/Library/LaunchDaemons`
* `agent`: run as the logged in user, config files in `/Library/LaunchAgents`


## `isdaemon`: Installation
* Create configuration `plist` file at `/Library/LaunchDaemons/com.insynchq.insync.daemon.plist`
* Load config file using `launchctl`


## `isdaemon`: Configuration
* `UserName`: `root`
* `PathState`: `/tmp/isdaemon.launch`
  * `launchd` will start and stop `isdaemon` depending on whether this file exists

