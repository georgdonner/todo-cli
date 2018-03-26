from setuptools import setup

setup(
  name='todo-cli-todoist',
  version='1.1.0',
  description='A CLI for managing Todoist tasks.',
  author='Georg Donner',
  url='https://github.com/georgdonner/todo-cli',
  packages=['todo', 'todo.commands', 'todo.helpers'],
  license='MIT',
  install_requires=[
    'todoist-python',
    'colorama'
  ],
  entry_points={
    'console_scripts': ['todo=todo.main:main']
  }
)