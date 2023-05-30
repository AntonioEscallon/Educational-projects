import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, classification_report
from matplotlib import pyplot as plt
from sklearn import tree
import dtreeviz


data2 = load_breast_cancer()
#print(data2)
data = pd.read_csv('/Users/antonioescallon23/Documents/GitHub/Educational-projects/data/windSpeedFile44082012.csv')
#data = data.drop(['Bouy Wind Speed','u','v','Hour Volatility:','End-behavior:','End-behavior power:','Correlation WSPD-PWR:'], axis=1)
print(data)
import time

t0 = time.time()


#print(data)
#print(data.columns)

#data[['"Bouy Wind Speed', 'u','v','new_wspd','PWR','target','Hour Volatility:','End-behavior:','End-behavior power:', 'Correlation WSPD-PWR:"']].replace(' ', ',', inplace=True)

#data['"Bouy Wind Speed'] = data['"Bouy Wind Speed'].str[1:]
#data['Correlation WSPD-PWR:"'] = data['Correlation WSPD-PWR:"'].str[:1]
#print(data)

#data[['"Bouy Wind Speed','u','v','new_wspd','PWR','target','Hour Volatility:','End-behavior:','End-behavior power:', 'Correlation WSPD-PWR:"']].astype(float)

#data.to_csv('thesisPWR.csv', sep='\t')

#print(data)
dataset2 = pd.DataFrame(data = data2['data'], columns= data2['feature_names'])
#print(dataset2)7
data_temp = data.drop(['target', 'Date', 'GTIME'], axis=1)
print(data_temp)
dataset = pd.DataFrame(data =  data_temp)


#All features to determine HSSD
x = dataset.copy()
#Target value 
y = data['target']

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.33)

clf = DecisionTreeClassifier()

clf = clf.fit(X_train, y_train)

predicitons = clf.predict(X_test)

prob_predictions = clf.predict_proba(X_test)
print(prob_predictions)

#Stopping the tree all the way before the leaves can be pure when we use max depth

accuracy = accuracy_score(y_test, predicitons)
precision = precision_score(y_test, predicitons)

print("Precision:", round(precision, 2))
print("Accuracy: ", round(accuracy,2))

report = classification_report(y_test, predicitons, target_names=['NOHSSD', 'HSSD'])

print(report)
feature_names= x.columns

fig = plt.figure(figsize=(100,100))
_ = tree.plot_tree(clf, feature_names = feature_names, class_names={0:'NOHSSD', 1:'HSSD'}, filled=True, fontsize=12)
plt.savefig("decisionTree.png")

viz_model = dtreeviz.model(clf,
                           X_train=x, y_train=y,
                           feature_names=feature_names,
                           target_name='',
                           class_names=['NOHSSD', 'HSSD'])

v = viz_model.view()     # render as SVG into internal object 
v.show()                 # pop up window
t1 = time.time()

total = t1-t0
print(total)
#v.save("/Users/antonioescallon23/Documents/GitHub/Educational-projects/data/decisionTreeVisualization.svg")  # optionally save as svg
