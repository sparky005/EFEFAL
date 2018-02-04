from setuptools import setup

install_requires = ["flask", "elasticsearch-dsl"]

setup(
        name="EFEFAL",
        version='0.1',
        description="Elk Front-End for Ansible Logging",
        author="sparky_005",
        author_email="sparky.005@gmail.com",
        license="MIT",
        packages=['efefal'],
        include_package_data=True,
        install_requires = install_requires,
    )
