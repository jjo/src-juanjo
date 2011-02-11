#!/usr/bin/python2.5

def coproc():
  while True:
    print (yield('mundo'))

a=coproc()
a.next()
print a.send('hola')
print a.send('hello')

