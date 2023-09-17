## A small app to familiarize with the `HTTP` protocol.

Just copied code presented [in the video](https://www.youtube.com/watch?v=4haMUvUxUJI) to check how it works (it works good).

Also, a small note about `TCP/IP`.
* `IP` protocol (*network* layer = layer 3 in the OSI model): 
is used to send / receive *packets*. The *IP address* is the abstraction of this level.
* `TCP` protocol (*transport* layer = layer 4 in the OSI model): 
is used to manage order and integrity of the packets: it can request damaged packets / remove duplicates and do other smart things to prevent a data loss. 
Such abstraction as *port* is used to allow multiple `TCP` connections to the same IP address.

We can think of pair `<IP-address: port>` as houses and flats in these houses. Such pairs often called *sockets*.
And, roughly speaking, we can classify sockets into two big categories: client and server sockets.
