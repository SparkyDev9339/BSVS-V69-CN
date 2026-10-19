from Classes.Files.CsvCache import read_csv


class PlayerThumbnails:
    def getThumbnailsCount(self):
        csv_file = read_csv('Classes/Files/assets/csv_logic/player_thumbnails.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:
            if row[0] != "":
                line_count += 1
        return line_count - 3
        
    def getCostThumbnailsByID(id):
        csv_file = read_csv('Classes/Files/assets/csv_logic/player_thumbnails.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:

            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if line_count - 2 == id:
                    SkinCost = {"Bling": row[12], "Diamonds": row[13]}
                    break
                if row[0] != "":
                    line_count += 1
        return SkinCost
    
    def getThumbnailsIdByName(name):
        csv_file = read_csv('Classes/Files/assets/csv_logic/player_thumbnails.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:

            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if row[0] == name:
                    ThumbnailsID = (line_count - 2)
                    break
                if row[0] != "":
                    line_count += 1
        return ThumbnailsID
