LogisticRegression =  + {'solver': 'saga', 'C': 1, 'l1_ratio': 0.4, 'max_iter': 100, 'penalty': 'elasticnet'}
KNN =  + {'n_neighbors': 11, 'p': 1, 'weights': 'distance'}
SVM =  + {'probability': True, 'C': 10, 'gamma': 'scale', 'kernel': 'rbf'}
DecisionTree =  + {'random_state': 42, 'criterion': 'gini', 'max_depth': None, 'max_features': None, 'min_samples_leaf': 3, 'min_samples_split': 9}
XGBoost =  + {'use_label_encoder': False, 'eval_metric': 'mlogloss', 'random_state': 42, 'verbosity': 0, 'device': 'cpu', 'tree_method': 'hist', 'colsample_bytree': 1.0, 'gamma': 0, 'learning_rate': 0.05, 'max_depth': 6, 'n_estimators': 400, 'reg_alpha': 0, 'reg_lambda': 1, 'subsample': 0.6}
RandomFores =  + {'random_state': 42, 'bootstrap': False, 'criterion': 'gini', 'max_depth': None, 'max_features': 'sqrt', 'min_samples_leaf': 4, 'min_samples_split': 10, 'n_estimators': 300}
NeuralNetwork =  + {'random_state': 42, 'activation': 'relu', 'alpha': 0.0001, 'hidden_layer_sizes': (10,), 'learning_rate_init': 0.01, 'max_iter': 500, 'solver': 'adam'}