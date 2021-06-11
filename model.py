from sklearn import svm
import joblib
import numpy as np

# customer ages
X_train = np.array([50, 17, 35, 23, 28, 40, 31, 29, 19, 62])
X_train = X_train.reshape(-1, 1)
# churn y/n
y_train = ["yes", "no", "no", "no", "yes", "yes", "yes", "no", "no", "yes"]

clf = svm.SVC(gamma=0.001, C=100.)
clf.fit(X_train, y_train)

joblib.dump(value=clf, filename="churn-model.pkl")
