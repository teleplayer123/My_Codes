# My_Codes

Description
----
This repository has a variety of programs I have written for learning purposes as well
as practical use. 

Contents
----
- [Backdoor Example](#backdoor)
- [Misc Programs](#misc)
- [Project Euler](#euler)


[Backdoor Example](bdoor/)
----
This is a simple python implementation of a "backdoor", which is a program that an attacker
uses to gain entry to a victims server where access would not usually be permitted. In order to be effective, 
an attacker would likely hide a backdoor in a program that a victim may install to their computer.

[bdoor.py](bdoor/bdoor.py)
----
This is the client code. It connects to the server, which would be listening for the client's connection on the 
victims computer. On successful connction, the client creates a pipe that allows communiction with a victims command
shell. This allows the attacker to access private information about the victims operating system, files, directories, etc.
Pythons os.Popen function is used to create the pipe, but has some limitations on what commands can be executed; so some
of these commands had to be hard coded.

[bd_server.py](bdoor/bd_server.py)
----
Here is the code for the backdoor server. When launched, starts listening for the client's connection. The server handles
the command requests sent by the client and returns the result. For commands that are accepted by os.Popen, the pipe returns a 
shell that can be queried with commands. As this method does not accept all commands, some popular commands are hard coded
to be processed and returned to the client by the server side. 

[bd_secure.py](bdoor/bd_secure.py)
----
This is the same backdoor client as the one listed above, with the added use of ssl certificate verification. For the backdoors
purposes, this does not really make sense to use. I made this more for practice and as an example on how to use ssl in a client
to server connection. The respective server program is [secure_server.py](bdoor/secure_server.py).

[bd_routes.py](bdoor/bd_routes.py) & [upload_routes.py](bdoor/upload_routes.py)
----
I wrote these programs to facilitate a situation where a compiled version of [runbd.py](bdoor/runbd.py) could be uploaded
to a server and then downloaded on another system, in an attempt to mimic a scenario where a victim machine downloads the 
backdoor and the attacker exploits it. I used a virtual machine on virtualbox as the victim computer, that could connect to
"localhost", and then download the uploaded file/files. In order for this to work, the compiled backdoor program must be used 
on the same operating system it was compiled on. 
