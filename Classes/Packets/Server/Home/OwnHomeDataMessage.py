"""OwnHomeDataMessage 24101 — CN 69.114.1 captured state.

Base values are expanded from the original 38,403-byte packet formerly stored
in writeHexa. Wire types/order follow v69 native decoders; v67 symbols identify
structures. Numeric field labels are native object offsets (not guessed names).
Shop offers, ReleaseEntry and recruit-road brawlers are empty.
Playable brawlers and enabled skins are unlocked using the bundled v69 CSV tables.
Packet-byte comments below refer to original capture positions.
Account IDs, name and name registration state come from player.
No capture file is needed at runtime.
"""
from Classes.Packets.PiranhaMessage import PiranhaMessage

import csv
from pathlib import Path


_ASSET_DIRECTORY = Path(__file__).resolve().parents[3] / 'Files' / 'assets' / 'csv_logic_v69'


def _read_unlock_table(name):
    with (_ASSET_DIRECTORY / (name + '.csv')).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        next(reader)  # CSV column types
        # Empty names continue the preceding record; they do not receive a data ID.
        return [row for row in reader if row['Name']]


_CHARACTERS = _read_unlock_table('characters')
_CARDS = _read_unlock_table('cards')
_SKINS = _read_unlock_table('skins')
_SKIN_CONFS = {row['Name']: row for row in _read_unlock_table('skin_confs')}
_PLAYABLE_HEROES = {
    row['Name']: index for index, row in enumerate(_CHARACTERS)
    if row['Type'] == 'Hero' and row['Disabled'].lower() != 'true' and row['ItemName']
}
_BRAWLER_UNLOCK_CARDS = tuple(
    (index, _PLAYABLE_HEROES[row['Target']])
    for index, row in enumerate(_CARDS)
    if row['Type'] == 'unlock' and row['MetaType'] == '0'
    and row['Disabled'].lower() != 'true' and row['Target'] in _PLAYABLE_HEROES
)
# Permanent equipment cards; event-only powers are excluded.
_BRAWLER_EQUIPMENT_CARDS = tuple(
    index for index, row in enumerate(_CARDS)
    if row['MetaType'] in {'4', '5', '6'}
    and row['Disabled'].lower() != 'true' and row['Target'] in _PLAYABLE_HEROES
)
# LogicClientAvatar::hasCard (0x101260EFC): Buffies use separate groups.
# MetaType 15 = star powers, 13 = gadgets, 16 = hypercharges.
_BUFFY_CARDS_BY_GROUP = {
    group: tuple(index for index, row in enumerate(_CARDS)
                 if row['MetaType'] == meta and row['Disabled'].lower() != 'true'
                 and row['Target'] in _PLAYABLE_HEROES)
    for meta, group in (('15', 37), ('13', 38), ('16', 39))
}

# Gear data IDs 0..18 from the previously bundled gear_boosts table.
_GEAR_IDS = tuple(range(19))

_UNLOCKED_SKINS = tuple(
    index for index, row in enumerate(_SKINS)
    if row['Disabled'].lower() != 'true' and row['Conf'] in _SKIN_CONFS
)
_PLAYER_ICONS = _read_unlock_table('player_thumbnails')
_EMOTES = _read_unlock_table('emotes')
_SKIN_WIDGETS = _read_unlock_table('skins.k2')
_SKIN_IDS_BY_NAME = {row['Name']: index for index, row in enumerate(_SKINS)}
_UNLOCKED_WIDGETS = tuple(
    _SKIN_IDS_BY_NAME[row['Name']] for row in _SKIN_WIDGETS
    if row['WidgetType'] in {'WidgetWing', 'WidgetHalo', 'WidgetMask'}
    and row['Name'] in _SKIN_IDS_BY_NAME
    and _SKIN_IDS_BY_NAME[row['Name']] in _UNLOCKED_SKINS
)
_OWNED_VANITY_ITEMS = (
    tuple((28, index) for index in range(len(_PLAYER_ICONS)))
    + tuple((52, index) for index in range(len(_EMOTES)))
)
if {hero for _, hero in _BRAWLER_UNLOCK_CARDS} != set(_PLAYABLE_HEROES.values()):
    raise ValueError('Missing unlock cards in v69 assets')




class OwnHomeDataMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 0

    def encode(self, fields, player):
        self.messagePayload = b''
        self.offset = 0
        self.bitoffset = 0
        self.writeVInt(1792340348)  # OwnHomeDataMessage +160
        self.writeVInt(-638033142)  # OwnHomeDataMessage +164
        self.writeLogicDailyData()
        self.writeLogicConfData()
        self.writeLogicClientHome(player)
        self.writeLogicClientAvatar(player)
        return self.messagePayload

    def decode(self):
        return {}

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 24101

    def getMessageVersion(self):
        return self.messageVersion

    def writeLogicDailyData(self):
        """Native decode 0x1013FC470; packet starts at byte 10."""

        # DailyData — packet byte 10
        self.writeVInt(2026291)  # native +0
        self.writeVInt(27652)  # native +4
        self.writeVInt(99999)  # native +8
        self.writeVInt(99999)  # native +12
        self.writeVInt(0)  # native +16
        self.writeVInt(454)  # native +20
        self.writeVInt(15)  # native +28
        self.writeDataReference(28, 0)  # native +40
        self.writeDataReference(43, 0)  # native +48

        # list56 — packet byte 26
        self.writeVInt(26)
        for x in range(26):
            self.writeVInt(x)

        # refs72 — packet byte 28
        self.writeVInt(1)  # count

        # refs72[0] — packet byte 29
        self.writeDataReference(29, 1117)  # 

        # refs88 — packet byte 32
        self.writeVInt(0)  # count

        # refs104 — packet byte 33
        self.writeVInt(0)  # count

        # Owned skins (LogicDailyData +120)
        self.writeVInt(len(_UNLOCKED_SKINS))
        for skin_id in _UNLOCKED_SKINS:
            self.writeDataReference(29, skin_id)

        # refs136 — packet byte 38
        self.writeVInt(0)  # count

        # refs152 — packet byte 39
        self.writeVInt(0)  # count

        # DailyData — packet byte 40
        self.writeVInt(0)  # native +172
        self.writeVInt(13)  # native +176
        self.writeVInt(0)  # native +180
        self.writeVInt(1)  # native +184
        self.writeBoolean(True)  # native +168
        self.writeVInt(0)  # native +188
        self.writeVInt(157)  # native +192
        self.writeVInt(1528851)  # native +196
        self.writeVInt(157)  # native +200
        self.writeVInt(1528851)  # native +204
        self.writeVInt(200)  # forced0
        self.writeVInt(200)  # forced4

        # forcedDrops — packet byte 62
        self.writeVInt(5)  # count

        # forcedDrops[0] — packet byte 63
        self.writeVInt(93)  # 

        # forcedDrops[1] — packet byte 65
        self.writeVInt(206)  # 

        # forcedDrops[2] — packet byte 67
        self.writeVInt(456)  # 

        # forcedDrops[3] — packet byte 69
        self.writeVInt(1001)  # 

        # forcedDrops[4] — packet byte 71
        self.writeVInt(2264)  # 

        # DailyData — packet byte 73
        self.writeBoolean(False)  # native +232
        self.writeVInt(0)  # native +236
        self.writeVInt(2)  # native +240
        self.writeVInt(0)  # native +244
        self.writeVInt(0)  # native +248
        self.writeVInt(0)  # native +252
        self.writeVInt(0)  # native +256

        # Shop offers
        self.writeVInt(0)

        # DailyData — packet byte 11765
        self.writeVInt(0)  # native +328
        self.writeVInt(-1)  # native +332

        # list344 — packet byte 11767
        self.writeVInt(3)  # count

        # list344[0] — packet byte 11768
        self.writeVInt(0)  # 

        # list344[1] — packet byte 11769
        self.writeVInt(1)  # 

        # list344[2] — packet byte 11770
        self.writeVInt(2)  # 

        # DailyData — packet byte 11771
        self.writeVInt(0)  # native +360
        self.writeVInt(0)  # native +364

        # refs368 — packet byte 11773
        self.writeInt8(3)  # count

        # DailyData — packet byte 11774
        self.writeDataReference(16, 0)  # ref368
        self.writeDataReference(16, 1)  # ref368
        self.writeDataReference(16, 2)  # ref368
        self.writeString('CY')  # native +392
        self.writeString('t.me/bsvschannel')  # native +400
        self.writeVInt(0)  # native +408

        # DailyData integer settings; 39/40 mark the ranked season as seen.
        daily_int_values = {
            15: 0, 66: 30, 31: 0, 69: 0,
            70: -1792340348, 71: 0, 72: -1792340348, 28: 1024,
            56: 4096, 74: 0, 41: 100, 75: 100,
            43: 10, 77: 30, 45: 75, 78: 75,
            46: 100, 53: 0, 54: 0, 55: 0,
            39: 50, 40: 50,
            73: 1,  # hasBuddyShopFreeDrawConsumed: hide the free Buffy gift
        }
        self.writeVInt(len(daily_int_values))
        for key, value in daily_int_values.items():
            self.writeVInt(value)
            self.writeVInt(key)

        # Cooldown — packet byte 11856
        self.writeVInt(0)  # count

        # BrawlPassSeason: season 54 only
        self.writeVInt(1)

        # BrawlPassSeason[0] — packet byte 15152
        self.writeVInt(54)  # native +0
        self.writeVInt(0)  # native +4
        self.writeBoolean(False)  # native +32
        self.writeVInt(0)  # native +36
        self.writeBoolean(False)  # native +41
        self.writeBoolean(True)  # native +40

        # BrawlPassSeason[0].bits8 — packet byte 15157
        self.writeBoolean(True)  # present
        self.writeInt(0)  # word0
        self.writeInt(0)  # word1
        self.writeInt(0)  # word2
        self.writeInt(0)  # word3

        # BrawlPassSeason[0].bits16 — packet byte 15173
        self.writeBoolean(True)  # present
        self.writeInt(4)  # word0
        self.writeInt(0)  # word1
        self.writeInt(0)  # word2
        self.writeInt(0)  # word3

        # BrawlPassSeason[0] — packet byte 15190
        self.writeBoolean(False)  # native +42

        # BrawlPassSeason[0].bits24 — packet byte 15191
        self.writeBoolean(True)  # present
        self.writeInt(0)  # word0
        self.writeInt(0)  # word1
        self.writeInt(0)  # word2
        self.writeInt(0)  # word3

        # BrawlPassSeason[0] — packet byte 15207
        self.writeDataReference(0, 0)  # native +48

        # BrawlPassSeason[0].entries56 — packet byte 15208
        self.writeVInt(0)  # count

        # BrawlPassSeason[0] — packet byte 15209
        self.writeInt(0)  # native +72

        # Quests — packet byte 15213
        self.writeBoolean(True)  # present

        # Quests.quests0 — packet byte 15214
        self.writeVInt(0)  # count

        # Quests — packet byte 15215
        self.writeVInt(319251)  # native +80
        self.writeVInt(0)  # native +84

        # Quests.quests32 — packet byte 15219
        self.writeVInt(0)  # count

        # Quests.quests48 — packet byte 15220
        self.writeVInt(0)  # count

        # Quests.quests16 — packet byte 15221
        self.writeVInt(0)  # count

        # Quests.quests64 — packet byte 15222
        self.writeVInt(0)  # count

        # Quests — packet byte 15223
        self.writeString(None)  # native +88

        # VanityItems — packet byte 15227
        self.writeBoolean(True)  # present

        # Owned profile icons and emotes
        self.writeVInt(len(_OWNED_VANITY_ITEMS))
        for table, item_id in _OWNED_VANITY_ITEMS:
            self.writeDataReference(table, item_id)
            self.writeVInt(1)
            self.writeVInt(1)
            self.writeVInt(1)

        # RankedSeason — packet byte 15253
        self.writeBoolean(True)  # present
        self.writeVInt(50)  # native +8
        self.writeVInt(11250)  # native +12; current ELO
        self.writeVInt(22)  # native +16; current rank: Pro
        self.writeVInt(1)  # native +20
        self.writeVInt(0)  # native +24
        self.writeVInt(1)  # native +28
        self.writeVInt(0)  # native +32
        self.writeVInt(11250)  # native +36; highest ELO
        self.writeVInt(0)  # native +40
        self.writeVInt(0)  # native +64
        self.writeVInt(0)  # native +68
        self.writeVInt(1)  # native +72
        self.writeVInt(0)  # native +76

        # RankedSeason.ranks — packet byte 15267
        self.writeVInt(0)  # count

        # DailyData — packet byte 15268
        self.writeInt(0)  # native +504
        self.writeVInt(0)  # native +32
        self.writeDataReference(0, 0)  # native +512

        # Rewards520 — packet byte 15274
        self.writeBoolean(False)  # present

        # Owned wings, head and face widgets (LogicDailyData +576)
        self.writeVInt(len(_UNLOCKED_WIDGETS))
        for skin_id in _UNLOCKED_WIDGETS:
            self.writeDataReference(29, skin_id)

        # map592 — packet byte 15276
        self.writeVInt(0)  # count

        # map632 — packet byte 15277
        self.writeVInt(0)  # count

        # map672 — packet byte 15278
        self.writeVInt(0)  # count

        # DailyData — packet byte 15279
        self.writeVInt(0)  # native +760

        # RandomChests — packet byte 15280
        self.writeBoolean(True)  # present

        # RandomChests.map0 — packet byte 15281
        self.writeVInt(0)  # count

        # RandomChests.map40 — packet byte 15282
        self.writeVInt(0)  # count

        # DailyData — packet byte 15283
        self.writeVInt(-1)  # native +336
        self.writeVInt(0)  # native +340
        self.writeVInt(0)  # native +36
        self.writeVInt(1495148)  # native +208
        self.writeVInt(8155148)  # native +212
        self.writeVInt(2644852)  # native +216

        # CompetitivePassSeasons — packet byte 15298
        self.writeVInt(0)  # count

        # refs272 — packet byte 15299
        self.writeVInt(0)  # count

        # DailyData — packet byte 15300
        self.writeDataReference(2, 607)  # native +288
        self.writeDataReference(0, 0)  # native +296
        self.writeDataReference(2, 608)  # native +304
        self.writeDataReference(2, 609)  # native +312

        # Esports — packet byte 15310
        self.writeBoolean(False)  # present

        # DailyData — packet byte 15311
        self.writeDataReference(2, 357)  # native +320

        # TrophyProtect — packet byte 15314
        self.writeBoolean(True)  # present
        self.writeVInt(0)  # native +0
        self.writeVInt(0)  # native +8
        self.writeVInt(0)  # native +4

        # list800 — packet byte 15318
        self.writeVInt(0)  # count

        # ProbabilityChest — packet byte 15319
        self.writeBoolean(True)  # present
        self.writeString(None)  # native +0
        self.writeString(None)  # native +8
        self.writeString(None)  # native +16
        self.writeString(None)  # native +24

        # ProbabilityChest.entries32 — packet byte 15336
        self.writeVInt(0)  # count

        # ProbabilityChest — packet byte 15337
        self.writeVInt(0)  # native +48

        # TrophyProtectCards — packet byte 15338
        self.writeVInt(0)  # count

        # map712 — packet byte 15339
        self.writeVInt(0)  # count

        # DailyData — packet byte 15340
        self.writeVInt(1000)  # TrophyRoadTier

        # Rewards560 — packet byte 15341
        self.writeBoolean(False)  # present

        # Rewards568 — packet byte 15342
        self.writeBoolean(False)  # present

    def writeLogicConfData(self):
        """Native decode 0x1013F92E0; packet starts at byte 15342."""

        eventSlots = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
            13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
            25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
            37, 38, 39, 40, 41, 43, 42, 44, 45, 46, 47, 48,
            49, 50, 51, 52, 100000, 100001, 100002, 100003, 100004, 100005, 100006, 100007,
            53, 54, 55, 56,
        ]
        self.writeVInt(len(eventSlots))
        for eventId in eventSlots:
            self.writeVInt(eventId)

        # events16 — packet byte 15424
        self.writeVInt(6)  # count

        for entry in (
            (-1273700251, 1, 0, 0, 56452, 5, (15, 24), (48, 5), 2, '', 0, 0, 0, 0, 0, 0, False, False, 0, False, 0, 0, False, False, False, False, -1, False, (0, 0), False, -1, -1, -1, -1, -1, -1, False, False, False, False, False, False, False, False),
            (-1275000251, 2, 0, 0, 13252, 5, (15, 1124), (48, 6), 2, '', 0, 0, 0, 0, 0, 0, False, False, 0, False, 0, 0, False, False, False, False, -1, False, (0, 0), False, -1, -1, -1, -1, -1, -1, False, False, False, False, False, False, False, False),
            (-1279300251, 3, 0, 0, 27652, 5, (15, 1026), (48, 0), 2, '', 0, 0, 0, 0, 0, 0, False, False, 0, False, 0, 0, False, False, False, False, -1, False, (0, 0), False, -1, -1, -1, -1, -1, -1, False, False, False, False, False, False, False, False),
            (-1286600292, 4, 0, 0, 6052, 5, (15, 18), (48, 2), 2, '', 0, 0, 0, 0, 0, 0, False, False, 0, False, 0, 0, False, False, False, False, -1, False, (0, 0), False, -1, -1, -1, -1, -1, -1, False, False, False, False, False, False, False, False),
            (-1276400251, 5, 0, 0, 13252, 0, (15, 1143), (48, 9), 2, '', 0, 0, 0, 0, 0, 0, False, False, 0, False, 0, 0, False, False, False, False, -1, False, (0, 0), False, -1, -1, -1, -1, -1, -1, False, False, False, False, False, False, False, False),
            (-1282200251, 6, 0, 0, 34852, 5, (15, 1178), (48, 20), 2, '', 0, 0, 0, 0, 0, 0, False, False, 0, False, 0, 0, False, False, False, False, -1, False, (0, 0), False, -1, -1, -1, -1, -1, -1, False, False, False, False, False, False, False, False),
        ):
            self._write_ConfData_events16_layout8(entry)

        # events32 — packet byte 16656
        self.writeVInt(0)  # count

        # events48 — packet byte 17356
        self.writeVInt(0)  # count

        list64 = [20, 35, 75, 140, 290, 480, 800, 1250, 1875, 2800]
        self.writeVInt(len(list64))
        for value in list64:
            self.writeVInt(value)

        # list80 — packet byte 17376
        self.writeVInt(4)  # count

        # list80[0] — packet byte 17377
        self.writeVInt(30)  # 

        # list80[1] — packet byte 17378
        self.writeVInt(80)  # 

        # list80[2] — packet byte 17380
        self.writeVInt(170)  # 

        # list80[3] — packet byte 17382
        self.writeVInt(360)  # 

        # list96 — packet byte 17384
        self.writeVInt(4)  # count

        # list96[0] — packet byte 17385
        self.writeVInt(300)  # 

        # list96[1] — packet byte 17387
        self.writeVInt(880)  # 

        # list96[2] — packet byte 17389
        self.writeVInt(2040)  # 

        # list96[3] — packet byte 17391
        self.writeVInt(4680)  # 

        # ReleaseEntry
        self.writeVInt(0)

        token_reward_milestones = [
            (501, 10008), (2, 10012), (5000, 10027), (5000, 10028), (1, 10033),
            (2000, 10035), (1, 10040), (0, 10051), (6900, 10060), (200, 127),
            (1, 134), (1, 203), (5, 576), (29001846, 640), (41000246, 1),
            (3, 16000246), (1000, 517), (0, 204), (1, 596), (0, 532),
            (0, 533), (100, 534), (1, 95), (1, 548), (40, 613),
            (1, 170), (1, 556), (2000, 557), (4000, 558), (1000018, 626),
            (29001543, 627), (29001548, 628), (29001544, 629), (1, 501), (29001549, 630),
            (10, 567), (29001545, 631), (100, 568), (29001550, 632), (2, 569),
            (29001751, 633), (200, 570), (29001844, 634), (10500, 122), (3, 571),
            (29001752, 635), (0, 572), (29001845, 636), (0, 573), (29001753, 637),
            (0, 574), (29001847, 638), (0, 575), (29001754, 639), (0, 212),
            (60051, 47), (1, 123), (200, 124), (60051, 48), (3, 50),
            (500, 1100), (500, 1101), (1, 1002), (500, 1102), (1, 36),
        ]
        self.writeVInt(len(token_reward_milestones))
        for field_4, field_0 in token_reward_milestones:
            self.writeVInt(field_4)
            self.writeVInt(field_0)

        # ConfTrophyProtectCard — packet byte 30674
        self.writeVInt(0)  # count

        # CustomEvent — packet byte 30675
        self.writeVInt(0)  # count

        # ShopChainOfferTheme — packet byte 30676
        self.writeVInt(1)  # count

        self._write_ConfData_ShopChainOfferTheme_layout18(('', (69, 13), True, '全新皮肤！', 0, 1, -439988, 942411, (29, 2060), True, '超值礼包！', 0, True, True, '3986f7ed648246e7f103f0b49b6b55ebce6f869a', '/f9643507-4a49-4df7-a961-75821830d845_theme_brawloween26.sc', 0, ''))

        # AdPlacement — packet byte 30849
        self.writeVInt(0)  # count

        # ThemeOverride — packet byte 30850
        self.writeVInt(0)  # count

        # JoinClubEvent — packet byte 30851
        self.writeVInt(0)  # count

        fortune_cookies = [
            '【巧劲破敌】精准出手抵千击',
            '今日战局可谓传奇，愿你即将解锁的新英雄亦是如此',
            '乱斗必胜诀：远离草丛保平安',
            '宝石近在咫尺，犹如探囊取物',
            '草丛蹲人一时爽，一直蹲人...哎你宝石掉啦',
            '当个好队友，格局一下就打开了！',
            '点赞结善缘，怼人损人品~',
            '黄历有云：今日宜带萌新',
            '下期战队赛一定不划水！',
            '版本迭代如浮云，操作意识定乾坤',
            '一代版本一代神？不不不，我的本命英雄就是我自己！',
            '哪里有永恒的T0英雄~？',
            '纵使版本变迁，你的本命英雄永远在线',
            '最强英雄永远是下个宝箱里的（吗？）',
            '好朋友，可以从刚匹配的队友开始。',
            '一个邀请可能成就他的高光时刻~',
            '善待萌新，这是在帮助昨天的自己~',
            '“魔法有力量，下一句是什么？”去问问社区的玩家吧！',
            '“飒！”如果你觉得你很秀的时候可以说（虽然也没什么用）',
            '克制莫提斯最好的英雄是什么——墙',
            '荒野乱斗，启动！',
            '越乱斗，越幸运。',
            '屡败屡战，永不言弃。',
        ]
        self.writeVInt(1)
        self.writeVInt(0)
        self.writeVInt(len(fortune_cookies))
        for text in fortune_cookies:
            self.writeBoolean(True)
            self.writeString(text)
            self.writeVInt(0)
        self.writeVInt(1014405)
        self.writeVInt(1)

        # ChronosAsset — packet byte 32053
        self.writeVInt(2)  # count

        # ChronosAsset[0].entries — packet byte 32054
        self.writeVInt(1)  # count

        # ChronosAsset[0].entries[0].entry — packet byte 32055
        self.writeBoolean(True)  # present

        # ChronosAsset[0].entries[0].entry.files — packet byte 32056
        self.writeVInt(0)  # count

        # ChronosAsset[0].entries[0].entry — packet byte 32057
        self.writeDataReference(121, 20)  # native +0

        # ChronosAsset[0].entries[0].entry.file8 — packet byte 32060
        self.writeBoolean(True)  # present
        self.writeString('9ba00429980160d621cc2919f27b771fbb0d10b0')  # file16
        self.writeString('/3f5d9418-8acb-4014-a765-9c4beee29436_collab_brawloween_2026_02.sc')  # file0

        # ChronosAsset[0] — packet byte 32175
        self.writeVInt(3)  # native +24
        self.writeVInt(747651)  # native +4
        self.writeVInt(-289148)  # native +0

        # ChronosAsset[1].entries — packet byte 32182
        self.writeVInt(1)  # count

        # ChronosAsset[1].entries[0].entry — packet byte 32183
        self.writeBoolean(True)  # present

        # ChronosAsset[1].entries[0].entry.files — packet byte 32184
        self.writeVInt(0)  # count

        # ChronosAsset[1].entries[0].entry — packet byte 32185
        self.writeDataReference(121, 10)  # native +0

        # ChronosAsset[1].entries[0].entry.file8 — packet byte 32188
        self.writeBoolean(True)  # present
        self.writeString('e9f1bc76f0d1dac5b687d2344857cb68a0d29bfb')  # file16
        self.writeString('/58e2eaaa-bc4b-4835-a717-9b5fc1ee03ba_quests_theme_brawloween2026.sc')  # file0

        # ChronosAsset[1] — packet byte 32305
        self.writeVInt(2)  # native +24
        self.writeVInt(1525251)  # native +4
        self.writeVInt(-1495148)  # native +0

        # ShopVisualGrouping — packet byte 32314
        self.writeVInt(0)  # count

        list384 = [
            0, 29, 79, 169, 349, 699, 999,
        ]
        self.writeVInt(len(list384))
        for value in list384:
            self.writeVInt(value)

        # list400 — packet byte 32328
        self.writeVInt(0)  # count

        list112 = [
            0, 100, 400, 1000, 3000,
        ]
        self.writeVInt(len(list112))
        for value in list112:
            self.writeVInt(value)

        # list424 — packet byte 32339
        self.writeVInt(0)  # count

        # ConfData — packet byte 32340
        self.writeString('')  # native +472

        # NewsLinks — packet byte 32344
        self.writeVInt(0)  # count

        # StorePromos — packet byte 32345
        self.writeVInt(0)  # count

        # ConfData — packet byte 32346
        self.writeBoolean(False)  # native +480

        # StoreLink — packet byte 32347
        self.writeVInt(0)  # count

        # DailyWinTrack — packet byte 32348
        self.writeVInt(1)  # count

        # DailyWinTrack[0].text48 — packet byte 32349
        self.writeBoolean(False)  # present

        # DailyWinTrack[0] — packet byte 32350
        self.writeVInt(1021907)  # native +0

        # DailyWinTrack[0].dailyWinRewards — packet byte 32353
        self.writeVInt(6)  # count

        # DailyWinTrack[0].dailyWinRewards[0].dailyRewards — packet byte 32354
        self.writeBoolean(True)  # present

        # DailyWinTrack[0].dailyWinRewards[0].dailyRewards.rewards — packet byte 32355
        self.writeVInt(1)  # count

        # DailyWinTrack[0].dailyWinRewards[0].dailyRewards.rewards[0].reward — packet byte 32356
        self.writeBoolean(True)  # present
        self.writeVInt(83)  # type
        self.writeVInt(1)  # amount
        self.writeDataReference(0, 0)  # reference
        self.writeVInt(0)  # extra

        # DailyWinTrack[0].dailyWinRewards[1].dailyRewards — packet byte 32362
        self.writeBoolean(True)  # present

        # DailyWinTrack[0].dailyWinRewards[1].dailyRewards.rewards — packet byte 32363
        self.writeVInt(1)  # count

        # DailyWinTrack[0].dailyWinRewards[1].dailyRewards.rewards[0].reward — packet byte 32364
        self.writeBoolean(True)  # present
        self.writeVInt(50)  # type
        self.writeVInt(1)  # amount
        self.writeDataReference(0, 0)  # reference
        self.writeVInt(0)  # extra

        # DailyWinTrack[0].dailyWinRewards[2].dailyRewards — packet byte 32369
        self.writeBoolean(True)  # present

        # DailyWinTrack[0].dailyWinRewards[2].dailyRewards.rewards — packet byte 32370
        self.writeVInt(1)  # count

        # DailyWinTrack[0].dailyWinRewards[2].dailyRewards.rewards[0].reward — packet byte 32371
        self.writeBoolean(True)  # present
        self.writeVInt(50)  # type
        self.writeVInt(1)  # amount
        self.writeDataReference(0, 0)  # reference
        self.writeVInt(0)  # extra

        # DailyWinTrack[0].dailyWinRewards[3].dailyRewards — packet byte 32376
        self.writeBoolean(True)  # present

        # DailyWinTrack[0].dailyWinRewards[3].dailyRewards.rewards — packet byte 32377
        self.writeVInt(1)  # count

        # DailyWinTrack[0].dailyWinRewards[3].dailyRewards.rewards[0].reward — packet byte 32378
        self.writeBoolean(True)  # present
        self.writeVInt(50)  # type
        self.writeVInt(1)  # amount
        self.writeDataReference(0, 0)  # reference
        self.writeVInt(0)  # extra

        # DailyWinTrack[0].dailyWinRewards[4].dailyRewards — packet byte 32383
        self.writeBoolean(True)  # present

        # DailyWinTrack[0].dailyWinRewards[4].dailyRewards.rewards — packet byte 32384
        self.writeVInt(1)  # count

        # DailyWinTrack[0].dailyWinRewards[4].dailyRewards.rewards[0].reward — packet byte 32385
        self.writeBoolean(True)  # present
        self.writeVInt(50)  # type
        self.writeVInt(1)  # amount
        self.writeDataReference(0, 0)  # reference
        self.writeVInt(0)  # extra

        # DailyWinTrack[0].dailyWinRewards[5].dailyRewards — packet byte 32390
        self.writeBoolean(True)  # present

        # DailyWinTrack[0].dailyWinRewards[5].dailyRewards.rewards — packet byte 32391
        self.writeVInt(1)  # count

        # DailyWinTrack[0].dailyWinRewards[5].dailyRewards.rewards[0].reward — packet byte 32392
        self.writeBoolean(True)  # present
        self.writeVInt(50)  # type
        self.writeVInt(1)  # amount
        self.writeDataReference(0, 0)  # reference
        self.writeVInt(0)  # extra

        # DailyWinTrack[0] — packet byte 32397
        self.writeVInt(0)  # native +4

        # DailyWinTrack[0].dailyWinCounts — packet byte 32398
        self.writeVInt(6)  # count

        # DailyWinTrack[0].dailyWinCounts[0] — packet byte 32399
        self.writeVInt(1)  # 

        # DailyWinTrack[0].dailyWinCounts[1] — packet byte 32400
        self.writeVInt(2)  # 

        # DailyWinTrack[0].dailyWinCounts[2] — packet byte 32401
        self.writeVInt(3)  # 

        # DailyWinTrack[0].dailyWinCounts[3] — packet byte 32402
        self.writeVInt(4)  # 

        # DailyWinTrack[0].dailyWinCounts[4] — packet byte 32403
        self.writeVInt(5)  # 

        # DailyWinTrack[0].dailyWinCounts[5] — packet byte 32404
        self.writeVInt(6)  # 

        # DailyWinTrack[0] — packet byte 32405
        self.writeDataReference(158, 0)  # native +40

        # StorePayOverride — packet byte 32408
        self.writeVInt(0)  # count

        list440 = [1, 5, 39, 3, 6, 33, 43, 4, 15, 42, 41, 35, 40]
        self.writeVInt(len(list440))
        for value in list440:
            self.writeVInt(value)

        shop_tab_events = [
            (1093251, 1021975, -289148, [
                (('dfdc6c4a25f809ec9138b19aea4bae54e0d17708', '/81672593-ca7f-4686-b067-9f943d6cd93e_theme_vince.sc'), (175, 4), ('9b0d86e52613be1cfd2426e2b5c0c09539bda0af', '/4cec4968-005e-4952-a332-57a75c92cde6_bazaar_tab_button_time_limited_3_vince.ui'), ('3a6b4c132792a5e4d654395940a541f616e190ce', '/b33d2c4d-f582-4fa3-8e65-d8eca7b956b4_shop_tab_vince.sc'), '', (0, 0), '', ('VINCE', 0), '', '', None, ''),
            ]),
            (1525251, 1021974, -1498748, [
                (('44eee5e1dca6c05d11b8ab59feaff056ba9eacd0', '/627f0e53-2707-483e-8d0c-882d2889711c_shop_tab_halloween.sc'), (175, 1), ('9f7a99a3ef7447bbb59263d0479dc4c35ceb8b2f', '/37cddb69-5ed7-4230-8e26-58551f922a14_bazaar_tab_button_season_halloween.ui'), ('3986f7ed648246e7f103f0b49b6b55ebce6f869a', '/f9643507-4a49-4df7-a961-75821830d845_theme_brawloween26.sc'), '', (0, 0), '', ('乱斗万圣节！', 0), '', '', None, ''),
            ]),
            (1525251, 1021973, -1498748, [
                (('44eee5e1dca6c05d11b8ab59feaff056ba9eacd0', '/627f0e53-2707-483e-8d0c-882d2889711c_shop_tab_halloween.sc'), (175, 2), ('adc58676c255a2dda130b49335f18c6a583fb972', '/c7662c69-c6e9-4525-8faf-2a81d3b813b3_bazaar_tab_button_tl1_halloween.ui'), ('3986f7ed648246e7f103f0b49b6b55ebce6f869a', '/f9643507-4a49-4df7-a961-75821830d845_theme_brawloween26.sc'), '', (0, 0), '', ('乱斗万圣节皮肤！', 0), '', '', None, ''),
            ]),
            (74706051, 1021172, -15668348, [
                (('48c04126876737cc94e96b4e1ab218d11d0463fe', '/71b45262-8f9c-4615-8c18-8bd2462e279b_theme_fantasy.sc'), (175, 0), None, None, '', (0, 0), '', ('精选特惠！', 0), '', '', None, ''),
                (None, (175, 4), None, None, '', (0, 0), '', ('文斯来啦！', 0), '', '', None, ''),
                (None, (175, 5), None, None, '', (0, 0), '', ('奇物商店！', 0), '', '', None, ''),
                (None, (175, 6), None, None, '', (0, 0), '', ('资源', 0), '', '', None, ''),
            ]),
            (1148871, 1021895, -2566328, [
                (None, (175, 3), None, None, '', (0, 0), '', ('懂你意思!', 0), '', '', None, ''),
            ]),
        ]

        def write_file(entry):
            self.writeBoolean(entry is not None)
            if entry is not None:
                self.writeString(entry[0])
                self.writeString(entry[1])

        self.writeVInt(len(shop_tab_events))
        for field_8, field_0, field_4, tabs in shop_tab_events:
            self.writeVInt(field_8)
            self.writeVInt(field_0)
            self.writeVInt(len(tabs))
            for tab in tabs:
                self.writeBoolean(tab is not None)
                if tab is None:
                    continue
                (file_104, reference_0, file_112, file_120, string_64,
                 reference_96, string_32, text_8, string_16, string_80,
                 file_128, string_48) = tab
                write_file(file_104)
                self.writeDataReference(*reference_0)
                write_file(file_112)
                write_file(file_120)
                self.writeString(string_64)
                self.writeDataReference(*reference_96)
                self.writeString(string_32)
                self.writeBoolean(text_8 is not None)
                if text_8 is not None:
                    self.writeString(text_8[0])
                    self.writeVInt(text_8[1])
                self.writeString(string_16)
                self.writeString(string_80)
                write_file(file_128)
                self.writeString(string_48)
            self.writeVInt(field_4)

    def writeHeroGears(self):
        # LogicHeroGears.decode (0x1013B58D8) reads two hero gear lists.
        # Send ownership and two equipped slots in both lists.
        for _ in range(2):
            self.writeVInt(len(_BRAWLER_UNLOCK_CARDS))
            for _, hero_id in _BRAWLER_UNLOCK_CARDS:
                self.writeDataReference(16, hero_id)
                self.writeVInt(len(_GEAR_IDS))
                for gear_id in _GEAR_IDS:
                    self.writeDataReference(62, gear_id)
                self.writeVInt(2)  # equipped slots
                self.writeDataReference(62, _GEAR_IDS[0])
                self.writeDataReference(62, _GEAR_IDS[1])

    def writeLogicClientHome(self, player):
        """Native decode 0x1013B7BA0 (after DailyData/ConfData); packet starts at byte 33964."""

        # Home — packet byte 33964
        self.writeLong(player.ID[0], player.ID[1])  # id

        # notifications — packet byte 33972
        self.writeVInt(0)  # count

        # Home — packet byte 33973
        self.writeVInt(-1)  # native +76
        self.writeBoolean(False)  # native +72

        # gachaDrops — packet byte 33975
        self.writeVInt(0)  # count

        # refs96 — packet byte 33976
        self.writeVInt(0)  # count

        # referencePairs — packet byte 33977
        self.writeVInt(0)  # count

        # calendar152 — packet byte 33978
        self.writeBoolean(False)  # present

        # calendar160 — packet byte 33979
        self.writeBoolean(False)  # present

        # calendar168 — packet byte 33979
        self.writeBoolean(False)  # present

        # calendar176 — packet byte 33979
        self.writeBoolean(False)  # present

        self.writeHeroGears()

        # RecruitRoad: no brawlers available or selected
        self.writeBoolean(True)
        self.writeVInt(0)  # refs8
        self.writeVInt(0)  # refs16
        self.writeDataReference(0, 0)  # selected brawler
        self.writeVInt(0)  # entries32
        self.writeVInt(0)  # entries40
        self.writeVInt(2)  # longs48
        self.writeVLong(4, 50)
        self.writeVLong(5, 50)
        self.writeVInt(0)  # native +56
        self.writeVInt(0)  # native +60
        self.writeVInt(0)  # refs64
        self.writeVInt(0)  # native +72
        self.writeVInt(0)  # list80
        self.writeVInt(0)  # native +88
        self.writeBoolean(False)  # native +92
        self.writeBoolean(True)  # native +93
        self.writeVInt(0)  # native +96
        self.writeVInt(0)  # native +100

        # masteries — packet byte 38017
        self.writeVInt(0)  # count

        # Home — packet byte 38018
        self.writeDataReference(0, 0)  # native +0
        self.writeDataReference(0, 0)  # native +8
        self.writeDataReference(0, 0)  # native +16
        self.writeDataReference(0, 0)  # native +24
        self.writeDataReference(0, 0)  # native +32
        self.writeDataReference(0, 0)  # native +40
        self.writeBoolean(False)  # native +48
        self.writeBoolean(False)  # native +49
        self.writeBoolean(False)  # native +50
        self.writeBoolean(False)  # native +51
        self.writeBoolean(False)  # native +52

        # heroBattleIntros — packet byte 38025
        self.writeVInt(0)  # count

        # slots — packet byte 38026
        self.writeVInt(0)  # count

        # claimables — packet byte 38027
        self.writeVInt(0)  # count

        # Home — packet byte 38028
        self.writeInt(-2144854853)  # seed
        self.writeBoolean(False)  # native +40
        self.writeVInt(0)  # native +44
        self.writeVInt(0)  # native +48
        self.writeVInt(56451)  # native +64

        # list72 — packet byte 38038
        self.writeVInt(0)  # count

        # Home — packet byte 38039
        self.writeVInt(0)  # native +88

        # list96 — packet byte 38040
        self.writeVInt(0)  # count

        # list112 — packet byte 38041
        self.writeVInt(0)  # count

        # Home — packet byte 38042
        self.writeVInt(1)  # native +200
        self.writeVInt(1)  # native +204
        self.writeVInt(1)  # native +208

        # list128 — packet byte 38045
        self.writeVInt(0)  # count

        # Home — packet byte 38046
        self.writeVInt(0)  # native +176
        self.writeBoolean(False)  # native +180

        # slots2 — packet byte 38048
        self.writeVInt(0)  # count

        # ContainerRewardsGiven — packet byte 38049
        self.writeVInt(0)  # count

        # slots3 — packet byte 38050
        self.writeVInt(0)  # count

        # AlliancePiggyBank — packet byte 38051
        self.writeBoolean(False)  # present

        # CollabEvent — packet byte 38052
        self.writeBoolean(False)  # present

        # SpecialEvent — packet byte 38052
        self.writeBoolean(False)  # present

        # seenStates — packet byte 38052
        self.writeVInt(1)  # count

        # seenStates[0] — packet byte 38053
        self.writeDataReference(118, 13)  # native +0
        self.writeVInt(1)  # native +8

        # ContestEvent — packet byte 38057
        self.writeBoolean(False)  # present

        # K2FreeHero — packet byte 38058
        self.writeBoolean(True)  # present
        self.writeVInt(0)  # native +0
        self.writeVInt(0)  # native +4
        self.writeVInt(0)  # native +8

        # K2FreeHero.gears — packet byte 38061
        self.writeVInt(0)  # count

        # K2BrawlPower — packet byte 38062
        self.writeBoolean(True)  # present
        self.writeVInt(2)  # slotCount

        # K2BrawlPower.slot0 — packet byte 38064
        self.writeBoolean(False)  # present

        # K2BrawlPower.slot1 — packet byte 38065
        self.writeBoolean(False)  # present

        # heroEntries — packet byte 38065
        self.writeVInt(0)  # count

        # PlayerRecords — packet byte 38066
        self.writeBoolean(False)  # present

        # SpecialRushEvent — packet byte 38067
        self.writeBoolean(False)  # present

        # EarlyAccessEvent — packet byte 38067
        self.writeBoolean(False)  # present

        # Block280 — packet byte 38067
        self.writeBoolean(True)  # present
        self.writeVInt(0)  # native +4
        self.writeVInt(0)  # native +0

        # Block352 — packet byte 38069
        self.writeBoolean(False)  # present

        # specialEvents — packet byte 38070
        self.writeVInt(0)  # count

        # CollabEvent2 — packet byte 38071
        self.writeBoolean(False)  # present

        # rogueliteEvents — packet byte 38072
        self.writeVInt(0)  # count

        # BuddyGacha — packet byte 38073
        self.writeBoolean(False)  # present

        # Home — packet byte 38074
        self.writeBoolean(False)  # native +384

        # Block288 — packet byte 38074
        self.writeBoolean(True)  # present
        self.writeBoolean(False)  # native +4
        self.writeVInt(0)  # native +8
        self.writeBoolean(False)  # native +12
        self.writeVInt(0)  # native +0

    def writeLogicClientAvatar(self, player):
        """Native decode 0x10125FE20; packet starts at byte 38077."""

        # Avatar — packet byte 38077
        self.writeVLong(player.ID[0], player.ID[1])  # id
        self.writeVLong(player.ID[0], player.ID[1])  # home_id
        self.writeVLong(player.ID[0], player.ID[1])  # third_id
        self.writeString(player.Name)  # name
        self.writeBoolean(player.Registered)  # name_set
        self.writeInt(-1)  # native +828
        self.writeVInt(43)  # commodityCount

        # commodities[0].array — packet byte 38113
        self.writeVInt(0)  # count

        # Owned cards and currencies (Avatar commodity group 0)
        slots = {
            (5, 8): (-1, 99999),
            (5, 23): (-1, 4564),
            (5, 38): (-1, 1),
            (23, 0): (-1, 1),
            (23, 24): (-1, 1),
            (23, 40): (-1, 1),
            (23, 52): (-1, 1),
            (23, 125): (-1, 1),
        }
        for card_id, _ in _BRAWLER_UNLOCK_CARDS:
            previous = slots.get((23, card_id), (-1, 0))
            slots[(23, card_id)] = (previous[0], max(1, previous[1]))
        self.writeVInt(len(slots))
        for (table, row), (value, count) in slots.items():
            self.writeDataReference(table, row)
            self.writeVInt(value)
            self.writeVInt(count)

        # Current and highest trophies for every unlocked brawler.
        for _ in range(2):  # commodity groups 1 and 2
            self.writeVInt(0)  # array count
            self.writeVInt(len(_BRAWLER_UNLOCK_CARDS))  # map count
            for _, hero_id in _BRAWLER_UNLOCK_CARDS:
                self.writeDataReference(16, hero_id)
                self.writeVInt(-1)
                self.writeVInt(3000)

        # commodities[3].array — packet byte 38162
        self.writeVInt(0)  # count

        # commodities[3].map — packet byte 38163
        self.writeVInt(0)  # count

        # commodities[4].array — packet byte 38164
        self.writeVInt(0)  # count

        # commodities[4].map — packet byte 38165
        self.writeVInt(4)  # count

        # commodities[4].map[0] — packet byte 38166
        self.writeDataReference(16, 6)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(310)  # count

        # commodities[4].map[1] — packet byte 38171
        self.writeDataReference(16, 10)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(50)  # count

        # commodities[4].map[2] — packet byte 38175
        self.writeDataReference(16, 13)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(0)  # count

        # commodities[4].map[3] — packet byte 38180
        self.writeDataReference(16, 25)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(180)  # count

        # commodities[5].array — packet byte 38185
        self.writeVInt(0)  # count

        # Power level 11: native commodity group 5 stores level minus one.
        self.writeVInt(len(_BRAWLER_UNLOCK_CARDS))
        for _, hero_id in _BRAWLER_UNLOCK_CARDS:
            self.writeDataReference(16, hero_id)
            self.writeVInt(-1)
            self.writeVInt(10)

        # Client ownership: sub_101260EFC reads commodity 6, state 1 or 2.
        # Selection: sub_101261E40 tests state 2 (one per hero and MetaType).
        self.writeVInt(0)  # array count
        self.writeVInt(len(_BRAWLER_EQUIPMENT_CARDS))
        selected = set()
        for card_id in _BRAWLER_EQUIPMENT_CARDS:
            card = _CARDS[card_id]
            key = (card['Target'], card['MetaType'])
            state = 1 if key in selected else 2
            selected.add(key)
            self.writeDataReference(23, card_id)
            self.writeVInt(-1)
            self.writeVInt(state)

        # commodities[7].array — packet byte 38210
        self.writeVInt(0)  # count

        # commodities[7].map — packet byte 38211
        self.writeVInt(5)  # count

        # commodities[7].map[0] — packet byte 38212
        self.writeDataReference(16, 0)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(2)  # count

        # commodities[7].map[1] — packet byte 38216
        self.writeDataReference(16, 6)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(2)  # count

        # commodities[7].map[2] — packet byte 38220
        self.writeDataReference(16, 10)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(2)  # count

        # commodities[7].map[3] — packet byte 38224
        self.writeDataReference(16, 13)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(2)  # count

        # commodities[7].map[4] — packet byte 38228
        self.writeDataReference(16, 25)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(2)  # count

        # commodities[8].array — packet byte 38232
        self.writeVInt(0)  # count

        # commodities[8].map — packet byte 38233
        self.writeVInt(0)  # count

        # commodities[9].array — packet byte 38234
        self.writeVInt(0)  # count

        # commodities[9].map — packet byte 38235
        self.writeVInt(0)  # count

        # commodities[10].array — packet byte 38236
        self.writeVInt(0)  # count

        # commodities[10].map — packet byte 38237
        self.writeVInt(0)  # count

        # commodities[11].array — packet byte 38238
        self.writeVInt(0)  # count

        # commodities[11].map — packet byte 38239
        self.writeVInt(0)  # count

        # commodities[12].array — packet byte 38240
        self.writeVInt(0)  # count

        # commodities[12].map — packet byte 38241
        self.writeVInt(0)  # count

        # commodities[13].array — packet byte 38242
        self.writeVInt(0)  # count

        # commodities[13].map — packet byte 38243
        self.writeVInt(0)  # count

        # commodities[14].array — packet byte 38244
        self.writeVInt(0)  # count

        # commodities[14].map — packet byte 38245
        self.writeVInt(0)  # count

        # commodities[15].array — packet byte 38246
        self.writeVInt(0)  # count

        # commodities[15].map — packet byte 38247
        self.writeVInt(0)  # count

        # commodities[16].array — packet byte 38248
        self.writeVInt(0)  # count

        # commodities[16].map — packet byte 38249
        self.writeVInt(4)  # count

        # commodities[16].map[0] — packet byte 38250
        self.writeDataReference(16, 6)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(124209476)  # count

        # commodities[16].map[1] — packet byte 38257
        self.writeDataReference(16, 10)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(124209462)  # count

        # commodities[16].map[2] — packet byte 38264
        self.writeDataReference(16, 13)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(124209395)  # count

        # commodities[16].map[3] — packet byte 38271
        self.writeDataReference(16, 25)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(124209510)  # count

        # commodities[17].array — packet byte 38278
        self.writeVInt(0)  # count

        # commodities[17].map — packet byte 38279
        self.writeVInt(0)  # count

        # commodities[18].array — packet byte 38280
        self.writeVInt(0)  # count

        # commodities[18].map — packet byte 38281
        self.writeVInt(0)  # count

        # commodities[19].array — packet byte 38282
        self.writeVInt(0)  # count

        # commodities[19].map — packet byte 38283
        self.writeVInt(0)  # count

        # commodities[20].array — packet byte 38284
        self.writeVInt(0)  # count

        # commodities[20].map — packet byte 38285
        self.writeVInt(0)  # count

        # commodities[21].array — packet byte 38286
        self.writeVInt(0)  # count

        # commodities[21].map — packet byte 38287
        self.writeVInt(0)  # count

        # commodities[22].array — packet byte 38288
        self.writeVInt(0)  # count

        # commodities[22].map — packet byte 38289
        self.writeVInt(1)  # count

        # commodities[22].map[0] — packet byte 38290
        self.writeDataReference(16, 0)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(3000)  # count

        # commodities[23].array — packet byte 38294
        self.writeVInt(0)  # count

        # commodities[23].map — packet byte 38295
        self.writeVInt(0)  # count

        # commodities[24].array — packet byte 38296
        self.writeVInt(0)  # count

        # commodities[24].map — packet byte 38297
        self.writeVInt(0)  # count

        # commodities[25].array — packet byte 38298
        self.writeVInt(0)  # count

        # commodities[25].map — packet byte 38299
        self.writeVInt(0)  # count

        # commodities[26].array — packet byte 38300
        self.writeVInt(0)  # count

        # commodities[26].map — packet byte 38301
        self.writeVInt(0)  # count

        # commodities[27].array — packet byte 38302
        self.writeVInt(0)  # count

        # commodities[27].map — packet byte 38303
        self.writeVInt(0)  # count

        # commodities[28].array — packet byte 38304
        self.writeVInt(0)  # count

        # commodities[28].map — packet byte 38305
        self.writeVInt(0)  # count

        # commodities[29].array — packet byte 38306
        self.writeVInt(0)  # count

        # commodities[29].map — packet byte 38307
        self.writeVInt(0)  # count

        # commodities[30].array — packet byte 38308
        self.writeVInt(0)  # count

        # commodities[30].map — packet byte 38309
        self.writeVInt(0)  # count

        # commodities[31].array — packet byte 38310
        self.writeVInt(0)  # count

        # commodities[31].map — packet byte 38311
        self.writeVInt(0)  # count

        # commodities[32].array — packet byte 38312
        self.writeVInt(0)  # count

        # commodities[32].map — packet byte 38313
        self.writeVInt(0)  # count

        # commodities[33].array — packet byte 38314
        self.writeVInt(0)  # count

        # commodities[33].map — packet byte 38315
        self.writeVInt(0)  # count

        # commodities[34].array — packet byte 38316
        self.writeVInt(0)  # count

        # commodities[34].map — packet byte 38317
        self.writeVInt(0)  # count

        # commodities[35].array — packet byte 38318
        self.writeVInt(0)  # count

        # commodities[35].map — packet byte 38319
        self.writeVInt(0)  # count

        # commodities[36].array — packet byte 38320
        self.writeVInt(0)  # count

        # commodities[36].map — packet byte 38321
        self.writeVInt(0)  # count

        # Buffies owned: commodity group 37.
        self.writeVInt(0)  # array count
        self.writeVInt(len(_BUFFY_CARDS_BY_GROUP[37]))
        for card_id in _BUFFY_CARDS_BY_GROUP[37]:
            self.writeDataReference(23, card_id)
            self.writeVInt(-1)
            self.writeVInt(1)  # owned

        # Buffies owned: commodity group 38.
        self.writeVInt(0)  # array count
        self.writeVInt(len(_BUFFY_CARDS_BY_GROUP[38]))
        for card_id in _BUFFY_CARDS_BY_GROUP[38]:
            self.writeDataReference(23, card_id)
            self.writeVInt(-1)
            self.writeVInt(1)  # owned

        # Buffies owned: commodity group 39.
        self.writeVInt(0)  # array count
        self.writeVInt(len(_BUFFY_CARDS_BY_GROUP[39]))
        for card_id in _BUFFY_CARDS_BY_GROUP[39]:
            self.writeDataReference(23, card_id)
            self.writeVInt(-1)
            self.writeVInt(1)  # owned

        # commodities[40].array — packet byte 38328
        self.writeVInt(0)  # count

        # commodities[40].map — packet byte 38329
        self.writeVInt(1)  # count

        # commodities[40].map[0] — packet byte 38330
        self.writeDataReference(16, 0)  # reference
        self.writeVInt(-1)  # value
        self.writeVInt(3000)  # count

        # commodities[41].array — packet byte 38334
        self.writeVInt(0)  # count

        # commodities[41].map — packet byte 38335
        self.writeVInt(0)  # count

        # commodities[42].array — packet byte 38336
        self.writeVInt(0)  # count

        # commodities[42].map — packet byte 38337
        self.writeVInt(0)  # count

        # Avatar — packet byte 38338
        self.writeVInt(99999)  # native +780
        self.writeVInt(99999)  # native +784
        self.writeVInt(1)  # native +772
        self.writeVInt(100)  # native +776
        self.writeVInt(0)  # native +788
        self.writeVInt(0)  # native +800
        self.writeVInt(0)  # native +804
        self.writeVInt(0)  # native +808
        self.writeVInt(0)  # native +812
        self.writeVInt(0)  # native +816
        self.writeVInt(0)  # native +820
        self.writeVInt(2)  # native +832
        self.writeVInt(0)  # native +836
        self.writeVInt(2)  # privacy
        self.writeVInt(15)  # native +848
        self.writeString('orog61TdaSys-ug98Nf7ysaaTPPg')  # native +856
        self.writeVInt(1)  # native +864
        self.writeVInt(0)  # native +872
        self.writeVInt(1)  # native +868
        self.writeVInt(100)  # native +880
        self.writeVInt(0)  # native +888
        self.writeVInt(0)  # native +892
        self.writeVInt(0)  # native +896
        self.writeVInt(-1)  # native +900

        # Gallery — packet byte 38395
        self.writeBoolean(True)  # present

        # Gallery.items — packet byte 38396
        self.writeVInt(0)  # count

        # Gallery — packet byte 38397
        self.writeVInt(0)  # native +40
        self.writeVInt(0)  # native +44

        # Avatar — packet byte 38399
        self.writeVInt(0)  # native +904
        self.writeBoolean(False)  # native +884
        self.writeVInt(0)  # native +908
        self.writeBoolean(False)  # native +885









    def _write_ConfData_events16_layout8(self, values):
        """events16: fields in native wire order."""
        (
            vInt_0,
            vInt_4,
            vInt_8,
            vInt_12,
            vInt_16,
            vInt_20,
            dataReference_24,
            dataReference_32,
            vInt_40,
            string_48,
            vInt_56,
            vInt_60,
            vInt_64,
            vInt_list72_count,
            vInt_88,
            vInt_100,
            boolean_104,
            boolean_map152_present,
            vInt_68,
            boolean_settings160_present,
            vInt_92,
            vInt_96,
            boolean_text112_present,
            boolean_text120_present,
            boolean_text128_present,
            boolean_reward168_present,
            vInt_list80_count,
            boolean_file136_present,
            dataReference_144,
            boolean_event176_present,
            vInt_refs192_count,
            vInt_refs216_count,
            vInt_refs224_count,
            vInt_refs200_count,
            vInt_list208_count,
            vInt_232,
            boolean_event240_present,
            boolean_event248_present,
            boolean_event256_present,
            boolean_event264_present,
            boolean_event272_present,
            boolean_event280_present,
            boolean_event288_present,
            boolean_event296_present,
        ) = values
        self.writeVInt(vInt_0)  # native +0
        self.writeVInt(vInt_4)  # native +4
        self.writeVInt(vInt_8)  # native +8
        self.writeVInt(vInt_12)  # native +12
        self.writeVInt(vInt_16)  # native +16
        self.writeVInt(vInt_20)  # native +20
        self.writeDataReference(*dataReference_24)  # native +24
        self.writeDataReference(*dataReference_32)  # native +32
        self.writeVInt(vInt_40)  # native +40
        self.writeString(string_48)  # native +48
        self.writeVInt(vInt_56)  # native +56
        self.writeVInt(vInt_60)  # native +60
        self.writeVInt(vInt_64)  # native +64
        self.writeVInt(vInt_list72_count)  # list72.count
        self.writeVInt(vInt_88)  # native +88
        self.writeVInt(vInt_100)  # native +100
        self.writeBoolean(boolean_104)  # native +104
        self.writeBoolean(boolean_map152_present)  # map152.present
        self.writeVInt(vInt_68)  # native +68
        self.writeBoolean(boolean_settings160_present)  # settings160.present
        self.writeVInt(vInt_92)  # native +92
        self.writeVInt(vInt_96)  # native +96
        self.writeBoolean(boolean_text112_present)  # text112.present
        self.writeBoolean(boolean_text120_present)  # text120.present
        self.writeBoolean(boolean_text128_present)  # text128.present
        self.writeBoolean(boolean_reward168_present)  # reward168.present
        self.writeVInt(vInt_list80_count)  # list80.count
        self.writeBoolean(boolean_file136_present)  # file136.present
        self.writeDataReference(*dataReference_144)  # native +144
        self.writeBoolean(boolean_event176_present)  # event176.present
        self.writeVInt(vInt_refs192_count)  # refs192.count
        self.writeVInt(vInt_refs216_count)  # refs216.count
        self.writeVInt(vInt_refs224_count)  # refs224.count
        self.writeVInt(vInt_refs200_count)  # refs200.count
        self.writeVInt(vInt_list208_count)  # list208.count
        self.writeVInt(vInt_232)  # native +232
        self.writeBoolean(boolean_event240_present)  # event240.present
        self.writeBoolean(boolean_event248_present)  # event248.present
        self.writeBoolean(boolean_event256_present)  # event256.present
        self.writeBoolean(boolean_event264_present)  # event264.present
        self.writeBoolean(boolean_event272_present)  # event272.present
        self.writeBoolean(boolean_event280_present)  # event280.present
        self.writeBoolean(boolean_event288_present)  # event288.present
        self.writeBoolean(boolean_event296_present)  # event296.present

    def _write_ConfData_events16_layout9(self, values):
        """events16: fields in native wire order."""
        (
            vInt_0,
            vInt_4,
            vInt_8,
            vInt_12,
            vInt_16,
            vInt_20,
            dataReference_24,
            dataReference_32,
            vInt_40,
            string_48,
            vInt_56,
            vInt_60,
            vInt_64,
            vInt_list72_count,
            vInt_88,
            vInt_100,
            boolean_104,
            boolean_map152_present,
            vLong_map152_0,
            string_map152_8,
            vInt_map152_16,
            dataReference_map152_24,
            dataReference_map152_32,
            bytes_map152_map_data,
            vLong_map152_48,
            string_map152_56,
            vInt_map152_64,
            vInt_map152_longs72_count,
            vInt_68,
            boolean_settings160_present,
            vInt_92,
            vInt_96,
            boolean_text112_present,
            boolean_text120_present,
            boolean_text128_present,
            boolean_reward168_present,
            vInt_list80_count,
            boolean_file136_present,
            dataReference_144,
            boolean_event176_present,
            vInt_refs192_count,
            vInt_refs216_count,
            vInt_refs224_count,
            vInt_refs200_count,
            vInt_list208_count,
            vInt_232,
            boolean_event240_present,
            boolean_event248_present,
            boolean_event256_present,
            boolean_event264_present,
            boolean_event272_present,
            boolean_event280_present,
            boolean_event288_present,
            boolean_event296_present,
        ) = values
        self.writeVInt(vInt_0)  # native +0
        self.writeVInt(vInt_4)  # native +4
        self.writeVInt(vInt_8)  # native +8
        self.writeVInt(vInt_12)  # native +12
        self.writeVInt(vInt_16)  # native +16
        self.writeVInt(vInt_20)  # native +20
        self.writeDataReference(*dataReference_24)  # native +24
        self.writeDataReference(*dataReference_32)  # native +32
        self.writeVInt(vInt_40)  # native +40
        self.writeString(string_48)  # native +48
        self.writeVInt(vInt_56)  # native +56
        self.writeVInt(vInt_60)  # native +60
        self.writeVInt(vInt_64)  # native +64
        self.writeVInt(vInt_list72_count)  # list72.count
        self.writeVInt(vInt_88)  # native +88
        self.writeVInt(vInt_100)  # native +100
        self.writeBoolean(boolean_104)  # native +104
        self.writeBoolean(boolean_map152_present)  # map152.present
        self.writeVLong(*vLong_map152_0)  # map152.0
        self.writeString(string_map152_8)  # map152.8
        self.writeVInt(vInt_map152_16)  # map152.16
        self.writeDataReference(*dataReference_map152_24)  # map152.24
        self.writeDataReference(*dataReference_map152_32)  # map152.32
        self.writeBytes(bytes(bytes_map152_map_data), len(bytes_map152_map_data))  # map152.map_data
        self.writeVLong(*vLong_map152_48)  # map152.48
        self.writeString(string_map152_56)  # map152.56
        self.writeVInt(vInt_map152_64)  # map152.64
        self.writeVInt(vInt_map152_longs72_count)  # map152.longs72.count
        self.writeVInt(vInt_68)  # native +68
        self.writeBoolean(boolean_settings160_present)  # settings160.present
        self.writeVInt(vInt_92)  # native +92
        self.writeVInt(vInt_96)  # native +96
        self.writeBoolean(boolean_text112_present)  # text112.present
        self.writeBoolean(boolean_text120_present)  # text120.present
        self.writeBoolean(boolean_text128_present)  # text128.present
        self.writeBoolean(boolean_reward168_present)  # reward168.present
        self.writeVInt(vInt_list80_count)  # list80.count
        self.writeBoolean(boolean_file136_present)  # file136.present
        self.writeDataReference(*dataReference_144)  # native +144
        self.writeBoolean(boolean_event176_present)  # event176.present
        self.writeVInt(vInt_refs192_count)  # refs192.count
        self.writeVInt(vInt_refs216_count)  # refs216.count
        self.writeVInt(vInt_refs224_count)  # refs224.count
        self.writeVInt(vInt_refs200_count)  # refs200.count
        self.writeVInt(vInt_list208_count)  # list208.count
        self.writeVInt(vInt_232)  # native +232
        self.writeBoolean(boolean_event240_present)  # event240.present
        self.writeBoolean(boolean_event248_present)  # event248.present
        self.writeBoolean(boolean_event256_present)  # event256.present
        self.writeBoolean(boolean_event264_present)  # event264.present
        self.writeBoolean(boolean_event272_present)  # event272.present
        self.writeBoolean(boolean_event280_present)  # event280.present
        self.writeBoolean(boolean_event288_present)  # event288.present
        self.writeBoolean(boolean_event296_present)  # event296.present

    def _write_ConfData_events16_layout10(self, values):
        """events16: fields in native wire order."""
        (
            vInt_0,
            vInt_4,
            vInt_8,
            vInt_12,
            vInt_16,
            vInt_20,
            dataReference_24,
            dataReference_32,
            vInt_40,
            string_48,
            vInt_56,
            vInt_60,
            vInt_64,
            vInt_list72_count,
            vInt_88,
            vInt_100,
            boolean_104,
            boolean_map152_present,
            vInt_68,
            boolean_settings160_present,
            vInt_settings160_8,
            string_settings160_16,
            vInt_settings160_24,
            vInt_settings160_28,
            vInt_settings160_32,
            vInt_settings160_ranks40_count,
            vInt_settings160_ranges56_count,
            vInt_settings160_ranges72_count,
            vInt_settings160_list88_count,
            vInt_settings160_list88_0,
            vInt_settings160_list88_1,
            vInt_settings160_list88_2,
            dataReference_settings160_104,
            vInt_settings160_list112_count,
            vInt_settings160_128,
            vInt_92,
            vInt_96,
            boolean_text112_present,
            string_text112_text,
            vInt_text112_id,
            boolean_text120_present,
            boolean_text128_present,
            string_text128_text,
            vInt_text128_id,
            boolean_reward168_present,
            vInt_list80_count,
            boolean_file136_present,
            dataReference_144,
            boolean_event176_present,
            vInt_refs192_count,
            dataReference_refs192_0,
            dataReference_refs192_1,
            dataReference_refs192_2,
            dataReference_refs192_3,
            dataReference_refs192_4,
            dataReference_refs192_5,
            dataReference_refs192_6,
            dataReference_refs192_7,
            dataReference_refs192_8,
            dataReference_refs192_9,
            dataReference_refs192_10,
            dataReference_refs192_11,
            dataReference_refs192_12,
            dataReference_refs192_13,
            dataReference_refs192_14,
            dataReference_refs192_15,
            dataReference_refs192_16,
            dataReference_refs192_17,
            dataReference_refs192_18,
            dataReference_refs192_19,
            dataReference_refs192_20,
            dataReference_refs192_21,
            dataReference_refs192_22,
            dataReference_refs192_23,
            dataReference_refs192_24,
            dataReference_refs192_25,
            dataReference_refs192_26,
            dataReference_refs192_27,
            vInt_refs216_count,
            vInt_refs224_count,
            vInt_refs200_count,
            vInt_list208_count,
            vInt_list208_0,
            vInt_232,
            boolean_event240_present,
            boolean_event248_present,
            boolean_event256_present,
            boolean_event264_present,
            boolean_event272_present,
            boolean_event280_present,
            boolean_event288_present,
            boolean_event296_present,
        ) = values
        self.writeVInt(vInt_0)  # native +0
        self.writeVInt(vInt_4)  # native +4
        self.writeVInt(vInt_8)  # native +8
        self.writeVInt(vInt_12)  # native +12
        self.writeVInt(vInt_16)  # native +16
        self.writeVInt(vInt_20)  # native +20
        self.writeDataReference(*dataReference_24)  # native +24
        self.writeDataReference(*dataReference_32)  # native +32
        self.writeVInt(vInt_40)  # native +40
        self.writeString(string_48)  # native +48
        self.writeVInt(vInt_56)  # native +56
        self.writeVInt(vInt_60)  # native +60
        self.writeVInt(vInt_64)  # native +64
        self.writeVInt(vInt_list72_count)  # list72.count
        self.writeVInt(vInt_88)  # native +88
        self.writeVInt(vInt_100)  # native +100
        self.writeBoolean(boolean_104)  # native +104
        self.writeBoolean(boolean_map152_present)  # map152.present
        self.writeVInt(vInt_68)  # native +68
        self.writeBoolean(boolean_settings160_present)  # settings160.present
        self.writeVInt(vInt_settings160_8)  # settings160.8
        self.writeString(string_settings160_16)  # settings160.16
        self.writeVInt(vInt_settings160_24)  # settings160.24
        self.writeVInt(vInt_settings160_28)  # settings160.28
        self.writeVInt(vInt_settings160_32)  # settings160.32
        self.writeVInt(vInt_settings160_ranks40_count)  # settings160.ranks40.count
        self.writeVInt(vInt_settings160_ranges56_count)  # settings160.ranges56.count
        self.writeVInt(vInt_settings160_ranges72_count)  # settings160.ranges72.count
        self.writeVInt(vInt_settings160_list88_count)  # settings160.list88.count
        self.writeVInt(vInt_settings160_list88_0)  # settings160.list88[0].
        self.writeVInt(vInt_settings160_list88_1)  # settings160.list88[1].
        self.writeVInt(vInt_settings160_list88_2)  # settings160.list88[2].
        self.writeDataReference(*dataReference_settings160_104)  # settings160.104
        self.writeVInt(vInt_settings160_list112_count)  # settings160.list112.count
        self.writeVInt(vInt_settings160_128)  # settings160.128
        self.writeVInt(vInt_92)  # native +92
        self.writeVInt(vInt_96)  # native +96
        self.writeBoolean(boolean_text112_present)  # text112.present
        self.writeString(string_text112_text)  # text112.text
        self.writeVInt(vInt_text112_id)  # text112.id
        self.writeBoolean(boolean_text120_present)  # text120.present
        self.writeBoolean(boolean_text128_present)  # text128.present
        self.writeString(string_text128_text)  # text128.text
        self.writeVInt(vInt_text128_id)  # text128.id
        self.writeBoolean(boolean_reward168_present)  # reward168.present
        self.writeVInt(vInt_list80_count)  # list80.count
        self.writeBoolean(boolean_file136_present)  # file136.present
        self.writeDataReference(*dataReference_144)  # native +144
        self.writeBoolean(boolean_event176_present)  # event176.present
        self.writeVInt(vInt_refs192_count)  # refs192.count
        self.writeDataReference(*dataReference_refs192_0)  # refs192[0].
        self.writeDataReference(*dataReference_refs192_1)  # refs192[1].
        self.writeDataReference(*dataReference_refs192_2)  # refs192[2].
        self.writeDataReference(*dataReference_refs192_3)  # refs192[3].
        self.writeDataReference(*dataReference_refs192_4)  # refs192[4].
        self.writeDataReference(*dataReference_refs192_5)  # refs192[5].
        self.writeDataReference(*dataReference_refs192_6)  # refs192[6].
        self.writeDataReference(*dataReference_refs192_7)  # refs192[7].
        self.writeDataReference(*dataReference_refs192_8)  # refs192[8].
        self.writeDataReference(*dataReference_refs192_9)  # refs192[9].
        self.writeDataReference(*dataReference_refs192_10)  # refs192[10].
        self.writeDataReference(*dataReference_refs192_11)  # refs192[11].
        self.writeDataReference(*dataReference_refs192_12)  # refs192[12].
        self.writeDataReference(*dataReference_refs192_13)  # refs192[13].
        self.writeDataReference(*dataReference_refs192_14)  # refs192[14].
        self.writeDataReference(*dataReference_refs192_15)  # refs192[15].
        self.writeDataReference(*dataReference_refs192_16)  # refs192[16].
        self.writeDataReference(*dataReference_refs192_17)  # refs192[17].
        self.writeDataReference(*dataReference_refs192_18)  # refs192[18].
        self.writeDataReference(*dataReference_refs192_19)  # refs192[19].
        self.writeDataReference(*dataReference_refs192_20)  # refs192[20].
        self.writeDataReference(*dataReference_refs192_21)  # refs192[21].
        self.writeDataReference(*dataReference_refs192_22)  # refs192[22].
        self.writeDataReference(*dataReference_refs192_23)  # refs192[23].
        self.writeDataReference(*dataReference_refs192_24)  # refs192[24].
        self.writeDataReference(*dataReference_refs192_25)  # refs192[25].
        self.writeDataReference(*dataReference_refs192_26)  # refs192[26].
        self.writeDataReference(*dataReference_refs192_27)  # refs192[27].
        self.writeVInt(vInt_refs216_count)  # refs216.count
        self.writeVInt(vInt_refs224_count)  # refs224.count
        self.writeVInt(vInt_refs200_count)  # refs200.count
        self.writeVInt(vInt_list208_count)  # list208.count
        self.writeVInt(vInt_list208_0)  # list208[0].
        self.writeVInt(vInt_232)  # native +232
        self.writeBoolean(boolean_event240_present)  # event240.present
        self.writeBoolean(boolean_event248_present)  # event248.present
        self.writeBoolean(boolean_event256_present)  # event256.present
        self.writeBoolean(boolean_event264_present)  # event264.present
        self.writeBoolean(boolean_event272_present)  # event272.present
        self.writeBoolean(boolean_event280_present)  # event280.present
        self.writeBoolean(boolean_event288_present)  # event288.present
        self.writeBoolean(boolean_event296_present)  # event296.present

    def _write_ConfData_events16_layout11(self, values):
        """events16: fields in native wire order."""
        (
            vInt_0,
            vInt_4,
            vInt_8,
            vInt_12,
            vInt_16,
            vInt_20,
            dataReference_24,
            dataReference_32,
            vInt_40,
            string_48,
            vInt_56,
            vInt_60,
            vInt_64,
            vInt_list72_count,
            vInt_88,
            vInt_100,
            boolean_104,
            boolean_map152_present,
            vInt_68,
            boolean_settings160_present,
            vInt_92,
            vInt_96,
            boolean_text112_present,
            string_text112_text,
            vInt_text112_id,
            boolean_text120_present,
            boolean_text128_present,
            string_text128_text,
            vInt_text128_id,
            boolean_reward168_present,
            vInt_list80_count,
            boolean_file136_present,
            dataReference_144,
            boolean_event176_present,
            vInt_refs192_count,
            dataReference_refs192_0,
            dataReference_refs192_1,
            dataReference_refs192_2,
            dataReference_refs192_3,
            dataReference_refs192_4,
            vInt_refs216_count,
            vInt_refs224_count,
            vInt_refs200_count,
            vInt_list208_count,
            vInt_list208_0,
            vInt_list208_1,
            vInt_list208_2,
            vInt_232,
            boolean_event240_present,
            dataReference_event240_32,
            vInt_event240_bonusStarDrops_count,
            vInt_event240_bonusStarDrops_0,
            vInt_event240_bonusStarDrops_1,
            vInt_event240_bonusStarDrops_2,
            vInt_event240_8,
            vInt_event240_12,
            boolean_event248_present,
            boolean_event256_present,
            boolean_event264_present,
            boolean_event272_present,
            boolean_event280_present,
            boolean_event288_present,
            boolean_event296_present,
        ) = values
        self.writeVInt(vInt_0)  # native +0
        self.writeVInt(vInt_4)  # native +4
        self.writeVInt(vInt_8)  # native +8
        self.writeVInt(vInt_12)  # native +12
        self.writeVInt(vInt_16)  # native +16
        self.writeVInt(vInt_20)  # native +20
        self.writeDataReference(*dataReference_24)  # native +24
        self.writeDataReference(*dataReference_32)  # native +32
        self.writeVInt(vInt_40)  # native +40
        self.writeString(string_48)  # native +48
        self.writeVInt(vInt_56)  # native +56
        self.writeVInt(vInt_60)  # native +60
        self.writeVInt(vInt_64)  # native +64
        self.writeVInt(vInt_list72_count)  # list72.count
        self.writeVInt(vInt_88)  # native +88
        self.writeVInt(vInt_100)  # native +100
        self.writeBoolean(boolean_104)  # native +104
        self.writeBoolean(boolean_map152_present)  # map152.present
        self.writeVInt(vInt_68)  # native +68
        self.writeBoolean(boolean_settings160_present)  # settings160.present
        self.writeVInt(vInt_92)  # native +92
        self.writeVInt(vInt_96)  # native +96
        self.writeBoolean(boolean_text112_present)  # text112.present
        self.writeString(string_text112_text)  # text112.text
        self.writeVInt(vInt_text112_id)  # text112.id
        self.writeBoolean(boolean_text120_present)  # text120.present
        self.writeBoolean(boolean_text128_present)  # text128.present
        self.writeString(string_text128_text)  # text128.text
        self.writeVInt(vInt_text128_id)  # text128.id
        self.writeBoolean(boolean_reward168_present)  # reward168.present
        self.writeVInt(vInt_list80_count)  # list80.count
        self.writeBoolean(boolean_file136_present)  # file136.present
        self.writeDataReference(*dataReference_144)  # native +144
        self.writeBoolean(boolean_event176_present)  # event176.present
        self.writeVInt(vInt_refs192_count)  # refs192.count
        self.writeDataReference(*dataReference_refs192_0)  # refs192[0].
        self.writeDataReference(*dataReference_refs192_1)  # refs192[1].
        self.writeDataReference(*dataReference_refs192_2)  # refs192[2].
        self.writeDataReference(*dataReference_refs192_3)  # refs192[3].
        self.writeDataReference(*dataReference_refs192_4)  # refs192[4].
        self.writeVInt(vInt_refs216_count)  # refs216.count
        self.writeVInt(vInt_refs224_count)  # refs224.count
        self.writeVInt(vInt_refs200_count)  # refs200.count
        self.writeVInt(vInt_list208_count)  # list208.count
        self.writeVInt(vInt_list208_0)  # list208[0].
        self.writeVInt(vInt_list208_1)  # list208[1].
        self.writeVInt(vInt_list208_2)  # list208[2].
        self.writeVInt(vInt_232)  # native +232
        self.writeBoolean(boolean_event240_present)  # event240.present
        self.writeDataReference(*dataReference_event240_32)  # event240.32
        self.writeVInt(vInt_event240_bonusStarDrops_count)  # event240.bonusStarDrops.count
        self.writeVInt(vInt_event240_bonusStarDrops_0)  # event240.bonusStarDrops[0].
        self.writeVInt(vInt_event240_bonusStarDrops_1)  # event240.bonusStarDrops[1].
        self.writeVInt(vInt_event240_bonusStarDrops_2)  # event240.bonusStarDrops[2].
        self.writeVInt(vInt_event240_8)  # event240.8
        self.writeVInt(vInt_event240_12)  # event240.12
        self.writeBoolean(boolean_event248_present)  # event248.present
        self.writeBoolean(boolean_event256_present)  # event256.present
        self.writeBoolean(boolean_event264_present)  # event264.present
        self.writeBoolean(boolean_event272_present)  # event272.present
        self.writeBoolean(boolean_event280_present)  # event280.present
        self.writeBoolean(boolean_event288_present)  # event288.present
        self.writeBoolean(boolean_event296_present)  # event296.present

    def _write_ConfData_events32_layout12(self, values):
        """events32: fields in native wire order."""
        (
            vInt_0,
            vInt_4,
            vInt_8,
            vInt_12,
            vInt_16,
            vInt_20,
            dataReference_24,
            dataReference_32,
            vInt_40,
            string_48,
            vInt_56,
            vInt_60,
            vInt_64,
            vInt_list72_count,
            vInt_88,
            vInt_100,
            boolean_104,
            boolean_map152_present,
            vInt_68,
            boolean_settings160_present,
            vInt_92,
            vInt_96,
            boolean_text112_present,
            boolean_text120_present,
            boolean_text128_present,
            boolean_reward168_present,
            vInt_list80_count,
            boolean_file136_present,
            dataReference_144,
            boolean_event176_present,
            vInt_refs192_count,
            vInt_refs216_count,
            vInt_refs224_count,
            vInt_refs200_count,
            vInt_list208_count,
            vInt_232,
            boolean_event240_present,
            boolean_event248_present,
            boolean_event256_present,
            boolean_event264_present,
            boolean_event272_present,
            boolean_event280_present,
            boolean_event288_present,
            boolean_event296_present,
        ) = values
        self.writeVInt(vInt_0)  # native +0
        self.writeVInt(vInt_4)  # native +4
        self.writeVInt(vInt_8)  # native +8
        self.writeVInt(vInt_12)  # native +12
        self.writeVInt(vInt_16)  # native +16
        self.writeVInt(vInt_20)  # native +20
        self.writeDataReference(*dataReference_24)  # native +24
        self.writeDataReference(*dataReference_32)  # native +32
        self.writeVInt(vInt_40)  # native +40
        self.writeString(string_48)  # native +48
        self.writeVInt(vInt_56)  # native +56
        self.writeVInt(vInt_60)  # native +60
        self.writeVInt(vInt_64)  # native +64
        self.writeVInt(vInt_list72_count)  # list72.count
        self.writeVInt(vInt_88)  # native +88
        self.writeVInt(vInt_100)  # native +100
        self.writeBoolean(boolean_104)  # native +104
        self.writeBoolean(boolean_map152_present)  # map152.present
        self.writeVInt(vInt_68)  # native +68
        self.writeBoolean(boolean_settings160_present)  # settings160.present
        self.writeVInt(vInt_92)  # native +92
        self.writeVInt(vInt_96)  # native +96
        self.writeBoolean(boolean_text112_present)  # text112.present
        self.writeBoolean(boolean_text120_present)  # text120.present
        self.writeBoolean(boolean_text128_present)  # text128.present
        self.writeBoolean(boolean_reward168_present)  # reward168.present
        self.writeVInt(vInt_list80_count)  # list80.count
        self.writeBoolean(boolean_file136_present)  # file136.present
        self.writeDataReference(*dataReference_144)  # native +144
        self.writeBoolean(boolean_event176_present)  # event176.present
        self.writeVInt(vInt_refs192_count)  # refs192.count
        self.writeVInt(vInt_refs216_count)  # refs216.count
        self.writeVInt(vInt_refs224_count)  # refs224.count
        self.writeVInt(vInt_refs200_count)  # refs200.count
        self.writeVInt(vInt_list208_count)  # list208.count
        self.writeVInt(vInt_232)  # native +232
        self.writeBoolean(boolean_event240_present)  # event240.present
        self.writeBoolean(boolean_event248_present)  # event248.present
        self.writeBoolean(boolean_event256_present)  # event256.present
        self.writeBoolean(boolean_event264_present)  # event264.present
        self.writeBoolean(boolean_event272_present)  # event272.present
        self.writeBoolean(boolean_event280_present)  # event280.present
        self.writeBoolean(boolean_event288_present)  # event288.present
        self.writeBoolean(boolean_event296_present)  # event296.present






    def _write_ConfData_ShopChainOfferTheme_layout18(self, values):
        """ShopChainOfferTheme: fields in native wire order."""
        (
            string_40,
            dataReference_0,
            boolean_text16_present,
            string_text16_text,
            vInt_text16_id,
            vInt_72,
            vInt_8,
            vInt_12,
            dataReference_32,
            boolean_text24_present,
            string_text24_text,
            vInt_text24_id,
            boolean_96,
            boolean_file104_present,
            string_file104_file16,
            string_file104_file0,
            vInt_overrides80_count,
            string_56,
        ) = values
        self.writeString(string_40)  # native +40
        self.writeDataReference(*dataReference_0)  # native +0
        self.writeBoolean(boolean_text16_present)  # text16.present
        self.writeString(string_text16_text)  # text16.text
        self.writeVInt(vInt_text16_id)  # text16.id
        self.writeVInt(vInt_72)  # native +72
        self.writeVInt(vInt_8)  # native +8
        self.writeVInt(vInt_12)  # native +12
        self.writeDataReference(*dataReference_32)  # native +32
        self.writeBoolean(boolean_text24_present)  # text24.present
        self.writeString(string_text24_text)  # text24.text
        self.writeVInt(vInt_text24_id)  # text24.id
        self.writeBoolean(boolean_96)  # native +96
        self.writeBoolean(boolean_file104_present)  # file104.present
        self.writeString(string_file104_file16)  # file104.file16
        self.writeString(string_file104_file0)  # file104.file0
        self.writeVInt(vInt_overrides80_count)  # overrides80.count
        self.writeString(string_56)  # native +56






