from setuptools import setup, find_packages

setup(
    name="corahbot",
    version="1.0.0",
    description="An improved bot for Corah IDLE RPG",
    author="CorahBot Developer",
    packages=find_packages(),
    install_requires=[
        "airtest",
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-logging-handler",
    ],
    entry_points={
        "console_scripts": [
            "corahbot=corahbot.main:main",
            "corahbot-api=corahbot.api:start_api",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Games/Entertainment",
    ],
)
