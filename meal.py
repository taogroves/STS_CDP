
class Meal:

    def __init__(self, name, calories, fat, carbs, protein, dietary_restrictions):
        self.name = name
        self.calories = calories
        self.fat = fat
        self.carbs = carbs
        self.protein = protein
        self.dietary_restrictions = dietary_restrictions

    # overload contstructor which takes in a string
    @classmethod
    def from_string(cls, string):
        # decode the string into a meal object
        name, calories, fat, carbs, protein, dietary_restrictions = string.split('|')
        return cls(name, calories, fat, carbs, protein, cls.decode_dietary_restrictions(dietary_restrictions))

    def __str__(self):
        # encode the meal object into a string separated by |
        return f'{self.name}|{self.calories}|{self.fat}|{self.carbs}|{self.protein}|{self.dietary_restrictions}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def get_dieatary_restrictions(self):
        return self.dietary_restrictions

    @classmethod
    def encode_dietary_restrictions(self, gluten_free, dairy_free, vegan, vegetarian):
        # encode the binary dietary restrictions into a digit
        return int(f'{int(gluten_free)}{int(dairy_free)}{int(vegan)}{int(vegetarian)}', 2)

    @classmethod
    def decode_dietary_restrictions(self, dietary_restrictions):
        # decode the digit into a set of boolean dietary restrictions
        return [bool(int(i)) for i in '{0:b}'.format(int(dietary_restrictions)).zfill(4)]


if __name__ == '__main__':
    print(Meal.decode_dietary_restrictions(3))
