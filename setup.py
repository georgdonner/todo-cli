from setuptools import setup

setup(
  name='todo-cli-todoist',
  version='1.0.0',
  description='A CLI for managing Todoist tasks.',
  author='Georg Donner',
  url='https://github.com/georgdonner/todo-cli',
  packages=['todo', 'helpers', 'commands'],
  license='MIT',
  install_requires=[
    'todoist-python',
    'colorama'
  ],
  entry_points={
    'console_scripts': ['todo=todo.main:main']
  }
)