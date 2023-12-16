# Documentació per fer calls a l'API

## Pujar resultats PBAC

Per pujar els resultats de l'enquesta PBAC s'ha de fer el següent:
- Fer una POST request a l'url: `/api/upload_encuesta_pbac`
- Al body de la POST posar els següents camps:
    - dia = (un numero del 1 en endavant)

    - compresa_poc_tacada = nombre enter
    - compresa_mitja_tacada = nombre enter
    - compresa_molt_tacada = nombre enter
    - compresa_coaguls = nombre enter 

    - tampo_poc_tacat = nombre enter
    - tampo_mitja_tacat = nombre enter
    - tampo_molt_tacat = nombre enter
    - tampo_coaguls = nombre enter 

    - usuari: id de l'usuari que fa la request

## Pujar resultats QOL

Per pujar els resultats de l'enquesta QOL s'ha de fer el següent:
- Fer una POST request a l'url: `/api/upload_encuesta_qol`
- Al body de la POST posar els següents camps:
    - mes_7_dies = boolean
    - mes_3_dies_abunda = boolean
    - regla_molesta = boolean
    - mancha_ropa = boolean
    - manchar_asiiento = boolean
    - evitar_activitats = boolean

    - usuari: id de l'usuari que fa la request

## Descarregar resultats PBAC

Per descarregar els resultats de totes les PBAC

- Fer una GET request a l'url: `/api/get_encuesta_pbac/<int:user_id>`

- Us retornará el següent objecte:

## Descarregar resultats QOL

Per descarregar els resultats de totes les QOL 

- Fer una GET request a l'url: `/api/get_encuesta_qol/<int:user_id>`

- Us retornará el següent objecte: