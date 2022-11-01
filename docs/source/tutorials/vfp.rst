Variable Fix Point Quantization
===============================

Micron DLA uses 16-bit fix point to represent numbers. The ``Compile`` function will convert the numbers in the onnx model from float 32-bit into 16-bit fix-point `Q8.8 <https://en.wikipedia.org/wiki/Q_(number_format)>`_. The default Micron DLA bitfile will run the model using Q8.8.

A Micron DLA bitfile with variable fix-point support is provided in order to reduce the discrepancy between the float 32-bit and the Q8.8 representation.

This bitfile allows the software to choose different QX.Y representations that is the best fit for different parts of the neural network model.

The SDK provides 2 options for variable fix-point quantization. **Before you try** these options, make sure to load the bitfile that supports variable fix-point into the FPGA.

**Option 1**: For each layer of the model, their weights and biases are converted into different QX.Y representations.

In this case, you can set ``V`` in the options using ``SetFlag`` function before ``Compile``:

.. code-block:: python

    ie = microndla.MDLA()
    ie.SetFlag('varfp', '1')
    #Compile to a file
    swnresults = ie.Compile('resnet18.onnx')

**Option 2**: Variable fix-point can be determined for input and output of each layer if one or more sample inputs are provided.

You will need to provide a set of sample inputs (calibration data) to ``Compile`` funtion. In addition to compiling the model, ``Compile`` will run the model with the calibration inputs using float32 and save the variable fix-point configuration for each input/output of each layer in the model. ``Compile`` will also convert the static data (weights and biases) to the appropriate fix-point representation, so no need for ``ie.SetFlag('varfp', '1')`` in this case.

Instead of using ``ie.Compile``, you use ``Quantize`` and give an array of input data:

.. code-block:: python
    
    # Load image into a numpy array
    img = LoadImage(args.image, args)
    imgs = []
    for fn in os.listdir(args.imagesdir):
        x = LoadImage(args.imagesdir + '/' + fn, args)
        imgs.append(x)

    # Create and initialize the Inference Engine object
    ie = microndla.MDLA()
    #Compile to a file
    swnresults = ie.Compile('resnet18.onnx', samples=imgs)

After that, ``Init`` and ``Run`` runs as usual using the saved variable fix-point configuration.

Checkout the example quantize.py <examples/python_api/quantize.py> which takes same arguments as ``simpledemo.py``. The only addition is a folder with the calibration input images for calibration data.