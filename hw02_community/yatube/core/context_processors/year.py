from datetime import datetime

def year(request):
    """Добавляет переменную с текущим годом."""
    year = datetime.now()
    year_str = int(year.strftime("%Y"))
    print(year_str)
    return {
       'year': year_str
    }