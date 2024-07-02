## Registro de Nuevo Usuario

Registra un nuevo usuario en el sistema.

### URL

```
POST /auth/users/
```

### Parámetros de la Solicitud

| Nombre       | Tipo    | Descripción                             |
|--------------|---------|-----------------------------------------|
| email        | string  | Correo electrónico del nuevo usuario.    |
| first_name   | string  | Nombre del nuevo usuario.                |
| last_name    | string  | Apellido del nuevo usuario.              |
| password     | string  | Contraseña del nuevo usuario.            |
| re_password  | string  | Confirmación de la contraseña.          |

### Ejemplo de Cuerpo de Solicitud

```json
{
    "email": "some_email@gmail.com",
    "first_name": "some_name",
    "last_name": "some_last_name",
    "password": "Test12345",
    "re_password": "Test12345"
}
```

### Respuesta Exitosa

- Código de Estado: 201 Created
- Body de Respuesta:

```json
{
    "message": "Usuario registrado exitosamente."
}
```

### Respuestas de Error

- Código de Estado: 400 Bad Request
- Body de Respuesta (ejemplo):

```json
{
    "error": "Los campos 'password' y 're_password' no coinciden."
}
```

- Código de Estado: 409 Conflict
- Body de Respuesta (ejemplo):

```json
{
    "error": "El correo electrónico ya está registrado en el sistema."
}
```

### Notas

- Asegúrate de que la contraseña cumpla con los requisitos de seguridad establecidos (longitud, complejidad, etc.).
- El campo 're_password' se utiliza para verificar que la contraseña haya sido ingresada correctamente.
- Si se produce un error, se devolverá un mensaje descriptivo junto con el código de estado correspondiente.

Para documentar el endpoint de activación de usuario que proporcionas, podemos seguir un formato similar al anterior, pero adaptado específicamente para este caso de uso:


## Activación de Usuario

Activa la cuenta de usuario utilizando el token proporcionado.

### URL

```
POST /auth/users/activation/
```

### Parámetros de la Solicitud

| Nombre | Tipo   | Descripción                              |
|--------|--------|------------------------------------------|
| uid    | string | Identificador único del usuario a activar.|
| token  | string | Token de activación generado para el usuario.|

### Ejemplo de Cuerpo de Solicitud

```json
{
    "uid": "MQ",
    "token": "c9k7oz-3ef36d97f963d3e9004344ebd26eb146"
}
```

### Respuesta Exitosa

- Código de Estado: 200 OK
- Body de Respuesta:

```json
{
    "detail": "La cuenta ha sido activada exitosamente."
}
```

### Respuestas de Error

- Código de Estado: 400 Bad Request
- Body de Respuesta (ejemplo):

```json
{
    "error": "El token proporcionado no es válido."
}
```

- Código de Estado: 404 Not Found
- Body de Respuesta (ejemplo):

```json
{
    "error": "El usuario con el UID especificado no existe."
}
```

### Notas

- El endpoint `POST /auth/users/activation/` se utiliza para activar la cuenta de un usuario utilizando el `uid` y el `token` proporcionados.
- Se recomienda generar y enviar el token de activación por correo electrónico al usuario durante el proceso de registro.
- Si el usuario intenta activar una cuenta que ya está activada, se puede manejar devolviendo un mensaje apropiado junto con el código de estado correspondiente.

Para documentar el endpoint `localhost:8000/auth/jwt/refresh` que permite refrescar el token de acceso JWT, aquí tienes una guía utilizando Markdown:

Para documentar el endpoint `localhost:8000/auth/jwt/create`, que genera tokens de acceso y actualización basados en credenciales de usuario, puedes estructurar la documentación de la siguiente manera:

---

## Crear Tokens JWT

Crea tokens de acceso y actualización utilizando las credenciales de usuario proporcionadas.

### URL

```
POST /auth/jwt/create
```

### Parámetros de la Solicitud

| Nombre   | Tipo   | Descripción                              |
|----------|--------|------------------------------------------|
| email    | string | Correo electrónico del usuario.           |
| password | string | Contraseña del usuario.                   |

### Ejemplo de Cuerpo de Solicitud

```json
{
    "email": "some_email@gmail.com",
    "password": "Test12345"
}
```

### Respuesta Exitosa

- Código de Estado: 200 OK
- Body de Respuesta:

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMjU1MzUxMiwiaWF0IjoxNzE5OTYxNTEyLCJqdGkiOiJlMjFlODI5Zjg4NmI0MDdiODJjMTc2NWFmZjhjZDUzMCIsInVzZXJfaWQiOjF9.g9FMTLRjcmlaqOyMkRCgx09i0lHVGiq3PiGqE5Cj5kM",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNTY2MzEyLCJpYXQiOjE3MTk5NjE1MTIsImp0aSI6IjA5N2ZlYjRlODk2ODQyMGRhNjIwMjA2MTMwZWY5OWY1IiwidXNlcl9pZCI6MX0.Flt_jBiksojeTY-Rx9JB3phIqAuJKOjDh1_6rNEywBU"
}
```

### Respuestas de Error

- Código de Estado: 400 Bad Request
- Body de Respuesta (ejemplo):

```json
{
    "error": "Credenciales inválidas."
}
```

- Código de Estado: 401 Unauthorized
- Body de Respuesta (ejemplo):

```json
{
    "error": "Correo electrónico o contraseña incorrectos."
}
```

### Notas

- Este endpoint se utiliza para autenticar al usuario y generar tokens JWT (JSON Web Tokens).
- El token de acceso (`access token`) se utiliza para acceder a recursos protegidos de la API.
- El token de actualización (`refresh token`) se utiliza para obtener un nuevo token de acceso sin necesidad de autenticar al usuario nuevamente.
- Asegúrate de que las credenciales de usuario se envíen de forma segura utilizando HTTPS para proteger la información sensible durante la transmisión.

## Refrescar Token JWT

Refresca el token de acceso JWT utilizando el token de actualización (`refresh token`) proporcionado.

### URL

```
POST /auth/jwt/refresh
```

### Parámetros de la Solicitud

| Nombre   | Tipo   | Descripción                              |
|----------|--------|------------------------------------------|
| refresh  | string | Token de actualización (`refresh token`). |

### Ejemplo de Cuerpo de Solicitud

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMjU1MzUxMiwiaWF0IjoxNzE5OTYxNTEyLCJqdGkiOiJlMjFlODI5Zjg4NmI0MDdiODJjMTc2NWFmZjhjZDUzMCIsInVzZXJfaWQiOjF9.g9FMTLRjcmlaqOyMkRCgx09i0lHVGiq3PiGqE5Cj5kM"
}
```

### Respuesta Exitosa

- Código de Estado: 200 OK
- Body de Respuesta:

```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNTY2NDU3LCJpYXQiOjE3MTk5NjE1MTIsImp0aSI6ImEyYjc5ZGNhZjI0OTRlY2FiZmQxMzg1YzRkZjE0NmQxIiwidXNlcl9pZCI6MX0.g9zWrEV97dOqVfd_RBYI_mr9cVLwpMgNMc9uavRGBRk"
}
```

### Respuestas de Error

- Código de Estado: 401 Unauthorized
- Body de Respuesta (ejemplo):

```json
{
    "detail": "Token de actualización no válido o expirado."
}
```

- Código de Estado: 400 Bad Request
- Body de Respuesta (ejemplo):

```json
{
    "error": "El token de actualización proporcionado es inválido."
}
```

### Notas

- Este endpoint se utiliza para obtener un nuevo token de acceso (`access token`) utilizando el token de actualización (`refresh token`).
- El token de actualización es utilizado para obtener un nuevo token de acceso sin necesidad de autenticar al usuario nuevamente.
- El token de actualización tiene una vida útil más larga que el token de acceso, lo que permite mantener la sesión activa durante más tiempo.
- Es importante manejar adecuadamente los errores y devolver mensajes claros que indiquen la causa del problema en caso de que la solicitud falle.

Para documentar el endpoint `localhost:8000/auth/jwt/verify`, que verifica la validez de un token JWT, aquí tienes una guía utilizando Markdown:

---

## Verificar Token JWT

Verifica la validez del token de acceso JWT proporcionado.

### URL

```
POST /auth/jwt/verify
```

### Parámetros de la Solicitud

| Nombre | Tipo   | Descripción                              |
|--------|--------|------------------------------------------|
| token  | string | Token de acceso JWT a verificar.          |

### Ejemplo de Cuerpo de Solicitud

```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNTY2NDU3LCJpYXQiOjE3MTk5NjE1MTIsImp0aSI6ImEyYjc5ZGNhZjI0OTRlY2FiZmQxMzg1YzRkZjE0NmQxIiwidXNlcl9pZCI6MX0.g9zWrEV97dOqVfd_RBYI_mr9cVLwpMgNMc9uavRGBRk"
}
```

### Respuesta Exitosa

- Código de Estado: 200 OK
- Body de Respuesta:

```json
{}
```

### Respuestas de Error

- Código de Estado: 401 Unauthorized
- Body de Respuesta (ejemplo):

```json
{
    "detail": "Token inválido o expirado."
}
```

- Código de Estado: 400 Bad Request
- Body de Respuesta (ejemplo):

```json
{
    "error": "No se proporcionó un token válido."
}
```

### Notas

- Este endpoint se utiliza para verificar la validez de un token de acceso JWT.
- El token de acceso JWT debe ser enviado en el cuerpo de la solicitud bajo el campo `token`.
- Si el token es válido, se responderá con un código de estado 200 y un cuerpo vacío (`{}`).
- Si el token no es válido (por ejemplo, si ha expirado o es inválido en términos de estructura), se responderá con un código de estado 401 o 400 junto con un mensaje descriptivo.
- Asegúrate de manejar adecuadamente la verificación de tokens JWT para garantizar la seguridad y la integridad de tu sistema de autenticación.

Para documentar el endpoint `localhost:8000/auth/users/me/`, que devuelve la información del usuario autenticado utilizando el token JWT enviado en el encabezado de autorización, puedes seguir esta estructura en Markdown:

---

## Obtener Detalles del Usuario Actual

Obtiene los detalles del usuario autenticado utilizando el token JWT proporcionado en el encabezado de autorización.

### URL

```
GET /auth/users/me/
```

### Encabezados

| Nombre         | Valor                                               |
|----------------|-----------------------------------------------------|
| Authorization  | JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tl... |

### Parámetros de la Solicitud

No se requieren parámetros adicionales en el cuerpo de la solicitud.

### Respuesta Exitosa

- Código de Estado: 200 OK
- Body de Respuesta:

```json
{
    "id": 1,
    "email": "some_email@gmail.com",
    "first_name": "some_name",
    "last_name": "some_last_name",
    "get_full_name": "firts_name_and_last_name",
    "get_short_name": "name"
}
```

### Respuestas de Error

- Código de Estado: 401 Unauthorized
- Body de Respuesta (ejemplo):

```json
{
    "detail": "No se proporcionó un token válido."
}
```

- Código de Estado: 403 Forbidden
- Body de Respuesta (ejemplo):

```json
{
    "detail": "Token de acceso no válido o expirado."
}
```

### Notas

- Este endpoint se utiliza para obtener los detalles del usuario actualmente autenticado.
- El token JWT debe ser enviado en el encabezado de autorización utilizando el formato `Authorization: JWT <token>`.
- Si el token es válido y corresponde a un usuario autenticado, se responderá con un código de estado 200 y los detalles del usuario en formato JSON.
- Asegúrate de manejar adecuadamente la validación del token JWT para garantizar la seguridad y la integridad de tu sistema de autenticación.