Basic micropython library to read the distance from an ultrasonic sensor
########################################################################

This library allows the micro:bit to read the distance from an ultrasonic sensor HCSR04 or similar.

It uses the SPI hardware internal device to measure the length of the returning echo, so by default you should connect the sonar echo pin to micro:bit pin 14 and th sonar trigger pin to micro:bit pin 15. The HC-SR04 works with 5V, so you should protect the micro:bit input with a couple of resistors. Note that you can use a US-100 with this library as well. The US-100 has the advantage that works directly with 3V, but it has a serial mode that provides better readings.

.. contents::

.. section-numbering::


Main features
=============

* Get the distance in cm from the sonar to an object.
* Sample program.


Library usage
=============


distance_cm()
+++++++++++++++++++++++


Get the distance in cm with one decimal.


.. code-block:: python

   from hcsr04 import HCSR04
   from microbit import sleep


   sonar=HCSR04()
   while True:
       print('%.1f' % sonar.distance_cm())
       sleep(1000)

