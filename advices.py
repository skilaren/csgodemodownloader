"""
Those constants are thresholds for advices

HE_EFF_***: percentage of effective HE grenades
HE_DNG_***: amount of damage

FLASH_EFF_***: percentage of effective FLASH grenades
FLASH_DUR_***: total duration
"""

HE_EFF_USELESS = 0.3
HE_EFF_SUCCESS = 0.7

HE_DMG_USELESS = 20
HE_DMG_SUCCESS = 50

FLASH_EFF_USELESS = 0.5
FLASH_EFF_SUCCESS = 0.8

FLASH_DUR_USELESS = 1
FLASH_DUR_SUCCESS = 3


def get_he_advice(grenades, return_additional_info=False):
    """
    This method gets list of grenades and defines advices in terms of effectiveness by hitting somebody
    and amount of damage for one grenade

    :param return_additional_info: boolean parameter for method to return additional info such as
    effectiveness percentage and average(mean) damage
    :param grenades: list of he grenades
    :return: numbers which describe advices in form (success, damage)
    """
    total = len(grenades)

    effective = [x for x in grenades if x.effective]
    effective_percentage = len(effective)/total

    if effective_percentage >= HE_EFF_SUCCESS:
        successful_advice = 2
    elif HE_EFF_USELESS < effective_percentage < HE_EFF_SUCCESS:
        successful_advice = 1
    else:
        successful_advice = 0

    mean_damage = 0
    for grenade in effective:
        mean_damage += grenade.total_damage

    mean_damage = mean_damage / len(effective)

    if mean_damage >= HE_DMG_SUCCESS:
        damage_advice = 2
    elif HE_DMG_USELESS < mean_damage < HE_DMG_SUCCESS:
        damage_advice = 1
    else:
        damage_advice = 0

    if return_additional_info:
        return successful_advice, damage_advice, effective_percentage, mean_damage
    return successful_advice, damage_advice


def get_flash_advice(grenades, return_additional_info=False):
    """
    This method gets list of grenades and defines advices in terms of effectiveness by flashing enemies
    and total duration for one flash

    :param return_additional_info: boolean parameter for method to return additional info such as
    effectiveness percentage and average(mean) damage
    :param grenades: list of flash grenades
    :return: numbers which describe advices in form (success, damage)
    """
    total = len(grenades)

    effective = [x for x in grenades if x.effective]
    effective_percentage = len(effective)/total

    if effective_percentage >= FLASH_EFF_SUCCESS:
        successful_advice = 2
    elif FLASH_EFF_USELESS < effective_percentage < FLASH_EFF_SUCCESS:
        successful_advice = 1
    else:
        successful_advice = 0

    mean_duration = 0
    for grenade in effective:
        mean_duration += grenade.total_duration

    mean_duration = mean_duration / len(effective)

    if mean_duration >= FLASH_DUR_SUCCESS:
        damage_advice = 2
    elif FLASH_DUR_USELESS < mean_duration < FLASH_DUR_SUCCESS:
        damage_advice = 1
    else:
        damage_advice = 0

    if return_additional_info:
        return successful_advice, damage_advice, effective_percentage, mean_duration
    return successful_advice, damage_advice


def get_he_advices_description(success, damage, **kwargs):
    result = ''
    if success == 2:
        result += 'You have excellent percentage of effectiveness'
    elif success == 1:
        result += 'You have good enough percentage of effectiveness'
    else:
        result += 'You throw mostly useless HE'

    if 'percentage' in kwargs:
        result += f' ({kwargs["percentage"]:.2%})'
    result += ' '

    if abs(damage - success) == 2:
        result += 'but '
    else:
        result += 'and '

    if damage == 2:
        result += 'damage of grenades is very high'
    elif damage == 1:
        result += 'damage of grenades is ok'
    else:
        result += 'damage of grenades is very low'

    if 'mean_damage' in kwargs:
        result += f' ({kwargs["mean_damage"]})'

    result += '.'

    return result


def get_flash_advices_description(success, duration, **kwargs):
    result = ''
    if success == 2:
        result += 'You have excellent percentage of effectiveness'
    elif success == 1:
        result += 'You have good enough percentage of effectiveness'
    else:
        result += 'You throw mostly useless flashes'

    if 'percentage' in kwargs:
        result += f' ({kwargs["percentage"]:.2%})'
    result += ' '

    if abs(duration - success) == 2:
        result += 'but '
    else:
        result += 'and '

    if duration == 2:
        result += 'average total flash time of one flash is very high'
    elif duration == 1:
        result += 'average total flash time of one flash is ok'
    else:
        result += 'average total flash time of one flash is very low'

    if 'mean_duration' in kwargs:
        result += f' ({kwargs["mean_duration"]:.2})'

    result += '.'

    return result
