from setuptools import setup

setup(
    name='marshmallow-helpers',
    version='0.2.0',
    packages=['marshenum'],
    author_email="zidder@hilearn.io",
    description="Ease marshmallow schema creation",
    classifiers=['Programming Language :: Python :: 3',
                 'Development Status :: 3 - Alpha'],
    install_requires=["attrs==19.3.0",
                      "marshmallow>=3.5.1",
                      "webargs==5.5.3"],
    dependency_links=["https://github.com/hilearn/marshmallow-annotations"]
)
