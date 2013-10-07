from setuptools import setup, find_packages
setup(
    name = "overkill-extra-bspwm",
    version = "0.1",
    install_requires=["overkill"],
    packages = find_packages(),
    namespace_packages = ["overkill", "overkill.extra"],
    author = "Steven Allen",
    author_email = "steven@stebalien.com",
    description = "Bspwm data source for overkill.",
    license = "GPL3",
    url = "http://stebalien.com"
)
