====================
Artifact PonyExpress
====================

Artifact PonyExpress (or simply Pony) is an artifact repository and package manager that aims to simplify software modules integration into big projects.
It is designed with native (read modern C++) development in mind but it is usefull everywhere there is an environment to setup in order to transform versioned data using any software. 

.. note:: As pony works well with binary components, the transformation function (the tool used to transform data) itself may be a packaged component.

Pony use MongoDB as backend to store your packages and meta-informations. The pony's MongoDB database is the **pony_store** and the only collection it uses as a repository is named **packages**.

You'll need a running local or remote MongoDB database in order to use pony. 

You can perform two main operation from the pony command line:
  
  - **charge** the pony to deliver your artifact to clients.
  - **deliver** dependencies of the working artifact to users.
  
For a quick taste see: :ref:`quick_start_guide`

--------
Use-case
--------

In a tipical application what you are going to do is integrate a bounce of existing modules that your organization has in the codebase, and write some more code to implement more functionality on top of them. So any project will require a start up fase when you'll setup a proper developing environment. This happen every time you'll start a project regardless of its dimensions, sometime it is a long and error prone process. And it is boring!

You have to get:

  * static libraries (and the related header files)
    
    * be sure they are compiled using compatible options against the one you are going to use in your projects. Some example are:
    
      * structure allignment
      * character dimensions (aka char vs wchar)
      * target platform
      * compiler version 
      * ... anything relevant in your working environment
            
  * header files for header only libraries
  * any dinamic link library you will need to run or test your executable
  * copy all those files in the right place in your project folder structure
  
And this operations may be performed multiple times if you really need to be sure what version of your component are using. I mean you really want to be sure the correct package is there at the moment your build engine is going to use it. Ideally, you should be able to create a sandbox environment directly from archived modules every time in order to avoid unreplicable bugs. This approch can help maintain a clean working environment which can be reproduced from green field each time.

As for my experience, if this process in't kept simple, it is avoided possibly resulting in a "personal" build environment (the product depends on the machine that build machine) and/or overly growth projects with more and more functionality added only because "it was the easiest place" to add some code/parameters instead of an isolated module.

Pony, as other package manager, aims to simplfy this process to let you have a working environment from just few metadata describing it and its dependencies. It aims to have this result the easiest way and without any interference with your build engine choise.

Package attributes
------------------

Pony act as a package manager and only as a package manager. It will not force you to leave your favourite build engine and, even if I'll focus on SCons, it will try to be as friendly as possible with any of them. 
Once developer has a stable version to release, he will ask the build engine to build and deliver a particular version of his artifact. The relevant attributes definition is completly up to the developer/user and described into a meta-informations file that can be stored alongside the sources. Additional meta-informations can be inserted by the build engine to describe build relevant informations such as structure allignment or target machine. 
The name used by pony to refers to the artifact packed with the related metadata is **box**. So pony load boxes to the repository when it's asked to manage them and deliver boxes as they are required.

A minimal meta-informations file can be something like:

.. code-block:: json

  {
    "NAME"          : "TheProjectName",
    "Version"       : "2.1.7"
  }

During the build process, depending on particular build parameters the meta-informations may become:

.. code-block:: json
  
  {
    "NAME"          : "TheProjectName",
    "Version"       : "2.1.7",
    "StructAllign"  : 1,
    "TARGET"        : "x86"
  }

To let the user be free to have a sandbox different from the final package structure, pony define a reserved attribute that will not be stored in the database called **__BOX_INSTRUCTIONS__**.
It is a list of packaging instructions, that is, a list of json objects that specify:
  
  * a source path using the attribute **FROM**
  * a destination path based on package root using the attribute **TO**
  * a file filter using the attribute **FILTER**

.. note:: Pony will package any file that fulfill the filter in the path indicated as source or in any subfolder. It will also mantain the folder structure below the source path.

Given a list of packaging instructions, pony will prepare the artifact content as a tarball stored as an attribute of the mongo document.

.. code-block:: json

  {
    "NAME"          : "TheProjectName",
    "Version"       : "2.1.7",
    "StructAllign"  : 1,
    "TARGET"        : "x86"

    "__BOX_INSTRUCTIONS__"  : [ 
                                {
                                  "FROM"    : "test/temp-data",
                                  "TO"      : "test-data",
                                  "FILTER"  : "*.txt",
                                },
                                
                                {
                                  "FROM"    : "test/temp-data/subfolder/subsubfolder",
                                  "TO"      : "moved-folder",
                                  "FILTER"  : "*.txt",
                                }
                              ]
  }


Specify dependencies
--------------------

Pony defines a component's special attribute named **DEPENDENCIES** which list any dependencies the component may have. This attribute may or may not be present, if it is not, pony interpret the missing attribute as absence of dependencies to retrive. 
Every dependency listed in the **DEPENDENCIES** attribute, is a meta-information object that describes the properties of the component to match to satisfy the component requirement.

To let the user organize his project independelly from the way its dependencies packages are organized, pony defines a special metadata named **__UNBOX_INSTRUCTIONS__** that describes the policy to use while extracting data from dependency packages. It is shared by all dependencies as packages are supposed to share a quite common structure. **__UNBOX_INSTRUCTIONS__** looks the same as **__BOX_INSTRUCTIONS__**, pony don't store them on the database just like it do for **__BOX_INSTRUCTIONS__**.

.. code-block:: json

   {
    "NAME"          : "TheProjectName",
    "MajorVersion"  : "2.1.7",
    "StructAllign"  : 1,
    "TARGET"        : "x86"
    
    "DEPENDENCIES"  : [
                        { 
                          "NAME"     : "FirstComponentName"
                          "Version"  : "1.2.0"
                          "TARGET"   : "x86"
                        },
                        { 
                          "NAME"     : "SecondComponentName"
                          "Version"  : { "$gte" : 1.0.0" }
                          "TARGET"   : "x86"
                        }
                      ]
                      
    "__UNBOX_INSTRUCTIONS__" : [
                                  {
                                    "FROM"    : "test-data",
                                    "TO"      : "test/results-data",
                                    "FILTER"  : "*.txt"
                                  },
                              
                                  {
                                    "FROM"    : "moved-folder",
                                    "TO"      : "test/results-data",
                                    "FILTER"  : "*.txt" 
                                  }
                               ]
  }
  
Pony allow user to specify (and require) any attribute, and some of those can also be appended during the build process (i.e. the TARGET may depend from a build parameter).
Attributes to describe required components may be specified using special functions (the ones available to query mongoDB). In the example above, the required version of *SecondComponentName* is any of the ones with version 1.0.0 or above available in the portfolio, also known as the **pony bag**. 

Command line
------------

It is quite simple to use pony from command line. To charge pony to manage your results just write:

.. code-block:: bash

  pony --meta "meta-informations.json" charge
  
While to retrieve dependencies, before you start build your project write:

.. code-block:: bash

  pony --meta "meta-informations.json" deliver
  
for an even simpler interface, use the standard name for the meta-informations file: **meta.json**. In this case you can just omit the --meta option.
More command line options are available to let the user specify MongoDB connection property. Here is the complete list:

    --meta    <meta-informations file>
    --mongo   <mongo-host> default localhost
    --port    <mongodb-port> default 27017
    --user    <mongodb user name> 
    --pwd     <mongodb user password>
 
Contents:

.. toctree::
   :maxdepth: 2
   
   quick-start
   python-interface
   scons-interaction



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

