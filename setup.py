import cx_Freeze
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
executables = [cx_Freeze.Executable("Python3_Game.py")]

cx_Freeze.setup(
    name="Save the World!",
    options ={"build_exe":{"packages":["pygame"],"include_files":["plane.png","background.png","Music\Platformer2.wav","Music\Button.wav"]}},
    description = "Save the World!",
    executables = executables
    )
