# API
## Заголовки
Каждый запрос должен сопровождаться следующими `http` заголовками:  
* `Content-Length`  
* `Content-type`  
* `Idempotency-Key`: [UUID-4](https://www.uuidgenerator.net/version4)  
На данный момент единственный поддерживаемый тип контента: `json`

## Ответы
Ввиду компактности API все ответы сервера содержаться в статус кодах и заголовках

### Получение количества свободных мест
####  Запрос
```
curl --request GET \
  --url http://127.0.0.1:4242/ \
  --header 'idempotency-key: 6820f356-995a-4de3-a691-941fd1adba65'
```
#### Ответ
```
200
Server: BaseHTTP/0.6 Python/3.7.0
Date: Mon, 20 May 2019 22:58:17 GMT
Places: 23
````

### Поставить машину на парковку
####  Запрос
```
curl --request POST \
  --url http://127.0.0.1:4242/ \
  --header 'content-type: application/json' \
  --header 'idempotency-key: a622c6fc-3058-42da-9544-8630a9699b8f' \
  --data '{
	"action": "store"
}'
```
#### Ответы
В случае успеха:
```
202
Server: BaseHTTP/0.6 Python/3.7.0
Date: Mon, 20 May 2019 22:35:31 GMT
Position: 5
````
В случае возникновения ошибки
```
400
Server: BaseHTTP/0.6 Python/3.7.0
Date: Mon, 20 May 2019 22:35:31 GMT
Error: Parking lot is full
````

### Забрать машину с парковки
####  Запрос
```
curl --request POST \
  --url http://127.0.0.1:4242/ \
  --header 'content-type: application/json' \
  --header 'idempotency-key: ee82921d-3ca7-4ed4-93a5-c8087be13aa7' \
  --data '{
	"action": "take",
	"position": 5
}'
```
#### Ответы
В случае успеха:
```
202
Server: BaseHTTP/0.6 Python/3.7.0
Date: Mon, 20 May 2019 22:35:31 GMT
````
В случае возникновения ошибки
```
400
Server: BaseHTTP/0.6 Python/3.7.0
Date: Mon, 20 May 2019 23:21:58 GMT
Error: No car at position
````
