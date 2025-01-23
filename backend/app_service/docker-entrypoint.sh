#!/bin/bash
# Первый аргумент в этом скрипте, откуда запускать программу, все остальные - аргументы для запуска

# Миграции:

pushd /migrations
# Пытаемся достучаться до БД, пробуя каждую секунду заново
attempts=0
max_attempts=10

while (( attempts < max_attempts )); do
  goose postgres "postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@postgres:5432/$POSTGRES_DB" up
  status=$?

  if [[ $status -eq 0 ]]; then
    echo "Migrations was successfully done"
    break
  fi

  let attempts=attempts+1
  echo "Can't do migrations. Trying again..."

  sleep 1
done

if (( attempt == max_attempts )); then
  echo "Can't do migrations after $attempts attempts. Stopping service."
fi

popd

# Теперь уже запускаем сам сервис
cd $1
shift
$@
