# La Guajira Salinity prediction

## Brief description
This repo is based in the Colombian open data about Hydrogeology and Salinity in La Guajira. Hoping this can help to our proud La Guajira communities to plan its water needs. The scope of this project is to predict the salinity of the underground water in the region, using the hydrogeology map and the salinity data. La Guajira is a desertic region in the north of Colombia. The water in the region is scarce and the salinity is high, making it difficult for the communities to have access to clean water. Many water in the region is supplied by underground wells that are drill by the communities or public entities. Is a key point to have an idea about the salinity of the underground water before to drill the well. This project try to aim this scope by a machine learning model that takes X, Y coordinates and estimate the water salinity in three categories "LOW SALINITY", "MEDIUM SALINITY" and "HIGH SALINITY". The data is from the Colombian government and is open to the public.

Data should be found in:

<ul>
  <li><a href="https://www.datos.gov.co/dataset/Salinidad-Guajira/fwz7-px8j/about_data">Salinity</a></li>
  <li><a href="https://datos-sgcolombiano.opendata.arcgis.com/maps/ecda31174a204641a96d57cb4b379d0a/about">La Guajira Hydrogeologic map</a></li>
</ul>

## About the analytical models
We will use the hydrogeology map as a source of features for the model, and the salinity data as the target variable. The model will be trained with the salinity data and the features extracted from the hydrogeology map. The model will be evaluated with a test set of salinity data that was not used in the training process. The model will be able to predict the salinity of the underground water in the region, given the X, Y coordinates. We will train the following models:
<ul>
  <li>Support Vector Machine</li>
  <li>Decision Tree</li>
  <li>Boosting</li>
  <li>Voting</li>
  <li>Bagging</li>
  <li>KNN</li>
  <li>Logistic Regression</li>
  <li>Neural Network</li>
</ul>
This development will be placed in a streamlit app that will allow the users to input the X, Y in a follium map and get the salinity prediction in the region. The app will display the model metrics and the data profiling.

## Setup
To perform this development we use python 3.10 an the libraries in //quirements.txt.
Using anaconda the setup is as follows:

`conda create -n guajira python==3.10`

`conda activate guajira`

`pip install -r requirements.txt`