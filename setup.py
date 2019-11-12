import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ss-quick",
    version="0.0.2",
    author="ChaneyZorn",
    author_email="chaneyzorn@gmail.com",
    url="https://github.com/Campanula/ss-quick",
    license="MIT",
    description="A tool loading gui-config.json for ss-local",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet :: Proxy Servers',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ss-quick=ss_quick.main_cli:main',
        ],
    }
)
