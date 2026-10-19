from Classes.Files.CsvCache import read_csv


class Regions:
    def getRegionByID(self, regionID):
        RegionID = 0
        csv_file = read_csv('Classes/Files/assets/csv_logic/regions.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:
            if line_count <= 1:
                line_count += 1
            elif line_count - 2 == regionID:
                RegionID = row[0]
                break
            else:
                line_count += 1

        return RegionID

    def getIDByRegion(self, regionName):
        RegionID = 0
        csv_file = read_csv('Classes/Files/assets/csv_logic/regions.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:
            if line_count <= 1:
                line_count += 1
            elif row[0] == regionName:
                RegionID = line_count - 2
                break
            else:
                line_count += 1

        return RegionID
