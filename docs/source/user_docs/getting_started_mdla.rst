Getting started with inference on MDLA
======================================

This tutorial will teach you how to run inference on MDLA. We will use a neural network pre-trained on ImageNet.
The program will process an image and return the top-5 classifications of the image. A neural network trained for an object
categorization task will output a probability vector. Each element of the vector contains the probability to its correspondent
category that is listed in a categories file.

In this tutorial you will need:

- One of the `pre-trained models <https://boartifactory.micron.com/ui/native/mdla-generic-dev-virtual/models>`_
- [Input image](./test-files): located in /test-files/
- [Categories file](./test-files/categories.txt): located in /test-files/
- [simpledemo.py](./examples/python_api/simpledemo.py): located in /examples/python_api/


Using Python
------------

Pytorch and torchvision pretrained model on ImageNet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the SDK folder, there is ``genonnx.py``. This script will create an ONNX file from [torchvision models](https://github.com/pytorch/vision/tree/master/torchvision).
This utility requires the latest pytorch and it can create an ONNX file from most networks present in the
torchvision package and also from networks in the pth format.

.. code-block:: console

    $ python3 genonnx.py resnet18

This command will download a pre-trained resnet18 network and create a file called resnet18.onnx

For more information about onnx please visit [https://onnx.ai/](https://onnx.ai/)

To convert tensorflow models into ONNX files please reference the section [6. Using with Tensorflow](#6-using-with-tensorflow)

Loading the FPGA with MDLA
^^^^^^^^^^^^^^^^^^^^^^^^^^

When you turn on the system, it will have the FPGA programmed with a default hardware definition. You need to load the MDLA bitfile only once after turning on the system.

You can load a MDLA bitfile of choice using:

.. code-block:: console

    $ python3 loadbitfile.py <bitfile path>

You can find the MDLA bitfiles in the pico-computing folder. The default pico-computing installation folder is:

``/usr/src/picocomputing-<version>/samples/InferenceEngine_5/firmware/``

Use the appropriate .tgz file for the system you have.

Loading the FPGA will take at max 5 min.
Loading the FPGA only fails when there are no FPGA cards available. If you find issues in loading FPGA check out [Troubleshooting](#11-troubleshooting-and-qa).
Micron DLA hardware will be loaded in the FPGA card. The following MDLA runs will not need to load the hardware anymore.

Running inference on Micron DLA hardware for one image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the SDK folder, there is simpledemo.py, which is a python demo application.
Its main parts are:

1. Parse the model and generate instructions
2. Get and preprocess input data
3. Init Micron DLA hardware
4. Run Micron DLA hardware
5. Get and display output

The user may modify steps 1 and 5 according to users needs.
Check out other possible application programs using Micron DLA hardware [here](http://fwdnxt.com/).
The example program is located in ``examples/python_api/``

You can run the network on hardware with this command, which will find the FPGA card that was loaded with Micron DLA hardware:

.. code-block:: console

    $python3 simpledemo.py <onnx file> <picture> -c <categories file.txt>

e.g., if you have the fwdnxt models in the same directory as SDK:

.. code-block:: console

    $python3 simpledemo.py ../../../model/alexnet.onnx ../../test-files/dog.jpg -c ../../test-files/categories.txt

If you used the example image with alexnet, the demo will output:

.. code-block:: console
    
    Doberman, Doberman pinscher 24.4178 
    Rottweiler 24.1749  
    black-and-tan coonhound 23.6127 
    Gordon setter 21.6492   
    bloodhound, sleuthhound 19.9336

Using C
-------

Running inference on the DLA for one image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the SDK folder, there is ``compile.c``, which compiles an ONNX model and outputs DLA instructions into a .bin file.
The ``simpledemo.c`` program will read this .bin file and execute it on the DLA.

The main functions are:

1. ``ie_compile``: parse ONNX model and generate the DLA instructions.
2. ``ie_init``: load the DLA bitfile into FPGA and load instructions and model parameters to shared memory.
3. ``ie_run``: load input image and execute on the DLA.

Check out other possible application programs using the DLA [here](http://fwdnxt.com/).

Make sure the MDLA bitfile was loaded into the FPGA before running it.

To run the demo, first run the following commands:


.. code-block:: console
    
    $ cd <sdk folder>/examples/c_api
    $ make
    $ ./compile <model.onnx> -i 224x224x3 -o instructions.bin

For example


.. code-block:: console
    
    $ ./compile ../../../model/alexnet.onnx -i 1x3x224x224 -o instructions.bin

Where ``-i`` is the input sizes: width x height x channels.
After creating the ``instructions.bin``, you can run the network on the DLA with this command, which will find the FPGA card that was loaded with the DLA:

.. code-block:: console
    
    $ ./simpledemo -i <picturefile> -c <categoriesfile> -s ./instructions.bin

If you used the example image with alexnet, the demo will output:

.. code-block:: console
       
    black-and-tan coonhound -- 23.9883
    Rottweiler -- 23.6445
    Doberman -- 23.3320
    Gordon setter -- 22.0195
    bloodhound -- 21.5000
