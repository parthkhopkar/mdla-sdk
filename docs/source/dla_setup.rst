Micron DLA set-up steps
=======================

1. Obtain necessary hardware: This SDK assumes that you are working on a desktop computer with Micron FPGA boards. For example: AC-511 and EX-750.
2. Install pico-computing tools and Micron DLA SDK. Check section [1.](#1-installation)
3. Run a sample example. Check sections [3.](#3-getting-started-inference-on-microndla-hardware) and [4.](#4-getting-started-inference-on-microndla-hardware-with-c)
4. Create your own application

This document provides tutorials and general information about the Micron DLA SDK.

The SDK contains `Docker <https://github.com/micronDLA/SDK/tree/master/docker>`_ files to create a docker image.

[**Docs**](docs/): Documentation.
* [Python API](docs/PythonAPI.md): Documentation of the python API can be found in docs/PythonAPI.md.
* [C API](docs/C%20API.md): Documentation of the C/C++ API can be found in docs/C API.md.

[**Examples**](examples/): Example code and tests.
* [c_api](examples/c_api): Example how to use the C API
* [pre_trained_models](examples/pre_trained_models): Examples using pre-trained models
* [python_api](examples/python_api): Example how to use the python API
* [tests](examples/tests): Samples to test neural network layers
* [website](examples/website): Example for making a web application with MDLA and Flask

[**Pytorch-MDLA**](https://github.com/micronDLA/pytorch_mdla): Tutorial on how to add Micro DLA into pytorch using [torchscript](https://pytorch.org/docs/stable/jit.html), [torchdynamo](https://github.com/pytorch/torchdynamo) or [functorch](https://github.com/pytorch/functorch).

[**Test-files**](test-files/): Files used for the examples and tutorials.