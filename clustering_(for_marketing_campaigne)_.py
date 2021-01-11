# -*- coding: utf-8 -*-
"""Clustering (for marketing campaigne) .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cvRvLm_vgOyl8J9g7qYDhmL8crfP67-1

# INTRODUCTION

# Business Task:

How to **cluster** customer data for marketing campaign?

# Data Source:

https://www.kaggle.com/loveall/clicks-conversion-tracking

# Data Content:

The data used in this project is from an anonymous organisation’s social media ad campaign. The data file can be downloaded from here. The file conversion_data.csv contains 1143 observations in 11 variables. Below are the descriptions of the variables:

1.) ad_id: an unique ID for each ad.

2.) xyzcampaignid: an ID associated with each ad campaign of XYZ company.

3.) fbcampaignid: an ID associated with how Facebook tracks each campaign.

4.) age: age of the person to whom the ad is shown.

5.) gender: gender of the person to whim the add is shown

6.) interest: a code specifying the category to which the person’s interest belongs (interests are as mentioned in the person’s Facebook public profile).

7.) Impressions: the number of times the ad was shown.

8.) Clicks: number of clicks on for that ad.

9.) Spent: Amount paid by company xyz to Facebook, to show that ad.

10.) Total conversion: Total number of people who enquired about the product after seeing the ad.

11.) Approved conversion: Total number of people who bought the product after seeing the ad.

# Method of clustering:

K-MEANS ALGORITHM

# Method of finding optimal number of clusters:

ELBOW METHOD

# Method of dimensionality reduction:

1.) PCA - PRINCIPAL COMPONENT ANALYSIS
2.) AUTOENCODERS - ANN UNSUPERVISED TRAINING

# Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px

from google.colab import drive
drive.mount('/content/drive')

"""# DataSet"""

training_set = pd.read_csv('KAG_conversion_data.csv')

training_set.info()

training_set.head()

training_set.describe()

training_set.columns.unique()

"""# Exploring and Visualizing the DataSet"""

# Perfoming some of countplots
sns.countplot(x='age', data=training_set)

sns.countplot(x='xyz_campaign_id', data=training_set)

sns.countplot(x='gender', data=training_set)

# Showing the pairplot for data set
plt.figure(figsize = (10, 10))
sns.pairplot(training_set, hue='gender')

# Changing the labels of 'gender'
training_set['gender'].unique()

gender_labels = training_set['gender'].values

gender_labels[gender_labels == 'M'] = 1

gender_labels[gender_labels == 'F'] = 0

training_set['gender'].unique()

# Changing the labels of 'age'
training_set['age'].unique()

age_labels = training_set['age'].values

age_labels[age_labels == '30-34'] = 32

age_labels[age_labels == '35-39'] = 37

age_labels[age_labels == '40-44'] = 42

age_labels[age_labels == '45-49'] = 47

age_labels

# Converting into numeric dtype
training_set['age']= pd.to_numeric(training_set['age'])

training_set['gender']= pd.to_numeric(training_set['gender'])

training_set.info()

training_set.drop(['ad_id', 'xyz_campaign_id', 'fb_campaign_id'],axis=1,inplace=True)

training_set.head(3)

# Checking the NaN values
sns.heatmap(training_set.isnull(), yticklabels = False, cbar = False, cmap="Blues")

# Combining the matplotlib.hist function with seaborn kdeplot()
# KDE Plot represents the Kernel Density Estimate
# KDE is used for visualizing the Probability Density of a continuous variable. 
# KDE demonstrates the probability density at different values in a continuous variable.

plt.figure(figsize=(10,50))
for i in range(len(training_set.columns)):
  plt.subplot(17, 1, i+1)
  sns.distplot(training_set[training_set.columns[i]], kde_kws={"color": "b", "lw": 3, "label": "KDE"}, hist_kws={"color": "g"})
  plt.title(training_set.columns[i])

plt.tight_layout();

# Analyzing the correlation matrix
sns.set(style="white", font_scale=2)

corr = training_set.corr()

mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

f, ax = plt.subplots(figsize=(7, 7))
f.suptitle("Correlation Matrix", fontsize = 40)

cmap = sns.diverging_palette(220, 10, as_cmap=True)

sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .6})

"""# K-MEANS Clustering"""

# Scaling the data first
scaler = StandardScaler()
training_set_scaled = scaler.fit_transform(training_set)

training_set_scaled

# Finding of potential number of clusters
scores_1 = []

range_values = range(1, 20)

for i in range_values:
  kmeans = KMeans(n_clusters = i)
  kmeans.fit(training_set_scaled)
  scores_1.append(kmeans.inertia_) 

plt.plot(scores_1, 'bx-')
plt.title('Finding the right number of clusters')
plt.xlabel('Clusters')
plt.ylabel('Scores') 
plt.show()

# Applying K-Means algorithm
kmeans = KMeans(5)
kmeans.fit(training_set_scaled)
labels = kmeans.labels_

cluster_centers = pd.DataFrame(data = kmeans.cluster_centers_, columns = [training_set.columns])
cluster_centers

cluster_centers = scaler.inverse_transform(cluster_centers)
cluster_centers = pd.DataFrame(data = cluster_centers, columns = [training_set.columns])
cluster_centers

y_kmeans = kmeans.fit_predict(training_set_scaled)
y_kmeans

training_set_cluster = pd.concat([training_set, pd.DataFrame({'cluster':labels})], axis = 1)
training_set_cluster.head() # we can save this output

# Plot the histogram of various clusters
for i in training_set.columns:
  plt.figure(figsize = (25, 5))
  for j in range(5):
    plt.subplot(1,5,j+1)
    cluster = training_set_cluster[training_set_cluster['cluster'] == j]
    cluster[i].hist(bins = 20)
    plt.title('{}    \nCluster {} '.format(i,j))
  
  plt.show()

"""# Optimization of the solution (by using PCA)"""

# Applying PCA (PRINCIPAL COMPONETNT ANALYSIS) - an unsupervised ML algorithm performs dimensionality reductions of the uncorrelated features

# Obtaining the principal components 
pca = PCA(n_components=2)
principal_comp = pca.fit_transform(training_set_scaled)
principal_comp

# Creating a dataframe with the two components
pca_df = pd.DataFrame(data = principal_comp, columns =['pca1','pca2'])
pca_df.head()

# Concatenating the clusters labels to the dataframe
pca_df = pd.concat([pca_df,pd.DataFrame({'cluster':labels})], axis = 1)
pca_df.head()

# Ploting the result

plt.figure(figsize=(10,5))
ax = sns.scatterplot(x="pca1", y="pca2", hue = "cluster", data = pca_df, palette =['red','green','blue','black','pink'])
plt.show()

"""# Optimization of the solution (by using AUTOENCODERS - ANN)"""

# Applying AUTOENCODERS and performing dimensionality reduction

from tensorflow.keras.layers import Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, Dropout
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.initializers import glorot_uniform
from keras.optimizers import SGD

encoding_dim = 7

input_df = Input(shape=(8,)) # number of features


# Glorot normal initializer (Xavier normal initializer) draws samples from a truncated normal distribution 

x = Dense(encoding_dim, activation='relu')(input_df)
x = Dense(500, activation='relu', kernel_initializer = 'glorot_uniform')(x)
x = Dense(500, activation='relu', kernel_initializer = 'glorot_uniform')(x)
x = Dense(2000, activation='relu', kernel_initializer = 'glorot_uniform')(x)

encoded = Dense(5, activation='relu', kernel_initializer = 'glorot_uniform')(x)  # number to reduction

x = Dense(2000, activation='relu', kernel_initializer = 'glorot_uniform')(encoded)
x = Dense(500, activation='relu', kernel_initializer = 'glorot_uniform')(x)

decoded = Dense(8, kernel_initializer = 'glorot_uniform')(x) # number of features

# autoencoder
autoencoder = Model(input_df, decoded)

#encoder - used for our dimention reduction
encoder = Model(input_df, encoded)

autoencoder.compile(optimizer= 'adam', loss='mean_squared_error')

autoencoder.fit(training_set_scaled, training_set_scaled, batch_size = 128, epochs = 25,  verbose = 1)

autoencoder.save_weights('autoencoder_v3.h5')

# Taking the autoencoder
pred = encoder.predict(training_set_scaled)
pred.shape

scores_2 = []

range_values = range(1, 20)

for i in range_values:
  kmeans = KMeans(n_clusters= i)
  kmeans.fit(pred)
  scores_2.append(kmeans.inertia_)

plt.plot(scores_2, 'bx-')
plt.title('Finding right number of clusters')
plt.xlabel('Clusters')
plt.ylabel('Scores') 
plt.show()

plt.plot(scores_1, 'bx-', color = 'r', label='scores_1')
plt.plot(scores_2, 'bx-', color = 'g', label='scores_2')

plt.title('Comparision of two methods of finding the right number of clusters')
plt.xlabel('Clusters')
plt.ylabel('Scores')
plt.legend()
plt.show()

# Applying K-Means after dimensionality reduction
kmeans = KMeans(3)
kmeans.fit(pred)
labels = kmeans.labels_
y_kmeans = kmeans.fit_predict(training_set_scaled)

training_set_cluster_2 = pd.concat([training_set, pd.DataFrame({'cluster':labels})], axis = 1)
training_set_cluster_2.head() # we can save this output

# Plot the histogram of various clusters
for i in training_set.columns:
  plt.figure(figsize = (35, 5))
  for j in range(3):
    plt.subplot(1,3,j+1)
    cluster = training_set_cluster_2[training_set_cluster_2['cluster'] == j]
    cluster[i].hist(bins = 20)
    plt.title('{}    \nCluster {} '.format(i,j))
  
  plt.show()

# using again PCA to reduce the 'pred' data to 3 dimensions for visualizig the clusters
pca = PCA(n_components = 3)
principal_comp = pca.fit_transform(pred)
principal_comp

pca_df = pd.DataFrame(data = principal_comp, columns = ['pca1', 'pca2', 'pca3'])
pca_df.head()

# Concatenate the clusters labels to the dataframe
pca_df = pd.concat([pca_df, pd.DataFrame({'cluster':labels})], axis = 1)
pca_df.head(3)

# Visualize clusters using 3D-Scatterplot

fig = px.scatter_3d(pca_df, x = 'pca1', y = 'pca2', z = 'pca3',
              color='cluster', symbol = 'cluster', size_max = 10, opacity = 0.7)
fig.update_layout(margin = dict(l = 0, r = 0, b = 0, t = 0))

"""# Done!"""