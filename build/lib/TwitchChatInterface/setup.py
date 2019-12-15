import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TwitchChatInterface-pkg-edog0049a", # Replace with your own username
    version="0.0.1",
    author="Eli Reid",
    author_email="elir@elireid.com",
    description="a way to interface with twitch irc chat",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eli-reid/Twitch-Chat-Interface",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)


