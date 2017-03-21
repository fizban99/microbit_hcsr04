Basic micropython library for the micro:bit to read the distance from an ultrasonic sensor
##########################################################################################

This library allows the micro:bit to read the distance from an ultrasonic sensor HCSR04 or similar.

It uses the SPI hardware internal device to measure the length of the returning echo, so by default you should connect the sonar echo pin to micro:bit pin 14 and the sonar trigger pin to micro:bit pin 15. The HC-SR04 works with 5V, so you should protect the micro:bit input with a couple of resistors to create a voltage divider (see, e.g. http://www.raspberrypi-spy.co.uk/2012/12/ultrasonic-distance-measurement-using-python-part-1/). Note that you can use a US-100 with this library as well. The US-100 has the advantage that works directly with 3V, so it does not require a voltage divider and you can connect it directly to the micro:bit. Note that the US-100 has a serial mode that provides better readings, so it is better to use the `other library`_ with it.

   .. _other library: https://github.com/fizban99/microbit_us100

   .. image:: ultrasonic.png
      :width: 100%
      :align: center

These sensors look like robot eyes. In fact, one eye is an emitter and the other is a receiver. The sensor is triggered with a pulse of around 10 microseconds. When it gets the pulse from the micro:bit, it sends an ultrasonic tone through one of the "eyes". The other eye detects the reflection of the sound. The sensor generates a pulse as wide as the time it took for the frequency to be detected. So the width of the "echo" pulse is equivalent to the time it takes the sound to reach the object and come back, which is twice as much as the distance to the object. 

   .. image:: spi1.png
      :width: 100%
      :align: center

The library uses the internal hardware spi device to measure the echo. SPI works by using one pin to set the clock speed, with pulses at the required frequency. Another pin is used to transmit bits at each clock cycle and the last pin is used to receive the bits from the other device. The library sends a pulse through MOSI and waits to receive something through MISO. Then, it measures the length of the returning pulse by counting the equivalent "bits".

  .. image:: spi2.png
      :width: 100%
      :align: center
      
      
Since the information is actually grouped in bytes, we need to identify the first time we receive something different than 0x00 and count its bits (our "preamble"), then wait until we receive something different than 0xFF (hexadecimal for the binary 11111111), which will be our "postamble" and then count the total nomber of bits as preamble + 8 x bytes in the middle + postamble. 

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


Get the distance in mm.


.. code-block:: python

   from hcsr04 import HCSR04
   from microbit import sleep


   sonar=HCSR04()
   while True:
       print('%.1f' % (sonar.distance_mm()/10))
       sleep(1000)

