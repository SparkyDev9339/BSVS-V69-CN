from Classes.Files.CsvCache import read_csv

class Sprays:
    def getSpraysIDSSpecificPrice(self, min, max):
        SpraysID = []
        csv_file = read_csv('Classes/Files/assets/csv_logic/sprays.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:
            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if row[2].lower() != 'true':
                    spray_gem_price = row[18]
                    if (spray_gem_price != ''):
                        if int(spray_gem_price) >= min and int(spray_gem_price) <= max:
                            SpraysID.append(line_count - 2)
                line_count += 1

        return SpraysID
        
    def getEmoteIdByName(name):
        csv_file = read_csv('Classes/Files/assets/csv_logic/sprays.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:

            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if row[0] == name:
                    SprayID = (line_count - 2)
                    break
                if row[0] != "":
                    line_count += 1
        return SprayID
        
    def getCostSprayByID(id):
        csv_file = read_csv('Classes/Files/assets/csv_logic/sprays.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:

            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if line_count - 2 == id:
                    SkinCost = {"Bling": row[18], "Diamonds": row[19]}
                    break
                if row[0] != "":
                    line_count += 1
        return SkinCost
