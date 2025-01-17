from typing import List, Tuple, Any
from math import floor


def pattern_element(div: int, speed: int, iterator: int, pattern: list) -> int:
    """Joseph Enguehard's algorithm for solving iteration speed"""
    return floor(iterator * speed / div) % len(pattern)

def compose_parametric_patterns(
    div: int, speed: int, iterator: int, items: List[Tuple[str, Any]],
    cast_to_int: bool = False, midi_overflow_protection: bool = False) -> list:
    final_message = []

    conv_function = int if cast_to_int else float

    for key, value in items:
        if value == []:
            continue
        if isinstance(value, list):
            new_value = value[
                pattern_element(
                    iterator=iterator, div=div, 
                    speed=speed, pattern=value)
            ]
            if new_value is None:
                for decreasing_index in range(iterator, -1, -1):
                    new_value = value[
                        pattern_element(
                            iterator=decreasing_index,
                            div=div,
                            speed=speed,
                            pattern=value,
                        )
                    ]
                    if new_value is None:
                        continue
                    else:
                        value = conv_function(new_value)
                        break
                if value is None:
                    raise ValueError("Pattern does not contain any value")
            else:
                value = conv_function(new_value)

            # Overflow protection takes place here for MIDI values (0-127)
            if midi_overflow_protection:
                if key != 'delay':
                    if value > 127: 
                        value = 127
                    elif value < 0:
                        value = 0
            final_message.extend([key, value])
        else:
            final_message.extend([key, conv_function(value)])

    return final_message

            # for key, value in self.content.items():
            #     if value == []:
            #         continue
            #     if isinstance(value, list):
            #         new_value = value[pattern_element(
            #             iterator=i, div=div, 
            #             speed=speed, pattern=value)]
            #         if new_value is None:
            #             # Besoin d'un index, d'un pattern
            #             for decreasing_index in range(i, -1, -1):
            #                 new_value = value[pattern_element(
            #                     iterator=decreasing_index,
            #                     div=div, speed=speed, 
            #                     pattern=value)]
            #                 if new_value is None:
            #                     continue
            #                 else:
            #                     value = float(new_value)
            #                     break
            #             # Si on a vraiment trouvé aucune valeur, il faut renvoyer une erreur
            #             if value is None:
            #                 raise ValueError('Pattern does not contain any value')
            #         else:
            #             value = float(new_value)
            #         final_message.extend([key, value])
            #     else:
            #         final_message.extend([key, float(value)])

