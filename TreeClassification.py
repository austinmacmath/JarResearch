#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 14:30:29 2019

@author: austinmac
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score

#X_train, X_test, y_train, y_test = train_test_split(train, target, train_size = (n - 1)/n)
#sets up random forest
clf = RandomForestClassifier(n_estimators = 10, max_depth = 4)
clf.fit(train, target)
#clf = SVC()
print("\n")
print"Forest:", cross_val_score(clf, train, target, cv = 5)
print("\n")

final_pred = clf.predict(clean)
final_pred = pd.DataFrame(data = {"Prediction": final_pred[0:]})

print"Score:", accuracy_score(original_clean["Vessel"], final_pred)

clean2 = pd.read_csv("clean.csv")
clean2 = clean2[["Form", "Group",]]
compare = pd.concat([clean2, final_pred], axis = 1)

