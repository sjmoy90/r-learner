SETUP


1. Clone repository.


2. Change working directory.

    cd rlearner


3. Set up virtual environment.

    virtualenv env -p python3.9


4. Activate virtual environment.

    source env/bin/activate


5. Install requirements.

    pip3 install -r requirements.txt


6. Install jupyter kernel for the virtual environment.

    ipython kernel install --user --name=env

  Note: if you wish to uninstall this kernel, run the following command:

    jupyter-kernelspec uninstall env


7. Select the installed kernel, `env`, to use jupyter notebook in this virtual environment.

  - Open jupyter notebook
  - Select Kernel > Change kernel > env
