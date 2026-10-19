from Classes.Files.CsvCache import read_csv

_PATH = 'Classes/Files/assets/csv_logic_v69/cards.csv'


class Cards:
    def getCardsListFromMetaType(self, meta_type):
        rows = read_csv(_PATH)
        meta, disabled = rows[0].index('MetaType'), rows[0].index('Disabled')
        return [i for i, row in enumerate(rows[2:])
                if row[meta] == str(meta_type) and row[disabled].lower() != 'true']

    def getBrawlerFromSepcificRarity(self, rarity):
        from Classes.Files.Classes.Characters import Characters
        rows = read_csv(_PATH)
        meta, disabled, rarity_col, target = (
            rows[0].index(name) for name in ('MetaType', 'Disabled', 'Rarity', 'Target'))
        names = {row[target] for row in rows[2:]
                 if row[meta] == '0' and row[disabled].lower() != 'true'
                 and row[rarity_col].lower() == rarity.lower()}
        characters = read_csv('Classes/Files/assets/csv_logic_v69/characters.csv')[2:]
        return [i for i in Characters.getBrawlersID() if characters[i][0] in names]

    @staticmethod
    def getCardIdByName(name):
        for i, row in enumerate(read_csv(_PATH)[2:]):
            if row[0] == f'{name}_unlock':
                return i
        raise ValueError(f'Unknown brawler card: {name}')

    @staticmethod
    def getCardRarityByName(name):
        rows = read_csv(_PATH)
        rarity = rows[0].index('Rarity')
        return rows[Cards.getCardIdByName(name) + 2][rarity]
