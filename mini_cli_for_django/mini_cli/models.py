from django.db import models
import subprocess
import re
import json 
from time import sleep

from django.contrib.auth import get_user_model
from .constants import FILENAME

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


    def execute(self):
        if valid_python_code(self.code):
            result = subprocess.run(
                self.code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            json_result = {
                'returncode': result.returncode,
                'stdout': result.stdout.decode('utf-8'),
                'stderr': result.stderr.decode('utf-8')
            }
            try:
                with open(FILENAME, 'w') as f:
                    json.dump(json_result,f)
            except Exception as e:
                print(e)
            return result
        else:
            raise Exception

    def save(self, **kwargs):
        with open(FILENAME, 'r') as f:
            result = json.load(f)
        print(result)

        if not result['returncode']:
            self.log = result['stdout']
        else:
            self.log = result['stderr']
        super().save(**kwargs)


def valid_python_code(code):
    if re.match(valid_code_pattern, code):
        return True
    return False


class Test(models.Model):
    test = models.TextField('test')
    another_field = models.CharField('field')
