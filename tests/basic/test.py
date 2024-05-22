import subprocess
import sys, os
from typing import Any

UP_DIR=os.path.abspath(os.path.join(
		os.path.dirname(__file__),
		"..",".."
	)
)
sys.path.append(UP_DIR)

from plsp import Logger, save_logger
from plsp.formatters.bundled import Time_Segment_Generator
from plsp.formatters.I_Final_Formatter import I_Final_Formatter
from plsp.__Color_Configuration import Color_Configuration, A_Foreground_Color, A_Background_Color
from plsp.formatters.Logging_Segment_Generator import Logging_Segment



# TODO: Experiment with `Enum` instead of `str` for the debug modes and contexts.
from plsp.Experimental_Logger import Experimental_Logger
from enum import Enum
class Debug_Mode (Enum):
	INFO = ()
	DETAIL = ()
	DEBUG = ()
	ERROR = ()
class Debug_Context (Enum):
	GENERIC = ()
	RENDERING = ()
	PHYSICS = ()
logger = Experimental_Logger(modes_t=Debug_Mode, contexts_t=Debug_Context)
#logger.show(Debug_Mode.DETAIL)
# NOTE: ONLY ONE LOGGER SHOULD EVER BE CREATED PER PROGRAM.
logger = Logger()



# The below sets the global context to generic.
# > The global context means that if we do `logger().our_debug_mode(...)`, we will use the global context.
# On the other hand, if we do `logger().our_context.our_debug_mode(...)`, we will use the specified context.
logger.set("global_context", "generic")




# Below is adding a debug contexts.
# > Debug contexts are used to separate logging from different parts of the program.
logger.add_debug_context("generic")
logger.add_debug_context("rendering")
logger.add_debug_context("physics")



# MORE ON THE BELOW FUNC LATER...
@logger.define_callback(id="error", multi_threaded=False)
def on_error(callback_data:dict[str,Any]):
	print("ENCOUNTERED AN ERROR:")
	print(callback_data["colored_text"])
	print("\n\nEXITING!!!")
	exit(1)
	


# Below is adding a debug modes.
# > Each subsequent call to `logger.add_debug_mode` will add a new debug mode that builds on-top of the previous.
# For example, the below will add the following debug modes:
# - info   -- lowest level of logging.
# - detail -- higher level of logging - If the active debug mode is set to detail, it will log both info and detail.
# - debug  -- higher still - If the active debug mode is set to debug, it will log all three.
logger.add_debug_mode("info")
logger.add_debug_mode("detail")
logger.add_debug_mode("debug")
# Error is separate from the above.
# Meaning that all `logger().error(...)` calls will be logged no matter the active debug mode.
# We can attach a callback to the debug mode to handle the error.
logger.add_debug_mode("error", separate=True, callback="error")



# START OF MODIFYING DEBUG CONTEXTS #



# Modification of debug context must be done separately to creation.
# Access the debug context by using the `Logger.debug_contexts` dictionary.

#logger.debug_contexts["generic"].set_enabled()  # Not required since it is enabled by default. 
logger.contexts["generic"].add_sink(
	sys.stdout,
	do_encode=False,    # If true, will encode the output (capable of handling ANSI escape codes).
	do_flush=True,      # If true, will flush the output after writing.
	do_serialize=False  # If true, will output a json string.
)
logger.contexts["rendering"].add_sink(sys.stdout)
logger.contexts["physics"].add_sink(sys.stdout)



# The below will add the time before each log message.
# TODO: The below is a bit messy and hard to read. Make it simpler and easier to follow.
# TODO:   E.g., instead of setting color for each, we can do something like `my_time_sg.set_all_color_config(my_first_cc)`.
my_time_sg = Time_Segment_Generator()
my_first_cc = Color_Configuration(
	A_Foreground_Color.BASIC_RED,
	A_Background_Color.BASIC_BRIGHT_BLACK
)
my_time_sg.day.color_config = my_first_cc
my_time_sg.month.color_config = my_first_cc
my_time_sg.year.color_config = my_first_cc
my_time_sg.hour.color_config = my_first_cc
my_time_sg.minute.color_config = my_first_cc
my_time_sg.second.color_config = my_first_cc
my_time_sg.microsecond.color_config = my_first_cc
my_time_sg.separator.color_config = Color_Configuration(
	A_Foreground_Color.BASIC_BLACK,
	A_Background_Color.BASIC_BRIGHT_BLACK
)
my_time_sg.date_separator.color_config = my_first_cc
my_time_sg.time_separator.color_config = my_first_cc
my_time_sg.second_microsecond_separator.color_config = my_first_cc



# Use `add_LSG` to add a LSG (Logging Segment Generator).
logger.contexts["generic"].add_LSG(my_time_sg)
logger.contexts["rendering"].add_LSG(my_time_sg)
logger.contexts["physics"].add_LSG(my_time_sg)



# The final formatter will reorder and return the resulting reordered list of segments.
# We are also given a `non_segments_string` which is the string that was not part of any segment.
# > For example, if we call `logger().info("Hello, World!")`, the `non_segments_string` will be "Hello, World!".
class my_final_formatter (I_Final_Formatter):
	def impl_handle(self, results: list[Logging_Segment], non_segments_string:"str") -> list[Logging_Segment]:
		return results+[
			Logging_Segment("NON_SEGMENT_1", f"\033[107m \033[0m "),
			Logging_Segment("NON_SEGMENT_2", non_segments_string)
		]



# Use `set_final_formatter` to set the final formatter.
logger.contexts["generic"].set_final_formatter(my_final_formatter())
logger.contexts["rendering"].set_final_formatter(my_final_formatter())
logger.contexts["physics"].set_final_formatter(my_final_formatter())



# END OF MODIFYING DEBUG CONTEXTS #



#
# Now we can use the debug contexts to log messages.
#

# To change the active debug mode, use the `show` method.
logger.show("info")
save_logger(logger, "_test_logger_")



# SEE: `_inner_test.py` for the actual test.
# We separate in order to test the `save_logger` and `load_logger` functions.
subprocess.run(f"{sys.executable} test_inner.py", shell=True, cwd=f"tests{os.path.sep}basic")
