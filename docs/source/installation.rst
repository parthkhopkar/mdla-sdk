Installation
============

System requirements
-------------------

The SDK assumes that you are working on a desktop computer with Micron FPGA boards.

Check out this `link <https://www.micron.com/products/advanced-solutions/advanced-computing-solutions>`_ to see what Micron FPGA system you have.

Installation has been tested on:

- Ubuntu 18.04 LTS Release, Kernel 4.15.0-39-generic
- CentOS 7.5

Requirements:

- `Pico-computing tools <https://picocomputing.zendesk.com/hc/en-us/>`_: Current version: pico-computing-2020.1. Please verify pico-computing functionality by refering to the document "PicoUsersGuide.pdf" and section "Running a Sample Program"
- `protobuf 3.6.1 <https://github.com/google/protobuf/releases/download/v3.6.1/protobuf-all-3.6.1.tar.gz>`_
- GCC 4.9 or higher
- Python 3
- numpy
- Pillow
- onnx
- torch

.. _pico_computing:

Pico computing
--------------

Pico-computing installer package can be requested from this `link <https://picocomputing.zendesk.com/hc/en-us/>`_. To make sure your FPGA system is working properly, install pico-computing tools.

It is highly recommended to read the `user guide <https://picocomputing.zendesk.com/hc/article_attachments/5378692674189/PicoUsersGuide.pdf>`_ to learn about your FPGA system as this SDK uses pico-computing tools.

Pico computing installer will install the SDK together with pico-computing. ``libmicrondla.so`` library should be present in ``/usr/local/lib/``.

If you have a previous version of pico-computing installed then uninstall it. And remove all ``picocomputing-2020.1`` and ``HMC_release`` folders before installing a new version of pico-computing.

After installation, reboot the machine.

To check if pico-computing tools installation was successful, you can run a sample program in ``/usr/src/picocomputing-2020.1/samples``.

If there is an issue going through this section, a quick check is to run the following commands. It should print the following outputs for AC511 system.

.. code-block::

    lspci | grep -i pico
        05:00.0 Memory controller: Pico Computing Device 0045 (rev 05)
        08:00.0 Memory controller: Pico Computing Device 0511 (rev 05)
    lsmod | grep -i pico
        pico                 3493888  12

After installing pico-computing, run install.sh to install the MDLA SDK

Python package (optional)
-------------------------

You can also install as a python package

.. code-block:: console

    $ git clone https://github.com/micronDLA/SDK

Then inside SDK folder do

.. code-block:: console

    $ python3 setup.py install --user

Docker Image (optional)
-----------------------

This step is optinal and only needed if you want to run as a docker image

If you want to use MDLA with docker, then you need to install :ref:`pico-computing <pico_computing>` and `Docker <https://docs.docker.com/get-docker/>`_.

To start a docker with the Micron DLA SDK you can either download prebuilt images or build them yourself. The benefit of custom building the image is that you can adjust the OS packages you want installed at build time. The trade-off is waiting through the build process of about 15-30min (depending on network and CPU speed).

Load prebuilt image
^^^^^^^^^^^^^^^^^^^

Download the docker image for your OS after requesting it `here <https://picocomputing.zendesk.com/hc/en-us/>`_.

For Ubuntu 18.04:

.. code-block:: console

    $ docker load < mdla_ubuntu18.04.tgz


For CentOS 7.5:

.. code-block:: console

    $ docker load < mdla_centos7.5.tgz

Build Image with Dockerfile
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Copy the OS specific picocomputing package to your docker build folder. Then build and tag the image (we add the latest tag for user convenience when running containers):

For Ubuntu 18.04:

.. code-block:: console

    $ mkdir docker_build
    $ cp /path/to/picocomputing_2020.1_all.deb docker_build
    $ cd docker_build
    $ docker build -f ../docker/Dockerfile.ubuntu -t micron/mdla:2020.1-ubuntu18.04 -t micron/mdla:latest .


For CentOS 7.5:

.. code-block:: console

    $ mkdir docker_build
    $ cp /path/to/picocomputing-2020.1.el6.x86_64.rpm docker_build
    $ cd docker_build
    $ docker build ../docker/Dockerfile.centos -t micron/mdla:2020.1-centos7.5 -t micron/mdla:latest .

Run Container
^^^^^^^^^^^^^

Check the tag of the docker image that you just loaded/built using:

.. code-block:: console

   $ docker images

Run the docker image using the `docker run` command:

.. code-block:: console

   $ docker run -it --rm -v "/path/to/models/on/host":/models --device=/dev/pico1 micron/dla

That will start you in the ``/home/mdla`` directory where the SDK is preinstalled. The ``-it`` flag means interactive, ``--rm`` deletes the container on exit, ``-v`` mounts a directory into the container, and ``--device`` mounts a host device into the container.

To make changes to the container (e.g. install editors, python libraries), remove the ``--rm`` flag so the container persists on exit.
You can then use the container id to ``docker commit <id>`` to a new image or ``docker restart <id>`` and ``docker attach <id>`` to reconnect a stopped container. You can also ``--name`` the container on run if you prefer not to use ids.

.. code-block:: console

    $ docker run -it -v "/path/to/models/on/host":/models --device=/dev/pico1 micron/dla
    root@d80174ce2995:/home/mdla# exit
    $ docker restart d80174ce2995
    $ docker attach d80174ce2995
    root@d80174ce2995:/home/mdla#

Run the example code provided. Check sections [3](#3-getting-started-inference-on-micron-dla-hardware) and [4](#4-getting-started-inference-on-micron-dla-hardware-with-c).