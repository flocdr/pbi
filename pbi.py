import numpy as np
import pandas as pd
from pandas._libs.tslibs.timedeltas import Timedelta
from pandas.tseries.offsets import MonthBegin, MonthEnd


date_fact = pd.to_datetime('today');
firstDayOfMonth = pd.Timestamp(date_fact.year, date_fact.month, 1);
lastDayOfMonth = firstDayOfMonth + MonthEnd(0);

moves = dataset;
# moves = pd.read_csv('./etmf-smat-mouvements.csv', sep=';')

moves['date_depart'] = pd.to_datetime(moves['date_depart'], format='%d/%m/%Y');
moves['date_arrivee'] = pd.to_datetime(moves['date_arrivee'], format='%d/%m/%Y');
print(moves['date_depart'])
print(moves['date_arrivee'])


moves = moves.sort_values(by='date_depart', ascending=False);

# ETABLISSEMENT DES POINTAGES

mouvements_par_matos = {}
# print(moves)

for index, move in moves.iterrows():
    
    if move['date_arrivee'] == '' :
        move['date_arrivee'] = moves['date_depart'];

    materiel = move['code_materiel']
    date_fin = lastDayOfMonth
    date_debut = move['date_arrivee']
    date_delta = move['date_depart']
    chantier = move['affectation']

    if materiel in mouvements_par_matos.keys():

        date_fin = mouvements_par_matos[materiel][-1]['date_delta']

    else:

        mouvements_par_matos[materiel]=[]

    print(date_debut, date_debut + MonthEnd(0))

    new_item = {
        'imputation' : chantier,
        'date_fin': date_fin,
        'date_debut' : date_debut,
        'date_delta' : date_delta 
    }
    
    mouvements_par_matos[materiel].append(new_item)


    # POINTAGE MENSUEL

pointages = [];

for machine, affectations in mouvements_par_matos.items():
    for affectation in affectations:
        nb_jours = 0;
        day = affectation['date_debut'];
        # print(machine, day)
        while day <= affectation['date_fin']:
            if day.weekday() in [0,1,2,3,4]:
                nb_jours += 1;
            day = day + pd.Timedelta(1, 'days')
        # print(machine, day)

        new_item = (
            machine,
            affectation['imputation'],
            affectation['date_debut'],
            affectation['date_fin'],
            nb_jours
        )
        # print(new_item)
        pointages.append(new_item);

# print(pointages)
pointages_detailed = []

for pointage in pointages:
    date_debut = pointage[2];
    date_fin = pointage[3]
    date_intermediaire = date_debut + MonthEnd(0);
    nb_jours = pd.bdate_range(date_debut, date_intermediaire);
    
    while date_intermediaire < date_fin:
        new_item = (
            pointage[0],
            pointage [1],
            date_debut,
            date_intermediaire,
            len(nb_jours)
        )
        pointages_detailed.append(new_item)
        date_debut = date_intermediaire + pd.Timedelta(1, 'days');
        date_intermediaire = date_debut + MonthEnd(0);
        nb_jours = pd.bdate_range(date_debut, date_intermediaire);

    nb_jours = pd.bdate_range(date_debut, date_fin);
    new_item = (
        pointage[0],
        pointage [1],
        date_debut,
        date_fin,
        len(nb_jours)
    );
    pointages_detailed.append(new_item);


pointages_detailed = np.array(pointages_detailed)
pointages_detailed = pd.DataFrame.from_records(pointages_detailed, columns=['materiel', 'affectation', 'debut', 'fin', 'nb_jours_ouvres']);
# print(pointages_detailed)
