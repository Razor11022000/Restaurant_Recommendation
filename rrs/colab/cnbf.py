from rrs.colab.utils import prettyPrint as pp
import pandas as pd

################ Content Based Filtering: Code Starts here #################


def knnClassifer(df_final):
    # Create X (all the features) and y (target)
    X = df_final.iloc[:, :-2]
    y = df_final['stars']
    # print(X.shape)
    # print(y.shape)

    # Split the data into train and test sets
    from sklearn.model_selection import train_test_split
    X_train_knn, X_test_knn, y_train_knn, y_test_knn = train_test_split(
        X, y, test_size=0.2, random_state=1)

    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score

    knn = KNeighborsClassifier(n_neighbors=20)
    knn.fit(X_train_knn, y_train_knn)

    #y_pred = knn.predict(X_test)
    accuracy_train = knn.score(X_train_knn, y_train_knn)
    accuracy_test = knn.score(X_test_knn, y_test_knn)

    print(f"Score on training set: {accuracy_train}")
    print(f"Score on test set: {accuracy_test}")
    return knn


def validateRes(res, df_final):

    validate_res = df_final[df_final["name"] == res]
    if len(validate_res) == 0:
        print("Enter valid res name")
        return
    else:
        return validate_res


#################### 1) Content Based Filtering - Model ####################

def content_based_filtering(df_final):

    ########### KNN Classifier ###########
    knn = knnClassifer(df_final)

    ########### Enter restaurant name here ############
    res_name = "Adelita Taqueria & Restaurant"

    test_set = validateRes(res_name, df_final).iloc[:, :-2]
    # print(test_set.shape)
    test_sample = df_final
    # print(test_sample.shape)
    test_sample = test_sample.drop(test_sample.index[test_set.index])
    # print(test_sample.shape)

    y_val = test_sample['stars']
    # print(y_val.shape)

    X_val = test_sample.iloc[:, :-2]
    # print(X_val.shape)

    print(test_set.shape)
    # print(X_val.shape)
    # print(y_val.shape)

    # fit model with validation set
    n_knn = knn.fit(X_val, y_val)

    # distances and indeces from validation set
    n_knn.kneighbors(test_set)
    # n_knn.kneighbors(test_set)[1][0]

    # create table distances and indeces from validattion restaurant
    final_table = pd.DataFrame(n_knn.kneighbors(test_set)[
                               0][0], columns=['distance'])
    final_table['index'] = n_knn.kneighbors(test_set)[1][0]
    final_table.set_index('index')

    # get names of the restaurant that similar to the validattion restaurant
    result = final_table.join(df_final, on='index')
    pp("Top restaurants based on KNN")
    print(result[['distance', 'index', 'name', 'stars']].head(5))

    return result[['distance', 'index', 'name', 'stars']].head(5)
