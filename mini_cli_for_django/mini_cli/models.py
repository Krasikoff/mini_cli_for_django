from django.db import models
import subprocess
import re
from time import sleep

from django.contrib.auth import get_user_model

User = get_user_model()

valid_code_pattern = '[a-zA-Z0-9,;._+:@%/-]'


class Rule(models.Model):
    code = models.TextField("Введите команду ssh")
    was_executed_before = models.BooleanField("Уже выполнялась", default=False)
    log = models.TextField("Результат выполнения", default='None')

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.code

    def save(self, **kwargs):
        if valid_python_code(self.code):
            result = subprocess.run(
                self.code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        else:
            raise Exception
        if not result.returncode:
            self.log = str(result.stdout.decode("utf-8"))
        else:
            self.log = str(result.stderr.decode("utf-8"))
        if 'migrate' in self.code:
            sleep(5)
        super().save(**kwargs)


def valid_python_code(code):
    if re.match(valid_code_pattern, code):
        return True
    return False


# class Test(models.Model):
#     test = models.TextField('test')
#     another_field = models.CharField('field')
