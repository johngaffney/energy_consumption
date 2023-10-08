from setuptools import setup

setup(
    name="energy_consumption",
    version="1.0",
    description="Package for Energy Consumption Analysis",
    package_dir={"": "energy_consumption"},
    install_requires=[
        "urllib3==1.26.6",
        "requests"
    ]
)
