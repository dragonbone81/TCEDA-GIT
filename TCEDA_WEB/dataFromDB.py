import collections
import requests

language_codes = {
    'source': 'https://datausa.io/',
    '003': 'Spanish',
    '006': 'Other Indic',
    '012': 'German',
    '015': 'Chinese'
}
# do we need two location dicts?--combine into 1
location_codeDict = {
    'merced': '05000US06047',
    'tuolumne': '05000US06109',
    'us': '01000US',
    'california': '04000US06',
}
location_dict = {
    location_codeDict.get('merced'): 'Merced',
    location_codeDict.get('tuolumne'): 'Tuolumne',
    location_codeDict.get('us'): 'United States',
    location_codeDict.get('california'): 'California',
}


def base_tuolumne_pop():
    """
    gets the latest population for toulumne
    :return: population of tuoulumne for most recent non projected year
    """
    """
    gets only latest population--might screw up percentages for years not "latest"
    """

    source = 'https://datausa.io/'
    url = 'https://api.datausa.io/api?show=geo&sumlevel=county&required=pop&year=latest&geo=05000US06109'
    r = requests.get(url)
    return r.json()['data'][0][2]


def base_us_pop():
    """
    gets latest population for US--same problem as above
    :return: population of US for most recent non projected year
    """
    source = 'https://datausa.io/'
    url = 'https://api.datausa.io/api?show=geo&sumlevel=nation&required=pop&year=latest'
    r = requests.get(url)
    return r.json()['data'][0][2]


def population_from_db():
    """
    gets population by year
    :return: out_dict- header, data, source
    """
    future_years = 8  # amount of years in future population is predicted
    source = 'https://www.opendatanetwork.com/'
    headers = {
        'X-App-Token': 'cQovpGcdUT1CSzgYk0KPYdAI0'
    }
    url = 'https://api.opendatanetwork.com/data/v1/values?app_token=cQovpGcdUT1CSzgYk0KPYdAI0&' \
          'forecast=%s&variable=demographics.population.count&' \
          'entity_id=0500000US06109&format=null&describe=true' % future_years
    r = requests.get(url, headers=headers)
    x = True
    out = collections.OrderedDict()
    header = {
        'year': 'Year',
        'projected': 'Projected',
        'population': 'Population',
    }
    # dict insertion too complication- simplify
    for year in r.json()['data']:
        if x:
            x = False
            continue
        else:
            date = year[0]
            population = year[1]
            projected = year[2]
            year_data = "Year %s: %s" % (date, int(population))
            if projected:
                year_data += " (Projected)"

            out.update(
                {
                    date: {
                        'date': date,
                        'population': population,
                        'projected': projected,
                    }
                }
            )
    out_dict = {
        'header': header,
        'data': out,
        'source': source,
    }
    return out_dict


def population_by_raceDB():
    """
    gets population by race distribution
    :return: out_dict - list[header], data, source
    """
    source = 'https://datausa.io/'
    url = 'https://api.datausa.io/api/?sort=desc&force=acs.yg_race&show=geo&sumlevel=all&year=all&geo=05000US06109'
    r = requests.get(url)
    headers = r.json()['headers']
    data = r.json()['data']
    race_info = {}
    tuolumne_popu = base_tuolumne_pop()
    for race in data:
        race_info.update(
            {
                race[0]: collections.OrderedDict(zip(headers, race))

            }
        )
    for key, year in race_info.iteritems():
        for key1, data in year.iteritems():
            if u'year' in key1 or u'geo' in key1 or key1.endswith('moe') or data == 0:
                pass
            else:
                year[key1] = "%s -> Percentage: %s%%" % (data, (data / tuolumne_popu) * 100)
                # not the best solution but meh--fix
    out_dict = {
        'header': headers,
        'data': race_info,
        'source': source,
    }
    return out_dict


def house_income_distDB():
    """
    gets house income distribution
    :return: dict { list[header], data, source }
    """
    source = 'https://datausa.io/'
    url = 'https://api.datausa.io/api/?sort=desc&force=acs.yg_income_distribution&show=geo&sumlevel=all&year=all&geo=01000US%2C05000US06109'
    r = requests.get(url)
    headers = r.json()['headers']
    data = r.json()['data']
    income_info = {}
    tuolumne_popu = base_tuolumne_pop()
    pop_us = base_us_pop()
    for income in data:
        income_info.update(
            {
                "%s->%s" % (income[0], income[1]): collections.OrderedDict(zip(headers, income))

            }
        )
    for key, year in income_info.iteritems():
        for key1, data in year.iteritems():
            if u'year' in key1 or u'geo' in key1 or key1.endswith('moe') or data == 0:
                pass
            else:
                if key.endswith('US'):
                    # year[key1] = "%s -> Percentage: %s%%" % (data, (data / pop_us) * 100)
                    year[key1] = (data / pop_us) * 100
                else:
                    # year[key1] = "%s -> Percentage: %s%%" % (data, (data / tuolumne_popu) * 100)
                    year[key1] = (data / tuolumne_popu) * 100
                    # not the best solution but meh
    return {
        'data': income_info,
        'header': headers,
        'source': source,
    }


def language_distDB():
    """
    gets language distribution by population
    :return: dict { list[header], data, source }
    """
    source = 'https://datausa.io/'
    url = 'https://api.datausa.io/api/?sort=desc&show=geo&where=language%3A%7E%5E002%2Cnum_speakers%3A%210&required=num_speakers%2Cnum_speakers_moe&sumlevel=all&year=all&geo=05000US06109'
    r = requests.get(url)
    out = {}
    # dict insertions is way too complicated---simplify
    for language in r.json()['data']:
        year = language[0]
        if year not in out:
            out.update(
                {
                    year: {
                        language[2]: [
                            language[0],
                            "%s -> %s" % (str(language[2]), language_codes.get(str(language[2]))),
                            language[3],
                            language[4],
                        ]
                    }
                }
            )
        else:
            out[year].update(
                {
                    language[2]: [
                        language[0],
                        "%s -> %s" % (str(language[2]), language_codes.get(str(language[2]))),
                        language[3],
                        language[4],
                    ]
                }
            )
    return {
        'data': out,
        'header': [
            'Year',
            'Language',
            'People',
            'Margin Of Error',
        ],
        'source': source,
    }


def household_incomeDB():
    """
    gets household income for different years-tuolunmne county
    :return: out_dict- header, data, source
    """
    source = 'https://datausa.io/'
    url = 'https://api.datausa.io/api/?sort=desc&show=geo&required=income%2Cincome_moe&sumlevel=all&year=all&geo=01000US%2C04000US06%2C05000US06109%2C05000US06047'
    r = requests.get(url)
    # why???
    header = {}
    header.update({
        'year': 'Year',
        'location': 'Location',
        'income': 'Median Household Income',
    })
    out = {}
    for location in r.json()['data']:
        year = location[0]
        location_code = location[1]
        income = location[2]
        if year not in out:
            out.update(
                {
                    year: {
                        location_code: {
                            'location': location_dict[location_code],
                            'income': income,
                            'year': year,
                        }
                    }
                }
            )
        else:
            out[year].update(
                {
                    location_code: {
                        'location': location_dict[location_code],
                        'income': income,
                        'year': year,
                    }
                }
            )
    out_dict = {
        'header': header,
        'data': out,
        'source': source,
    }
    return out_dict
