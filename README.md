# 4chan-json-to-graphml
A tool to convert the JSON representation of a 4chan thread into a GraphML file (for use in R/igraph, etc.).

# How to use
Either specify a link to 4chan JSON or a file. Running `python3 4chan_json_to_graphml.py -h` will demonstrate correct usage.

# Where can I get 4chan JSON from?
This tool will work with JSON from the official 4chan website, as well as some archives (desuarchive.org and 4plebs.org are tested and working correctly). For 4chan, just add `.json` to the regular thread URL. For 4plebs, use `https://archive.4plebs.org/BOARD/thread/NUM.json`, replacing `BOARD` with the board abbreviation of the thread you're after, and `NUM` with the thread number. For desuarchive, use `https://desuarchive.org/_/api/chan/thread?board=BOARD&num=NUM`, where `BOARD` is the board abbreviation of the thread you're after, and `NUM` is the thread number.
