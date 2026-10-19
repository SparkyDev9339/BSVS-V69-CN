from Classes.Files.CsvCache import read_csv

class Emotes:

    def getPinsIDSSpecificPrice(self, min, max):
        EmotesID = []
        csv_file = read_csv('Classes/Files/assets/csv_logic/emotes.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:
            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if row[1].lower() != 'true':
                    pin_gem_price = row[18]
                    if (pin_gem_price != ''):
                        if int(pin_gem_price) >= min and int(pin_gem_price) <= max:
                            EmotesID.append(line_count - 2)
                if row[0] != "":
                    line_count += 1

        return EmotesID
        
    def getEmoteIdByName(name):
        csv_file = read_csv('Classes/Files/assets/csv_logic/emotes.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:

            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if row[0] == name:
                    EmotesID = (line_count - 2)
                    break
                if row[0] != "":
                    line_count += 1
        return EmotesID
    
    def getCostPinsByID(id):
        csv_file = read_csv('Classes/Files/assets/csv_logic/emotes.csv')
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
