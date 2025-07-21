import datetime
import pymysql
from sshtunnel import SSHTunnelForwarder
from peewee import *
import peewee


ssh_host = ""
ssh_port = 22
ssh_username = ''
ssh_password = ''

db_host = ''
db_port = 3306
db_name = ''
db_user = ''
db_password = ''


tunnel = SSHTunnelForwarder(
    (ssh_host, ssh_port),
    ssh_username=ssh_username,
    ssh_password=ssh_password,
    remote_bind_address=(db_host, db_port),
    local_bind_address=('127.0.0.1', 0)
)


tunnel.start()


local_port = tunnel.local_bind_port


db = MySQLDatabase(
    db_name,
    user=db_user,
    password=db_password,
    host='127.0.0.1',
    port=local_port
)

class BaseModel(Model):
    class Meta:
        database = db

class Country(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=255)
    class Meta:
        db_table = "Country"
        order_by = ('created_at',)

class Region(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=255)
    idCountry = ForeignKeyField (Country, related_name='Region_ibfk_1', to_field='id', on_delete='cascade',
                               on_update='cascade',column_name='idCountry', null = True)
    class Meta:
        db_table = "Region"
        order_by = ('created_at',)


class City(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=255)
    idRegion = ForeignKeyField (Region, related_name='City_ibfk_1', to_field='id', on_delete='cascade',
                               on_update='cascade',column_name='idRegion', null = True)
    lat = DoubleField(null=True)
    lon = DoubleField(null=True)
    class Meta:
        db_table = "City"
        order_by = ('created_at',)

class Person(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=255)
    patronymic = CharField(max_length=255)
    surname = CharField(max_length=255)
    maidenName = CharField(max_length=255)
    phone = BigIntegerField(null=True)
    yearOfDeath = IntegerField(null=True)
    monthOfDeath = IntegerField(null=True)
    dayOfDeath = IntegerField(null=True)
    yearOfBirth = IntegerField(null=True)
    monthOfBirth = IntegerField(null=True)
    dayOfBirth = IntegerField(null=True)
    idCountry = ForeignKeyField(Country, related_name='Person_ibfk_544', to_field='id', on_delete='cascade',
                                on_update='cascade', column_name='idCountry', null = True)
    idCity = ForeignKeyField(City, related_name='Person_ibfk_545', to_field='id', on_delete='cascade',
                                on_update='cascade', column_name='idCity',null = True)
    idRegion = ForeignKeyField(Region, related_name='Person_ibfk_546', to_field='id', on_delete='cascade',
                               on_update='cascade', column_name='idRegion',null = True)
    idCountryOfBirth = ForeignKeyField(Country, related_name='Person_ibfk_613', to_field='id', on_delete='cascade',
                                on_update='cascade', column_name='idCountryOfBirth',null = True)
    idCityOfBirth = ForeignKeyField(City, related_name='Person_ibfk_614', to_field='id', on_delete='cascade',
                                on_update='cascade', column_name='idCityOfBirth',null = True)
    idRegionOfBirth = ForeignKeyField(Region, related_name='Person_ibfk_615', to_field='id', on_delete='cascade',
                                on_update='cascade', column_name='idRegionOfBirth',null = True)
    gender = IntegerField()
    school = TextField(null=True)
    college = TextField(null=True)
    university = TextField(null=True)
    work = TextField(null=True)
    comment = TextField(null=True)
    email = CharField(max_length=255)
    password = CharField(max_length=255)
    fio = CharField(max_length=255)
    age = IntegerField(null=True)
    role = IntegerField(null=True)
    isActive = IntegerField(null=True)
    isAlive = IntegerField(null=True)
    marriageinfo = TextField(null=True)
    class Meta:
        db_table = "Person"
        order_by = ('created_at',)

class Family(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=255)
    idFamilyOwner = ForeignKeyField(Person, related_name='Region_ibfk_1', to_field='id', on_delete='cascade',
                            on_update='cascade', column_name='idFamilyOwner', null = True)
    class Meta:
        db_table = "Family"
        order_by = ('created_at',)

class FamilyConnection(BaseModel):
    id = PrimaryKeyField(null=False)
    idPerson = ForeignKeyField(Person, related_name='FamilyConnection_ibfk_207', to_field='id', on_delete='cascade',
                                on_update='cascade', column_name='idPerson', null = True)
    idFamily = ForeignKeyField(Family, related_name='FamilyConnection_ibfk_208', to_field='id', on_delete='cascade',
                                on_update='cascade', column_name='idFamily', null=True)
    class Meta:
        db_table = "FamilyConnection"
        order_by = ('created_at',)

class TypeofRelationship(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=255)
    class Meta:
        db_table = "TypeofRelationship"
        order_by = ('created_at',)

class Relationships(BaseModel):
    id = PrimaryKeyField(null=False)
    fromId = ForeignKeyField(Person, related_name='Relationships_ibfk_265', to_field='id', on_delete='cascade',
                                on_update='cascade', column_name='fromId', null = True)
    toId = ForeignKeyField(Person, related_name='Region_ibfk_266', to_field='id', on_delete='cascade',
                                on_update='cascade', column_name='toId', null=True)
    typeId = ForeignKeyField(TypeofRelationship, related_name='Region_ibfk_267', to_field='id', on_delete='cascade',
                                on_update='cascade', column_name='typeId', null=True)
    class Meta:
        db_table = "Relationships"
        order_by = ('created_at',)

def close_tunnel():
    if tunnel.is_active:
        tunnel.stop()


