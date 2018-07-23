from cx_Freeze import setup, Executable

# On appelle la fonction setup
import sys
from cx_Freeze import setup, Executable

executables = [
    Executable("Game.py"),
]

buildOptions = dict(
    compressed=True,
    includes=["sys", "re", "random"],
    path=sys.path + ["modules"]  # OU ["Lib"] essaie les deux
)

setup(
    name="controle",
    version="1.0",
    description="blablabla",
    options=dict(build_exe=buildOptions),
    executables=executables
)