try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from package_metadata import __version__, __description__, __long_description__, __license__, __url__

setup(
    name='rdflib-plugins',
    version=__version__,
    author='Alex Tucker',
    author_email='alex@floop.org.uK',
    license=__license__,
    url=__url__,
    description=__description__,
    keywords='rdflib plugin serializer ntriples nquads',
    long_description=__long_description__,
    entry_points = {
        'rdf.plugins.serializer': [
            'ntfix = plugins.serializers:NTSerializer',
            'nq = plugins.serializers:NQSerializer'
            ],
        }
)
