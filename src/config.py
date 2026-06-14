"""
Channel Whitelist - Developer Girls
Mapping validated via frequency and API filtering (Category 28).
"""

CHANNEL_WHITELIST = {
    "DATA_AND_CLOUD": [
        "UCh9sXMUqoEZfAUTyoBBF54Q",  # Sidney Cirqueira - Microsoft Fabric
        "UCdoadna9HFHsxXWhafhNvKw",  # AWS Events
        "UCl-5oPIbTAwLZ0hF_dCUyLQ",  # Jornada de Dados - Luciano Vasconcelos
        "UCnErAicaumKqIo4sanLo7vQ",  # Luan Moreno | Engenharia de Dados Academy
        "UCd6MoB9NC6uYN2grvUNT-Zg",  # Amazon Web Services
        "UCBe1E-CJMlmF5zQ8442D2bw",  # Descomplicando Dados
        "UCqFAXxARXQHx0t_mm_eElcA",  # ROQT | Data & AI
    ],
    "DEVELOPMENT_AND_BACKEND": [
        "UCKJ2JOMmbgpoRnu7G6-notQ",  # Programador Aventureiro
        "UC0_XSYG_kmbDnP6eywpdJjA",  # Python Expert
        "UCxHBj6mfMn7AChmbpvDroKg",  # Python Dev & AI
        "UCFKZxStYsOVrzdN_FCZ0NGg",  # diegoveloper
        "UCTyCe-0QDRju-yC5Cr83eeQ",  # Código Espinoza
    ],
    "WOMEN_IN_TECH_AND_COMMUNITIES": [
        "UC0fWxMTSHEUpB5KX6_KST9A",  # Rainha do pip install
        "UCJ1o6qvMUF_W2cmeFBkYYbQ",  # Code Queens
        "UCSTScc8pgOSiYTg08kT63eQ",  # Mulher Tech Sim Senhor
        "UCnEY-ZQhEf3Ga351x7hanVA",  # Elas no código
        "UCgFhS0ijMry-4iqFrhHTs3A",  # Associação Ser Mulher em Tech
    ]
}

# Consolidates all keys into a single list for the extractor
CONSOLIDATED_TARGET_CHANNELS = (
    CHANNEL_WHITELIST["DATA_AND_CLOUD"] +
    CHANNEL_WHITELIST["DEVELOPMENT_AND_BACKEND"] +
    CHANNEL_WHITELIST["WOMEN_IN_TECH_AND_COMMUNITIES"]
)