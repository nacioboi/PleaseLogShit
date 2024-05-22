import sys, os
UP_DIR=os.path.abspath(os.path.join(
		os.path.dirname(__file__),
		"..",".."
	)
)
sys.path.append(UP_DIR)

from plsp import load_logger

plsp = load_logger("_test_logger_")



plsp().info("This is using the generic context.")
plsp().info("It works since we set a global context.")



class renderer:
	def __init__(self):
		plsp().rendering.detail("The rendering engine in this engine is pretty simple!")



class physics:
	def __init__(self):
		plsp().physics.detail("The physics engine in this engine is pretty simple!")


my_renderer = renderer()

plsp.show("detail")

my_physics = physics()







from plsp import infoinject



infoinject.set_name_of_logger("plsp")



@infoinject.add_instruction("fib", line=1, debug_mode="info", debug_context="generic", args_for_logger=(
	f"n = {infoinject.Var_Ref('n')}",
))
@infoinject.add_instruction("fib", line=2, debug_mode="detail", debug_context="generic", args_for_logger=(
	f"n is", "less than or equal to 1"
),
	end="\n.\n"
)
@infoinject.add_instruction("fib", line=4, debug_mode="info", debug_context="generic", args_for_logger=(
	f"n is greater than 1",
	f"Now actually calculating... n-1 and n-2"
))
@infoinject.inject("fib", globals(), locals())
def fib(n):
	if n <= 1:
		return n
	else:
		return fib(n-1) + fib(n-2)



fib(2)
