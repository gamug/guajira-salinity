LogisticRegression = {'solver': 'saga', 'C': 0.8, 'l1_ratio': 0, 'max_iter': 400, 'penalty': 'l1'}
KNN = {'n_neighbors': 6, 'p': 1, 'weights': 'distance'}
SVM = {'probability': True, 'C': 10, 'gamma': 'scale', 'kernel': 'rbf'}
DecisionTree = {'random_state': 42, 'criterion': 'entropy', 'max_depth': None, 'max_features': None, 'min_samples_leaf': 4, 'min_samples_split': 2}
XGBoost = {'use_label_encoder': False, 'eval_metric': 'mlogloss', 'random_state': 42, 'verbosity': 0, 'device': 'cpu', 'tree_method': 'hist', 'colsample_bytree': 1.0, 'gamma': 0, 'learning_rate': 0.01, 'max_depth': 6, 'n_estimators': 200, 'reg_alpha': 0.5, 'reg_lambda': 0, 'subsample': 0.8}
RandomFores = {'random_state': 42, 'bootstrap': True, 'criterion': 'entropy', 'max_depth': None, 'max_features': 'sqrt', 'min_samples_leaf': 2, 'min_samples_split': 2, 'n_estimators': 100}
NeuralNetwork = {'random_state': 42, 'activation': 'relu', 'alpha': 0.001, 'hidden_layer_sizes': 10, 'learning_rate_init': 0.01, 'max_iter': 1000, 'solver': 'adam'}