import plsp
import sys







# NOTE: ONLY ONE LOGGER SHOULD EVER BE CREATED PER PROGRAM.
logger = plsp.Logger()




# use below to separate log files based on debug mode instead of debug context.
#plsp.set("io_based_on_mode", True)



# The below sets the global context to generic.
logger.set("global_context", "generic")



# Below is adding a debug context.
# It is a bit more complicated than setting up debug contexts so you dont have to set all the parameters at once.
logger.add_debug_context("generic")
logger.add_debug_context("rendering")
logger.add_debug_context("physics")



# Below is adding a debug mode.
logger.add_debug_mode("info")
logger.add_debug_mode("detail")
logger.add_debug_mode("debug")
logger.add_debug_mode("error", separate=True)



# START OF MODIFYING DEBUG CONTEXTS #

# You may modify the debug contexts after they are created.
# Access the debug context by using the `Logger.debug_contexts` dictionary.

logger.get_debug_context("generic").set_is_active(True)
logger.get_debug_context("generic").add_direction(IODirection(False, sys.stdout.fileno(), None))
logger.get_debug_context("rendering").set_is_active(True)
logger.get_debug_context("rendering").add_direction(IODirection(False, sys.stdout.fileno(), None))
logger.get_debug_context("physics").set_is_active(True)
logger.get_debug_context("physics").add_direction(IODirection(False, sys.stdout.fileno(), None))
					       
# The below will add the time before each log message.
logger.get_debug_context("generic").add_format_layer(TimeFormatter())
logger.get_debug_context("rendering").add_format_layer(TimeFormatter())
logger.get_debug_context("physics").add_format_layer(TimeFormatter())
#
## The below will add which ever function called the log message.
#plsp.get_debug_context("generic").add_format_layer(CallerFormatter)
#plsp.get_debug_context("rendering").add_format_layer(CallerFormatter)
#plsp.get_debug_context("physics").add_format_layer(CallerFormatter)
#

# END OF MODIFYING DEBUG CONTEXTS #



# Now we can use the debug contexts to log messages.
logger.set_debug_mode("info")



plsp.save_logger(logger, "test_logger")



# Run...
import subprocess, sys
subprocess.run(f"{sys.executable} _inner_test.py", shell=True, cwd=".")
