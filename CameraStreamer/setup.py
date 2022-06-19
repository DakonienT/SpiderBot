from setuptools import setup, find_packages

setup(
   name='CameraStreamer',
   version='1.0',
   description='this package will provide an executable to stream live flux from a webcam to a web browser, and process YOLO detection on it.',
   author='Simon Faucher',
   author_email='simonfaucher99@gmail.com',
   packages=find_packages(),
   classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.0",
        "Topic :: Communications",
    ],
   install_requires=['wheel', 'bar', 'greek', 'flask', 'opencv-python', 'logging', 'psutil'], #external packages acting as dependencies
)