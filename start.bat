docker run -e POSTGRES_USER=pepe -e POSTGRES_PASSWORD=pepe -e POSTGRES_DB=pepe -p 5432:5432 -d postgres

pushd "frontend/frontend"
start /B npm run dev
popd

pushd migrations
goose postgres "user=pepe dbname=pepe password=pepe" up
popd

pushd "backend/app_service/src"
start /B uvicorn main:app
popd

cd infra
docker-compose up
