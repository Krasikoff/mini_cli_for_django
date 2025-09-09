# mini_cli_for_django

- Иногда если нужно выполнить какую-нибудь команду в shell. 
К примеру:

```shell
ls -la
echo "SOME_PARAM=XXX" >> .env
touch file.txt
cp db.sqlite3 db_backup.sqlite3
rm somefile.txt
python manage.diffsettings
```
и лезть в ssh на сервере неохота или не представляется возможным.

- Некоторые команды имеют ограничения. Такие как:
```shell
python manage.py makemigrations
python manage.py migrate
```
можно выполнить если БД postgresql, а не sqlite3. Sqlite3 не позволит выполнить миграции, т.к. блокирует БД.


