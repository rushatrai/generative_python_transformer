# Generative Python Transformer

A machine learning project that aims to test the extent to which [GPT-2](https://github.com/openai/gpt-2) is able to understand Python syntax.

[Live demo](https://huggingface.co/spaces/equ1/generative_python_transformer) available.

# Model

The model used is a GPT-2 large which has been trained on around 40 MBs worth of Python code scraped from Github for approximately 16 GPU hours on 4x Nvidia GTX 1080Tis. Results show that the model is able to successfully learn Python syntax, and given more training time, computation resources and data, should be able to provide accurate code autocompletion.

# Colab Notebook
A notebook tutorial that goes over the finer details of this project can be found [here](https://colab.research.google.com/drive/1hlkhrvdhdnTodMrPcMZLdC2CEqelZDMZ?usp=sharing).

# License
MIT
