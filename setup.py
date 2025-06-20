from setuptools import setup

APP = ["pdf_to_png.py"]
OPTIONS = {
    "argv_emulation": True,
    "includes": [
        "tkinter",
    ],
    "excludes": [
        "zmq",
    ],
}

setup(
    app=APP,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
