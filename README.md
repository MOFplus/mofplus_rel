# mofplus

mofplus is the API library to the [MOFplus](www.mofplus.org) webpage. It can be used to download topologies, bbs, structures, ...

### INSTALLING

In order to install molsys, clone this repository into the destination of your choosing (we always use /home/%USER/sandbox/, also the installation instructions below use this path)

```
https://github.com/MOFplus/mofplus.git or git@github.com:MOFplus/mofplus.git
```

Afterwards the PATH and PYTHONOATH have to be updated. Add to your .bashrc :
```
export PATH=/home/$USER/sandbox/molsys/scripts:$PATH
alias mofplus="python -i /home/$USER/sandbox/mofplus/mofplus/ff.py"
```


Mandatory dependencies are:

* numpy (pip install numpy)
* xmlrpc (pip install xmlrpc)
* registration on [MOFplus](www.mofplus.org) 

## Running the tests

There will soon be a testing framework framework available.

## Building the Documentation

Mandatory dependencies to built the documentation can be obtained via pip:
```
pip install Sphinx
pip install sphinx-rtd-theme
```
The Documentation can be compiled by running
```
make html
```
in the doc folder.
A Built directory containing
```
/built/html/index.html
```
was created. It can be opened with the browser of your choice

## Contributing

TBA

## License

TBA

## Acknowledgments


