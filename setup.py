from setuptools import setup, find_packages

def readme():
    data = ''
    try:
        f = open('README.md', 'r'):
        data = f.read()
        return data
    except:
        return 'No readme provided.'
    finally:
        f.close()
setup(
    name="AdaptiveControl",
    author="Christopher De Jesus",
    author_email="cd525@cornell.edu",
    description="A framework for allowing serial control of the host device..",
    long_description=readme(),
    long_description_content_type="text/markdown",
    version="0.2",
    packages=find_packages(),
)
