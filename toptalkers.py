import os, sys, re, operator, collections, time

# Define a function for printing
def echo(t):
    sys.stdout.write(t)
    sys.stdout.flush()

# Regex for finding IP on line
def ipgrep(line):
    out = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
    return out

unique_ip = {}

# Open file or stdin
try:
    with open(sys.argv[1], "r") as log:
        log = log.readlines()

except IndexError:
    with sys.stdin as log:
        log = log.readlines()

# Iterate over lines and collect unique IPs and their counts
i = 0
for line in log:
    i += 1
    ip = ipgrep(line)
    try:
        s = unique_ip[ip[0]] + 1
    except KeyError:
        s = 1
    unique_ip.update({ip[0]: s})

# Sort the entries with largest first.
top_talkers = sorted(unique_ip.items(), key=operator.itemgetter(1), reverse = True)

# Find the top talker and length of value
magnitude = len(str(top_talkers[0][1]))

# Set minimum value for header formatting.
if magnitude < 3:
    magnitude = 3

# Count all lines
total = 0
for entry in top_talkers:
    total = total + entry[1]

# Print header
echo("\n%s%s\n" % ("IP address".rjust(15), "hits".rjust(magnitude + 2)))

# Print top talkers if share of traffic is over 1% of total
for line in top_talkers:
    if int(line[1]) > (total / 100):
        i = 0
        echo("%s%s " % (line[0].rjust(15), str(line[1]).rjust(magnitude + 2)))
        # Draw comparison graphics
        while i < (line[1] / (top_talkers[0][1] / 50)):
            i += 1
            echo(":")
        echo("\r\n")
echo("%s%s\n" % ("All".rjust(15), str(total).rjust(magnitude + 2)))

exit()
