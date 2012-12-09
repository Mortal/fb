Constructs a GraphViz graph of your local social network, that is, a graph of
all your friends with edges between mutual friends.

Get an OAuth access token, for instance via
https://developers.facebook.com/tools/explorer, and pass it as the first
argument to the Python 3 script friendnetwork.py.

Redirect the output from the script to a file, for instance graph.dot, and plot
it using the fdp tool of GraphViz:

```sh
fdp -Tpng -ograph.png graph.dot
```
