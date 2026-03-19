from app.services.google_places import get_route

def calculate_distance(origin: str, destination: str) -> dict:
    """
    Calcula a distância entre dois locais usando a API de Direções do Google.
    
    :param origin: Local de origem.
    :param destination: Local de destino.
    :return: Dicionário com informações sobre a rota e distância.
    """
    route_data = get_route(origin, destination)
    
    if 'routes' in route_data and len(route_data['routes']) > 0:
        route = route_data['routes'][0]
        distance = route['legs'][0]['distance']
        duration = route['legs'][0]['duration']
        
        return {
            "distance": distance['text'],
            "duration": duration['text'],
            "steps": route['legs'][0]['steps']
        }
    
    return {"error": "No route found"}