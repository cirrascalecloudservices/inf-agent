import setuptools
setuptools.setup(name='inf-agent', scripts=['inf-agent.py'], data_files=[('etc/systemd/system', ['etc/systemd/system/cirrascale-inf-agent.service'])])
