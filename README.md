note, the copy of pygal used is a forked copy.  
In order to run correctly, first do the following:  
```buildoutcfg
$ git clone https://github.com/peter-amerkhanian/pygal.git
$ cd pygal
$ python setup.py build
$ python setup.py install
```
The rest of the packages can be installed simply with pip:
```buildoutcfg
$ pip install -r requirements.txt
```