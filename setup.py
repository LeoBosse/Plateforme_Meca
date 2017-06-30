from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(name = "Horde",
    version = "0.2",
    description = "plateforme",
    executables = [Executable("main.py")],
)
