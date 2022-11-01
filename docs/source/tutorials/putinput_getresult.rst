PutInput and GetResult
======================

This tutorial teaches you to use :meth:`PutInput <microndla.MDLA.PutInput>` and :meth:`GetResult <microndla.MDLA.GetResult>` API calls.

PutInput will load the input data into the memory that is shared between the host and the Micron DLA.

GetOutput will read the output (results) from the memory. GetOutput can be blocking or non-blocking. Use :meth:`SetFlag <microndla.MDLA.SetFlag>` function to use blocking or non-blocking mode. 
The user does not need to care to start the inference engine. 
PutInput and GetResult will take care of that as soon as the inference engine becomes free.

Blocking means that a call to GetResult will wait for the DLA to finish processing.

Non-blocking means that GetResult will return immediately: with or without the result depending whether the DLA has finished processing.

These two functions are important in a streaming application. The programmer can overlap the time for these two tasks: input loading and getting results.

Some care has to be taken in order to avoid deadlocks. There is only one inference engine and only two internal buffers where input and output are stored. 
So if a user issues three PutInput in sequence without any GetResult between (or waiting in another thread), 
the third PutInput will block indefinitely waiting for a buffer to become available, something that will never happen if the user will not call GetResult to get the result of the first PutInput, freeing the associated results buffer. 
Particular care has to be taken when dealing with multiple inference engine objects: they all share the common hardware, so again there can be only one outstanding PutInput. 
Consider this sequence:

- PutInput on the first object
- PutInput on the first object
- PutInput on the second object
- GetResult on the second object

This will result in a deadlock, because PutInput on the second object will wait for a buffer to become free and this cannot happen until the user calls GetResult on the first object. 
Having a thread for each object always waiting for the results, will assure that this will not happen.

.. image:: ../images/tutorials/double_buffer.jpg

Examples using PutInput and GetOutput are located `here <https://github.com/micronDLA/SDK/tree/master/examples/python_api>`_.

- pollingdemo.py : is an example of non-blocking mode. The program will poll GetResult until it returns the output.

- interleavingdemo.py : is an example that shows how to pipeline PutInput and GetResult calls. There are two separate memory regions to load inputs and get results. While PutInput loads to one region, GetResult fetches the output from another region. Each image is labeled with the **userobj** to keep track of which input produced the returned output.

- threadeddemo.py : shows how to use two threads to process multiple images in a folder. One thread calls GetResult and another calls PutInput. This is the preferred way to work, as it will give the best possible performance.

- threadedbatchdemo.py : similar to ``threadeddemo.py``. It shows how to process images in a batch using PutInput and GetResult.