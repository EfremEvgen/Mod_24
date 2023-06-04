from api import PetFrients
from settings import valid_email, valid_password
import os

pf = PetFrients()
def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Sokr', animal_type='Ovchark',
                                     age='12', pet_photo='images/2.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_valid_data_u(name='Барбоскин', animal_type='двортерьер',
                                         age='4', pet_photo='images/2.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key,'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key,'Vasya', 'Kot', '5', 'images/1.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

def test_put_info_pet(name = 'Rodik', animal_type = 'Oslik', age = 18 ):
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
       raise Exception("There is no my pets")

def test_add_new_pet_without_foto(name = ' Kewka', animal_type = 'Obezyana', age = 45):

    _,auth_key = pf.get_api_key(valid_email,valid_password)

    status, result = pf.add_new_pet_no_foto(auth_key, name, animal_type, age)
    assert  status == 200
    assert result['name'] == name

def test_add_photo_of_pet(pet_photo='images/3.jpg'):
    _,auth_key = pf.get_api_key(valid_email,valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_no_foto(auth_key, 'Dobryi', 'Makak', 6)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.add_foto_pet(auth_key, pet_id, pet_photo)

    assert status == 200
