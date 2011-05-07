from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.dexterity.more_widgets',
      version=version,
      description="Extra form widgets",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'':'src'},      
      namespace_packages=['collective', 'collective.dexterity'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.autopermission',        # Schema permissions
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
