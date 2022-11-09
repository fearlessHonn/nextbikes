map_styles = {
    'Light': 'mapbox://styles/mapbox/light-v10',
    'Dark': 'mapbox://styles/mapbox/dark-v10',
    'Satellite': 'mapbox://styles/mapbox/satellite-v9',
    'Streets': 'mapbox://styles/mapbox/streets-v11',
    'Outdoors': 'mapbox://styles/mapbox/outdoors-v11',
    'Satellite Streets': 'mapbox://styles/mapbox/satellite-streets-v11',
    'Navigation Day': 'mapbox://styles/mapbox/navigation-day-v1',
    'Navigation Night': 'mapbox://styles/mapbox/navigation-night-v1'
}

color1 = [211, 83, 12]  # D38312
color2 = [168, 32, 79]  # A83279


def get_color(max_id):
    return [
        f"{color1[0]} + {color2[0] - color2[0]} * (id / {max_id})",
        f"{color1[1]} + {color2[1] - color1[1]} * (id / {max_id})",
        f"{color1[2]} + {color2[2] - color1[2]} * (id / {max_id})"
        f"155 + 100 * (id / {max_id})"
    ]
