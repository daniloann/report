import peewee
import json
import smtplib

from bd import Country, db, Region, City, Person, Family, FamilyConnection, Relationships, TypeofRelationship

def getbyidcountry(id):
    try:
        if db.is_closed():
            db.connect()
        country = Country.get(Country.id == id)
        country_dict = {
            'id': country.id,
            'name': country.name
        }
        return json.dumps(country_dict, ensure_ascii=False)
    except Exception as e:
        print(f"Error: {e}")
        error_response = {'error': str(e)}
        return json.dumps(error_response, ensure_ascii=False)

def allcountry():
    try:
        if db.is_closed():
            db.connect()
        countrys = Country.select()
        country_dict=[]
        for country in countrys:
            country_dict.append ( {
                'id': country.id,
                'name': country.name
         })
        return json.dumps(country_dict, ensure_ascii=False)
    except Exception as e:
        print(f"Error: {e}")
        error_response = {'error': str(e)}
        return json.dumps(error_response, ensure_ascii=False)

def addcountry(name):
    try:
        if db.is_closed():
            db.connect()
        country = Country.create(name=name)
        country_dict = {
            'id': country.id,
            'name': country.name
        }
        return json.dumps(country_dict, ensure_ascii=False)
    except Exception as e:
        print(f"Error: {e}")
        error_response = {'error': str(e)}
        return json.dumps(error_response, ensure_ascii=False)

def regionsofcountry(id):
    try:
        if db.is_closed():
            db.connect()
        country=Country.get(Country.id==id)
        regions = Region.select().where(Region.idCountry == country.id)
        region_dict = []
        for region in regions:
            region_dict.append  ({
                'id': region.id,
                'name': region.name
            })
        return json.dumps(region_dict, ensure_ascii=False)
    except Exception as e:
        print(f"Error: {e}")
        error_response = {'error': str(e)}
        return json.dumps(error_response, ensure_ascii=False)

def cityesofregion(id):
    try:
        if db.is_closed():
            db.connect()
        region = Region.get(Region.id == id)
        cities = City.select().where(City.idRegion == region.id)
        city_dict = []
        for city in cities:
            city_dict.append ({
                'id': city.id,
                'name': city.name,
                'lat': city.lat,
                'lon': city.lon
            })
        return json.dumps(city_dict, ensure_ascii=False)
    except Exception as e:
        print(f"Error: {e}")
        error_response = {'error': str(e)}
        return json.dumps(error_response, ensure_ascii=False)

def searchperson(fio):
    try:
        if db.is_closed():
            db.connect()
        persons = Person.select()
        person_dict = []
        for person in persons:
            if person.fio.find(fio) != -1:
                person_dict.append ({
                    'id': person.id,
                    'fio': person.fio,
                })
        return json.dumps(person_dict, ensure_ascii=False)

    except Exception as e:
        print(f"Error: {e}")
        error_response = {'error': str(e)}
        return json.dumps(error_response, ensure_ascii=False)

def searchinfo(json_data):
    try:
        if db.is_closed():
            db.connect()
        conditions = []
        if 'gender' in json_data:
            conditions.append (Person.gender == json_data.get ('gender'))

        if 'yearOfBirth' in json_data:
            conditions.append(Person.yearOfBirth == json_data.get ('yearOfBirth'))

        if 'monthOfBirth' in json_data:
            conditions.append(Person.monthOfBirth == json_data.get ('monthOfBirth'))

        if 'dayOfBirth' in json_data:
            conditions.append(Person.dayOfBirth == json_data.get ('dayOfBirth'))

        if 'yearOfDeath' in json_data:
            conditions.append(Person.yearOfDeath == json_data.get('yearOfDeath'))

        if 'monthOfDeath' in json_data:
            conditions.append(Person.monthOfDeath == json_data.get ('monthOfDeath'))

        if 'dayOfDeath' in json_data:
            conditions.append(Person.dayOfDeath == json_data.get ('dayOfDeath'))

        if 'isAlive' in json_data:
            conditions.append(Person.isAlive == json_data.get ('isAlive'))

        if 'idCountryOfBirth' in json_data:
            conditions.append(Person.idCountryOfBirth == json_data.get ('idCountryOfBirth'))

        if 'idCityOfBirth' in json_data:
            conditions.append(Person.idCityOfBirth == json_data.get ('idCityOfBirth'))

        if 'idRegionOfBirth' in json_data:
            conditions.append(Person.idRegionOfBirth == json_data.get ('idRegionOfBirth'))

        ageStart = json_data.get ('ageStart')
        ageEnd = json_data.get ('ageEnd')
        if ageStart is not None and ageEnd is not None:
            if int(ageStart) < int(ageEnd):
                conditions.append (Person.age.between(ageStart,ageEnd))
            else:
                print("Error: Incorrect age range")
                return json.dumps({"Error": "Incorrect age range"}, ensure_ascii=False )
        elif ageStart is not None:
            conditions.append(Person.age >= ageStart)
        elif ageEnd is not None:
            conditions.append(Person.age <= ageEnd)

        persons=Person.select()

        if 'sorting' in json_data:
            sorting = json_data.get('sorting')
            field = sorting.get ('field')
            direction = sorting.get ('direction')
            if field and direction:
                sort = None
                if field == 'name':
                    sort = Person.name
                elif field == 'surname':
                    sort = Person.surname
                elif field == 'yearOfBirth':
                    sort = Person.yearOfBirth
                elif field == 'yearOfDeath':
                    sort = Person.yearOfDeath
                if field is not None:
                    if direction == 'ASC':
                        persons = persons.order_by(sort.asc())
                    elif direction == 'DESC':
                        persons = persons.order_by(sort.desc())

        if 'pageSize' in json_data and 'pageOffset' in json_data:
            pageSize = int(json_data.get('pageSize'))
            pageOffset = int(json_data.get ('pageOffset'))
            persons = persons.limit(pageSize).offset(pageOffset)

        if conditions:
            persons = persons.where(*conditions)

        person_dict = []
        for person in persons:
            person_data= {
                'id': person.id or 0,
                'name': person.name or "",
                'patronymic': person.patronymic or "",
                'surname': person.surname or "",
                'phone': person.phone or 0,
                'yearOfBirth' : person.yearOfBirth or 0,
                'monthOfBirth' : person.monthOfBirth or 0,
                'dayOfBirth' : person.dayOfBirth or 0,
                'yearOfDeath' : person.yearOfDeath or 0,
                'monthOfDeath' : person.monthOfDeath or 0,
                'dayOfDeath': person.dayOfDeath or 0,
                'gender': person.gender or 0,
                'school':person.school or "",
                'college': person.college or "",
                'university': person.university or "",
                'work': person.work or "",
                'email': person.email or "",
                'password':person.password or "",
                'age': person.age or 0,
                'role': person.role or 0,
                'isActive':person.isActive or 0,
                'isAlive' : person.isAlive or 0,
                'idCountry' : person.idCountry.name if person.idCountry else 0,
                'idCity' : person.idCity.name if person.idCity else 0,
                'idRegion' : person.idRegion.name if person.idRegion else 0,
                'idCountryOfBirth': person.idCountryOfBirth.name if person.idCountryOfBirth else 0,
                'idCityOfBirth': person.idCityOfBirth.name if person.idCityOfBirth else 0,
                'idRegionOfBirth': person.idRegionOfBirth.name if person.idRegionOfBirth else 0
            }
            person_dict.append(person_data)
        return json.dumps(person_dict, ensure_ascii=False)

    except Exception as e:
        print(f"Error: {e}")
        error_response = {'error': str(e)}
        return json.dumps(error_response, ensure_ascii=False)

from enum import Enum
class Relation(Enum):
    father =1
    mother =2
    daughter =3
    son=4
    wife=5
    husband =6

def getbyId(json_data):
    try:
        if db.is_closed():
            db.connect()
        idPerson = None
        idFamily = None
        if 'idPerson' in json_data:
            idPerson = json_data.get ('idPerson')
        if 'idFamily' in json_data:
            idFamily = json_data.get ('idFamily')
        relativies = {
            'father': None,
            'mother': None,
            'husband': [],
            'wife': [],
            'daughter': [],
            'son': []
        }
        from_relationships = Relationships.select().where(Relationships.fromId == idPerson).execute()
        from_rel = []
        for rel in from_relationships:
            if FamilyConnection.select().where((FamilyConnection.idFamily==idFamily) &
                                               (FamilyConnection.idPerson == rel.fromId)).exists():
                from_rel.append(rel)
                for relationship in from_rel:
                    relation_type = TypeofRelationship.select().where(
                        TypeofRelationship.id == relationship.typeId).get()
                    rel_type = relation_type.name
                    other_person = Person.get(Person.id == relationship.toId)
                    person_info = {
                        'id': other_person.id,
                        'name': other_person.name,
                        'surname': other_person.surname,
                        'gender': other_person.gender
                    }
                    if rel_type == Relation.father.name:
                        relativies['father'] = person_info
                    elif rel_type == Relation.mother.name:
                        relativies['mother'] = person_info
                    elif rel_type == Relation.son.name:
                        if person_info not in relativies['son']:
                            relativies['son'].append(person_info)
                    elif rel_type == Relation.daughter.name:
                        if person_info not in relativies['daughter']:
                            relativies['daughter'].append(person_info)
                    elif rel_type == Relation.wife.name:
                        if person_info not in relativies['wife']:
                            relativies['wife'].append(person_info)
                    elif rel_type == Relation.husband.name:
                        if person_info not in relativies['husband']:
                            relativies['husband'].append(person_info)

        to_relationships = Relationships.select().where(Relationships.toId == idPerson)
        to_rel = []

        for rel in to_relationships:
            if FamilyConnection.select().where((FamilyConnection.idFamily == idFamily) &
                                               (FamilyConnection.idPerson == rel.toId)).exists():
                to_rel.append(rel)
                for relationship in to_rel:
                    relation_type = TypeofRelationship.select().where(
                        TypeofRelationship.id == relationship.typeId).get()
                    rel_type = relation_type.name
                    other_person = Person.get(Person.id == relationship.fromId)
                    person_info = {
                        'id': other_person.id,
                        'name': other_person.name,
                        'surname': other_person.surname,
                        'gender': other_person.gender
                    }
                    if rel_type == Relation.son.name:
                        if not relativies['father']:
                            relativies['father'] = person_info
                    elif rel_type == Relation.daughter.name:
                        if not relativies['mother']:
                            relativies['mother'] = person_info
                    elif rel_type == Relation.father.name:
                        if other_person.gender == 1:
                            if person_info not in relativies['son']:
                                relativies['son'].append(person_info)
                        else:
                            if person_info not in relativies['daughter']:
                                relativies['daughter'].append(person_info)
                    elif rel_type == Relation.mother.name:
                        if other_person.gender == 1:
                            if person_info not in relativies['son']:
                                relativies['son'].append(person_info)
                        else:
                            if person_info not in relativies['daughter']:
                                relativies['daughter'].append(person_info)
                    elif rel_type == Relation.husband.name:
                        if person_info not in relativies['wife']:
                            relativies['wife'].append(person_info)
                    elif rel_type == Relation.wife.name:
                        if person_info not in relativies['husband']:
                            relativies['husband'].append(person_info)

        person = Person.get(Person.id == idPerson)
        family = Family.get(Family.id == idFamily)

        result = {
            'id_Person': person.id,
            'name': person.name or "",
            'patronymic': person.patronymic or "",
            'surname': person.surname or "",
            'phone': person.phone or 0,
            'yearOfBirth' : person.yearOfBirth or 0,
            'monthOfBirth' : person.monthOfBirth or 0,
            'dayOfBirth' : person.dayOfBirth or 0,
            'yearOfDeath' : person.yearOfDeath or 0,
            'monthOfDeath' : person.monthOfDeath or 0,
            'dayOfDeath': person.dayOfDeath or 0,
            'gender': person.gender or 0,
            'school':person.school or "",
            'college': person.college or "",
            'university': person.university or "",
            'work': person.work or "",
            'email': person.email or "",
            'password':person.password or "",
            'age': person.age or 0,
            'role': person.role or 0,
            'isActive':person.isActive or 0,
            'isAlive' : person.isAlive or 0,
            'idCountry' : person.idCountry.name if person.idCountry else 0,
            'idCity' : person.idCity.name if person.idCity else 0,
            'idRegion' : person.idRegion.name if person.idRegion else 0,
            'idCountryOfBirth': person.idCountryOfBirth.name if person.idCountryOfBirth else 0,
            'idCityOfBirth': person.idCityOfBirth.name if person.idCityOfBirth else 0,
            'idRegionOfBirth': person.idRegionOfBirth.name if person.idRegionOfBirth else 0,
            'idFamily' : idFamily,
            'name_family':family.name,
            'relatives': relativies
        }
        return json.dumps(result, ensure_ascii=False)

    except Exception as e:
        print(f"Error: {e}")
        error_response = {'error': str(e)}
        return json.dumps(error_response, ensure_ascii=False)

def password(json_data):
    try:
        if db.is_closed():
            db.connect()
        if 'idPerson' in json_data:
            idPerson = json_data.get ('idPerson')
        if 'password' in json_data:
            password = json_data.get ('password')
        if 'new_password' in json_data:
            new_password = json_data.get('new_password')
        person = Person.get (Person.id==idPerson)
        if person.password != password:
            print("Error: Incorrect password")
            return json.dumps({"Error": "Incorrect password"}, ensure_ascii=False)
        else:
            person.password = new_password
            person.save()
            if person.email is not None:
                smtp_server = "smtp.gmail.com"
                port = 587  # для TLS, порт 465 — для SSL
                server = smtplib.SMTP(smtp_server, port)
                server.starttls()
                email = "davidkroll42@gmail.com"
                email_password = ""
                server.login(email, email_password)
                from_email = email
                to_email = "danilovaanna607@gmail.com"
                subject = "Изменение пароля"
                message = f"Привет,{person.name}! Изменение пароля прошло успешно."
                server.sendmail(from_email, to_email, f"Subject: {subject}\n\n{message}".encode('utf-8'))
                server.quit()
        return json.dumps('Новый пароль сохранен', ensure_ascii=False)

    except Exception as e:
        print(f"Error: {e}")
        error_response = {'error': str(e)}
        return json.dumps(error_response, ensure_ascii=False)

def get_family_tree(json_data, current_generation=0, visited = None):
    try:
        if db.is_closed():
            db.connect()

        if visited is None:
            visited = set()

        if 'idPerson' in json_data:
            idPerson = json_data.get('idPerson')
        if 'idFamily' in json_data:
            idFamily = json_data.get('idFamily')
        if 'max_generation' in json_data:
            max_generation = json_data.get('max_generation')
        else:
            max_generation = 3

        if int(current_generation) > int(max_generation):
            return None

        if idPerson in visited:
            return None
        visited.add(idPerson)

        person = Person.get(Person.id==idPerson)

        def get_person_info(person_obj):
            return {
                'idPerson': person_obj.id,
                'idFamily': idFamily,
                'name': person_obj.name,
                'patronymic': person_obj.patronymic or "",
                'surname': person_obj.surname or "",
                'phone': person_obj.phone or 0,
                'yearOfBirth': person_obj.yearOfBirth or 0,
                'monthOfBirth': person_obj.monthOfBirth or 0,
                'dayOfBirth': person_obj.dayOfBirth or 0,
                'yearOfDeath': person_obj.yearOfDeath or 0,
                'monthOfDeath': person_obj.monthOfDeath or 0,
                'dayOfDeath': person_obj.dayOfDeath or 0,
                'gender': person_obj.gender or 0,
                'school': person_obj.school or "",
                'college': person_obj.college or "",
                'university': person_obj.university or "",
                'work': person_obj.work or "",
                'email': person_obj.email or "",
                'password': person_obj.password or "",
                'age': person_obj.age or 0,
                'role': person_obj.role or 0,
                'isActive': person_obj.isActive or 0,
                'isAlive': person_obj.isAlive or 0,
                'idCountry': person_obj.idCountry.name if person_obj.idCountry else 0,
                'idCity': person_obj.idCity.name if person_obj.idCity else 0,
                'idRegion': person_obj.idRegion.name if person_obj.idRegion else 0,
                'idCountryOfBirth': person_obj.idCountryOfBirth.name if person_obj.idCountryOfBirth else 0,
                'idCityOfBirth': person_obj.idCityOfBirth.name if person_obj.idCityOfBirth else 0,
                'idRegionOfBirth': person_obj.idRegionOfBirth.name if person_obj.idRegionOfBirth else 0,
                'father': None,
                'mother': None,
                'husband': [],
                'wife': [],
                'son': [],
                'daughter': []
            }
        relatives = {
            'father': None,
            'mother': None,
            'husband': [],
            'wife': [],
            'daughter': [],
            'son': []
        }
        parents_rel = Relationships.select().where(
            (Relationships.fromId == idPerson) &
            (
                    (TypeofRelationship.name == Relation.father.name) |
                    (TypeofRelationship.name == Relation.mother.name)
            )
        ).join(TypeofRelationship).execute()

        for rel in parents_rel:
            parent = Person.get(Person.id == rel.toId)
            parent_info = get_person_info(parent)

            if parent.id == idPerson:
                continue

            if TypeofRelationship.get(TypeofRelationship.id == rel.typeId).name == Relation.father.name:
                if parent.gender == 1:
                    relatives['father'] = parent_info
            elif TypeofRelationship.get(TypeofRelationship.id == rel.typeId).name == Relation.mother.name:
                if parent.gender == 0:
                    relatives['mother'] = parent_info

            if int(current_generation) + 1 <= int(max_generation):
                recursive_data = {
                    'idPerson': parent.id,
                    'idFamily': idFamily,
                    'max_generation': max_generation
                }
                recursive_result = get_family_tree(recursive_data, current_generation + 1, visited)
                if recursive_result:
                    recursive_data = json.loads(recursive_result)
                    if TypeofRelationship.get(TypeofRelationship.id == rel.typeId).name == Relation.father.name:
                        if parent.gender == 1:
                            relatives['father'].update({
                                'father': recursive_data.get('father'),
                                'mother': recursive_data.get('mother')
                             })
                    elif TypeofRelationship.get(TypeofRelationship.id == rel.typeId).name == Relation.mother.name:
                        if parent.gender == 0:
                            relatives['mother'].update({
                                'father': recursive_data.get('father'),
                                'mother': recursive_data.get('mother')
                             })

        child_rel = Relationships.select().where(
            (Relationships.fromId == idPerson) &
            (
                    (TypeofRelationship.name == Relation.son.name) |
                    (TypeofRelationship.name == Relation.daughter.name)
            )
        ).join(TypeofRelationship).execute()
        child_relationships=[]

        added_child= set()

        for rel in child_rel:
            if FamilyConnection.select().where((FamilyConnection.idFamily == idFamily) &
                                                (FamilyConnection.idPerson == rel.fromId)).exists() \
                    and FamilyConnection.select().where((FamilyConnection.idFamily == idFamily) &
                                                        (FamilyConnection.idPerson == rel.toId)).exists():
                child_relationships.append(rel)
            for rel in child_relationships:
                child = Person.get(Person.id == rel.toId)
                child_info = get_person_info(child)
                rel_type = TypeofRelationship.get(TypeofRelationship.id == rel.typeId).name
                if child.id == idPerson:
                    continue

                if child.id not in added_child:
                    if TypeofRelationship.get(TypeofRelationship.id == rel.typeId).name == Relation.son.name:
                        if child.gender == 1:

                            relatives['son'].append(child_info)
                            added_child.add(child.id)
                    else:
                        relatives['daughter'].append(child_info)
                        added_child.add(child.id)
                if current_generation + 1 <= int(max_generation):
                    recursive_data = {
                            'idPerson': child.id,
                            'idFamily': idFamily,
                            'max_generation': max_generation
                        }
                    recursive_result = get_family_tree(recursive_data, current_generation + 1, visited.copy())
                    if recursive_result:
                        recursive_data = json.loads(recursive_result)
                        if rel_type == Relation.son.name:
                            for son in relatives['son']:
                                if son['idPerson'] == child.id:
                                    son.update({
                                        'daughter': recursive_data.get('daughter'),
                                        'wife':recursive_data.get('wife'),
                                        'husband': recursive_data.get('husband'),
                                        'son': recursive_data.get('son')
                                    })
                        else:
                            for daughter in relatives['daughter']:
                                if daughter['idPerson'] == child.id:
                                    daughter.update({
                                        'daughter': recursive_data.get('daughter'),
                                        'wife':recursive_data.get('wife'),
                                        'husband': recursive_data.get('husband'),
                                        'son': recursive_data.get('son')
                                    })

        wife_rel = Relationships.select().where(
            (Relationships.fromId == idPerson) &
            (TypeofRelationship.name == Relation.wife.name)
        ).join(TypeofRelationship).execute()

        added_wives = set()

        wife_relationships =[]

        for rel in wife_rel:
            if FamilyConnection.select().where((FamilyConnection.idFamily == idFamily) &
                                                (FamilyConnection.idPerson == rel.fromId)).exists() \
                    and FamilyConnection.select().where((FamilyConnection.idFamily == idFamily) &
                                                (FamilyConnection.idPerson == rel.toId)).exists():
                wife_relationships.append(rel)
            for relationship in wife_relationships:
                wife_id = relationship.toId
                if wife_id == idPerson:
                    continue
                if wife_id not in added_wives:
                    wife = Person.get(Person.id == wife_id)
                    wife_info = get_person_info(wife)
                    relatives['wife'].append(wife_info)
                    added_wives.add(wife_id)
                    if current_generation + 1 <= int(max_generation):
                        recursive_data = {
                            'idPerson': wife_id,
                            'idFamily': idFamily,
                            'max_generation': max_generation
                        }
                        recursive_result = get_family_tree(recursive_data, current_generation + 1, visited.copy())
                        if recursive_result:
                            recursive_data = json.loads(recursive_result)
                            for wife in relatives['wife']:
                                if wife['idPerson'] == wife_id:
                                    wife.update({
                                        'father': recursive_data.get('father'),
                                        'mother': recursive_data.get('mother'),
                                        'son': recursive_data.get('son'),
                                        'daughter': recursive_data.get('daughter')
                                    })

        husband_rel = Relationships.select().where(
            (Relationships.fromId == idPerson) &
            (TypeofRelationship.name == Relation.husband.name)
        ).join(TypeofRelationship).execute()
        added_husbands = set()
        husband_relationships=[]
        for rel in husband_rel:
            if FamilyConnection.select().where((FamilyConnection.idFamily == idFamily) &
                                               (FamilyConnection.idPerson == rel.fromId)).exists() \
                    and FamilyConnection.select().where((FamilyConnection.idFamily == idFamily) &
                                                        (FamilyConnection.idPerson == rel.toId)).exists():
                husband_relationships.append(rel)
            for relationship in husband_relationships:
                husband_id = relationship.toId
                if husband_id == idPerson:
                    continue
                if husband_id not in added_husbands:
                    husband = Person.get(Person.id == husband_id)
                    husband_info = get_person_info(husband)
                    relatives['husband'].append(husband_info)
                    added_husbands.add(husband_id)
                    if current_generation + 1 <= int(max_generation):
                        recursive_data = {
                            'idPerson': husband_id,
                            'idFamily': idFamily,
                            'max_generation': max_generation
                        }
                        recursive_result = get_family_tree(recursive_data, current_generation + 1, visited.copy())
                        if recursive_result:
                            recursive_data = json.loads(recursive_result)
                            for husband in relatives['husband']:
                                if husband['idPerson'] == husband_id:
                                    husband.update({
                                        'father': recursive_data.get('father'),
                                        'mother': recursive_data.get('mother'),
                                        'son': recursive_data.get('son'),
                                        'daughter': recursive_data.get('daughter')
                                    })

        result = {
            **get_person_info(person),
            'idFamily': idFamily,
            'father': relatives['father'],
            'mother': relatives['mother'],
            'husband': relatives['husband'],
            'wife': relatives['wife'],
            'son': relatives['son'],
            'daughter': relatives['daughter']
        }
        return json.dumps(result, ensure_ascii=False)

    except Exception as e:
        print(f"Error: {e}")
        error_response = {'error': str(e)}
        return json.dumps(error_response, ensure_ascii=False)
