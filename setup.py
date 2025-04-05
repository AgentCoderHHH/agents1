from setuptools import setup, find_packages

setup(
    name="agentopenapi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
        "flask>=2.0.0",
        "psutil>=5.9.0"
    ],
) 