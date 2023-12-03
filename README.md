SETUP


1. Clone repository.

    ```
    git clone https://github.com/sjmoy90/rlearner.git
    ```

2. Change working directory.

    ```
    cd rlearner
    ```

3. Set up virtual environment, `env_rlearner`.

    ```
    virtualenv env_rlearner -p python3.9
    ```

4. Activate virtual environment.

    ```
    source env_rlearner/bin/activate
    ```

5. Install requirements.

    ```
    pip3 install -r requirements.txt
    ```

6. Install jupyter kernel for the virtual environment.

    ```
    ipython kernel install --user --name=env_rlearner
    ```

  This creates a kernel, `env_rlearner`, located here:

    ~/Library/Jupyter/kernels/env_rlearner

  Note: if you wish to uninstall this kernel, run the following command:

    jupyter-kernelspec uninstall env_rlearner

7. Select the installed kernel, `env_rlearner`, to use jupyter notebook in this virtual environment.

  - Open jupyter notebook
  - Select Kernel > Change kernel > env_rlearner
