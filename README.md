# devious-spyware
some rather devious multifunctioning spyware

protocols:
constant transmit and receive between server and client at regular intervals (1s maybee? idk can be throttled to help performance)
in this case server is the machine with the spy program
they have a buffer that can be filled and is then sent on the next cycle
each machine can then process and continue to fill the buffer and then continue the cycle
for complex things like images, a new socket can be negociated to transmit and receive this in parralel to the original
