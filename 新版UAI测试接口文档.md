# 新版 UAI 测试接口文档

## 📌 接口：发送注册验证码

- **请求方法**：`POST`
- **请求地址**：`http://localhost:8000/api/users/auth/send-sms/`
- **请求头部**：

| Key | Value |
|-----|-------|
| Content-Type | application/json |

- **请求 Body（JSON）**：

```json
{
  "phone": "18512292336",
  "code_type": "register"
}
```

---

## 📌 接口：短信验证码注册

- **请求方法**：`POST`
- **请求地址**：`http://localhost:8000/api/users/auth/sms-register/`
- **请求头部**：

| Key | Value |
|-----|-------|
| Content-Type | application/json |

- **请求 Body（JSON）**：

```json
{
  "phone": "18512292336",
  "sms_code": "123456"
}
```

---

## 📌 接口：获取用户资料

- **请求方法**：`GET`
- **请求地址**：`http://localhost:8000/api/users/user/profile/`
- **请求头部**：

| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNTE2Mjk4LCJpYXQiOjE3NTA1MDkwOTgsImp0aSI6ImMxYmY4M2U2N2UwMDQ2ZWZiNzQ3ZTdmODBmYzFjZjQzIiwidXNlcl9pZCI6ImYwMGIyODQ5LTg4ZDktNDlmNC04ZjgzLTczOWEzNzBiMDVjNiJ9.pSJe8YjMX_7TtF_BluxuBAj63rmwfXkvbIZqUivAlrE |


---

## 📌 接口：设置登录密码

- **请求方法**：`POST`
- **请求地址**：`http://localhost:8000/api/users/user/change_password/`
- **请求头部**：

| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNTE2Mjk4LCJpYXQiOjE3NTA1MDkwOTgsImp0aSI6ImMxYmY4M2U2N2UwMDQ2ZWZiNzQ3ZTdmODBmYzFjZjQzIiwidXNlcl9pZCI6ImYwMGIyODQ5LTg4ZDktNDlmNC04ZjgzLTczOWEzNzBiMDVjNiJ9.pSJe8YjMX_7TtF_BluxuBAj63rmwfXkvbIZqUivAlrE |

- **请求 Body（JSON）**：

```json
{
  "new_password": "Test123456",
  "confirm_password": "Test123456"
}
```

---

## 📌 接口：退出登录

- **请求方法**：`POST`
- **请求地址**：`http://localhost:8000/api/users/auth/logout/`
- **请求头部**：

| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNTE4MjgzLCJpYXQiOjE3NTA1MTEwODMsImp0aSI6IjI5NDBiZGMzYWE0ZjQ5MGU4MzBiZDgzMjljODI0NzlmIiwidXNlcl9pZCI6ImYwMGIyODQ5LTg4ZDktNDlmNC04ZjgzLTczOWEzNzBiMDVjNiJ9.InlpzZs8mmmha9v8GDjoXi3Z7mi2JTqwULflxiL3_SU |

- **请求 Body（JSON）**：

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MTExNTg4MywiaWF0IjoxNzUwNTExMDgzLCJqdGkiOiI0ZjkyNDI3NjEyYWY0MjdkODMxNzRkYzZmOWM4NmNjOSIsInVzZXJfaWQiOiJmMDBiMjg0OS04OGQ5LTQ5ZjQtOGY4My03MzlhMzcwYjA1YzYifQ.4brSXDs8Bff2aQvYl59KiEsWRyonvOSfWPpnPBZtb4Y"
}
```

---

## 📌 接口：密码登录测试

- **请求方法**：`POST`
- **请求地址**：`http://localhost:8000/api/users/auth/login/`
- **请求头部**：

| Key | Value |
|-----|-------|
| Content-Type | application/json |

- **请求 Body（JSON）**：

```json
{
  "phone": "18512292336",
  "password": "Test123456"
}
```

---

## 📌 接口：用登录后的新 token 获取用户资料

- **请求方法**：`GET`
- **请求地址**：`http://localhost:8000/api/users/user/profile/`
- **请求头部**：

| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNTE4NzI1LCJpYXQiOjE3NTA1MTE1MjUsImp0aSI6IjY0ZmRjMzNkM2I1MzRhZDVhYzRmNmRjMGJlNDhiNjg1IiwidXNlcl9pZCI6ImYwMGIyODQ5LTg4ZDktNDlmNC04ZjgzLTczOWEzNzBiMDVjNiJ9.18-GBn9h_yGAp3rZGZz8fu9lYJezb9R7hCBj9gKMJDo |


---

## 📌 接口：短信验证码登录流程

- **请求方法**：`POST`
- **请求地址**：`http://localhost:8000/api/users/auth/send-sms/`
- **请求头部**：

| Key | Value |
|-----|-------|
| Content-Type | application/json |

- **请求 Body（JSON）**：

```json
{
  "phone": "18512292336",
  "code_type": "login"
}
```

---

## 📌 接口：短信验证码登录

- **请求方法**：`POST`
- **请求地址**：`http://localhost:8000/api/users/auth/sms-login/`
- **请求头部**：

| Key | Value |
|-----|-------|
| Content-Type | application/json |

- **请求 Body（JSON）**：

```json
{
  "phone": "18512292336",
  "sms_code": "123456"
}
```

---

## 📌 接口：刷新 Token 测试

- **请求方法**：`POST`
- **请求地址**：`http://localhost:8000/api/users/auth/refresh/`
- **请求头部**：

| Key | Value |
|-----|-------|
| Content-Type | application/json |

- **请求 Body（JSON）**：

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MTExNjYxMywiaWF0IjoxNzUwNTExODEzLCJqdGkiOiI4ZDdhNGU4Y2YwZWQ0MThhOTQ2N2JiYjg1YTNiZDEzNiIsInVzZXJfaWQiOiJmMDBiMjg0OS04OGQ5LTQ5ZjQtOGY4My03MzlhMzcwYjA1YzYifQ.CxdsZzJ-EU81L2NkMLoTXN2dze-tftuUigQWqiiNqX0"
}
```

--- 