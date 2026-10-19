from Classes.Files.CsvCache import read_csv

_PATH = 'Classes/Files/assets/csv_logic_v69/characters.csv'


class Characters:
    @staticmethod
    def getBrawlersID():
        rows = read_csv(_PATH)
        kind, disabled = rows[0].index('Type'), rows[0].index('Disabled')
        return [i for i, row in enumerate(rows[2:])
                if row[kind] == 'Hero' and row[disabled].lower() != 'true'
                and row[0] != 'MechaDudeBig']

    def getBrawlerFromSepcificRarity(self, rarity):
        from Classes.Files.Classes.Cards import Cards
        return Cards.getBrawlerFromSepcificRarity(self, rarity)

    @staticmethod
    def getBrawlerIdByName(name):
        for i, row in enumerate(read_csv(_PATH)[2:]):
            if row[0] == name:
                return i
        raise ValueError(f'Unknown brawler: {name}')

    getBrawlerIDByName = getBrawlerIdByName

    @staticmethod
    def getBrawlerNameByID(id):
        rows = read_csv(_PATH)[2:]
        if not 0 <= id < len(rows):
            raise ValueError(f'Unknown brawler ID: {id}')
        return rows[id][0]
