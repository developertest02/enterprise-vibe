from setuptools import setup, find_packages

setup(
    name="enterprise-auth",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.3.3",
        "psycopg2-binary>=2.9.7",
        "sqlalchemy>=2.0.21",
        "pydantic>=2.4.2",
        "bcrypt>=4.0.1",
        "python-dotenv>=1.0.0"
    ],
    author="Enterprise Vibe Team",
    author_email="team@vibe.com",
    description="Authentication API for Enterprise Vibe",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vibe/enterprise-auth",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)