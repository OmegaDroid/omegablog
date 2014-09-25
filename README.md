This is a very simple blog engine that can create, edit and delete posts.

Requirements
============

To install the requirements run:

```
$ pip install -r requirements.pip
```

To compile the css you will also require less. This can be done using:
```
$ sudo apt-get install node-js npm
$ npm install less
$ lessc omegablog/static/less/omegablog.less > omegablog/static/css/COMPILED/omegablog.css
```

Tests
=====

The project comes with a full suite of tests (both web interface and logic). To run them use:
```
$ python omegablog/manage.py test
```
