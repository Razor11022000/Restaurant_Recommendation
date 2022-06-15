import pickle
from rrs.utils import prettyPrint
import pandas as pd
import numpy as np
from rrs.recommedation_pojo import Recommedation
from rrs.utils import Text_process


class TF_IDF:
    path_for_philadelphia_pkl = "rrs/model/tf_idf_model_on_philadephia_data.pkl"
    path_for_neworleans_pkl = "rrs/model/tf_idf_model_on_neworleans_data.pkl"
    path_for_nashville_pkl = "rrs/model/tf_idf_model_on_nashville_data.pkl"

    def __init__(self, city):
        prettyPrint("TF_IDF")
        self.city = city
        # city based dataset switch
        if city == "Philadelphia":
            loaded_model = open(self.path_for_philadelphia_pkl, 'rb')
            business_dataset_path = "rrs/dataset/philadephia_sub.csv"
        elif city == "New Orleans":
            loaded_model = open(self.path_for_neworleans_pkl, 'rb')
            business_dataset_path = "rrs/dataset/NewOrleans_sub.csv"
        elif city == "Nashville":
            loaded_model = open(self.path_for_nashville_pkl, 'rb')
            business_dataset_path = "rrs/dataset/Nashville_sub.csv"

        prettyPrint("tf_idf_model_on_philadephia_data.pkl file loaded")

        self.P = pickle.load(loaded_model)
        self.Q = pickle.load(loaded_model)
        self.userid_vectorizer = pickle.load(loaded_model)

        prettyPrint("tf_idf_model_on_philadephia_data.pkl params loaded")

        self.df_business = pd.read_csv(business_dataset_path)
        prettyPrint("dataset loaded")

        loaded_model.close()

    def produce_recommendations(self, sentence, n):
        words = sentence

        tp = Text_process()
        test_df = pd.DataFrame([words], columns=['text'])
        test_df['text'] = test_df['text'].apply(tp.text_process)
        test_vectors = self.userid_vectorizer.transform(test_df['text'])
        test_v_df = pd.DataFrame(test_vectors.toarray(
        ), index=test_df.index, columns=self.userid_vectorizer.get_feature_names())

        predictItemRating = pd.DataFrame(
            np.dot(test_v_df.loc[0], self.Q.T), index=self.Q.index, columns=['Rating'])
        topRecommendations = pd.DataFrame.sort_values(
            predictItemRating, ['Rating'], ascending=[0])[:n]

        topNRecommendations = []

        for i in topRecommendations.index:
            name = self.df_business[self.df_business['business_id']
                                    == i]['name'].iloc[0]
            cat = str(
                self.df_business[self.df_business['business_id'] == i]['categories'].iloc[0])

            stars = str(
                self.df_business[self.df_business['business_id'] == i]['stars'].iloc[0])

            rcount = str(
                self.df_business[self.df_business['business_id'] == i]['review_count'].iloc[0])

            topNRecommendations.append(Recommedation(
                name, cat, stars, rcount, self.city))
            print(
                self.df_business[self.df_business['business_id'] == i]['name'].iloc[0])
            print(self.df_business[self.df_business['business_id'] == i]
                  ['categories'].iloc[0])
            print(str(self.df_business[self.df_business['business_id'] == i]['stars'].iloc[0]) + ' '+str(
                self.df_business[self.df_business['business_id'] == i]['review_count'].iloc[0]))
            print('')

        return topNRecommendations
