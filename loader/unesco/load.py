import pandas as pd
from unesco.models import Category, Region, Iso, States, Site

Category.objects.all().delete()
Region.objects.all().delete()
Iso.objects.all().delete()
States.objects.all().delete()
Site.objects.all().delete()

data = pd.read_csv('unesco/load.csv')

def parse_row(r):
    from unesco.models import Category, Region, Iso, States, Site

    # Category
    try:
        ca = Category.objects.get(name=r['category'])
    except:
        ca = Category(name=r['category'])
        ca.save()

    # Region
    try:
        re = Region.objects.get(name=r['region'])
    except:
        re = Region(name=r['region'])
        re.save()

    # Iso
    try:
        iso = Iso.objects.get(name=r['iso'])
    except:
        iso = Iso(
            name=r['iso'],
            region=re)
        iso.save()

    # States
    try:
        st = States.objects.get(name=r['states'])
    except:
        st = States(
            name=r['states'],
            region = re,
            iso = iso )
        st.save()

    # Site
    try: # check year
        year = int(r['year'])
    except:
        year = None

    try:
        longitude = float(r['longitude'])
    except:
        longitude = None

    try:
        latitude = float(r['latitude'])
    except:
        latitude = None

    try:
        area_hectares = float(r['area_hectares'])
    except:
        area_hectares = None

    si = Site(
        name = r['name'],
        description = r['description'],
        justification = r['justification'],
        year = year,
        longitude = longitude,
        latitude = latitude,
        area_hectares = area_hectares,
        category = ca,
        region = re,
        iso = iso,
        state = st)
    si.save()

data.apply(parse_row, axis=1)
