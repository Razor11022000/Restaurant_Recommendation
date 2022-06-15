from pprint import pp
import pandas as pd
from rrs.recommender import Recommender


class Restaurant_Recommender:
    def __init__(self, city):
        if city == "New Orleans":
            review_dataset_path = "rrs/dataset/NewOrleans_reviews_sub.csv"
            business_dataset_path = "rrs/dataset/NewOrleans_sub.csv"
        elif city == "Philadelphia":
            review_dataset_path = "rrs/dataset/philadephia_reviews_sub.csv"
            business_dataset_path = "rrs/dataset/philadephia_sub.csv"
        elif city == "Nashville":
            review_dataset_path = "rrs/dataset/Nashville_reviews_sub.csv"
            business_dataset_path = "rrs/dataset/Nashville_sub.csv"

    # review_dataset_path = "rrs/dataset/philadephia_reviews_sub.csv"
    # business_dataset_path = "rrs/dataset/philadephia_sub.csv"
        self.toronto_reviews_sub = pd.read_csv(review_dataset_path)
        self.df_businesses_toronto = pd.read_csv(business_dataset_path)

    def train_test_split(self):
        # Split train and test
        self.toronto_reviews_train = self.toronto_reviews_sub[self.toronto_reviews_sub.year < 2019]
        self.toronto_reviews_test = self.toronto_reviews_sub[self.toronto_reviews_sub.year == 2019]
        print('Before, # reviews: ', len(self.toronto_reviews_train))
        self.toronto_reviews_train = self.toronto_reviews_train[~self.toronto_reviews_train.duplicated(
            subset=['user_id', 'business_id'], keep='last')]
        print('After,  # reviews: ', len(self.toronto_reviews_train))

    def get_recommendations(self, rest_name):
        # Initialise and fit the recommender class
        rec = Recommender()
        # Create the user-rx matrix
        rec.set_user_item_matrix(self.toronto_reviews_train,
                                 'user_id', 'business_id', 'stars')

        # Fit the FunkSVD - this will create a warning about contiguous arrays which can be ignored

        try:
            rec.fit(latent_features=10, learning_rate=0.005,
                    iters=25, print_every=5)
        except:
            rec.fit(latent_features=10, learning_rate=0.005,
                    iters=25, print_every=5)

        # rest_id = self.df_businesses_toronto[
        #     self.df_businesses_toronto['name'] == rest_name]

        rest_id = self.df_businesses_toronto.loc[self.df_businesses_toronto['name']
                                                 == rest_name, 'business_id']
        print("@@@@@@@@@@@")
        print(rest_id.iloc[0])
        print(type(rest_id.iloc[0]))

        # out = rec.get_similar_items('U0md3UhNA2123G-vYR9hWQ', 20)
        out = rec.get_similar_items(rest_id.iloc[0], 5)

        recoms = rec.get_item_names(self.df_businesses_toronto, out, 'name', [
                                    'similarity', 'latitude', 'longitude', 'review_count'])
        map = rec.plot_locations(
            recoms, 'name', 'latitude', 'longitude', info=None, search_string='toronto')

        # save the map
        import os

        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        CWD = "C:/Users/Midhun/Desktop/FYP/Restuarant_Recommendation/rrs/templates/rrs/"
        print("######################")
        path = os.path.join(CWD, "map.html")
        print(path)
        map.save(path)
