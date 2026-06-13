# World Cup 2026 groups and teams
# Source: Official draw held on December 5, 2025, at the Kennedy Center, Washington D.C.

GRUPOS: dict[str, list[str]] = {
    "A": ["🇲🇽 Mexico", "🇿🇦 South Africa", "🇰🇷 South Korea", "🇨🇿 Czech Republic"],
    "B": ["🇨🇦 Canada", "🇧🇦 Bosnia and Herzegovina", "🇶🇦 Qatar", "🇨🇭 Switzerland"],
    "C": ["🇧🇷 Brazil", "🇲🇦 Morocco", "🇭🇹 Haiti", "🏴 Scotland"],
    "D": ["🇺🇸 United States", "🇵🇾 Paraguay", "🇦🇺 Australia", "🇹🇷 Turkey"],
    "E": ["🇩🇪 Germany", "🇨🇼 Curaçao", "🇨🇮 Ivory Coast", "🇪🇨 Ecuador"],
    "F": ["🇳🇱 Netherlands", "🇯🇵 Japan", "🇸🇪 Sweden", "🇹🇳 Tunisia"],
    "G": ["🇧🇪 Belgium", "🇪🇬 Egypt", "🇮🇷 Iran", "🇳🇿 New Zealand"],
    "H": ["🇪🇸 Spain", "🇨🇻 Cape Verde", "🇸🇦 Saudi Arabia", "🇺🇾 Uruguay"],
    "I": ["🇫🇷 France", "🇸🇳 Senegal", "🇮🇶 Iraq", "🇳🇴 Norway"],
    "J": ["🇦🇷 Argentina", "🇩🇿 Algeria", "🇦🇹 Austria", "🇯🇴 Jordan"],
    "K": ["🇵🇹 Portugal", "🇨🇩 DR Congo", "🇺🇿 Uzbekistan", "🇨🇴 Colombia"],
    "L": ["🏴 England", "🇭🇷 Croatia", "🇬🇭 Ghana", "🇵🇦 Panama"],
}

# ---------------------------------------------------------------------------
# Official knockout bracket - World Cup 2026
# Source: FIFA / Wikipedia (2026_FIFA_World_Cup_knockout_stage)
# ---------------------------------------------------------------------------

# Round of 32 - (match_number, team_slot_1, team_slot_2)
# slot: ("1","A") = 1st place from Group A, ("2","B") = 2nd place from Group B, ("3",None) = best third place
BRACKET_R32: list[tuple] = [
    (73,  ("2", "A"), ("2", "B")),
    (74,  ("1", "E"), ("3", None)),
    (75,  ("1", "F"), ("2", "C")),
    (76,  ("1", "C"), ("2", "F")),
    (77,  ("1", "I"), ("3", None)),
    (78,  ("2", "E"), ("2", "I")),
    (79,  ("1", "A"), ("3", None)),
    (80,  ("1", "L"), ("3", None)),
    (81,  ("1", "D"), ("3", None)),
    (82,  ("1", "G"), ("3", None)),
    (83,  ("2", "K"), ("2", "L")),
    (84,  ("1", "H"), ("2", "J")),
    (85,  ("1", "B"), ("3", None)),
    (86,  ("1", "J"), ("2", "H")),
    (87,  ("1", "K"), ("3", None)),
    (88,  ("2", "D"), ("2", "G")),
]

# Round of 16 - (match_number, previous_match_1, previous_match_2)
BRACKET_R16: list[tuple] = [
    (89, 73, 75),
    (90, 74, 77),
    (91, 76, 78),
    (92, 79, 80),
    (93, 83, 84),
    (94, 81, 82),
    (95, 86, 88),
    (96, 85, 87),
]

# Quarterfinals
BRACKET_QF: list[tuple] = [
    (97,  89, 90),
    (98,  93, 94),
    (99,  91, 92),
    (100, 95, 96),
]

# Semifinals
BRACKET_SF: list[tuple] = [
    (101, 97,  98),
    (102, 99, 100),
]

# The final and third-place playoff are derived from the semifinals (generated in the app)
