Constructs a GraphViz graph of your local social network, that is, a graph of
all your friends with edges between mutual friends.

Get an OAuth access token, for instance via
https://developers.facebook.com/tools/explorer, and pass it as the first
argument to the Python 3 script friendnetwork.py. As the second argument, pass
the field you would like to label nodes by: id, name or first_name are good
choices.

Redirect the output from the script to a file, for instance graph.dot, and plot
it using the fdp tool of GraphViz:

```sh
python3 friendnetwork.py ACCESS_TOKEN first_name > graph.dot
fdp -Tpng -ograph.png graph.dot
```
