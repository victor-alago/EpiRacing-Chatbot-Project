
# EpiRacing Chatbot Deployment with Flask and PyTorch

Welcome to my EpiRacing Chatbot project! EpiRacing is an innovative students club in EPITA Paris. This application is designed to interact with users interested in racing and motorsport events, providing information on events, club benefits, and much more.

It is my hope that some day in the future the EpiRacing club at EPITA will become part of the EPITA Students Associations.


## Prerequisites:
Before you begin, ensure you have the following installed on your system:
- Python 3.8 or higher
- pip (Python package installer)



## Initial Setup:

### 1. Clone the Repository
Start by cloning the repository to your local machine. You can also download the project zip.

### 2. Create a Virtual Environment
I recommend that you use a virtual environment to avoid conflicts with other Python projects:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
Install all the necessary dependencies:
```bash
pip install Flask torch torchvision nltk openai flask-login python-dotenv
```

### 4. Install NLTK Packages
You need to download the `punkt` tokenizer models for the Natural Language Toolkit (NLTK) library, which are essential for the chatbot’s text processing:
```bash
python -m nltk.downloader punkt
```

## Running the Application

### Train the Model
Before starting the Flask app, you need to train the neural network model:
```bash
python train.py
```
This will create a `data.pth` file that contains the trained model.

### Start the Flask Application
Finally, run the Flask application:
```bash
python app.py
```
This will start the server, and you can interact with the chatbot by navigating to `http://127.0.0.1:5000/` in your web browser.
`Remember that you will need to create a .env file before running the app. I attached an example`

## Additional Information
For more detailed information on the project architecture and customization, refer to the project documentation in the `Docs` directory.

## Contributing
It is my hope that some day in the future the EpiRacing club at EPITA will become real. I started this project on my own but your contributions to the EpiRacing project are welcome. 

Together, we can achieve something truly special here!!!

