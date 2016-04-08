from django.conf import settings
#------------------ Return token if does not exit then create -------------------#
from models import UserSetting
from serializer import UserSettingSerializer


def get_all_usersetting(user_id):
    queryset = UserSetting.objects.filter(user_id=user_id)
    return queryset


def get_setting_value_by_key(getkey, user_id):
    usersettingvalue = UserSetting.objects.get(
        setting_id__key=getkey, user_id=user_id)
    return usersettingvalue


def update_user_setting(getkey, getvalue, user_id):
    getkeydata = UserSetting.objects.filter(
        setting_id__key=getkey, user_id=user_id).update(value=getvalue)
    return getkeydata
