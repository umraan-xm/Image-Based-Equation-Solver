# Image-Based-Equation-Solver
A PyQt5 desktop application that solves the equation contained in an image.

## Environment
Install and activate the environment using conda

`conda env create -f environment.yaml`

`conda activate tf`

## Data

The symbol recognition model is trained using the Kaggle handwritten symbol dataset https://www.kaggle.com/datasets/xainano/handwrittenmathsymbols.

Add a folder called "Data" in the base directory. Inside this folder add '+', '-', 'times', '=', 'X', 'Y' and 0-9 folders. Make sure that each symbol folder contains exactly 6000 images. You may need to use `expand.py` to augment certain datasets.

Run `solver_data.py` to create the training dataset.

## Training

Run `solver_training.py` to train the model.

## Start

Start the application.

 `python main.py`
 
 ## Screenshots
 
![image](https://user-images.githubusercontent.com/120903301/227707803-eeb60dc6-2264-4f8e-8c2a-970e7ef167ac.png)

![image](https://user-images.githubusercontent.com/120903301/227707902-e83c049c-016f-4ed3-a8e6-e2291450a0e6.png)

![image](https://user-images.githubusercontent.com/120903301/227708088-c8d769c4-8d9c-4d42-8779-d7d4d760af93.png)

![image](https://user-images.githubusercontent.com/120903301/227708253-e70ba2a2-9b0b-491d-a25e-a2f3bf2a1dd7.png)

![image](https://user-images.githubusercontent.com/120903301/227708340-9dc04635-438b-455f-a993-448ff656f93c.png)

![image](https://user-images.githubusercontent.com/120903301/227708390-7460b663-4a72-42a9-a47f-3fe75de468ac.png)

### History Database
![image](https://user-images.githubusercontent.com/120903301/227708468-e104823d-64c0-4907-b85a-5b5799207060.png)
