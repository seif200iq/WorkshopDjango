import os
import django
from fastmcp import FastMCP
from asgiref.sync import sync_to_async

# Initialize Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firstProject.settings")
django.setup()

# Importation des modèles Django après initialisation pour éviter des erreurs de configuration
from ConferenceApp.models import Conference
from SessionApp.models import Session

# Create an MCP server
mcp = FastMCP("Conference Assistant")


@mcp.tool()
async def list_conferences() -> str:
    """
    List all available conferences.
    """
    @sync_to_async
    def _get_conferences():
        # Fonction interne synchrone pour récupérer la liste des conférences depuis la base de données
        return list(Conference.objects.all())
    
    conferences = await _get_conferences()
    
    if not conferences:
        return "No conferences found."
    
    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date})"
        for c in conferences
    ])


@mcp.tool()
async def get_conference_details(name: str) -> str:
    """
    Get details of a specific conference by name.
    """
    @sync_to_async
    def _get_conference():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"
    
    conference = await _get_conference()
    
    if conference == "MULTIPLE":
        return f"Multiple conferences found matching '{name}'. Please be more specific."
    
    if not conference:
        return f"Conference '{name}' not found."
    
    return (
        f"Name: {conference.name}\n"
        f"Theme: {conference.get_theme_display()}\n"
        f"Location: {conference.location}\n"
        f"Dates: {conference.start_date} to {conference.end_date}\n"
        f"Description: {conference.description}"
    )


@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """
    List sessions for a specific conference.
    """
    @sync_to_async
    def _get_sessions():
        try:
            conference = Conference.objects.get(name__icontains=conference_name)
            return list(conference.sessions.all()), conference
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None
    
    result, conference = await _get_sessions()
    
    if result == "MULTIPLE":
        return f"Multiple conferences found matching '{conference_name}'. Please be more specific."
    
    if conference is None:
        return f"Conference '{conference_name}' not found."
    
    sessions = result
    
    if not sessions:
        return f"No sessions found for conference '{conference.name}'."
    
    session_list = []
    for s in sessions:
        session_list.append(
            f"- {s.title} ({s.start_time} - {s.end_time}) in {s.room}\n"
            f"  Topic: {s.topic}"
        )
    
    return "\n".join(session_list)


@mcp.tool()
async def filter_conferences(theme: str = None, start_date: str = None, end_date: str = None, location: str = None) -> str:
    """
    Filter conferences by theme, date range, or location.
    You can provide any combination of filters:
    - theme: Filter by conference theme
    - start_date: Filter conferences starting from this date (YYYY-MM-DD format)
    - end_date: Filter conferences ending before this date (YYYY-MM-DD format)
    - location: Filter by location (case-insensitive partial match)
    """
    from django.db.models import Q
    from datetime import datetime
    
    @sync_to_async
    def _filter_conferences():
        queryset = Conference.objects.all()
        
        # Filter by theme if provided
        if theme:
            queryset = queryset.filter(theme__icontains=theme)
        
        # Filter by start_date if provided
        if start_date:
            try:
                date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
                queryset = queryset.filter(start_date__gte=date_obj)
            except ValueError:
                return "ERROR", f"Invalid start_date format. Use YYYY-MM-DD format."
        
        # Filter by end_date if provided
        if end_date:
            try:
                date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
                queryset = queryset.filter(end_date__lte=date_obj)
            except ValueError:
                return "ERROR", f"Invalid end_date format. Use YYYY-MM-DD format."
        
        # Filter by location if provided
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        return list(queryset), None
    
    result, error = await _filter_conferences()
    
    if error:
        return error
    
    conferences = result
    
    if not conferences:
        filters_applied = []
        if theme:
            filters_applied.append(f"theme='{theme}'")
        if start_date:
            filters_applied.append(f"start_date>={start_date}")
        if end_date:
            filters_applied.append(f"end_date<={end_date}")
        if location:
            filters_applied.append(f"location='{location}'")
        
        filter_str = ", ".join(filters_applied) if filters_applied else "applied filters"
        return f"No conferences found matching the {filter_str}."
    
    result_lines = [f"Found {len(conferences)} conference(s) matching the filters:\n"]
    
    for c in conferences:
        result_lines.append(
            f"- {c.name}\n"
            f"  Theme: {c.get_theme_display()}\n"
            f"  Location: {c.location}\n"
            f"  Dates: {c.start_date} to {c.end_date}"
        )
    
    return "\n\n".join(result_lines)


if __name__ == "__main__":
    mcp.run(transport="stdio")

