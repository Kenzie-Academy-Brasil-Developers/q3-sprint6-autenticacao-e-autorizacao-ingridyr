<p align="center">
    Essa API foi contruída com objetivo de treinar cadastros e logins.
</p>

<h2 align ='center'> API </h2>
<h3 align ='center'> Cadastro de uma novo usuário </h3>

`POST /api/signup - FORMATO DA REQUISIÇÃO:`

```json
{
    "name": "John",
    "last_name": "Wick",
    "email": "johnwick@gmail.com",
    "password": "BabaYaga"
}
```

`POST /api/signup - FORMATO DA RESPOSTA - STATUS 201:`

```json
{
	"name": "John",
	"last_name": "Wick",
	"email": "johnwick@gmail.com"
}
```

<h3 align ='center'> Login </h3>

`POST /api/login - FORMATO DA REQUISIÇÃO:`

```json
{
    "email": "johnwick@gmail.com",
    "password": "BabaYaga"
}
```

`POST /api/login - FORMATO DA RESPOSTA - STATUS 200:`

```json
{
	"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MTUxNDk0NSwianRpIjoiMjI3MzNlYTUtYjI1Mi00MjM4LTg5YjItZDBkYzFjMTBmMjZiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MiwibmFtZSI6IkpvaG4iLCJsYXN0X25hbWUiOiJXaWNrIiwiZW1haWwiOiJqb2hud2lja0BnbWFpbC5jb20iLCJwYXNzd29yZF9oYXNoIjoicGJrZGYyOnNoYTI1NjoyNjAwMDAkdnRld1B2Q28ybEF5QkY0SCQ4NGJlZDVjOWE5NmZhYzEyYWUxMGEwMmViYjZhMjZmNGYyNTQzMGZiYzg5NzE1Nzc3ZGJhY2ExYTcwMzUxMzA2In0sIm5iZiI6MTY1MTUxNDk0NSwiZXhwIjoxNjUxNjAxMzQ1fQ.WO5DUHIY1hWw7LVIUeaMPIeC-1ryGCbazYxlNz3Iwcg"
}
```

<h3 align ='center'> Atualização das informações do usuário </h3>

`PUT /api - FORMATO DA REQUISIÇÃO:`

```json
{
    "name": "John",
    "last_name": "Wick II",
    "email": "johnwick@gmail.com",
    "password": "BabaYaga"
}
```

`PUT /api - FORMATO DA RESPOSTA - STATUS 200:`

```json
{
	"name": "John",
	"last_name": "Wick II",
	"email": "johnwick@gmail.com"
}
```

<h3 align ='center'> Visualização de informações do usuário </h3>

`GET /api`

<blockquote>
  Obs: não possui corpo de requisição.
  -> Necessário access_token (gerado no login) inserido no headers para autorização de acesso. 
</blockquote>

`GET /api - FORMATO DA RESPOSTA - STATUS 200:`

```json
{
	"name": "John",
	"last_name": "Wick II",
	"email": "johnwick@gmail.com"
}
```