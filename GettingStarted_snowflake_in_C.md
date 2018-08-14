# Tutorial - Inference on Snowflake using C 

This tutorial will teach you how to run inference on Snowflake using C code. We will use a neural network pre-trained on ImageNet.
The program will process an image and return the top-5 classification of the image.  
In this tutorial you will need:
* One of the [pre-trained models](http://fwdnxt.com/models/)
* Input image. Some image samples are [here](https://github.com/FWDNXT/Snowflake-SDK/tree/master/test-files)
* [Categories file](https://github.com/FWDNXT/Snowflake-SDK/blob/master/test-files/categories.txt)
* Source code in [here](https://github.com/FWDNXT/Snowflake-SDK/tree/master/sdk/examples/C)
* libsnowflake.so: add libsnowflake to the [sdk folder](https://github.com/FWDNXT/Snowflake-SDK/tree/master/sdk). You can get the libsnowflake.so by a request to [FWDNXT](http://fwdnxt.com/)

**Running inference on Snowflake for one image**

In the SDK folder, there is compile.c, which compiles a ONNX model and outputs Snowflake instructions into a .bin file.
The simpledemo.c program will read this .bin file and execute it on Snowflake.  
The main functions are:
1) snowflake_compile: parse ONNX model and generate Snowflake instructions.
2) snowflake_init: load Snowflake bitfile into FPGA and load instructions and model parameters to shared memory.
3) snowflake_run: load input image and execute Snowflake.

Check out other possible application programs using Snowflake [here](http://fwdnxt.com/).  
To run the demo, first run the following commands:

```
cd <sdk folder>/examples/C
make
export LD_LIBRARY_PATH=../../
./compile -m <model.onnx> -i 224x224x3 -o instructions.bin
```
Where `-i` is the input sizes: width x height x channels.  
After creating the `instructions.bin`, you can run the following command to execute it: 

`./simpledemo -i <picturefile> -c <categoriesfile> -s ./instructions.bin -b <bitfile.bit>`

`-b` option will load the specified Snowflake bitfile into a FPGA card.  
Loading the FPGA and bringing up the HMC will take at max 5 min.
Loading the FPGA only fails when there are no FPGA cards available. If you find issues in loading FPGA check out [Troubleshooting](https://github.com/FWDNXT/Snowflake-SDK/blob/master/Troubleshooting.md).  
After the first run, Snowflake will be loaded in the FPGA card. The following runs will not need to load Snowflake anymore.
You can run the network on Snowflake with this command, which will find the FPGA card that was loaded with Snowflake:

`./simpledemo -i <picturefile> -c <categoriesfile> -s ./instructions.bin`

If you used the example image with alexnet, the demo will output:

```
black-and-tan coonhound -- 23.9883
Rottweiler -- 23.6445
Doberman -- 23.3320
Gordon setter -- 22.0195
bloodhound -- 21.5000
```