from .formatters.Logging_Segment_Generator import I_Logging_Segment_Generator
from .formatters.I_Final_Formatter import I_Final_Formatter
from .__Debug_Mode import Debug_Mode
from .__IO_Direction import IO_Direction

from io import IOBase, TextIOWrapper
import sys







class Debug_Context:



	__slots__ = (
		"name",
		"segment_generators",
		"final_formatter",
		"is_active",
		"directions",
		"__write_to_handle",
		"__write_to_file"
	)



	def __init__(self, name:str) -> None:
		self.name = name

		self.segment_generators:"list[I_Logging_Segment_Generator]" = []
		self.final_formatter:"I_Final_Formatter|None" = None

		self.is_active:"bool|None" = None
		self.directions:"list[IO_Direction]|None" = None



	def set_final_formatter(self, formatter:"I_Final_Formatter") -> None:
		self.final_formatter = formatter



	def set_is_active(self, new_is_active:bool) -> None:
		self.is_active = new_is_active



	def add_direction(self, do_encode:"bool", file_handle:"int|None"=None, file_path:"str|None"=None) -> None:
		if self.directions is None:
			self.directions = []
		self.directions.append(
			IO_Direction(
				do_encode=do_encode,
				file_handle=file_handle,
				file_path=file_path
			)
		)



	def add_logging_segment(self, formatter):
		self.segment_generators.append(formatter)



	def __evaluate_instruction(self, instruction_part, arg_part):
		if instruction_part == "is_active":
			self.is_active = eval(arg_part)
		
		elif instruction_part == "write_to_handle":
			self.__write_to_handle = eval(arg_part)

		elif instruction_part == "write_to_file":
			self.__write_to_file = eval(arg_part)



	def __inner__add_contents_to_log(self, contents:str, direction: IO_Direction) -> None:
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
			f.flush()

		finally:
			if f and (not direction.file_handle in [1,2]) and not f.closed:
				f.close()



	def _add_contents_to_log(self, contents:str) -> None:
		assert self.directions is not None, "No directions to write to."
		for direction in self.directions:
			self.__inner__add_contents_to_log(contents, direction)



	def _handle(self, debug_mode:"Debug_Mode", active_debug_level:"Debug_Mode", *args, **kwargs):
		# QUICK NOTE: the `debug_mode` parameter should be used to change the output and the
		# `active_debug_mode` parameter should be used to determine if we should write to the output.

		s = ""
		for arg in args:
			s += f"{str(arg)} "

		ACCEPTED_KWARGS = ["end"]
		for kwarg in kwargs:
			if kwarg not in ACCEPTED_KWARGS:
				raise Exception(f"Unknown keyword argument {kwarg}.")

		if "end" in kwargs:
			s += kwargs["end"]
		else:
			s += "\n"
		
		formatted_s = ""
		for formatter in self.segment_generators:
			formatted_s += I_Logging_Segment_Generator._handle(formatter)
		
		s = I_Final_Formatter._handle(self.final_formatter, formatted_s, s)
		
		overridden_instructions = debug_mode.overridden_instructions or []

		for instruction in overridden_instructions:
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
			self._add_contents_to_log(s)
			return

		raise Exception("This should never happen.")







