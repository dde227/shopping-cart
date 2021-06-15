# shopping-cart

To run app, first add a requirements.txt with the following package:
    python-dotenv

Second, add a .env file with a variable TAX_RATE set equal to the desired tax rate. For example, if the tax rate is 8.75%, then the .env file should read:
    TAX_RATE = 0.0875

Thirsd, create the necessary conda environment as below:
    conda create -n shopping-env python=3.8 
    conda activate shopping-env
    pip install -r requirements.txt

    