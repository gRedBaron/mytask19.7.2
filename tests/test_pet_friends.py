from api import PetFriends
from settings import valid_email, valid_password
import os
import random


class TestPetFriends:
    def setup_class(self):
        self.pf = PetFriends()

    def test_get_api_key_for_valid_user(self, email=valid_email, password=valid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

    def test_get_api_key_with_empty_data(self, email='', password=''):
        status, result = self.pf.get_api_key(email, password)
        assert status == 403
        assert False if 'key' in result else True

    def test_get_api_key_for_valid_user_with_invalid_password(self, email=valid_email, password='123pet'):
        status, result = self.pf.get_api_key(email, password)
        assert status == 403
        assert False if 'key' in result else True

    def test_update_last_general_pet_info_with_valid_key(self, name='Тест', animal_type='собака', age=5):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, '')

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status != 200
            assert result['name'] != name
        else:
           raise Exception("There is no my pets")

    def test_get_all_pets_with_valid_key(self, filter=''):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

    def test_get_all_pets_with_invalid_key(self, filter=''):
        auth_key = {'key': hex(random.randint(10 ** 66, 10 ** 67))}
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 403
        assert False if 'pets' in result else True

    def test_get_user_pets_with_valid_key(self, filter='my_pets'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

    def test_add_new_pet_with_valid_key(self, name='Мурзик', animal_type='кот',
                                         age='4', pet_photo=os.path.join('images', 'cat.jpg')):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name
        assert result['pet_photo']

    def test_add_new_pet_with_incorrect_data(self, name='', animal_type=None,
                                         age='five', pet_photo=os.path.join('images', 'text_file.txt')):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 400
        assert not isinstance(result, dict)

    def test_add_new_pet_simple_with_valid_key(self, name='Мурзик', animal_type='кот', age='4'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet_simple(auth_key, name, animal_type, age)
        assert status == 200
        assert result['name'] == name

    def test_successful_update_last_user_pet_info_with_valid_key(self, name='Барсик', animal_type='кот', age=5):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        else:
           raise Exception("There is no my pets")


    def test_successful_set_photo_for_last_user_pet_with_valid_key(
            self, pet_photo=os.path.join('images', 'another_cat.jpg')):

        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
            last_pet_id = my_pets['pets'][0]['id']
            status, result = self.pf.set_pet_photo(auth_key, last_pet_id, pet_photo)
            assert status == 200
            assert result['pet_photo']
        else:
           raise Exception("There is no my pets")

    def test_successful_delete_last_user_pet_with_valid_key(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')

        if len(my_pets['pets']) > 0:
            last_pet_id = my_pets['pets'][0]['id']
            status, result = self.pf.delete_pet(auth_key, last_pet_id)
            assert status == 200
            # т.к. из-за известного бага не приходит тело ответа, сравним id нового крайнего питомца с удаленным
            _, my_pets = self.pf.get_list_of_pets(auth_key, 'my_pets')
            new_last_pet_id = my_pets['pets'][0]['id']
            assert new_last_pet_id != last_pet_id
        else:
           raise Exception("There is no my pets")