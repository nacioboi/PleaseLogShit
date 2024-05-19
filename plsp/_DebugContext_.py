from .formatters._Formatter_ import IFormatter
from .formatters._FinalFormatter_ import IFinalFormatter
from .formatters.defaults import DefaultFinalFormatter
from ._DebugMode_ import DebugMode
from ._Direction_ import IODirection

from io import IOBase, TextIOWrapper
import sys







def _debug_print(self, prefix:str, *args, **kwargs):

	"""
	DO NOT CALL THIS DIRECTLY.

	At the end of the day, this is our special function that actually prints to the screen (or file).

	Args:
		prefix (str): 	The prefix to the log message.
		*args: 		The log message, works like the `print` function.
		**kwargs: 	The keyword arguments to pass to the print function.
				  Currently, only the `end` keyword argument is supported.

	Raises:
	    Exception: If an unknown keyword argument is passed.
	"""

	str = f"{prefix}"
	for arg in args:
		str += f"{arg} "
	str += "\033[0m"

	for kwarg in kwargs:
		if kwarg == "end":
			continue
		else:
			raise Exception(f"Unknown keyword argument {kwarg}.")

	if "end" in kwargs:
		str += kwargs["end"]

	self._add_contents_to_log(str)







class DebugContext:



	__slots__ = (
		"name",
		"format_layers",
		"final_formatter",
		"is_active",
		"directions",
		"__write_to_handle",
		"__write_to_file"
	)



	def __init__(self, name:str) -> None:
		self.name = name

		self.format_layers:"list[IFormatter]" = []
		self.final_formatter:"IFinalFormatter" = DefaultFinalFormatter()

		self.is_active:"bool|None" = None
		self.directions:"list[IODirection]|None" = None



	def set_final_formatter(self, formatter:"IFinalFormatter") -> None:
		self.final_formatter = formatter



	def set_is_active(self, new_is_active:bool) -> None:
		self.is_active = new_is_active



	def add_direction(self, direction:IODirection) -> None:
		if self.directions is None:
			self.directions = []
		self.directions.append(direction)



	def add_format_layer(self, formatter):
		self.format_layers.append(formatter)




	def __evaluate_instruction(self, instruction_part, arg_part):
		if instruction_part == "can_ever_write":
			self.is_active = eval(arg_part)
		
		elif instruction_part == "write_to_handle":
			self.__write_to_handle = eval(arg_part)

		elif instruction_part == "write_to_file":
			self.__write_to_file = eval(arg_part)



	def __inner__add_contents_to_log(self, contents:str, direction: IODirection) -> None:
		try:

			f = None

			direction.validate()

			if direction.file_handle is not None:
				if direction.file_handle == 1:
					f = sys.stdout
				elif direction.file_handle == 2:
					f = sys.stderr
				else:
					f = open(direction.file_handle, "a")
			elif direction.file_path is not None:
				f = open(direction.file_path, "a")
			else:
				raise Exception("No file handle or file path to write to.")

			if not isinstance(f, IOBase):
				raise Exception("No file handle to write to.")
			
			f.write(contents)
			f.write("\n")

		finally:
			if f and (not direction.file_handle in [1,2]) and not f.closed:
				f.close()



	def __add_contents_to_log(self, contents:str) -> None:
		assert self.directions is not None, "No directions to write to."
		for direction in self.directions:
			self.__inner__add_contents_to_log(contents, direction)



	def __handle(self, debug_mode:"DebugMode", active_debug_level:"DebugMode", *args, **kwargs):
		# QUICK NOTE: the `debug_mode` parameter should be used to change the output and the
		# `active_debug_mode` parameter should be used to determine if we should write to the output.

		# First check that this context is valid.
		if self.is_active is None and self.__write_to_handle is None:
			raise Exception("`can_ever_write` and `write_to_handle` cannot both be None.")

		str = ""
		
		is_first = True
		for format_layer in self.format_layers:
			str = IFormatter.__handle(format_layer, str, is_first)
			is_first = False
		
		str = self.final_formatter.raw_handle(str)
		
		override_instructions = debug_mode.override_instructions or []

		for instruction in override_instructions:
			instruction_part, arg_part = instruction.split("=")
			self.__evaluate_instruction(instruction_part, arg_part)

		# All conditions where we cannot write.
		if active_debug_level.level == -1 and debug_mode.level == -1:
			if not active_debug_level.name == debug_mode.name:
				return
		elif active_debug_level.level < debug_mode.level:
			return
		elif self.is_active is None or (self.is_active is not None and not self.is_active):
			return

		if active_debug_level.level >= debug_mode.level:
			_debug_print(self, str, *args, **kwargs)
			return

		raise Exception("This should never happen.")







__all__ = ["DebugContext"]