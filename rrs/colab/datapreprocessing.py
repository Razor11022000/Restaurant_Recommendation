from rrs.colab.ml3 import extract_keys, str_to_dict
import pandas as pd
from rrs.colab.utils import prettyPrint as pp


def data_preprocessing(df_business):
    cityName = "Philadelphia"
    # Select only businesses in Philadelphia and currently open
    city = df_business[(df_business['city'] == cityName) & (
        df_business['is_open'] == 1)]
    philadelphia = city[['business_id', 'name',
                         'address', 'categories', 'attributes', 'stars']]
    # print(city.shape)
    # print(philadelphia.shape)

    # getting just restaurants from Philadelphia business
    rest = philadelphia[philadelphia['categories'].str.contains(
        'Restaurant.*') == True].reset_index()
    # printShapeAndHeadDf(rest)

    # get dummies from nested attributes
    # list(rest['attributes'])
    rest['BusinessParking'] = rest.apply(lambda x: str_to_dict(
        extract_keys(x['attributes'], 'BusinessParking')), axis=1)
    rest['Ambience'] = rest.apply(lambda x: str_to_dict(
        extract_keys(x['attributes'], 'Ambience')), axis=1)
    rest['GoodForMeal'] = rest.apply(lambda x: str_to_dict(
        extract_keys(x['attributes'], 'GoodForMeal')), axis=1)
    rest['Dietary'] = rest.apply(lambda x: str_to_dict(
        extract_keys(x['attributes'], 'Dietary')), axis=1)
    rest['Music'] = rest.apply(lambda x: str_to_dict(
        extract_keys(x['attributes'], 'Music')), axis=1)

    print(rest.shape)
    rest.head()

    # create table with attribute dummies
    df_attr = pd.concat([rest['attributes'].apply(pd.Series), rest['BusinessParking'].apply(pd.Series),
                        rest['Ambience'].apply(
                            pd.Series), rest['GoodForMeal'].apply(pd.Series),
                        rest['Dietary'].apply(pd.Series)], axis=1)
    df_attr_dummies = pd.get_dummies(df_attr)
    df_attr_dummies

    # get dummies from categories
    df_categories_dummies = pd.Series(rest['categories']).str.get_dummies(',')
    print(df_categories_dummies.shape)
    df_categories_dummies

    # pull out names and stars from rest table
    result = rest[['name', 'stars']]
    pp("Result")
    print(result)

    # Concat all tables and drop Restaurant column
    df_final = pd.concat(
        [df_attr_dummies, df_categories_dummies, result], axis=1)
    df_final.drop('Restaurants', inplace=True, axis=1)

    # map floating point stars to an integer
    mapper = {1.0: 1, 1.5: 2, 2.0: 2, 2.5: 3,
              3.0: 3, 3.5: 4, 4.0: 4, 4.5: 5, 5.0: 5}
    df_final['stars'] = df_final['stars'].map(mapper)

    pp("produceFinalDataFrame: Final Dataframe")
    print(df_final.head())

    return df_final
