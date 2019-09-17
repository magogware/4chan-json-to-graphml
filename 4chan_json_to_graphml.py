# Need JSON, RegEx, Sys, and URL libraries
import json, re, sys, urlllib.request

# If a URL has been given on the CLI, proceed
if len(sys.argv) > 1:

    # Parse the url from the command line
    url = str(sys.argv[1])
    
    # Get the thread number to use as a file name
    filename = (re.findall("\\d+.json", url))[0].replace("json", "graphml")
    
    # Open 4chan JSON URL
    with urllib.request.urlopen(url) as response:

        # Store JSON data
        data = json.loads(response.read().decode())

        # Open graphml file for writing
        with open(filename, "w+") as graph_file:
    
            # Create a dictionary to store the
            # node id corresponding to a post number
            d = {'a':1}
            
            # Create a regular expression to catch
            # replies in a post's text
            exp = "(\\#p\\d+)"

            # Create a counter to keep track of
            # the current node id
            i = 0
            
            # Print out XML preamble
            graph_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\">")
            graph_file.write("<key id=\"g_type\" for=\"graph\" attr.name=\"type\" attr.type=\"string\"/><key id=\"v_name\" for=\"node\" attr.name=\"name\" attr.type=\"string\"/>")
            graph_file.write("<graph id=\"G\" edgedefault=\"directed\"><data key=\"g_type\">www-hyperlink</data>")

            # Loop through all posts in a thread
            for post in data['posts']:

                # Create the node id string
                node_id = "n"+str(i)
                d[str(post['no'])] = node_id

                # Print the node XML, using the
                # post number as the name
                graph_file.write("<node id=\""+node_id+"\">")
                graph_file.write("<data key=\"v_name\">"+str(post['no'])+"</data>")
                graph_file.write("</node>")

                # If the post has text, parse it for
                # replies
                if "com" in post.keys():

                    # Use the regex to catch replies
                    text = post['com']
                    replies_to = re.findall(exp, text)

                    # Loop through all replies gathered
                    for reply in replies_to:

                        # Clean extra characters off reply
                        reply = reply.replace("#p", "")

                        # If we have information on the reply...
                        if reply in d.keys():

                            # Find the node id corresponding to the
                            # post number being replied to
                            replied_to = d[reply]

                            # Construct the edge XML and print it
                            edge_xml  = "<edge source=\""+node_id+"\" target=\""+replied_to+"\">"
                            graph_file.write(edge_xml)
                            graph_file.write("</edge>")

                # Increment the node ID counter
                i = i + 1

            # Close off the GraphML
            graph_file.write("</graph></graphml>")
