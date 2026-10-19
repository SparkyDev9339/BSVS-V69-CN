from Classes.Files.CsvCache import read_csv


class Locations:
    def getAllMaps():
        Maps = []
        csv_file = read_csv('Classes/Files/assets/csv_logic/locations.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:
            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if row[1].lower() != 'true':
                        Maps.append(line_count - 2)
                if row[0] != "":
                    line_count += 1
        return Maps
