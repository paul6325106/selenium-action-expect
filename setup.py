from setuptools import setup


def get_readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='paul6325106.selenium-action-expect',
    version='1.0.dev0',
    description='Demonstration of Selenium page model with expectations for an interface across different test system'
                ' implementations',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    packages=[
        'paul6325106.actionexpect'
    ],
    package_dir={'': 'src'},
    python_requires='>=3.7',
    install_requires=[
        'selenium'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-mock',
            'pytest-rerunfailures',
            'pytest-runner',
            'pytest-xdist'
        ],
        'lint': [
            'mypy',
            'pycodestyle'
        ]
    },
    zip_safe=False
)
