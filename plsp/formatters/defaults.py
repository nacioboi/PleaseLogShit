from ._Formatter_ import IFormatter
from ._FinalFormatter_ import IFinalFormatter







class DefaultFinalFormatter(IFinalFormatter):



	def raw_handle(self, string:str) -> str:
		return self._strip_postfixes(string)
	





