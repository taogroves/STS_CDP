import datetime
import json

from main import hash_dump
import meal

class Location:

    def __init__(self, loc_id, name, description, address, phone, hours, menu=None):
        self.name = name
        self.description = description
        self.address = address
        self.phone = phone
        if isinstance(hours, dict):
            self.hours = {}
            for k in hours.keys():
                self.hours[self.day_to_int(k)] = hours[k]
        else:
            self.hours = self.calc_hours(hours)
        self.loc_id = loc_id
        self.menu = menu if menu else []

    # registers a new location to the database
    @classmethod
    def register_location(cls, name, description, address, phone, hours):
        with open('locations.json', 'r') as f:
            locations = json.load(f)
        loc_id = hash_dump(name + address)
        locations[loc_id] = {
            'name': name,
            'description': description,
            'address': address,
            'phone': phone,
            'hours': hours,
            'menu': []
        }
        with open('locations.json', 'w') as f:
            json.dump(locations, f, indent=4)
        return loc_id

    # returns a location object from the database
    @classmethod
    def get_location(cls, loc_id):
        with open('locations.json', 'r') as f:
            locations = json.load(f)
        if loc_id in locations:
            return cls(loc_id, locations[loc_id]['name'], locations[loc_id]['description'], locations[loc_id]['address'], locations[loc_id]['phone'], locations[loc_id]['hours'])
        return None

    # adds a menu item to the location's menu
    def add_menu_item(self, m):
        self.menu.append(m)

        with open('locations.json', 'r') as f:
            locations = json.load(f)
        if self.loc_id in locations:
            locations[self.loc_id]['menu'].append(str(m))
            with open('locations.json', 'w') as f:
                json.dump(locations, f, indent=4)
            return True
        return False

    # converts various string representations of weekdays to an int
    @staticmethod
    def day_to_int(day):
        if isinstance(day, str):
            day = day.lower()
            if day in ['monday', 'mon']:
                return 0
            elif day in ['tuesday', 'tues']:
                return 1
            elif day in ['wednesday', 'wed']:
                return 2
            elif day in ['thursday', 'thurs']:
                return 3
            elif day in ['friday', 'fri']:
                return 4
            elif day in ['saturday', 'sat']:
                return 5
            elif day in ['sunday', 'sun']:
                return 6
        return day

    # constructs a dictionary representation of the given opening hours
    @classmethod
    def calc_hours(cls, hours):
        hours_dict = {}
        for i in range(len(hours)):
            if hours[i] != 'Closed':
                hours_dict[i] = []
                for time in hours[i].split(','):
                    hours_dict[i].append((datetime.datetime.strptime(time.split('-')[0], '%I:%M%p').time(), datetime.datetime.strptime(time.split('-')[1], '%I:%M%p').time()))
        return hours_dict

    def is_open(self):
        if datetime.datetime.now().weekday() in self.hours:
            now = datetime.datetime.now()
            for time in self.hours[now.weekday()]:
                if time[0] <= now.time() <= time[1]:
                    return True
        return False

    def is_open_at(self, day, t: str):
        day = self.day_to_int(day)
        if day in self.hours:
            now = datetime.datetime.strptime(t, '%I:%M%p')
            for i in range(len(self.hours[day]) - 1):
                if datetime.datetime.strptime(self.hours[day][i], '%H:%M') <= now <= datetime.datetime.strptime(self.hours[day][i+1], '%H:%M'):
                    return True
        return False

    def get_hours(self, day: int):
        if day in self.hours:
            return self.hours[day]
        return None


    def __str__(self):
        return str(self.loc_id)


if __name__ == '__main__':
    location = Location(1, 'Test', 'Test', 'Test', 'Test', ['9:00AM-10:00AM', '11:00AM-12:00PM', 'Closed', '6:00AM-10:00PM', 'Closed', 'Closed', 'Closed'])
    print(location.is_open())
    print(location.hours)

    print(Location.calc_hours(['9:00AM-10:00AM', '11:00AM-12:00PM']))

