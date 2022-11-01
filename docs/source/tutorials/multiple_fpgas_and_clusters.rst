Multiple FPGAs and Clusters
===========================

This tutorial will teach you how to run inference on Micron DLA inference engine using multiple FPGAs and clusters.

Multiple FPGAs with input batching
----------------------------------

Suppose that you have a desktop computer with two AC-511 FPGAs cards connected to a EX-750 PCI backplane. T
o simplify this example, let us assume there is one cluster per FPGA card. 
We will see how to use multiple clusters in the following sections. 
The SDK can receive two images and process one image on each FPGA. 
The Micron DLA instructions and model parameters are broadcast to each FPGA card's main memory (HMC). 
The following code snippet shows you how to do this:

.. code-block:: python

    import microndla
    import numpy as np
    numfpga = 2
    numclus = 1
    # Create Micron DLA API
    sf = microndla.MDLA()
    # Generate instructions
    sf.SetFlag({'nfpgas': str(numfpga), 'nclusters': str(numclus)})
    sf.Compile('resnet18.onnx')
    in1 = np.random.rand(2, 3, 224, 224).astype(np.float32)
    input_img = np.ascontiguousarray(in1)
    # Create a location for the output
    output = sf.Run(input_img)

``sf.Compile`` will parse the model from model.onnx and save the generated Micron DLA instructions. Here numfpga=2, so instructions for two FPGAs are created.
``nresults`` is the output size of the model.onnx for one input image (no batching).
The expected output size of ``sf.Run`` is twice ``nresults``, because numfpga=2 and two input images are processed. ``input_img`` is two images concatenated.

.. image:: ../images/tutorials/2fpga2img.png

Multiple FPGAs with different models
------------------------------------

The SDK can also run different models on different FPGAs. 
Each ``microndla.MDLA()`` instance will create a different set of Micron DLA instructions for a different model and load it to a different FPGA.
The following code snippet shows you how to do this:

.. code-block:: python

    import microndla
    import numpy as np
    # Create Micron DLA API
    sf1 = microndla.MDLA()
    # Create second Micron DLA API
    sf2 = microndla.MDLA()
    # Generate instructions for model1
    sf1.Compile('resnet50.onnx')
    # Generate instructions for model2
    sf2.Compile('resnet18.onnx')
    in1 = np.random.rand(3, 224, 224).astype(np.float32)
    in2 = np.random.rand(3, 224, 224).astype(np.float32)
    input_img1 = np.ascontiguousarray(in1)
    input_img2 = np.ascontiguousarray(in2)
    output1 = sf1.Run(input_img1)
    output2 = sf2.Run(input_img2)

The code is similar to the previous section. 
Each instance will compile, init and execute a different model on different FPGA.
The diagram below shows this type of execution:

.. image:: ../images/tutorials/2fpga2model.png

Multiple clusters with input batching
-------------------------------------

For simplicity, now assume you have one FPGA and inside it we have two Micron DLA clusters. 
Each cluster can execute its own set of instructions, so we can also batch the input (just like the two FPGA case before). 
The difference is that both clusters share the same main memory in the FPGA card. 
The number of results returned by Compile() will be the total number of results, for both clusters, in this case. 
Following a similar strategy as the two FPGA with input batching example, the following code snippet shows you how to use two clusters to process two images:

.. code-block:: python

    import microndla
    import numpy as np
    numfpga = 1
    numclus = 2
    # Create Micron DLA API
    sf = microndla.MDLA()
    # Generate instructions
    sf.SetFlag('nclusters', str(numclus))
    sf.Compile('resnet18.onnx')
    in1 = np.random.rand(2, 3, 224, 224).astype(np.float32)
    input_img = np.ascontiguousarray(in1)
    output = sf.Run(input_img)

.. image:: ../images/tutorials/2clus2img.png

Multiple clusters without input batching
----------------------------------------

The SDK can also use both clusters on the same input image. 
It will split the operations among the two clusters.
The following code snippet shows you how to use two clusters to process one image:

.. code-block:: python

    import microndla
    import numpy as np
    numfpga = 1
    numclus = 2
    # Create Micron DLA API
    sf = microndla.MDLA()
    sf.SetFlag({'nclusters': str(numclus), 'clustersbatchmode': '1'})
    # Generate instructions
    sf.Compile('resnet18.onnx')
    in1 = np.random.rand(3, 224, 224).astype(np.float32)
    input_img = np.ascontiguousarray(in1)
    output = sf.Run(input_img)

Use ``sf.SetFlag('nobatch', '1')`` to set the compiler to split the workload among two clusters and generate the instructions.
You can find more information about the option flags [here](docs/Codes.md).
Now the output size is not twice of ``nresults`` because you expect output for one inference run.
The diagram below shows this type of execution:

.. image:: ../images/tutorials/2clus1img.png

Multiple clusters with different models
---------------------------------------

The following example shows how to run different models using different clusters in parallel. 
Currently, a cluster for each model is allowed. But different number of cluster per model is not allowed. 
For example, 3 clusters for a model and then 1 cluster for another.
The example code is in `here <https://github.com/micronDLA/SDK/blob/master/examples/python_api/twonetdemo.py>`_

.. code-block:: python

    import microndla
    import numpy as np
    nclus = 2
    img0 = np.random.rand(3, 224, 224).astype(np.float32)
    img1 = np.random.rand(3, 224, 224).astype(np.float32)
    ie = microndla.MDLA()
    ie2 = microndla.MDLA()
    ie.SetFlag({'nclusters': nclus, 'clustersbatchmode': 1})
    ie2.SetFlag({'nclusters': nclus, 'firstcluster': nclus, 'clustersbatchmode': 1})
    ie.Compile('resnet18.onnx')
    ie2.Compile('alexnet.onnx', MDLA=ie)
    ie.PutInput(img0, None)
    ie2.PutInput(img1, None)
    result0, _ = ie.GetResult()
    result1, _ = ie2.GetResult()

In the code, you create one MDLA object for each model and compile them. 
For the first model, use 2 clusters together. 
For the second model, assign the remaining 2 clusters to it. Use ``firstcluster`` flag to tell ``Compile`` which cluster is the first cluster it is going to use.
In this example, first model uses clusters 0 and 1 and second model uses clusters 2 and 3. 
In ``Compile``, pass the previous MDLA object to link them together so that they get loaded into memory in one go. 
In this case, you must use ``PutInput`` and ``GetResult`` paradigm (this [section](#6-tutorial---putinput-and-getresult)), you cannot use ``Run``.

.. image:: ../images/tutorials/2clus2model.png

All clusters with different models in sequence
----------------------------------------------

This example shows how to load multiple models and run them in a sequence using all clusters. 
This is similar to previous example, the only difference is that all clusters are used for each model. 
It uses same principle of creating different MDLA objects for each model and link different MDLAs in ``Compile``.

.. code-block:: python

    import microndla
    import numpy as np
    nclus = 2
    img0 = np.random.rand(3, 224, 224).astype(np.float32)
    img1 = np.random.rand(3, 224, 224).astype(np.float32)
    ie = microndla.MDLA()
    ie2 = microndla.MDLA()
    ie.SetFlag({'nclusters': nclus, 'clustersbatchmode': 1})
    ie2.SetFlag({'nclusters': nclus, 'clustersbatchmode': 1})
    ie.Compile('resnet18.onnx')
    ie2.Compile('alexnet.onnx', MDLA=ie)
    result0 = ie.Run(img0)
    result1 = ie2.Run(img1)

.. image:: ../images/tutorials/2clus2seqmodel.png

Multiple clusters with even bigger batches
------------------------------------------

It's possible to run batches of more than than the number of clusters or FPGAs. 
Each cluster will process multiple images. 
This is enabled with the ``imgs_per_cluster`` flag. 
In order to process 32 images, 16 by each cluster, this code will do the work:

.. code-block:: python

    import microndla
    import numpy as np
    numfpga = 1
    numclus = 2
    # Create Micron DLA API
    sf = microndla.MDLA()
    sf.SetFlag({'nclusters': str(numclus), 'imgs_per_cluster': '16'})
    # Generate instructions
    sf.Compile('resnet18.onnx')
    in1 = np.random.rand(32, 3, 224, 224).astype(np.float32)
    input_img = np.ascontiguousarray(in1)
    output = sf.Run(input_img) # Run

Batching using MVs
------------------

It's possible to use MV-level parallelism. MV is a computation unit present inside of a cluster and they can be configured to run different images.
This is generally more efficient than leaving different MV units process the same image.
In order to enable this, you have to set the ``mvbatch`` flag. 
Keep in mind that this can be only done when ``imgs_per_cluster`` is a multiple of 4, since there are 4 MV units available inside of a cluster.

.. code-block:: python

    import microndla
    import numpy as np
    numfpga = 1
    numclus = 2
    # Create Micron DLA API
    sf = microndla.MDLA()
    sf.SetFlag({'nclusters': str(numclus), 'imgs_per_cluster': '16', 'mvbatch': '1'})
    # Generate instructions
    sf.Compile('resnet18.onnx')
    in1 = np.random.rand(32, 3, 224, 224).astype(np.float32)
    input_img = np.ascontiguousarray(in1)
    output = sf.Run(input_img)
