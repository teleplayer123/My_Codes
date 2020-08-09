# My_Codes

Description
----
This repository has a variety of programs I have written for learning purposes as well
as practical use. 

Contents
----
- [Backdoor Example](#Bdoor)
- [Misc Programs](#Misc)
- [Project Euler](#Project Euler)


[Bdoor](bdoor/)
----
This is a simple python implementation of a "backdoor", which is a program that an attacker
uses to gain entry to a victims server where access would not usually be permitted. In order to be effective, 
an attacker would likely hide a backdoor in a program that a victim may install to their computer.

[bdoor.py](bdoor/bdoor.py)

This is the client code. It connects to the server, which would be listening for the client's connection on the 
victims computer. On successful connction, the client creates a pipe that allows communiction with a victims command
shell. This allows the attacker to access private information about the victims operating system, files, directories, etc.
Pythons os.Popen function is used to create the pipe, but has some limitations on what commands can be executed; so some
of these commands had to be hard coded.

[bd_server.py](bdoor/bd_server.py)

Here is the code for the backdoor server. When launched, starts listening for the client's connection. The server handles
the command requests sent by the client and returns the result. For commands that are accepted by os.Popen, the pipe returns a 
shell that can be queried with commands. As this method does not accept all commands, some popular commands are hard coded
to be processed and returned to the client by the server side. 

[bd_secure.py](bdoor/bd_secure.py)

This is the same backdoor client as the one listed above, with the added use of ssl certificate verification. For the backdoors
purposes, this does not really make sense to use. I made this more for practice and as an example on how to use ssl in a client
to server connection. The respective server program is [secure_server.py](bdoor/secure_server.py).

[bd_routes.py](bdoor/bd_routes.py) & [upload_routes.py](bdoor/upload_routes.py)

I wrote these programs to facilitate a situation where a compiled version of [runbd.py](bdoor/runbd.py) could be uploaded
to a server and then downloaded on another system, in an attempt to mimic a scenario where a victim machine downloads the 
backdoor and the attacker exploits it. I used a virtual machine on virtualbox as the victim computer, that could connect to
"localhost", and then download the uploaded file/files. In order for this to work, the compiled backdoor program must be used 
on the same operating system it was compiled on. 

[Misc](misc/)
----
This folder contains various little programms I have written over the years. Listed here are some of the more useful ones:

-[a2h.py](misc/a2h.py) is a cli program that takes an ascii string and converts it to hexadecimal. A usage message
is shown when the program is run with no arguments. This program can be useful in exploits, when dealing with memory
address's of binaries.
 
-[checksum.py](misc/checksum.py) is a program I use often to verify provided checksums of download files. I adapted
this program to be a cli for linux using a bash shellscript. The three main arguments...filename, compare_hash(hash value provided by
the creator of the program to download), and hash_alg(i.e. sha256)...are passed to the program and run, checking that the contents
of the files to be downloaded have not been altered.

-[hexd.py](misc/hexd.py) is a hexdump program that takes a file and writes its contents in hexadecimal and ascii to
an outfile passed as an argument. If no outfile name is provided, a new dumpfile is created based on the current time.

-[randpass.py](misc/randpass.py) is one of my favorite programs I have written. It simply generates a random password
based on a string passed by the user. Other arguments can be supplied to control length and randomness of the returned
passsword. The returned passwords are not meant to be easily remembered, so I would recommend writing them down, or taking
the time to memorize them. I also adapted this program to a cli using a bash shellscipt.

[Project Euler](project_euler/)
----

