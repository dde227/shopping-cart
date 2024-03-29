# shopping-cart

To run app, first add a requirements.txt with the following package:  
    python-dotenv
    sendgrid==6.6.0  

Second, add a .env file with a variable TAX_RATE set equal to the desired tax rate. For example, if the tax rate is 8.75%, then the .env file should read:  
    TAX_RATE = 0.0875  
The .env file should also include the API key, template ID, and email address associated with the user's SendGrid account. 

Finally, create the necessary conda environment as below:      
    conda create -n shopping-env python=3.8  
    conda activate shopping-env  
    pip install -r requirements.txt  

Now, to run the app, enter the following:  
    python shopping_cart.py

Once in the app, enter the product number and then hit enter - note, if an invalid product number is entered you will be prompted to try again. Continue entering all products until all have been input, and then tpye "done" or "DONE" and hit enter. After doing so, the app will return an itemized receipt along with a subtotal, tax, and total. Finally, the app will ask if the customer wants an email receipt. If so, the customer will be prompted to enter the email address they'd like the email receipt sent to. 
