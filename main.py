import datetime
import json
import hashlib
import location
import meal


def hash_dump(input):
    if isinstance(input, str):
        input = input.encode('utf-8')
    return str(hashlib.md5(input).hexdigest())

def signup_user(first, last, age, email, password):
    """Sign up a new user."""
    with open('users.json', 'r') as f:
        users = json.load(f)
    usr_id = hash_dump(email)
    if usr_id in users:
        raise ValueError('User is already registered.')

    pwd_hash = hash_dump(password)
    users[usr_id] = {
        'first': first,
        'last': last,
        'age': age,
        'email': email,
        'meal_history': {}
    }
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

    with open('user_login.json', 'r') as f:
        logins = json.load(f)

    logins[email] = {'pwd': pwd_hash, 'usr_id': usr_id}

    with open('user_login.json', 'w') as f:
        f.write(json.dumps(logins, indent=4))

    return usr_id

def login_user(email, password):
    """Login a user."""
    with open('user_login.json', 'r') as f:
        logins = json.load(f)
    if email in logins:
        if logins[email]['pwd'] == hash_dump(password):
            return logins[email]['usr_id']
    return None

def get_user_id(email):
    """Get user id."""
    with open('user_login.json', 'r') as f:
        logins = json.load(f)
    if email in logins:
        return logins[email]['usr_id']
    return None

def get_user_data(usr_id):
    """Get user data."""
    with open('users.json', 'r') as f:
        users = json.load(f)
    if usr_id in users:
        return users[usr_id]
    return None

def get_meal_history(usr_id):
    with open('users.json', 'r') as f:
        users = json.load(f)
    if usr_id in users:
        meals = []
        for m in users[usr_id]['meal_history']:
            meals.append(meal.Meal.from_string(users[usr_id]['meal_history'][m]))
        return meals
    return None

# add a meal to a user's meal history
def log_meal(usr_id, meal, time=datetime.datetime.now()):
    with open('users.json', 'r') as f:
        users = json.load(f)
    if usr_id in users:
        users[usr_id]['meal_history'][time.strftime("%m/%d/%Y, %H:%M:%S")] = str(meal)
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
        return True
    return False

if __name__ == '__main__':
    # register John Doe as a user and login as him
    signup_user('John', 'Doe', 25, "jondon@gmail.com", "123456")
    user_id = login_user('jondon@gmail.com', '123456')
    print(get_user_data(user_id))


    # register a new location called "The Diner" which is open from 8am to 10pm on weekdays
    diner_id = location.Location.register_location('The Diner', 'A diner', '123 Main St', '555-555-5555', {'mon': ['8:00', '22:00'], 'tue': ['8:00', '22:00'], 'wed': ['8:00', '22:00'], 'thu': ['8:00', '22:00'], 'fri': ['8:00', '22:00']})
    diner = location.Location.get_location(diner_id)

    # add five menu items to the diner's menu
    diner.add_menu_item(meal.Meal('Burger', 500, 30, 50, 10, meal.Meal.encode_dietary_restrictions(0, 0, 0, 0)))
    diner.add_menu_item(meal.Meal('Fries', 300, 20, 30, 5, meal.Meal.encode_dietary_restrictions(0, 0, 1, 1)))
    diner.add_menu_item(meal.Meal('Salad', 250, 15, 25, 5, meal.Meal.encode_dietary_restrictions(1, 1, 1, 1)))
    diner.add_menu_item(meal.Meal('Chicken', 400, 20, 40, 10, meal.Meal.encode_dietary_restrictions(1, 1, 0, 0)))
    diner.add_menu_item(meal.Meal('Steak', 600, 40, 50, 20, meal.Meal.encode_dietary_restrictions(1, 1, 0, 0)))


    # if the diner is open on 11/10/2022 at 2pm, print the two lowest calorie meals
    if diner.is_open_at("mon", "02:00PM"):
        print(diner.menu)
        print(s := sorted(diner.menu, key=lambda x: x.calories)[:2])

        # add the two lowest calorie meals to John Doe's meal history, one at 2pm on 11/10/22 and one right now
        log_meal(user_id, s[0], datetime.datetime(2022, 11, 10, 14, 0, 0))
        log_meal(user_id, s[1])

        # print John Doe's information
        print(get_user_data(user_id))

        # print the dietary restrictions of the last meal John Doe ate
        print(get_meal_history(user_id)[-1].dietary_restrictions)



