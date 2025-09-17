from .models import Genre, Artist


# Global data
def global_data(request):
    return {
        "genres": Genre.objects.all(),
    }
