## Computer Architecture: An Overview

Note:
Goal is to discuss how computer works in general.

Some definitions of computer architecture limit it only hardware, but here we'll
discuss the software parts as well.



## Von Neumann Architecture
* Control Unit
* ALU (Arithmetic Logic Unit)
* Memory
* Input/Output


### Control Unit
Provides signal and timings.

Directs flow of data.

Typically part of the CPU.


### Arithmetic Logic Unit
Performs calculations.


### Memory
In the Von Neumann model, the memory contains both program and data and doesn't
distinguish between the two.

Typically refers to the RAM (Random Access Memory). But it can also refer to the
caches and, to some extent, secondary storage (e.g. hard disk).


### Input/Output
I/O are external sources of data, such as storage or interfaces to the user,
e.g.:

* Hard disk
* Mouse
* Monitor
* Printer


### Bus
Data lines between the different components, the most important of which is the
memory bus (connection between CPU and memory).


### Von Neumann Bottleneck
Despite the speed of the CPU and the capacity of the memory, the speed of the
computation is limited by the bus because the instructions are also stored in
memory. Instructions and data cannot be accessed at the same time because they
share a common bus.

Note: Mitigations to this problem will be discussed later.


### Current architectures are more complicated now
But they are still generally based on the Von Neumann model.

Now there are configurations where you have things such as:

* Multiple CPUs
* Multiple cores
* External processing units (e.g. GPUs)



## CPU
#### Central Processing Unit
* Controls the computer and its peripherals
* Performs most of the calculations
* Primary coordinator


### How does a CPU work?
<img src="images/CPU.svg" alt="CPU" height="400" />

Note: Refer to the Von Neumann Architecture


### CPU clock rate
* Controls the rate of execution
* Each clock tick represents a transition of state.
* Note that not all instructions finish in a single tick, so, externally there
  might be no state change but internally there is (transistor/gate states).


### Motherboard
![Motherboard diagram](images/Motherboard_diagram.svg)

_(Intel architecture)_


### Motherboard
* The motherboard binds all the peripherals together, creating an
  interconnection between the devices.
* Provides power, cooling, etc.


### Peripherals
* Has its own controller.
* DMA (Direct Memory Access)
* Hardware interrupt
* Drivers


### Hardware interrupt
* More efficient than busy-waiting.
* Interrupt-driven processing is similar to event-driven programming.


### Hardware interrupt examples
#### Keyboard
* There is a registered interrupt handler to process a particular IRQ (Interrupt
  Request). The OS usually does the registration.
* After a key press, an interrupt will be sent to the CPU.
* If there's an interrupt, the handler will be executed instead of the next
  instruction of the program currently being executed.
* The handler will read the code of the key pressed from the controller of the
  keyboard.


### Hardware interrupt examples
#### Hard disk (without DMA)
* The CPU issues a read request to the hard drive by writing to the hard disk
  controller. The specific instructions depend on the hard disk (the driver
  knows this).
* The controller reads the values in the specified address (or address range).
  The hard disk controller independently does its job while the CPU executes
  other instructions.
* When the controller is ready (the values are stored in its own registers),
  it signals an interrupt to the CPU.
* Similar to the keyboard example, a handler will be executed and the CPU then
  reads the values from the controller.


### Hardware interrupt examples
#### Hard disk (with DMA)
* With DMA, the read request comes with the specified memory location where the
  read values will be stored. So instead of storing the values in its own
  registers, it stores the read values in the memory.
* Because of DMA, the hard drive controller directly communicates with the
  memory controller instead of going through the CPU. This removes lots of
  back-and-forth communication between the CPU and the hard drive, since usually
  the values read from the hard drive are going to be stored in memory anyways.


### Instruction cycle
<img src="images/Comp_fetch_execute_cycle.png" alt="Fetch-execute cycle" height="600" />


### Machine code
Machine code is the code directly processed by the CPU via the instruction
cycle. It is stored in the code section of the program.

Machine code consists of a series of opcodes with "arguments". Intel
architectures have variable-length opcodes.


### Assembly
Closest language next to machine code. Almost one-to-one correspondence with
machine code.

Contains different sections like the data section and the code section.

The code section contains a series of assembly instructions. Assembly
instructions (with arguments) roughly corresponds to opcodes.


### Assembly Instructions
#### Examples
* LOAD
* ADD
* SUB
* JMP

Note: JMP instructions have long and short variants, in order to account for
caches.


### Function call
* Stack
* Arguments
* Return values


### Software interrupt
Interrupts that are not triggered by an external peripheral.

* Exceptions (e.g. divide by zero).
* Timers
* Page fault
* System call



## Operating System
Direct layer between a program and the hardware.

Provides various services like resource management.

Note: Very difficult to program against the hardware directly.


### Layers
<img src="images/Layers.svg" alt="Layers" height="600" />


### Resource management
#### Examples
* Hard drive access
* Memory access
  * Virtual memory
* CPU scheduling
* Display
* Keyboard input
* Networking


### System call
User-mode programs call to kernel-mode.

Functions that only the OS can do.
Note that this is different from user privileges (e.g. root access).

Normally, system calls are not invoked directly by programs. There's a
higher-level library that you use that does for you (e.g. libc, Win32).

Note:
Modern CPUs can set what the current instruction cannot do. The OS have the
highest privilege (also called CPU mode), unless the OS is running on top of a
virtual machine.

Not all functions in these top-level libraries use system calls.


### System call
#### Examples
* Read/write to/from a file
  * Filesystem access in general
* Create a new process
* Listen to a port


### Device driver
Knows how to communicate to the corresponding device's controllers.

Runs together with the kernel.

Note:
Since device drivers is part of the "kernel program", it has the same privilege
as the kernel. It can bypass system calls (and its associated costs) which is
normally required for performant hardware communication.

With this power comes with responsibility as poor programming can result in the
whole system crashing. Or worse, as it can also result to permanent damage to
hardware.

Malicious software, such as rootkits, can be installed via drivers. Since they
have unrestricted privilege, it's very difficult to detect and get rid of them.


### Application Binary Interface
* Specifies how binary files (e.g. executable files) are layed out, like:
  * Headers
  * Code section
  * Data section
* Function calling convention
* How to make system calls



## Process
Encapsulates an instance of a program.

* Code
* Memory
  * Stack
  * Heap
* Handles/descriptors to resources
* Privileges
* Process state


### Process states
<img src="images/Process_states.svg" alt="Process states" height="600" />
Note:
Signals can be sent to force a process to be suspended (until continued) or
terminated.


### Concurrent execution
Multi-tasking via process scheduling.

General-purpose operating systems do it _pre-emptively_.

Note:
Concurrent execution is different from parallel execution (although parallel
implies concurrent). Parallel execution means that multiple instructions are
actually being run at the same time, which is only possible with hardware
support (e.g. multi-core, hyperthreading).

Pre-emptive multi-tasking is done via software interrupts (timers).


### Thread
Smallest stream of instructions

A process always has at least one (the main thread). Multiple threads under the
same process share everything in that process except their own stacks.

Note:
Mention lightweight threads like greenlets and goroutines.
Also mention the dangers of multi-threaded programming.


### Sample process life cycle
Note:
* Two processes
* One process has two threads.
* System call
* Context switch
* Blocking call
* Send signal



## Further reading
* Structured Computer Organization by Tanenbaum
* [LectureCA-all-slides.pdf](http://www.fb9dv.uni-duisburg.de/vs/en/education/dv3/lecture/freinatis/LectureCA-all-slides.pdf)
Note:
Tanenbaum is our textbook while at school. Not sure how good it is relative to
other books, since I haven't read those other books.
