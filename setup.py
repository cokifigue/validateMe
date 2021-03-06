from setuptools import setup

setup(
    name='validateMe',
    packages=['validateMe'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-restplus',
        'flask-sqlalchemy',
        'flask-migrate',
        'hashids',
    ],
)
