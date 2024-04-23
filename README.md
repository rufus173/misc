# devious-spyware
some rather devious multifunctioning spyware
only funcitonal within my home network
has additional functionality if pil is installed

protocols:
uses port 8017
constant transmit and receive between server and client at regular intervals (1s maybee? idk can be throttled to help performance)
in this case server is the machine with the spy program
they have a buffer that can be filled and is then sent on the next cycle
each cyle can be repeated for each item in the buffer(processed one at a time)
each machine can then process and continue to fill the buffer and then continue the cycle
for complex things like images, a new socket can be negociated to transmit and receive this in parralel to the original
