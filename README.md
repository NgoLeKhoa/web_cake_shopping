In order to run this app, you'll need two programs installed on your computer: [1] pip and [2] virtualenv.

1. pip
  To install pip, go to https://pip.pypa.io/en/latest/installing.html and follow the instructions for your operating system.

2. virtualenv

  To install virtualenv, go to the command line and type:

    pip install virtualenv


Running the app

1. Open the command line and navigate to the folder where the app's code lives.

2. Create a new virtual environment
  From the command line, create a new isolated Python development environment by typing

    virtualenv venv

3. Enter the isolated dev environment by typing on bash shell

  source venv/bin/activate

4. Install the app's dependencies

  Provided is a list of these dependencies as a file called requirements.txt.

    pip install -r requirements.txt

  This command will install the all app's dependencies.

5. Create the app's database

  Direct to webapp/library

  Unlock the line "Base.metadata.create_all(engine)" on models.py

  Type this command to run the script models.py which will create the app's database:

    python models.py

  Transfer data for the first-time run by type the script:

    python transfer_data.py

7. Run the app
  Redirect to root folder. From the command line, type

    python runserver.py

  And visit http://localhost:5000/ in a browser to see the app.

