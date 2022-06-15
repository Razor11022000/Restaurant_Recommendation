class Recommedation:
    def __init__(self, restName, cuisine, stars, reviewCount, city):
        self.restName = restName
        # List of categories
        self.cuisine = cuisine.split(", ")
        self.stars = round(float(stars))
        self.reviewCount = reviewCount
        self.city = city
