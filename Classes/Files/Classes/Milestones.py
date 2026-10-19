from Classes.Files.CsvCache import read_csv

class Milestones:
    def getTrophyRoadLvL(lvlID):
        csv_file = read_csv('Classes/Files/assets/csv_logic/milestones.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:

            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if row[0] == f"goal_6_{lvlID}":
                    MilestoneData = {"lvlID": {lvlID}, "Trophies": row[3], "PrimaryLvlUpRewardType": row[9], "PrimaryLvlUpRewardCount": row[10], "PrimaryLvlUpRewardData": row[12]}
                    print(MilestoneData)
                    break
                if row[0] != "":
                    line_count += 1
        return MilestoneData
    
    def getBrawlPassLvl(MilestoneID, BrawlPassSeason, lvlID):
        csv_file = read_csv('Classes/Files/assets/csv_logic/milestones.csv')
        csv_reader = csv_file
        line_count = 0
        for row in csv_reader:

            if line_count == 0 or line_count == 1:
                line_count += 1
            else:
                if row[0] == f"Goal_{MilestoneID}_{BrawlPassSeason}_{lvlID}":
                    MilestoneData = {"MilestoneID": MilestoneID, "BrawlPassSeason": BrawlPassSeason, "lvlID": {lvlID}, "BrawlPassTokens": row[4], "PrimaryLvlUpRewardType": row[9], "PrimaryLvlUpRewardCount": row[10], "PrimaryLvlUpRewardData": row[12]}
                    print(MilestoneData)
                    break
        return MilestoneData
