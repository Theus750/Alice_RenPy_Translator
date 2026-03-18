label start:
    e "Hello [player_name]!"
    e _("Localized dialogue")
    e _('Localized single quote dialogue')
    "Narration text"
    _("Localized narration")
    _('Localized single quote narration')
    menu:
        "Go to beach":
            jump beach
        _("Leave now"):
            jump leave
        _('Leave single quote'):
            jump leave_single

label branch:
    if points > 5:
        e "You got {points} points"
        e ("This was inside parentheses")
        e (_("Nested localized dialogue"))
        e (_('Nested single quote dialogue'))
