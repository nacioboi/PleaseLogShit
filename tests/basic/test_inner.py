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



