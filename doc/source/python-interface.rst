====================
The python interface
====================

pony is primarelly a python library to use within scripts executed by build engine. It is developed with **Scons** in mind but you can use it from any build engine once you can interface it with python code or your build engine can interface at least with the command line. As anyone I've ever tried.
pony let you do two fondamental operations:
  
  - charge a box
  - deliver box's dependencies
  
.. note::
  
  In the pony's jargon, a package is called **box**. So, when you are ready with a new version of your artifact, you will charge the pony to manage it asking to package it in a **box** and depot it into its **store**. When any user need some artifact to resolve its dependencies, he will ask the **pony** to **deliver** its dependencies.
  
The **charge** operation
-----------------------

The charge operation consist of make a tarball of the an artifact you are going to store into the bag (the portfolio of available projects) and then actually store it as a document into a mongo database with any metadata is relevant in your context. 
The created tarball can be organized as for your preference; This means the structure stored into the tarball can differ from the source one on your filesystem. That is, you can define your own package structure.
So, what pony needs to **charge** an artifact is:

  - a list of **pack instructions**
  - a metadata object
  
**pack instructons** describe the move operations from the folder into the file system to a folder into the tarball box, pony uses to package your artifact into a box.
Say, for example, you want to charge the **pony** to manage all the .txt files that are in your sandbox in  test/temp-data into a folder named *test-data* at the root of tarball. You can define a **pack instruction** like: 

.. code-block:: python

  instruction = pony.pack('test/temp-data', 'test-data', '*.txt')

Of course you can have multiple instructions to perform during the creation of the box.

.. code-block:: python

  instructions = [ 
                    pony.pack('test/temp-data', 'test-data', '*.txt'),
                    pony.pack('test/temp-data/subfolder/subsubfolder', 'moved-folder', '*.txt')
                  ]
    
  meta = {"NAME"    : "dep-v1",
          "VERSION" : "1.0.0"}
  pony.charge(instructions, meta)
  
In the example above, I've introduced also some metadata. Specify metadata is as simple as construct a python dictionary. You can read it from a metainformation file then alter it during the build process to capture information feed as build parameters (i.e. structure allignment or target platform are good candidates).
  
  
The **deliver** operation
-----------------------

The **deliver** operation is the one you can ask the pony to perform to satisfy your project requirements. 
It is pretty similar to the charge operation. In fact you send the pony a list of **unpack instructions** to describe the folder structure you want to create/fill on your sandbox.

.. code-block:: python

  json_string = """
      [
              {   "NAME" :  "dep-v1",
                  "VERSION" :  {"$gte" : "0.9.0"} 
              },
              
              {   "NAME"      : "prj61",
                  "VERSION"   : "1.3.0"
              }
      ]"""
      
  meta_request = json.loads(json_string)

  instructions =  [   pony.unpack('test-data', 'test/results-data'),
                      pony.unpack('moved-folder', 'test/results-data')
                  ]
                    

  pony.deliver(instructions, meta_request)  

The snippet above requires two projects from the bag named **dep-v1** and **prj61** and move their content according to the list of unpack operations.  


The metadata file
-----------------

You may want not to store your metadata directly into your build script or, at least, you may not want to store there all of them. Indeed you can define metadata for your project into a json file then use it as a source of meta-requirements and of meta-informations. 
A metadata for a project named **prj100** at version **1.2.1** depending on **dep-v1** at least at version **0.9.0** and on **prj61** exactly at version **1.3.0** may look like:

.. code-block:: json

  {
    "NAME"    : "prj100",
    "VERSION" : "1.2.1",
  
    "DEPENDENCIES" :  [
                        {   "NAME" :  "dep-v1",
                            "VERSION" :  {"$gte" : "0.9.0"} 
                        },
                        
                        {   "NAME"      : "prj61",
                            "VERSION"   : "1.3.0"
                        }
                      ]         
  }

while the python code that can be used to resolve dependencies looks like:

.. code-block:: python

  import pony

  instructions =  [   pony.unpack('test-data', 'test/results-data'),
                      pony.unpack('moved-folder', 'test/results-data')
                  ]
                
  pony.deliver_all( instructions, "metadata_file.json")

  # ... some build 

  pony.charge(   [ 
                    pony.pack('test/temp-data', 'test-data', '*.txt'),
                    pony.pack('test/temp-data/subfolder/subsubfolder', 'moved-folder', '*.txt')
                  ], 
                  "metadata_file.json"
  )
  
  
.. toctree::
  :maxdepth: 2
  
  
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
