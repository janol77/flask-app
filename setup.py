from setuptools import find_packages, setup

setup(name="mantenedor-optica",
      version = "0.1",
      description = "Mantenedor para Optica",
      author = "Alejandro Medina",
      platforms = ["any"],
      license = "GPLv3",
      packages = find_packages(),
      install_requires = ["Flask==0.11.1", "flask-mongoengine==0.8", "Flask-Login==0.4.0"],
      )