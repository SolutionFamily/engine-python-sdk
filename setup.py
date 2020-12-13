from setuptools import setup, find_packages

setup(
    name='solutionfamily',
    packages=['solutionfamily'],
    include_package_data=True,
    install_requires=['lxml', 'requests', 'python-dateutil'],
    version='1.0.2',
    description='A Python SDK for interacting with SolutionFamily\'s Solution Engine.',
    long_description='A Python SDK for interacting with SolutionFamily\'s Solution Engine.',
    long_description_content_type='text/x-rst',
    url='https://github.com/SolutionFamily/engine-python-sdk',
    download_url='https://github.com/SolutionFamily/engine-python-sdk/dist/v1.0.0.tar.gz',
    keywords=['SolutionFamily', 'solutionengine' 'iot', 'sdk'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],    
    maintainer='Chris Tacke',
    maintainer_email='chris.tacke@solution-family.com'
)
