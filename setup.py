from distutils.core import setup
setup(
    name = 'shinden',
    packages = ['shinden'],  
    version = '0.3',      
    license='MIT',        
    description = 'bs4 web scrapping api for shinden.pl',   
    author = 'ShaderLight',                    
    url = 'https://github.com/ShaderLight/shinden.py',   
    download_url = 'https://github.com/ShaderLight/shinden.py/archive/v0.3.1.tar.gz',   
    keywords = ['shinden', 'api', 'web scrapping'],   
    install_requires=[            
            'requests',
            'beautifulsoup4',
        ],
    classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    ],
)
