import csv
import math
import datetime
import calendar
from functools import reduce


class QuakeHandler:
    DATA = list()

    def __init__(self):
        self.extract_data_from_file()

    def extract_data_from_file(self) -> None:
        with open("quake.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.DATA = [row for row in reader]

    def calculate_quakes_number_by_richter(self, richter=6.0) -> int:
        counter = 0
        for row in self.DATA:
            if float(row["Richter"]) > richter:
                counter += 1
        return counter

    def find_deepest_earthquakes(self, list_to_sort=None) -> list:
        return sorted(self.DATA if list_to_sort is None else list_to_sort, key=lambda x: float(x['Focal depth']))[::-1]

    def find_strongest_earthquakes(self, list_to_sort=None) -> list:
        return sorted(self.DATA if list_to_sort is None else list_to_sort, key=lambda x: float(x["Richter"]))[::-1]

    def find_top_deepest_earthquakes(self, topn=10, list_to_sort=None) -> list:
        return self.find_deepest_earthquakes(list_to_sort)[:topn]

    def find_top_strongest_earthquakes(self, topn=10, list_to_sort=None) -> list:
        return self.find_strongest_earthquakes(list_to_sort)[:topn]

    def find_quakes_by_pole(self, pole: str) -> list:
        # Count quakes in South pole
        if pole.lower() == "south":
            return [row for row in self.DATA if float(row["Latitude"]) < 0]

        # Count quakes in North pole
        if pole.lower() == "north":
            return [row for row in self.DATA if float(row["Latitude"]) > 0]

        # Count quakes in West pole
        if pole.lower() == "west":
            return [row for row in self.DATA if float(row["Longitude"]) < 0]

        # Count quakes in East pole
        if pole.lower() == "east":
            return [row for row in self.DATA if float(row["Longitude"]) > 0]

    def calculate_quakes_number_by_pole(self, pole: str) -> int:
        return len(self.find_quakes_by_pole(pole))

    def find_top_strongest_earthquakes_by_pole(self, pole: str) -> list:
        return self.find_top_strongest_earthquakes(list_to_sort=self.find_quakes_by_pole(pole))

    def find_top_deepest_earthquakes_by_pole(self, pole: str) -> list:
        return self.find_top_deepest_earthquakes(list_to_sort=self.find_quakes_by_pole(pole))

    def find_pole_by_highest_params(self, param) -> str:
        poles = (self.find_top_strongest_earthquakes_by_pole('South'),
                 self.find_top_strongest_earthquakes_by_pole('North'),
                 self.find_top_strongest_earthquakes_by_pole('West'),
                 self.find_top_strongest_earthquakes_by_pole('East'))
        names = ("South Pole", "North Pole", "West", "East")
        sums = [reduce(lambda x, y: float(x[param]) if type(x).__name__ != 'float' else x + float(y[param]),
                       pole) for pole in poles]
        return names[sums.index(max(sums))]

    def find_pole_with_strongest_earthquakes(self) -> str:
        return self.find_pole_by_highest_params("Richter")

    def find_pole_with_deepest_earthquakes(self) -> str:
        return self.find_pole_by_highest_params("Focal depth")

    @staticmethod
    def calculate_the_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def find_the_most_remote_earthquake(self) -> tuple:
        distances = list()
        for i in range(len(self.DATA) - 1):
            for j in range(i + 1, len(self.DATA)):
                distances.append((
                    self.calculate_the_distance(
                        float(self.DATA[i]["Latitude"]),
                        float(self.DATA[i]["Longitude"]),
                        float(self.DATA[j]["Latitude"]),
                        float(self.DATA[j]["Longitude"])), self.DATA[i]))
        return sorted(distances, key=lambda x: x[0], reverse=True)[1]


class AirQualityHandler:
    DATA = list()
    TOKENS = list()

    def __init__(self):
        self.extract_data_from_file()
        self.get_tokens()

    def extract_data_from_file(self) -> None:
        with open("AirQualityUCI.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=';')
            self.DATA = [row for row in reader]

    def get_tokens(self):
        self.TOKENS = list(self.DATA[0].keys())[2:]

    def create_correct_data(self) -> list:
        data = list()
        for row in self.DATA:
            correct = True
            for key in row.keys():
                if row[key] == "-200":
                    correct = False
            if correct:
                data.append(row)
        return data

    def find_concentration_limits(self, token: str, limit='max') -> None or dict:
        data = self.create_correct_data()

        if limit.lower() not in ('max', 'min'):
            print("ERROR: invalid limit's name")
            return None

        if token not in self.TOKENS:
            print("ERROR: invalid token's name")
            return None

        if limit.lower() == 'max':
            return max(data, key=lambda x: float(x[token]))

        if limit.lower() == 'min':
            return min(data, key=lambda x: float(x[token]))

    @staticmethod
    def find_date_and_time_in_entry(entry: dict) -> tuple:
        return entry["Date"], entry["Time"]

    def find_the_date_of_the_boundary_air_concentration(self,  token: str, limit='max') -> str:
        return " ".join(self.find_date_and_time_in_entry(self.find_concentration_limits(token, limit)))

    @staticmethod
    def find_week_day_by_date(date: str) -> str:
        return calendar.day_name[datetime.datetime.strptime(date, "%d/%m/%Y").date().weekday()]

    def find_week_day_with_average_concentration(self, limit='max') -> None or str:
        if limit.lower() not in ('max', 'min'):
            print("ERROR: invalid limit's name")
            return None

        data = self.create_correct_data()
        date = dict()
        max_values = [self.find_concentration_limits(token, limit="max")[token] for token in self.TOKENS]

        for row in data:
            cur_values = [row[token] for token in self.TOKENS if token not in ("Date", "Time", "average")]
            row["average"] = sum([float(cur_values[i]) / float(max_values[i]) for i in range(len(max_values))])
        date = max(data, key=lambda x: x["average"]) if limit == "max" else min(data, key=lambda x: x["average"])

        return self.find_week_day_by_date(date["Date"]) + f" ({date['Date']}, {date['Time']}) "

    @staticmethod
    def find_target_points(data: list, token: str, period=3, increase=False, extremum='min') -> list:
        target_entries = list()
        if not increase:
            for i in range(period - 1, len(data)):
                flag = True
                for j in range(i, i - period + 1, -1):
                    if not (float(data[j][token]) <= float(data[j - 1][token])):
                        flag = False
                        break
                if flag:
                    if extremum == 'min':
                        for j in range(i, i + period):
                            target_entries.append(data[i])
                    else:
                        target_entries.append(data[i])
        else:
            for i in range(len(data) - period):
                flag = True
                for j in range(i, i + period - 1):
                    if not (float(data[j][token]) >= float(data[j + 1][token])):
                        flag = False
                        break
                if flag:
                    if extremum == 'max':
                        for j in range(i, i + period):
                            target_entries.append(data[i])
                    else:
                        target_entries.append(data[i])
        return target_entries

    def find_local_minimums(self, token: str, period=3) -> list:
        if token not in self.TOKENS:
            print("ERROR: invalid token's name")
            return None

        data = self.create_correct_data()
        target_points = self.find_target_points(data, token, period=period, increase=False)
        return self.find_target_points(target_points, token, period=period, increase=True)

    def find_local_maximums(self, token: str, period=3) -> list:
        if token not in self.TOKENS:
            print("ERROR: invalid token's name")
            return None

        data = self.create_correct_data()
        target_points = self.find_target_points(data, token, period=period, increase=True, extremum='max')
        return self.find_target_points(target_points, token, period=period, increase=False, extremum='max')

    def find_time_of_frequent_minimums(self, token: str) -> str:
        if token not in self.TOKENS:
            print("ERROR: invalid token's name")
            return None

        times = {entry["Time"]: 0 for entry in self.DATA}
        for minimum in self.find_local_minimums(token, period=3):
            times[minimum["Time"]] += 1
        return max(times.items(), key=lambda x: x[1])[0]

    def find_time_of_frequent_maximums(self, token: str) -> str:
        if token not in self.TOKENS:
            print("ERROR: invalid token's name")
            return None

        times = {entry["Time"]: 0 for entry in self.DATA}
        for maximum in self.find_local_maximums(token, period=3):
            times[maximum["Time"]] += 1
        return max(times.items(), key=lambda x: x[1])[0]


def quake_handler_demonstration() -> None:
    quake_handler = QuakeHandler()
    print(f"Quakes which have Richter > 6: {quake_handler.calculate_quakes_number_by_richter()}")
    print(f"Top the deepest quakes: {quake_handler.find_top_deepest_earthquakes()}")
    print(f"Top the strongest quakes: {quake_handler.find_top_strongest_earthquakes()}")
    print("*" * 175 + "\n")

    # South Pole
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", end="")
    print(f"Quakes in South Pole: {quake_handler.calculate_quakes_number_by_pole('South')}")
    print(f"Top the strongest quakes in South Pole: {quake_handler.find_top_strongest_earthquakes_by_pole('South')}")
    print()
    print(f"Top the deepest quakes in South Pole: {quake_handler.find_top_deepest_earthquakes_by_pole('South')}")
    print("*" * 175 + "\n")

    # North Pole
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", end="")
    print(f"Quakes in North Pole: {quake_handler.calculate_quakes_number_by_pole('North')}")
    print(f"Top the strongest quakes in North Pole: {quake_handler.find_top_strongest_earthquakes_by_pole('North')}")
    print()
    print(f"Top the deepest quakes in North Pole: {quake_handler.find_top_deepest_earthquakes_by_pole('North')}")
    print("*" * 175 + "\n")

    # West Pole
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", end="")
    print(f"Quakes in West Pole: {quake_handler.calculate_quakes_number_by_pole('West')}")
    print(f"Top the strongest quakes in West Pole: {quake_handler.find_top_strongest_earthquakes_by_pole('West')}")
    print()
    print(f"Top the deepest quakes in West Pole: {quake_handler.find_top_deepest_earthquakes_by_pole('West')}")
    print("*" * 175 + "\n")

    # East Pole
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", end="")
    print(f"Quakes in East Pole: {quake_handler.calculate_quakes_number_by_pole('East')}")
    print(f"Top the strongest quakes in East Pole: {quake_handler.find_top_strongest_earthquakes_by_pole('East')}")
    print()
    print(f"Top the deepest quakes in East Pole: {quake_handler.find_top_deepest_earthquakes_by_pole('East')}")
    print("*" * 175 + "\n")

    print(f"The pole with the strongest earthquakes: {quake_handler.find_pole_with_strongest_earthquakes()}")
    print(f"The pole with the deepest earthquakes: {quake_handler.find_pole_with_deepest_earthquakes()}")
    print(f"The the most remote earthquake is: {quake_handler.find_the_most_remote_earthquake()}")


def air_quality_handler_demonstration() -> None:
    air_quality_handler = AirQualityHandler()
    print(f"Date and Time: {air_quality_handler.find_the_date_of_the_boundary_air_concentration('CO(GT)', limit='max')}")
    print(f"Day with the highest average concentration of substances:"
          f" {air_quality_handler.find_week_day_with_average_concentration('max')}")
    print(f"Day with the lowest average concentration of substances:"
          f" {air_quality_handler.find_week_day_with_average_concentration('min')}")
    print(f"Time of the most frequent minimums: {air_quality_handler.find_time_of_frequent_minimums('CO(GT)')}")
    print(f"Time of the most frequent maximums: {air_quality_handler.find_time_of_frequent_maximums('CO(GT)')}")


def main():
    # quake_handler_demonstration()
    air_quality_handler_demonstration()


if __name__ == '__main__':
    main()
