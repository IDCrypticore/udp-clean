#!/usr/bin/env python

import signal
import sys
import time
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# Signal handler for stopping pipeline before destruction.
def signal_handler(sig, frame):
    p.set_state(Gst.State.NULL)
    sys.exit(0)

# Initialize gstreamer
GObject.threads_init()
Gst.init(None)

# Defining the pipeline 
gst_str = "udpsrc port=5000 ! application/x-rtp,encoding-name=H264 ! rtpjitterbuffer latency=1000 drop-on-latency=false ! rtph264depay ! h264parse ! nvv4l2decoder ! nvvidconv ! xvimagesink"

# Creating the pipeline
p = Gst.parse_launch (gst_str)

# Register signal handler for proper termination if receiving SIGINT, for instance Ctrl-C
signal.signal(signal.SIGINT, signal_handler)

# Start the pipeline
p.set_state(Gst.State.READY)
p.set_state(Gst.State.PAUSED)
p.set_state(Gst.State.PLAYING)

# Run for 1000s 
time.sleep(1000)

# Done. Stop the pipeline before clean up on exit.
p.set_state(Gst.State.NULL)
exit(0)
