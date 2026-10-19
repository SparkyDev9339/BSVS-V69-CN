from Classes.Packets.PiranhaMessage import PiranhaMessage


import Configuration

from Classes.Packets.PiranhaMessage import PiranhaMessage


class LoginOkMessage(PiranhaMessage):
    def __init__(self, messageData):
        super().__init__(messageData)
        self.messageVersion = 1

    def encode(self, fields, player):
        #self.writeHexa("000000060792FF14000000060792FF140000002867396D3237656466747262653432727033397A386334376D347936646A386E3374636D7461797877FFFFFFFFFFFFFFFF0000003B000000D4000000010000000470726F64000000CC00004E7600000046FFFFFFFF0000000D313733353534383430373835340000000D3137323934343534343130303000000000FFFFFFFF000000024348FFFFFFFF00000001FFFFFFFF000000020000002668747470733A2F2F67616D652D6173736574732E627261776C737461727367616D652E636F6D0000002468747470733A2F2F67616D652D6173736574732D322E627261776C73746172732E636F6D000000020000002368747470733A2F2F6576656E742D6173736574732E627261776C73746172732E636F6D0000002568747470733A2F2F6576656E742D6173736574732D322E627261776C73746172732E636F6D000000014DA4010000789C258EDB7282301445BF4887BBE511C32D29098DDCF3D211644AB859C516C9D7D74C1FCFD9B3D7DAED86EEE782F298A309F7D864E938C689B292D4EFA2946ECC6D1EB18B06061493F5D4A8C471C24565B0C2E311404A5B3AB2FB9EAB54DE5D1D34F2F6330155C291BD6F37B4FE0BA016A5DE4684A313D7D1620017381F15D85F391428C4DE05C7D925CC7B4782E6AA504799D5812F5809E56FACE74AC2D766B207C8575EE9B2FFAD34733EBE725169E3C012685D42A4B264E5E7C297FC2711582529355E5E5D72DAF035BAF7742C321DF7DE86DD466EF9913E1A905F16E4A2D489529548480F0B6C2E339C0E3A01CA130365C372FF349A0D80169BFCA5D1727B3F581479CD09FD2ECC35AF1D7E1B17126C1F07EBD47741143EB2B3AD91E179350FEB0CEADDE74DEB670BED76CFC14FD08DA48F2813EB970076B5CB12901AA7D6A277FA0723CA8B9C01FFFFFFFF00000018414141426C42612F44766973485157614145465261513D3DFFFFFFFF0000002D69746D732D617070733A2F2F6974756E65732E6170706C652E636F6D2F6170702F696431323239303136383037FFFFFFFF020000002C476D4C7A384F2F6976374D5552387242494175363778302B64635A453763622F5A49316B483675724B59413D0100000034737570657263656C6C5F706C6174666F726D5F32303137303531383038313934373334372D6231386461353334613132366663310100000017737570657263656C6C2E68656C7073686966742E636F6D01000000203662663766303436316638613661613835623966356262643566356461336264")
        self.writeLong(player.ID[0], player.ID[1])
        self.writeLong(player.ID[0], player.ID[1])
        self.writeString(player.Token)
        self.writeString()
        self.writeString()
        self.writeInt(66)
        self.writeInt(258)
        self.writeInt(1)
        self.writeString("dev")
        self.writeInt(0)
        self.writeInt(0)
        self.writeInt(0)
        self.writeString()
        self.writeString()
        self.writeString()
        self.writeInt(0)
        self.writeString()
        self.writeString("CA")
        self.writeString()
        self.writeInt(0)
        self.writeString()
        self.writeInt(2)
        self.writeString('https://game-assets.brawlstarsgame.com')
        self.writeString('http://a678dbc1c015a893c9fd-4e8cc3b1ad3a3c940c504815caefa967.r87.cf2.rackcdn.com')
        self.writeInt(3)
        self.writeString('https://event-assets-2.brawlstars.com')
        self.writeString('https://event-assets.brawlstars.com')
        self.writeString('https://24b999e6da07674e22b0-8209975788a0f2469e68e84405ae4fcf.ssl.cf2.rackcdn.com/event-assets')
        self.writeVInt(0)
        self.writeCompressedString(b'')
        self.writeBoolean(True)
        self.writeBoolean(False)
        self.writeString()
        self.writeString()
        self.writeString()
        self.writeString('https://play.google.com/store/apps/details?id=com.supercell.brawlstars')
        self.writeString()
        self.writeBoolean(False)

        self.writeBoolean(False)
        if False:
            self.writeString()

        self.writeBoolean(False)
        if False:
            self.writeString()

        self.writeBoolean(False)
        if False:
            self.writeString()

        self.writeBoolean(False)
        if False:
            self.writeString()


    def decode(self):
        fields = {}
        fields["AccountID"] = self.readLong()
        fields["HomeID"] = self.readLong()
        fields["PassToken"] = self.readString()
        fields["FacebookID"] = self.readString()
        fields["GamecenterID"] = self.readString()
        fields["ServerMajorVersion"] = self.readInt()
        fields["ContentVersion"] = self.readInt()
        fields["ServerBuild"] = self.readInt()
        fields["ServerEnvironment"] = self.readString()
        fields["SessionCount"] = self.readInt()
        fields["PlayTimeSeconds"] = self.readInt()
        fields["DaysSinceStartedPlaying"] = self.readInt()
        fields["FacebookAppID"] = self.readString()
        fields["ServerTime"] = self.readString()
        fields["AccountCreatedDate"] = self.readString()
        fields["StartupCooldownSeconds"] = self.readInt()
        fields["GoogleServiceID"] = self.readString()
        fields["LoginCountry"] = self.readString()
        fields["KunlunID"] = self.readString()
        fields["Tier"] = self.readInt()
        fields["TencentID"] = self.readString()

        ContentUrlCount = self.readInt()
        fields["GameAssetsUrls"] = []
        for i in range(ContentUrlCount):
            fields["GameAssetsUrls"].append(self.readString())

        EventUrlCount = self.readInt()
        fields["EventAssetsUrls"] = []
        for i in range(EventUrlCount):
            fields["EventAssetsUrls"].append(self.readString())

        fields["SecondsUntilAccountDeletion"] = self.readVInt()
        fields["SupercellIDToken"] = self.readCompressedString()
        fields["IsSupercellIDLogoutAllDevicesAllowed"] = self.readBoolean()
        fields["isSupercellIDEligible"] = self.readBoolean()
        fields["LineID"] = self.readString()
        fields["SessionID"] = self.readString()
        fields["KakaoID"] = self.readString()
        fields["UpdateURL"] = self.readString()
        fields["YoozooPayNotifyUrl"] = self.readString()
        fields["UnbotifyEnabled"] = self.readBoolean()

        Unknown1 = self.readBoolean()
        fields["Unknown1"] = Unknown1
        if Unknown1:
            fields["Unknown2"] = self.readString()

        Unknown3 = self.readBoolean()
        fields["Unknown3"] = Unknown1
        if Unknown3:
            fields["Unknown4"] = self.readString()

        Unknown5 = self.readBoolean()
        fields["Unknown5"] = Unknown1
        if Unknown5:
            fields["Unknown6"] = self.readString()

        Unknown7 = self.readBoolean()
        fields["Unknown7"] = Unknown1
        if Unknown7:
            fields["Unknown8"] = self.readString()
        super().decode(fields)
        return fields

    def execute(message, calling_instance, fields):
        pass

    def getMessageType(self):
        return 20104

    def getMessageVersion(self):
        return self.messageVersion