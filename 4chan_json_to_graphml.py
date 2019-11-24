import argparse, json, re, urllib.request, sys

####################
## Argument setup
####################

# Set up argument parser
parser = argparse.ArgumentParser(description="Parse the JSON "\
                                             "representation of a "\
                                             "4chan thread into GraphML")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-l", "--link",
                    help="Specify a link to 4chan JSON to parse",
                    type=str,
                    default='')
group.add_argument("-f", "--file",
                    help="Specify a file storing 4chan JSON to parse",
                    type=str,
                    default='')
parser.add_argument("-d", "--desu",
                    dest="desu",
                    action="store_true",
                    help="Indicate that the JSON is from desuarchive")
parser.add_argument("output",
                    help="Name for output (GraphML) file",
                    type=str)

# Parse arguments
args = parser.parse_args()

###############
## Parser
###############


def json_to_graphml(data, filename, desu):

    # Open graphml file for writing
    with open(filename, "w+") as graph_file:

        # Create a dictionary to store the
        # node id corresponding to a post number
        d = {'a':1}
        
        # Create appropriate regex to catch
        # replies and comments (depending on JSON source)
        if desu:
            quote = re.compile("(&gt;&gt;\\d+)")
            comment = "comment"
            num = "num"

            # If using desuarchive, strip the thread
            # number heading from the JSON
            threadnum = list(data.keys())[0]
            data = data[threadnum]

        else:
            quote = re.compile("(>>\\d+)")
            comment = "com"
            num = "no"

        # Create a counter to keep track of
        # the current node id
        i = 0
        
        # Print out XML preamble
        graph_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\">\n")
        graph_file.write("<key id=\"g_type\" for=\"graph\" attr.name=\"type\" attr.type=\"string\"/>\n")
        graph_file.write("<key id=\"v_name\" for=\"node\" attr.name=\"name\" attr.type=\"string\"/>\n")
        graph_file.write("<key id=\"v_comment\" for=\"node\" attr.name=\"comment\" attr.type=\"string\"/>\n")
        graph_file.write("<graph id=\"G\" edgedefault=\"directed\"><data key=\"g_type\">www-hyperlink</data>\n")

        # Compile some regex to catch expressions that will break XML
        span = re.compile("(<span .*>.*<\\s*\\/span>)")
        a = re.compile("(<a .*>.*<\\s*\\/a>)")
        br = re.compile("(<br\\s*\\/?>)")
        symb = re.compile("(&(\\w+;)?)|(<|>)")
        link = re.compile("(https?://[^\\s]+)")
        
        # If using desuarchive JSON, parse the
        # OP post (which is in a separate JSON field)
        if desu:

            # Store the OP as node 0
            post = data['op']
            
            # Create the node id string
            node_id = "n"+str(i)
            d[(post[num])] = node_id
            
            # Print the node XML, using the
            # post number as the name
            graph_file.write("<node id=\""+node_id+"\">\n")
            graph_file.write("\t<data key=\"v_name\">"+str(post['num'])+"</data>\n")
            sanitised_comment = symb.sub("", quote.sub("", link.sub("", a.sub("", span.sub("", br.sub(" ", post[comment])))))).replace("\n", " ")
            graph_file.write("\t<data key=\"v_comment\">"+sanitised_comment+"</data>\n")
            graph_file.write("</node>\n")
            
            # Increment the counter
            i = i + 1

        # Loop through all posts in a thread
        data = data['posts']
        if desu:
            keys = list(data.keys())
        else:
            keys = data
        for key in keys:
            if desu:
                post = data[key]
            else:
                post = key

            # Create the node id string
            node_id = "n"+str(i)
            d[str(post[num])] = node_id

            # Print the node XML, using the
            # post number as the name
            graph_file.write("<node id=\""+node_id+"\">\n")
            graph_file.write("\t<data key=\"v_name\">"+str(post[num])+"</data>\n")
            if comment in post.keys():
                sanitised_comment = symb.sub("", quote.sub("", link.sub("", a.sub("", span.sub("", br.sub(" ", post[comment])))))).replace("\n", " ")
            else:
                sanitised_comment = ""
            graph_file.write("\t<data key=\"v_comment\">"+sanitised_comment+"</data>\n")
            graph_file.write("</node>\n")

            # If the post has text, parse it for
            # replies
            if comment in post.keys():

                # Use the regex to catch replies
                text = post[comment]
                replies_to = quote.findall(text)

                # Loop through all replies gathered
                for reply in replies_to:

                    # Clean extra characters off reply
                    if desu:
                        reply = reply.replace(">>", "")
                    else:
                        reply = reply.replace("&gt;&gt;", "")

                    # If we have information on the reply...
                    if reply in d.keys():

                        # Find the node id corresponding to the
                        # post number being replied to
                        replied_to = d[reply]

                        # Construct the edge XML and print it
                        edge_xml  = "<edge source=\""+node_id+"\" target=\""+replied_to+"\">"
                        graph_file.write(edge_xml)
                        graph_file.write("</edge>\n")

            # Increment the node ID counter
            i = i + 1

        # Close off the GraphML
        graph_file.write("</graph>\n</graphml>")

#################
## Main function
#################

# If we have a link, download the JSON file
if args.link:

    # Open 4chan JSON URL
    with urllib.request.urlopen(args.link) as response:
        data = json.loads(response.read().decode())

        # Perform the correct parse for different
        # JSON layouts
        if args.desu:
            json_to_graphml(data, args.output, True)
        else:
            json_to_graphml(data, args.output, False)

# If we have a file, use that as our JSON source
elif args.file:

    # Open the JSON file
    with open(args.file, "r") as response:
        data = json.loads(response.read())

        # Perform the correct parse for different
        # JSON layouts
        if args.desu:
            json_to_graphml(data, args.output, True)
        else:
            json_to_graphml(data, args.output, False)
