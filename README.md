# CS350_Visualization
Some utilities for visualizing the running of CS350 assignments

## A1 Traffic problem
To visualize how your traffic protocol works, you can add DEBUG (so you can turn them off and on) or kprintf statements to the traffic\_synch.c file. Note that this will slow down the simulation so remember to turn the prints off when you are benchmarking. Since kprintf is atomic the prints won't be all over the place.

### Instructions
In this case, D denotes one of the directions in ['N', 'E', 'S', 'W'].

Put this somewhere in `intersection_sync_init`
>\>\>\>INITIALIZING\_SIMULATION

Put this before all the locks (before you enter the intersection) in `intersection_before_entry`
>\>\>\>WAIT\_FOR\_INTERSECTION: D D

Put this before after the locks (before you enter the intersection) in `intersection_before_entry`
>\>\>\>GOING\_INTO\_INTERSECTION: D D

Put this before you unblock a car in `intersection_after_exit` when you are leaving the intersection (or else after you unblock a car it might print before you do)
>\>\>\>LEAVING\_INTERSECTION: D D

Put this somewhere in `intersection_sync_cleanup`
>\>\>\>FINISHING\_SIMULATION

Run it like `python visualize_traffic.py example_simulation_log.txt 0.5 100`

The two command line argument are:
>1. The log file of the printout from running the traffic simulation (with the above printouts added) 
>2. The gap wait time between processing events
>3. An optional fast\_forward breakpoint which will start the animation at that line onwards.
