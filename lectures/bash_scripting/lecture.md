## Intro to Bash scripting



## What is Bash?
From the Wikipedia entry:

> "Bash is a Unix shell and command language..."

As a Unix shell, it allows users to call programs in their system. <!-- .element: class="fragment" -->

But it also has builtin commands separate from system programs. <!-- .element: class="fragment" -->



## Why use Bash?
- Servers usually don't have GUI interfaces, so the only way to interact with them is through the terminal. <!-- .element: class="fragment" -->
- Some tasks can be completed faster using the terminal. <!-- .element: class="fragment" -->
  - This is also useful in automation. For example, package build scripts in Mac and Linux. <!-- .element: class="fragment" -->


## Why use Bash?
- It can be powerful if used correctly.
  - https://aadrake.com/command-line-tools-can-be-235x-faster-than-your-hadoop-cluster.html
  - Amazon Elastic Map Reduce (EMR) and mrjob were used to compute some statistics on win/loss ratios for chess games.
  - Since the problem is basically just to look at the result lines of each file and aggregate the different results, it seems ideally suited to stream processing with shell commands.
  - Hadoop cluster - results in about **26 minutes.**
  - laptop - results in about **12 seconds!** <!-- .element: class="fragment" -->


## REKT!
![function](images/supahotfire.gif)



## Shebang
Most Bash scripts start with a shebang: `#!/bin/bash`

This indicates that the script will be executed with the indicated interpreter: in this case, `/bin/bash`.

The interpreter will only be used when the script is executed. <!-- .element: class="fragment" -->

- If it is passed as an argument to an interpreter, it will be ignored. <!-- .element: class="fragment" -->

```
$ cat shebang.sh
#!/bin/bash -x

echo "Hello"
```



## Variables
You don't need to declare a variable, just assigning a value will create it.

```
$ cat hello_world.sh
#!/bin/bash

STR="Hello World!"
echo "$STR"
```


## Assignment
Variable assignment is of the form `<variable>=<value>`. Putting spaces between the parts will raise an error.

```
$ cat assign.sh
#!/bin/bash

# This works.
VAR="value"
echo "$VAR"

# This does not.
VAR = "VALUE"
```


## Variables
Bash will not raise an error with unset variables. By default it treats unset variables as blank strings.

```
$ cat unset_var.sh
#!/bin/bash

echo "$STR"
```


## Variables
To raise warnings on unset variables, set the *u* flag.

```
$ cat warn_unset_var.sh
#!/bin/bash
set -u

echo "$STR"
```



## Capturing the output of a command
To store the output of a command in a variable, enclose the command in backticks (``) or $()

```
$ cat capturing.sh
#!/bin/bash

# The date command prints the current date and time.
DATE=`date`

echo "$DATE"

# This works too.
NEW_DATE=$(date)

echo "$NEW_DATE"
```



## Filename expansion
Bash does not recognize regular expressions. Instead it performs globbing which uses the following special characters:

- \* - matches zero or more characters
- ? - matches one character
- [] - matches an element of the character list inside the square brackets. Case insensitive.



## Escaping special characters
The backslash character \ is used to escape special characters.



## Quoting variables
- Single quotes - removes the special meaning of every character between the quotes. Everything inside single quotes becomes a literal string.
- Double quotes - prevents reinterpretation of all special characters within the quoted string -- except $, ` (backquote), and \ (escape). No word splitting or filename expansion is performed.  <!-- .element: class="fragment" -->


## Quoting variables
```
$ cat quoting.sh
#!/bin/bash

# $SHELL contains the current shell.

# This will just print the string $SHELL.
echo '$SHELL'

echo "---"

# This will print the value of the $SHELL variable.
echo "$SHELL"
```


## Quoting variables
```
$ cat word_splitting.sh
#!/bin/bash

list="one two three"

for l in $list; do
  echo $l
done
# one
# two
# three

echo "---"

for l in "$list"; do
  echo $l
done
# one two three
```


# Quoting variables
```
$ cat expansion.sh
#!/bin/bash

LYRICS="When you wish upon a *"

# Not the desired result.
echo $LYRICS

echo "---"

# Printed properly.
echo "$LYRICS"
```


## To quote or not to quote
When in doubt, **double-quote every parameter expansion** in your shell commands.

```
$ cat values_with_spaces.sh
#!/bin/bash

SOURCE="source file"
DEST="dest file"

# This won't work.
cp -v $SOURCE $DEST

# This works.
cp -v "$SOURCE" "$DEST"
```



## Return code
- When a command exits, it returns an integer value between 0 and 255 inclusive. This is used by the calling application to determine if the command succeeded.
- 0 - success
- nonzero - error
- The return code of the last ran command is stored in `$?`.

```
$ cat return_code.sh
#!/bin/bash

# false is a shell builtin that always returns 1
false
echo "Return code is $?"

echo "---"

# true is a shell builtin that always returns 0
true
echo "Return code is $?"
```



## Control operators
- command1 && command2 - command2 will only be run if the return code of command1 is 0
- command1 || command2 - command2 will only be run if the return code of command1 is nonzero <!-- .element: class="fragment" -->
- They can also be chained: command1 && command2 && command3 || ... <!-- .element: class="fragment" -->


## Control operators
```
$ cat control.sh
#!/bin/bash

false && echo "This will not be printed"
echo "---"
true && echo "This will be printed"
echo "---"
false || echo "This will be printed"
echo "---"
true || echo "This will not be printed"
echo "---"
true || echo "This will not be printed" && echo "But this will be printed"
echo "---"
true || { echo "This will not be printed" && echo "Because of grouping this will not be printed too"; }
```



## Conditional blocks
```
if COMMANDS; then
  COMMANDS
elif COMMANDS; then
  COMMANDS
...
else
  COMMANDS
fi
```


## Conditional blocks
```
$ cat simple_if.sh
#!/bin/bash

if [ "a" = "b" ]; then
  echo "They are equal."
else
  echo "They are not equal."
fi

# Strictly any command can be used with if.
if echo "This works."; then
  echo "This is printed."
fi
```


## The [ builtin
- `[` - a shell builtin that performs tests on the given arguments.
- The `]` at the end is just a required argument by `[`. It is not part of the command.


## String operators
| | |
|-|-|
| STRING = STRING | True if the first string is identical to the second. |
| STRING != STRING | True if the first string is not identical to the second. |
| STRING < STRING | True if the first string sorts before the second. |
| STRING > STRING | True if the first string sorts after the second. |


## Integer operators
| | |
|-|-|
| INT -eq INT | True if both integers are identical. |
| INT -ne INT | True if the integers are not identical. |
| INT -lt INT | True if the first integer is less than the second. |
| INT -gt INT | True if the first integer is greater than the second. |
| INT -le INT | True if the first integer is less than or equal to the second. |
| INT -ge INT | True if the first integer is greater than or equal to the second. |


## Examples
```
$ cat compare.sh
#!/bin/bash

a="100"
b="20"

# This compares lexicographically
if [ "$a" \< "$b" ]; then
  echo "This will print."
fi

# This compares numerically
if [ "$a" -gt "$b" ]; then
  echo "This will also print."
fi

c="foo"
d="foo"
e="Foo"

# String comparison
if [ "$c" = "$d" ]; then
  echo "The strings are equal."
fi

# Small letters sort after capital letters
if [ "$c" \> "$e" ]; then
  echo "$c sorts after $e."
fi

# String comparison using integer operators won't work
if [ "$c" -eq "$d" ]; then
  echo "This raises an error."
fi

f="0.1"
g="0.10"

# Bash only compares integers
if [ "$f" -eq "$g" ]; then
  echo "These raises an error too."
fi
```


## The [[ keyword
- Similar to [ with some differences:
  - Has pattern matching
  - No need to escape operators with special characters
  - Not implemented by all shells

```
$ cat matching.sh
#!/bin/bash

a="foobar"
b="[a-z]*"

if [[ "$a" = $b ]]; then
  echo "$a matches pattern $b."
fi

if [[ "$a" != "$b" ]]; then
  echo "$a is not equal to the string $b."
fi

if [[ "$a" > "$b" ]]; then
  echo "$a sorts later than $b."
  echo "No need to escape the > operator."
fi
```


## [[ vs [
- When making a Bash script, always use `[[` rather than `[`.
- When making a shell script which may end up being used in an environment where Bash is not available, use `[` because it is more portable.



## Looping
```
# Repeat as long as COMMAND returns 0
while COMMAND; do
  COMMANDS
done

# Repeat as long as COMMAND returns nonzero
until COMMAND; do
  COMMANDS
done

# Repeat the loop for each WORD, setting VAR to each WORD in turn
for VAR in WORDS; do
  COMMANDS
done

# Evaluate the first arithmetic expression.
# Repeat the loop so long as the second arithmetic expression is successful.
# At the end of each loop evaluate the third arithmetic expression.
for (( EXPR; EXPR; EXPR; )); do
  COMMANDS
done
```


## Examples
```
$ cat loops.sh
#!/bin/bash

a=10
while (( a > 0 )); do
  echo "$a"
  (( a-- ))
done

echo "---"
a=10
until (( a < 1 )); do
  echo "$a"
  (( a-- ))
done

echo "---"
for v in $(seq 10 -1 1); do
  echo "$v"
done

echo "---"
for (( a=10; a > 0; a-- )); do
  echo "$a"
done
```


## Looping on files
```
$ cat file_looping.sh
#!/bin/bash

# This won't work
for f in $(ls *.txt); do
  cat "$f"
done

# This won't work either
for f in "$(ls *.txt)"; do
  cat "$f"
done

# This works
for f in *.txt; do
  cat "$f"
done
```



## Resources
- http://mywiki.wooledge.org/ - teaches Bash features with proper usage
- http://www.tldp.org/LDP/Bash-Beginners-Guide/html/index.html - Bash guide for beginners
- http://www.tldp.org/LDP/abs/html/index.html - Advanced Bash scripting
- man pages
