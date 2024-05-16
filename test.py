from plsp import Logger, load_logger, save_logger
from plsp import DebugContext, DebugMode, IODirection
from plsp.formatters.bundled import TimeFormatter

import sys



# NOTE: ONLY ONE LOGGER SHOULD EVER BE CREATED PER PROGRAM.
plsp = Logger()



# use below to separate log files based on debug mode instead of debug context.
#plsp.set("io_based_on_mode", True)



# The below sets the global context to generic.
plsp.set("global_context", "generic")



# Below is adding a debug context.
# It is a bit more complicated than setting up debug contexts so you dont have to set all the parameters at once.
plsp.add_debug_context("generic")
plsp.add_debug_context("rendering")
plsp.add_debug_context("physics")



# Below is adding a debug mode.
plsp.add_debug_mode("info")
plsp.add_debug_mode("detail")
plsp.add_debug_mode("debug")
plsp.add_debug_mode("error", separate=True)



# START OF MODIFYING DEBUG CONTEXTS #

# You may modify the debug contexts after they are created.
# Access the debug context by using the `Logger.debug_contexts` dictionary.

plsp.get_debug_context("generic").set_can_ever_write(True)
plsp.get_debug_context("generic").add_direction(IODirection(False, sys.stdout.fileno(), None))
plsp.get_debug_context("rendering").set_can_ever_write(True)
plsp.get_debug_context("rendering").add_direction(IODirection(False, sys.stdout.fileno(), None))
plsp.get_debug_context("physics").set_can_ever_write(True)
plsp.get_debug_context("physics").add_direction(IODirection(False, sys.stdout.fileno(), None))
					       
# The below will add the time before each log message.
plsp.get_debug_context("generic").add_format_layer(TimeFormatter())
plsp.get_debug_context("rendering").add_format_layer(TimeFormatter())
plsp.get_debug_context("physics").add_format_layer(TimeFormatter())
#
## The below will add which ever function called the log message.
#plsp.get_debug_context("generic").add_format_layer(CallerFormatter)
#plsp.get_debug_context("rendering").add_format_layer(CallerFormatter)
#plsp.get_debug_context("physics").add_format_layer(CallerFormatter)
#

# END OF MODIFYING DEBUG CONTEXTS #



# Now we can use the debug contexts to log messages.
plsp.set_debug_mode("info")



save_logger(plsp, "test_logger")



# Run...
import subprocess, sys
subprocess.run(f"{sys.executable} _inner_test.py", shell=True, cwd=".")
