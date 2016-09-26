"""
Reads the simulation events from the command line passed in file and reruns the
simulation with animations Basically, to use this you need to have the
following print statements in your traffic simulation output log (where D is
the direction in ['N', 'E', 'S', 'W']):

PUT THIS SOMEWHERE IN THE SIMULATION INITIALIZATION
>>>INITIALIZING_SIMULATION

PUT THIS BEFORE ALL THE LOCKS BEFORE YOU ENTER THE INTERSECTION
>>>WAIT_FOR_INTERSECTION: D D

PUT THIS AFTER ALL THE LOCKS BEFORE YOU ENTER THE INTERSECTION
>>>GOING_INTO_INTERSECTION: D D

PUT THIS BEFORE YOU UNBLOCK A CAR WHEN YOU ARE LEAVING THE INTERSECTION OR ELSE
THAT CAR WILL PRINT ENTERING FIRST BEFORE THIS PRINTS
>>>LEAVING_INTERSECTION: D D

NOTE: PUT THIS SOMEWHERE IN THE SIMULATION CLEANUP
>>>FINISHING_SIMULATION
"""

import pygame
import time
import re
import sys
from traffic_state import TrafficState

# Get the file events from the file passed in 
if len(sys.argv) < 2:
    print "No simulation log file passed in!"
    sys.exit()

# If a fast forward point in the events is passed in, then we only animate starting at that point (since we only want to see events after that)
if len(sys.argv) < 3:
    print "No time step between events passed in"
    sys.exit()
else:
    try:
        event_gap = float(sys.argv[2])
    except Exception as e:
        print "Error parsing time step (should be an float)"
        raise e

# If a fast forward point in the events is passed in, then we only animate starting at that point (since we only want to see events after that)
if len(sys.argv) == 4:
    print "Fast forwarding to set breakpoint event!"
    try:
        fast_forward = int(sys.argv[3])
    except Exception as e:
        print "Error parsing fast forward point (should be an integer)"
        raise e
else:
    fast_forward = 0

sim_file = file(sys.argv[1], "r")

# Process the lines into events
lines = sim_file.readlines()
ind_start = 0

# Read to the start of the simulation
while True:
    if re.match(r'>>>INITIALIZING_SIMULATION', lines[ind_start]):
        break
    ind_start += 1

# Read to the end of the simulation
ind_end = ind_start
while True:
    if re.match(r'>>>FINISHING_SIMULATION', lines[ind_end]):
        break
    ind_end += 1

lines = lines[(ind_start+1):ind_end]  # We don't want to include the starting line

# Process all of the prints into events
events = []
for line in lines:
    event = re.match(r'>>>(.*): (\w) (\w)', line).groups()
    assert len(event) == 3
    events.append(event)

"""
Simulate the traffic again
"""

# Since we are making everything symmetrical, the window is a square and all the animations are simply rotations of each other depending on which direction they are

# Create the traffic simulator
traffic = TrafficState()
animate = False

for i, event in enumerate(events):
    print "%d:" % i, event
    # Check if we have hit our fast_forward point
    if i == fast_forward:
        animate = True

    if event[0] == "WAIT_FOR_INTERSECTION":
        traffic.waiting(event[1], event[2], animate)
    elif event[0] == "GOING_INTO_INTERSECTION":
        traffic.in_intersection(event[1], event[2], animate)
    elif event[0] == "LEAVING_INTERSECTION":
        traffic.leaving_intersection(event[1], event[2], animate)
    else:
        raise Exception("Unknown event: %s" % event[0])

    if animate:
        pygame.display.flip()
        time.sleep(event_gap)
