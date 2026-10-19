from Classes.Files.CsvCache import read_csv

class Skins:
    def getSkinsIDSSpecificPrice(self, min, max):
        SkinsID = []
        csv_file = read_csv('Classes/Files/assets/csv_logic/skins.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:
            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if row[2].lower() != 'true':
                    skin_gem_price = row[csv_file[0].index("PriceGems")]
                    if (skin_gem_price != ''):
                        if int(skin_gem_price) >= min and int(skin_gem_price) <= max:
                            SkinsID.append(line_count - 2)
                if row[0] != "":
                    line_count += 1

        return SkinsID
        
    def getSkinIdByName(name):
        csv_file = read_csv('Classes/Files/assets/csv_logic/skins.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:

            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if row[0] == name:
                    SkinID = (line_count - 2)
                    break
                if row[0] != "":
                    line_count += 1
        return SkinID
    
    def getBrawlerBySkin(self, skinID):
        csv_file = read_csv('Classes/Files/assets/csv_logic/skins.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:

            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if line_count - 2 == skinID:
                    confName = row[1]
                    csv_file = read_csv('Classes/Files/assets/csv_logic/skin_confs.csv')
                    csv_reader = csv_file
                    line_count2 = 0
                    for row2 in csv_reader:

                        if line_count2 == 0 or line_count2 == 1:
                            line_count2 += 1
                        else:
                            if row2[0] == confName:
                                brawlerName = row2[1]
                                csv_file = read_csv('Classes/Files/assets/csv_logic/characters.csv')
                                csv_reader = csv_file
                                line_count3 = 0
                                for row3 in csv_reader:
                                    if line_count3 == 0 or line_count3 == 1:
                                        line_count3 += 1
                                    else:
                                        if row3[0] == brawlerName:
                                            return line_count3 - 2
                                        if row3[0] != "":
                                            line_count3 += 1
                            if row2[0] != "":
                                line_count2 += 1
                if row[0] != "":
                    line_count += 1
    
    def getCostSkinByID(id):
        csv_file = read_csv('Classes/Files/assets/csv_logic/skins.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:

            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if line_count - 2 == id:
                    SkinCost = {"Bling": row[csv_file[0].index("PriceBling")], "Diamonds": row[csv_file[0].index("PriceGems")]}
                    break
                if row[0] != "":
                    line_count += 1
        return SkinCost
    
    def getEmoteSkinByID(id):
        csv_file = read_csv('Classes/Files/assets/csv_logic/skins.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:

            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if line_count - 2 == id:
                    SkinEmote = {"Emote": row[5]}
                    break
                if row[0] != "":
                    line_count += 1
        return SkinEmote
