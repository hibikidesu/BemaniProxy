from .model import Model
from enum import Enum


__all__ = [
    "get_version_string",
    "SDVX",
    "DANCERUSH",
    "IIDX",
    "JUBEAT",
    "LOVEPLUS",
    "MUSECA",
    "NOSTALGIA",
    "POPN",
    "FUTURETOMTOM",
    "REFLECBEAT",
    "DANCEEVOLUTION"
]


class SDVX(Enum):
    BOOTH = "SDVX"
    INFINITE_INFECTION = "SDVX2"
    GRAVITY_WARS = "SDVX3"
    GRAVITY_WARS_S2 = "SDVX3s2"
    HEAVENLY_HAVEN = "SDVX4"
    VIVID_WAVE = "SDVX5"


class DANCERUSH(Enum):
    STARDOM = "DANCERUSH_STARDOM"


class IIDX(Enum):
    RED = "IIDX11"
    HAPPY_SKY = "IIDX12"
    DISTORTED = "IIDX13"
    GOLD = "IIDX14"
    DJ_TROOPERS = "IIDX15"
    EMPRESS = "IIDX16"
    SIRIUS = "IIDX17"
    RESORT_ANTHEM = "IIDX18"
    LINCLE = "IIDX19"
    TRICORO = "IIDX20"
    SPADA = "IIDX21"
    PENDUAL = "IIDX22"
    COPULA = "IIDX23"
    SINOBUZ = "IIDX24"
    CANNON_BALLERS = "IIDX25"
    ROOTAGE = "IIDX26"
    HEROIC_VERSE = "IIDX27"


class JUBEAT(Enum):
    JUBEAT = "JUBEAT"
    JUKEBEAT = "JUKEBEAT"
    RIPPLES = "JUBEAT_RIPPLES"
    RIPPLES_APPEND = "JUBEAT_RIPPLES_APPEND"
    KNIT = "JUBEAT_KNIT"
    KNIT_APPPEND = "JUBEAT_KNIT_APPEND"
    COPIOUS = "JUBEAT_COPIOUS"
    COPIOUS_APPEND = "JUBEAT_COPIOUS_APPEND"
    SAUCER = "JUBEAT_SAUCER"
    SAUCER_FULFILL = "JUBEAT_SAUCER_FULFILL"
    PROP = "JUBEAT_PROP"
    QUBELL = "JUBEAT_QUBELL"
    CLAN = "JUBEAT_CLAN"
    FESTO = "JUBEAT_FESTO"


class LOVEPLUS(Enum):
    LOVEPLUS = "LOVEPLUS"


class MUSECA(Enum):
    MUSECA = "MUSECA"
    MUSECA2 = "MUSECA2"


class NOSTALGIA(Enum):
    NOSTALGIA = "NOSTALGIA"
    FORTE = "NOSTALGIA_FORTE"
    NOSTALGIA2 = "NOSTALGIA2"
    NOSTALGIA3 = "NOSTALGIA3"


class POPN(Enum):
    IROHA = "POPN12"
    CARNIVAL = "POPN13"
    FEVER = "POPN14"
    ADVENTURE = "POPN15"
    PARTY = "POPN16"
    THE_MOVIE = "POPN17"
    SENGOKU_RETSUDEN = "POPN18"
    TUNE_STREET = "POPN19"
    FANTASIA = "POPN20"
    SUNNY_PARK = "POPN21"
    LAPISTORIA = "POPN22"
    ECLALE = "POPN23"
    USAGI_NO_NEKO_TO_SHOUNEN_NO_YUME = "POPN24"
    PEACE = "POPN25"
    WELCOME_TO_WONDERLAND = "POPN26"


class FUTURETOMTOM(Enum):
    FUTURETOMTOM = "FutureTomTom"
    FUTURETOMTOM2 = "FutureTomTom2"


class REFLECBEAT(Enum):
    REFLECBEAT = "REFLECBEAT"
    LIMELIGHT = "REFLECBEAT_LIMELIGHT"
    COLETTE = "REFLECBEAT_COLETTE"
    GROOVIN = "REFLECBEAT_GROOVIN"
    GROOVIN_UPPER = "REFLECBEAT_GROOVIN_UPPER"
    VOLZZA = "REFLECBEAT_VOLZZA"
    VOLZZA2 = "REFLECBEAT_VOLZZA_2"
    ETERNITY = "REFLECBEAT_ETERNITY"


class DANCEEVOLUTION(Enum):
    DANCEEVOLUTION = "DanceEvolution"


def get_version_string(m: Model) -> Enum:
    game_code = m.game.upper()

    # SDVX
    if game_code == "KFC":
        if 2012011800 <= m.version < 2013060500:
            return SDVX.BOOTH
        if 2013060500 <= m.version < 2014112000:
            return SDVX.INFINITE_INFECTION
        if 2014112000 <= m.version < 2015120400:
            return SDVX.GRAVITY_WARS
        if 2015120400 <= m.version < 2016122100:
            return SDVX.GRAVITY_WARS_S2
        if 2016122100 <= m.version < 2019022800:
            return SDVX.HEAVENLY_HAVEN
        if m.version >= 2019022800:
            return SDVX.VIVID_WAVE

    # DANCERUSH
    if game_code == "REC":
        if m.version >= 2017120800:
            return DANCERUSH.STARDOM

    # IIDX
    if game_code == "I00":
        if m.version >= 2008111900:
            return IIDX.EMPRESS
    if game_code == "JDJ":
        if m.version >= 2009102100:
            return IIDX.SIRIUS
    if game_code == "JDZ":
        if m.version >= 2010091500:
            return IIDX.RESORT_ANTHEM
    if game_code == "KDZ":
        if m.version >= 2011091500:
            return IIDX.LINCLE
    if game_code == "LDJ":
        if 2012091904 <= m.version < 2013100200:
            return IIDX.TRICORO
        if 2013100200 <= m.version < 2014091700:
            return IIDX.SPADA
        if 2014091700 <= m.version < 2015111100:
            return IIDX.PENDUAL
        if 2015111100 <= m.version < 2016102400:
            return IIDX.COPULA
        if 2016102400 <= m.version < 2017122100:
            return IIDX.SINOBUZ
        if 2017122100 <= m.version < 2018110700:
            return IIDX.CANNON_BALLERS
        if 2018110700 <= m.version < 2019101600:
            return IIDX.ROOTAGE
        if m.version >= 2019101600:
            return IIDX.HEROIC_VERSE

    # JUBEAT
    if game_code == "H44":
        if m.version >= 2008072400:
            return JUBEAT.JUBEAT
    if game_code == "I44":
        if m.dest == "U":
            return JUBEAT.JUKEBEAT
        if 2009080400 <= m.version < 2010012500:
            return JUBEAT.RIPPLES
        if m.version >= 2010012500:
            return JUBEAT.RIPPLES_APPEND
    if game_code == "J44":
        if 2010070400 <= m.version < 2011011400:
            return JUBEAT.KNIT
        if m.version >= 2011011400:
            return JUBEAT.KNIT_APPPEND
    if game_code == "K44":
        if 2011083100 <= m.version < 2012031400:
            return JUBEAT.COPIOUS
        if m.version >= 2012031400:
            return JUBEAT.COPIOUS_APPEND
    if game_code == "L44":
        if 2012082400 <= m.version < 2014030300:
            return JUBEAT.SAUCER
        if 2014030300 <= m.version < 2015022000:
            return JUBEAT.SAUCER_FULFILL
        if 2015022000 <= m.version < 2016033000:
            return JUBEAT.PROP
        if 2016033000 <= m.version < 2017051200:
            return JUBEAT.QUBELL
        if 2017051200 <= m.version < 2018090500:
            return JUBEAT.CLAN
        if m.version >= 2018090500:
            return JUBEAT.FESTO

    # LOVEPLUS
    if game_code == "KLP":
        return LOVEPLUS.LOVEPLUS

    # MUSECA
    if game_code == "PIX":
        if 2015112300 <= m.version < 2016072700:
            return MUSECA.MUSECA
        if m.version >= 2016072700:
            return MUSECA.MUSECA2

    # NOSTALGIA
    if game_code == "PAN":
        if 2017012500 <= m.version < 2017071900:
            return NOSTALGIA.NOSTALGIA
        if 2017071900 <= m.version < 2018092600:
            return NOSTALGIA.FORTE
        if 2018092600 <= m.version < 2019120200:
            return NOSTALGIA.NOSTALGIA2
        if m.version >= 2019120200:
            return NOSTALGIA.NOSTALGIA3

    # POPN
    if game_code == "G15":
        if m.version >= 2007091800:
            return POPN.ADVENTURE
    if game_code == "H16":
        if m.version >= 2008032400:
            return POPN.PARTY
    if game_code == "I17":
        if m.version >= 2009022500:
            return POPN.THE_MOVIE
    if game_code == "J39":
        if m.version >= 2009121400:
            return POPN.SENGOKU_RETSUDEN
    if game_code == "K39":
        if m.version >= 2010122200:
            return POPN.TUNE_STREET
    if game_code == "L39":
        if m.version >= 2011110200:
            return POPN.FANTASIA
    if game_code == "M39":
        if 2012110000 <= m.version < 2014062500:
            return POPN.SUNNY_PARK
        if 2014062500 <= m.version < 2015112600:
            return POPN.LAPISTORIA
        if 2015112600 <= m.version < 2016121400:
            return POPN.ECLALE
        if 2016121400 <= m.version < 2018101700:
            return POPN.USAGI_NO_NEKO_TO_SHOUNEN_NO_YUME
        if m.version >= 2018101700:
            return POPN.PEACE

    # FutureTomTom
    if game_code == "MMD":
        if 2013052400 <= m.version < 2013121700:
            return FUTURETOMTOM.FUTURETOMTOM
        if m.version >= 2013071200:
            return FUTURETOMTOM.FUTURETOMTOM2

    # TODO ddr, gitadora

    # ReflecBeat
    if game_code == "KBR":
        if m.version >= 2010110400:
            return REFLECBEAT.REFLECBEAT
    if game_code == "LBR":
        if 2011111600 <= m.version < 2012112100:
            return REFLECBEAT.LIMELIGHT
        if m.version >= 2012112100:
            return REFLECBEAT.COLETTE
    if game_code == "MBR":
        if 2013051300 <= m.version < 2014060402:
            return REFLECBEAT.COLETTE
        if 2014060402 <= m.version < 2014112000:
            return REFLECBEAT.GROOVIN
        if 2014112000 <= m.version < 2015102800:
            return REFLECBEAT.GROOVIN_UPPER
        if 2015102800 <= m.version < 2016030200:
            return REFLECBEAT.VOLZZA
        if 2016030200 <= m.version < 2016120100:
            return REFLECBEAT.VOLZZA2
        if m.version >= 2016120100:
            return REFLECBEAT.ETERNITY

    # GITADORA TODO
    if game_code == "K33":
        if m.version >= 2011012400:
            return "GUITARFREAKS_V8"
    if game_code == "K33":
        if m.version >= 2011022400:
            return "DRUMMANIA_V8"
    if game_code == "J33":
        if m.version >= 2010020200:
            return "GUITARFREAKS_XG"
    if game_code == "J32":
        if m.version >= 2010020200:
            return "DRUMMANIA_XG"

    # BeatStream
    if game_code == "NBT":
        if 2014070100 <= m.version < 2015122100:
            return "BEATSTREAM"
        if m.version >= 2015122100:
            return "BEATSTREAM2"

    # DanceEvolution
    if game_code == "KDM":
        return DANCEEVOLUTION.DANCEEVOLUTION

    raise Exception("Game Not Found")
