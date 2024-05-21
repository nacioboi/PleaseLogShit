import subprocess
import sys, os

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



# NOTE: ONLY ONE LOGGER SHOULD EVER BE CREATED PER PROGRAM.
logger = Logger()



# Use below to separate log files based on debug mode instead of debug context.
# NOTE: NOT YET SUPPORTED...
# TODO: IMPLEMENT.
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

# Modification of debug context must be done separately to creation.
# Access the debug context by using the `Logger.debug_contexts` dictionary.

logger.debug_contexts["generic"].set_is_active(True)
logger.debug_contexts["generic"].add_direction(
	do_encode=False,
	file_handle=sys.stdout.fileno(),
	file_path=None
)
logger.debug_contexts["rendering"].set_is_active(True)
logger.debug_contexts["rendering"].add_direction(
	do_encode=False,
	file_handle=sys.stdout.fileno(),
	file_path=None
)
logger.debug_contexts["physics"].set_is_active(True)
logger.debug_contexts["physics"].add_direction(
	do_encode=False,
	file_handle=sys.stdout.fileno(),
	file_path=None
)
					       
# The below will add the time before each log message.
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

logger.debug_contexts["generic"].add_logging_segment(my_time_sg)
logger.debug_contexts["rendering"].add_logging_segment(my_time_sg)
logger.debug_contexts["physics"].add_logging_segment(my_time_sg)

class my_final_formatter (I_Final_Formatter):
	def impl_handle(self, results: list[Logging_Segment], non_segments_string:"str") -> list[Logging_Segment]:
		return results+[
			Logging_Segment("NON_SEGMENT_1", f"\033[107m \033[0m "),
			Logging_Segment("NON_SEGMENT_2", non_segments_string)
		]

logger.debug_contexts["generic"].set_final_formatter(my_final_formatter())
logger.debug_contexts["rendering"].set_final_formatter(my_final_formatter())
logger.debug_contexts["physics"].set_final_formatter(my_final_formatter())

# END OF MODIFYING DEBUG CONTEXTS #



#
# Now we can use the debug contexts to log messages.
#

logger.set_active_debug_mode("info")
save_logger(logger, "_test_logger_")



# SEE: `_inner_test.py` for the actual test.
# We separate in order to test the `save_logger` and `load_logger` functions.
subprocess.run(f"{sys.executable} test_inner.py", shell=True, cwd=f"tests{os.path.sep}basic")
