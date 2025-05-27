from setuptools import setup  # type: ignore

setup(
    name="Non Planar Desformator",
    version="0.1.0",
    description="User friendly interface for non planar slicing",
    author="EmmanuelMess",
    packages=["non_planar_desformation"],
    install_requires=["numpy", "pyvistaqt", "PySide6"],
)