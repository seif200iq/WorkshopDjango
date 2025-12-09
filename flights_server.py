from mcp.server.fastmcp import FastMCP 
import os
import json

FLIGHT_PATH = os.path.join(os.path.dirname(__file__),"flights.json")
mcp=FastMCP(name="flightInfo")
def _load_flights():
    with open(FLIGHT_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("flights", [])

@mcp.resource("flights://today")
def flights_resource():
 """
 Resource qui expose la liste des vols du jour.
 L'URL 'flights://today' sera visible par Copilot/Claude.
 """
 with open(FLIGHT_PATH, "r", encoding="utf-8") as f:
     return f.read()

def find_flight(flight_number: str) -> str:
    """Trouve un vol par son numéro (ex: AF1234)"""
    flights = _load_flights()

    for flight in flights:
        if flight.get("flight_number", "").upper() == flight_number.upper():
            return f"""✈️ Vol {flight["flight_number"]} ({flight["airline"]})
            {flight["departure_city"]} → {flight["arrival_city"]}
            Départ : {flight["departure_time"]} | Arrivée : {flight["arrival_time"]}
            Statut : {flight["status"]}
            """
    return f"Vol {flight_number} non trouvé aujourd'hui."

@mcp.tool()
def flights_to(destination: str) -> str:
    """Liste tous les vols à destination d'une ville aujourd'hui."""
    flights = _load_flights()

    # Filtrer les vols
    matches = [f for f in flights if destination.lower() in f["arrival_city"].lower()]

    # Aucun vol trouvé
    if not matches:
        return f"Aucun vol trouvé vers {destination.title()} aujourd'hui."

    # Construction du résultat
    result = f"Vols vers {destination.title()} ({len(matches)} trouvé(s)) :\n\n"

    for f in matches:
        result += (
            f"• {f['flight_number']} ({f['airline']}) → "
            f"{f['arrival_city']} à {f['arrival_time']} – {f['status']}\n"
        )

    return result.strip()

@mcp.tool()
def flights_by_status(status: str) -> str:
    """
    Retourne tous les vols ayant un statut particulier.
    Exemples de statuts : 'Retardé', 'À l'heure', 'Annulé', 'En attente', etc.
    """
    flights = _load_flights()
    
    # Filtrer les vols par statut (insensible à la casse)
    matches = [
        f for f in flights 
        if status.lower() in f.get("status", "").lower()
    ]
    
    if not matches:
        return f"Aucun vol trouvé avec le statut '{status}' aujourd'hui."
    
    result = f"Vols avec le statut '{status}' ({len(matches)} trouvé(s)) :\n\n"
    
    for f in matches:
        result += (
            f"• {f['flight_number']} ({f['airline']})\n"
            f"  {f['departure_city']} → {f['arrival_city']}\n"
            f"  Départ : {f['departure_time']} | Arrivée : {f['arrival_time']}\n"
            f"  Statut : {f['status']}\n\n"
        )
    
    return result.strip()

@mcp.tool()
def flights_dashboard() -> str:
    """
    Affiche un tableau de bord complet avec des statistiques sur tous les vols :
    - Nombre total de vols
    - Répartition par statut
    - Répartition par compagnie aérienne
    - Liste des destinations
    """
    flights = _load_flights()
    
    if not flights:
        return "Aucun vol disponible aujourd'hui."
    
    # Statistiques par statut
    status_count = {}
    airline_count = {}
    destinations = set()
    
    for flight in flights:
        status = flight.get("status", "Inconnu")
        status_count[status] = status_count.get(status, 0) + 1
        
        airline = flight.get("airline", "Inconnue")
        airline_count[airline] = airline_count.get(airline, 0) + 1
        
        destinations.add(flight.get("arrival_city", "Inconnue"))
    
    # Construction du tableau de bord
    result = "📊 TABLEAU DE BORD DES VOLS DU JOUR\n"
    result += "=" * 50 + "\n\n"
    
    result += f"✈️ Nombre total de vols : {len(flights)}\n\n"
    
    result += "📈 Répartition par statut :\n"
    for status, count in sorted(status_count.items()):
        percentage = (count / len(flights)) * 100
        result += f"  • {status} : {count} vol(s) ({percentage:.1f}%)\n"
    
    result += "\n🏢 Répartition par compagnie aérienne :\n"
    for airline, count in sorted(airline_count.items(), key=lambda x: x[1], reverse=True):
        result += f"  • {airline} : {count} vol(s)\n"
    
    result += f"\n🌍 Destinations ({len(destinations)}) :\n"
    result += f"  {', '.join(sorted(destinations))}\n"
    
    # Alertes spéciales
    result += "\n⚠️ ALERTES :\n"
    delayed = status_count.get("Retardé", 0)
    if delayed > 0:
        result += f"  ⚠️ {delayed} vol(s) en retard nécessitent une attention\n"
    else:
        result += "  ✅ Aucun vol en retard\n"
    
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio")
