from setuptools import find_packages, setup


setup(
    name='department_app',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==1.1.2',
        'flask-marshmallow==0.14.0',
        'Flask-Migrate==2.5.3',
        'Flask-RESTful==0.3.8',
        'Flask-SQLAlchemy==2.4.4',
        'Flask-WTF==0.14.3',
        'psycopg2-binary==2.8.6',
    ],
    python_requires='>=3.7'
)
