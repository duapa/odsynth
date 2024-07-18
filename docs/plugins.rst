Plugin System and the Home Directory
=====================================
It is possible for developers to plugin in their own providers, formatters and writers to the Data Synthesis system by loading the user added components from the **ODSYNTH_HOME** directory.  The ODSYNTH_HOME is  specified by setting the environment variable `ODSYNTH_HOME`::

    export ODSYNTH_HOME=./sample_home_folder


An ODSYNTH Home folder is expected to have the following subfolders the various developer plugins:

* **providers** for user added providers

* **formatters** for user added formatters

* **writers** for user added writers