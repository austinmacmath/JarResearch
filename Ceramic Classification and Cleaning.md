
![MARC](MARC_LOGO_BEST.png "MARC")
# Ceramic Classification & Data Cleaning

**Austin Mac**  
**June 20, 2019**

## Introduction

El Pilar, a Maya city first discovered by Archeologist Dr. Anabel Ford in 1983, is the site of thousands of ceramic fragments which were collected, measured, and subsequently recorded in a database for further analysis. These data have persisted relatively untouched since collection, and remain to be extrapolated in order to expand our knowledge of ancient Maya culture. Typically, ceramic data have not been analyzed to their fullest extent. We would like to take advantage of this new information. 

## Goal

The goal of this project was to classify ceramics into one of four vessel types: jars, bowls, plates, or vases. 

## Process

Initially, this process seemed straightforward. In the CSV file containing data for thousands of ceramic fragments, the attributes *Form* and *Group* helped easily categorize ceramics into a distinct vessel type. Numeric values (e.g. 71) under the *Form* column dictated where a ceramic should be classfied. A corresponding code (e.g. BG1) under the *Group* column confirmed the classification. 

**Ex:** Ceramic 5812 has a *Form* number of 71, indicating that this ceramic is a "Bowl, unspecified" and a *Group* code of BG1 indicating that it should be categorized under "Bowl Group 1". Seeing as both the *Form* number and the *Group* code are in agreement with each other, it is evident that Ceramic 5812 is a Bowl.  

However, there were inconsistencies between *Form* number and *Group* code for approximately 10% of the dataset. This was an issue because classification depended on two attributes which conflicted with each other. Instead of utilizing *Form* and *Group* to classify the ceramics, the variables: *SITE*, *Shape*, *RimDiameter*, *Pocking*, *HCL*, and *WallThick* were used.

With the help of a Random Forest Classfier (RFC), the above six variables were used to categorize the inconsistent ceramics. First the RFC had to be fit. This meant running a properly classified dataset through the RFC to train it to detect patterns in the data. Then, given certain variables, this learned pattern detection could be applied to classify previously unseen ceramics. But before fitting the RFC, data cleaning was in order. Starting with the *SITE* column from the properly classified data, rows which did not have a valid *SITE* value were eliminated.

```python
ceramics = ceramics.dropna(subset = ["SITE"])
```

Since *SITE* is a discrete value, it cannot be approximated with a mean or a median. Thus, the choice was made to eliminate rows with null values under *SITE*. When dealing with the relatively continuous variables *RimDiameter*, *Pocking*, *HCL*, and *WallThick* from the properly classified data, the invalid values of each column were filled with their respective median. This was done to retain as large a sample as possible while maintaining a robust center.

```python
ceramics2["RimDiameter"] = ceramics2["RimDiameter"].fillna(ceramics2["RimDiameter"]
.median(skipna = True))

ceramics2["Pocking"] = ceramics2["Pocking"].fillna(ceramics2["Pocking"]
.median(skipna = True))

ceramics2["HCL"] = ceramics2["HCL"].fillna(ceramics2["HCL"]
.median(skipna = True))

ceramics2["WallThick"] = ceramics2["WallThick"].fillna(ceramics2["WallThick"]
.median(skipna = True))
```

After cleaning the data, the RFC was ready for fitting. A training and target set from the cleaned data were created in order to fit the RFC. 

```python
train = ceramics2[["SITE", "Shape", "RimDiameter", "Pocking", "HCL", "WallThick"]]
target = ceramics2["Vessel"]
```

The purpose of the training set and the target set is to fit the RFC. More elaborately, the training and target set are fed into the RFC, and an algorithm is created which creates a map from the training set to the target set. Then, this algorithm is applied to a new testing set, where a chosen variable is predicted. 

In this particular case, the RFC creates an algorithm which maps us from the variables *SITE*, *Shape*, *RimDiameter*, *Pocking*, *HCL*, and *WallThick* to *Vessel*. Then, we can apply this algorithm to predict the *Vessel* type of a new ceramic given the variables *SITE*, *Shape*, *RimDiameter*, *Pocking*, *HCL*, and *WallThick*. 

After defining some parameters in the RFC, the fitting process is completed with the "fit" method below. 

```python
RandomForestClassifier(n_estimators = 10, max_depth = 4)
fit(train, target)
```

After fitting the RFC, the algorithm can now be used to predict the vessel type of a specific, unknown ceramic. We can then feed the "predict" method with a new set of variables *SITE*, *Shape*, *RimDiameter*, *Pocking*, *HCL*, and *WallThick* which are all contained in the "clean" set.

```python
clean = clean[["SITE", "Shape", "RimDiameter", "Pocking", "HCL", "WallThick"]]
predict(clean)
```

The "predict" method returns the *Vessel* type of the ceramic, which is either: "Bowls", "Jars", "Plates", or "Vases". 

## Results

The RFC predicted that the inconsistent ceramics should be classified in a manner which agrees with their *Group* code. Below is a sample (n = 11) of the predictions juxtaposed with the corresponding ceramics. The leftmost column, *Index*, contains a unique value for the index of a particular ceramic in our particular CSV. The next column, *Form*, contains the form number for a ceramic. The *Group* column contains a value which represents the ceramic type and group number of a ceramic. The rightmost column *Prediction* contains the values which have been predicted by the Random Forest. 

**Ex:** The ceramic with *Index* 0 has *Form* 1, indicating that it is a Vase. However, its *Group* is JG1, indicating that it has been sorted into Jar Group 1. This contradicts the previous statement since a ceramic cannot be a Jar and a Vase. The value under the *Prediction* column is "Jars", reflecting how the RFC predicted that this particular ceramic should be classified as a Jar. Since the value under the *Prediction* column is consistent with the value under the *Group* column, we can take *Group* to be the accurate attribute to classify ceramics. 

| Index | Form | Group | Prediction | 
|-------|------|-------|------------| 
| 0     | 1    | JG1   | Jars       | 
| 50    | 22   | PG2   | Plates     | 
| 57    | 31   | BG2   | Bowls      | 
| 67    | 33   | VG1   | Vases      | 
| 191   | 71   | PG1   | Plates     | 
| 221   | 72   | BG2   | Bowls      | 
| 278   | 72   | JG1   | Jars       | 
| 279   | 72   | BG2   | Bowls      | 
| 429   | 78   | JG1   | Vases      | 
| 430   | 78   | JG1   | Jars       | 
| 431   | 78   | PG1   | Plates     | 

<sub>
**Note:** The columns for *SITE*, *Shape*, *RimDiameter*, *Pocking*, *HCL*, and *WallThick* have been omitted from the presentation for the sake of clarity. This omission from the table below does not affect the results in any way.
</sub>

When each and every *Prediction* value was compared against its corresponding *Group* code, the score was calculated to be approximately 0.97. This means that in 97% of the dataset of inconsistent ceramics, the value predicted by the RFC agreed with its corresponding *Group* code. Thus, we can conclude that **_Group_ code is the correct indicator of vessel type, not _Form_ number**. All that remains to do is to correct the original dataset and update the Access database in MARC.

## Further Research

Utilizing different machine learning techniques, such as a support vector machine could've assisted in the sorting process. Although the high score of the RFC and its tendency not to overfit made this classifier ideal for this project. Next steps include approximating missing data in other columns of the dataset using machine learning, creating interactive datamaps of various distributions, and illuminating the history of El Pilar. 

