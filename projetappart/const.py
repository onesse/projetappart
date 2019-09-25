from enum import Enum

URL_LEBONCOIN = "https://www.leboncoin.fr/recherche/"


class RechercheCategorie(Enum):
    VOITURES = 2  # Fonctionnalité non développée
    VENTES_IMMOBILIERES = 9
    LOCATIONS_IMMOBILIERES = 10


# Installations supplémentaires présentes
installations = {
    "terrasse": ["terrasse", "balcon"],
    "garage": ["parking", "garage"],
    "piscine": ["piscine"],
    "clim": ["clim", "climatisation", "climatisé"],
    "rez-de-chaussée": ["rez-de-chaussée"]
}

# Quartiers de Toulon
quartiers_toulon = ["haute ville", "pont du las", "mourillon", "saint jean du var", "champ de mars", "sainte musse",
                    "saint roch", "les routes", "aguillon", "serinette", "cap brun", "cathedrale", "petit bois",
                    "port", "temple", "port", "besagne", "gare", "lamalgue", "beaucaire", "darboussede"]

# annonces à rejeter si elles contiennent les mots suivants
a_rejeter = ["viager", "à construire", "programme", "colocation", "location dans appartement", "chambre dans appartement",
             "échange HLM"]


class Ville(Enum):
    TOULON = "Toulon"
    LA_GARDE = "La Garde_83130"
    SEYNE_SUR_MER = "La Seyne-sur-Mer_83500"
    OLLIOULES = "Ollioules_83190"
    SIX_FOUR_LES_PLAGES = "Six-Fours-les-Plages_83140"
    SANARY_SUR_MER = "Sanary-sur-Mer_83110"


class TypeImmobilier(Enum):
    NEUF = "new"
    ANCIEN = "old"
    VIAGER = "viager"


class TypeBien(Enum):
    MAISON = 1
    APPARTEMENT = 2
    TERRAIN = 3
    PARKING = 4
    AUTRE = 5


class TypeLocation(Enum):
    MEUBLEE = 1
    NON_MEUBLEE = 2


class TypeAnnonce(Enum):
    PARTICULIER = "private"
    PROFESSIONNEL = "pro"
