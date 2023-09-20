# TRIPO

本项目是一个支持用户以帖子的形式线上分享他们所到地区见闻和感受的社交平台。

## 效果图

<img src="./assets/Tripo/Login.png" alt="Login" style="zoom:33%;" /><img src="./assets/Tripo/Signup.png" alt="Signup" style="zoom:33%;" /><img src="./assets/Tripo/Community.png" alt="Community" style="zoom:33%;" /><img src="./assets/Tripo/New.png" alt="New" style="zoom:33%;" /><img src="./assets/Tripo/MultiPost.png" alt="MultiPost" style="zoom:33%;" /><img src="./assets/Tripo/Map.png" alt="Map" style="zoom:33%;" /><img src="./assets/Tripo/AI.png" alt="AI" style="zoom:33%;" /><img src="./assets/Tripo/Community-1.png" alt="Community-1" style="zoom:33%;" />



## 特色

- 支持AI以图生文，通过用户上传的风景图片自动生成描述文字，还可以根据用户的意愿进行细粒度微调。
- waited for adding ...

## 安装与使用

提供关于如何安装和使用你的应用的详细说明。

### 安装

描述如何在本地环境中安装你的应用。

```bash
pip install your-package
```

### 使用

提供一些基本的使用示例。

```bash
python manage.py runserver
```

## 技术栈

列出你在项目中使用的技术和框架。

- Django (Python)
- Mysql (ORM)
- Nginx
- Torch
- POSTMAN

## API文档


### Verification(验证码发送)

* **Description**

  * This API is used generate verification code and send to the user's email.
  * The verification code applies to both register-time email verification and password reset.
  * Note that a generated code is validated within 5 minutes, and can be used only once.
  * Each email can request the verification code once a minute, if a new code is request, the older code will expire immediately even if it is generated with 5 minutes.

* **Request**
  * HTTP GET - Stateless, token is not required

* **Respond**
  * HTTP 403 - Request restricted, this is because you request the code too frequently (at most once a minute).
  * HTTP 200 - Success, the code has been sent to the designated email

* **Query Params**
  * email：zhangyi_hu@foxmail.com



### Register(注册)

* **Description**

  * This API is used to register a new account by a new email.

* **Request**
  * HTTP POST - Stateless, token is not required

* **Respond**

  * HTTP 200 - the emai has been registered successfully.
  * HTTP 301 - the email had been registered.

- **Body** **example**

  {
      "email": "zhangyi_hu@foxmail.com",
      "code": "4424",
      "username": "hzy",
      "password": "hzy123"
  }



### Reset(密码重置)

* **Description**

  * This API is used to reset the certain account's password.
  * PS: You need the verification code sent from our backend in 5 mins.

* **Request**

  * HTTP POST - Stateless, token is not required.

* **Respond**

  * HTTP 200 - Successfully reset the password.
  * HTTP 404 - Fail to change a non-existent account's password.

* **Body** **example**
  * {
        "email": "naifu.liang@foxmail.com",
        "code": "5096",
        "password": "12345"
    }



### Login(登录)

* **Description**

  * using username(regard it as emai) and password to login

* **Bodyform-data**
  * username：zhangyi_hu@foxmail.com
  * password：hzy123



### Refresh(刷新验证码)

* **Description**

  * Use fresh token to update the token when access token is expired

* **Bodyform-data**

  * refresh:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NjIyMzMyMiwiaWF0IjoxNjk0OTI3MzIyLCJqdGkiOiI5YzI0ODNlYWFiNmY0NzIzODllMDU1MTY3NGIzN2ZmZCIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoibmFpZnUyOTcifQ.YhChhg6C801G10-vHDHjK8n03xeDAMBAVaHpvGwS-mE

    


### get user info(获取用户信息)

* **Description**
   * This API is used to get a user's information.

* **Request**
  * HTTP GET - Stateful, token is required

* **Respond**

  * JsonResponse - Sucessfully get the user's information in the database.
  * HTTP 404 - Fail to get the user's information according to the given uid.

- **AuthorizationBearer Token**

  * Token： eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NjIyMzMyMiwiaWF0IjoxNjk0OTI3MzIyLCJqdGkiOiI5YzI0ODNlYWFiNmY0NzIzODllMDU1MTY3NGIzN2ZmZCIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoibmFpZnUyOTcifQ.YhChhg6C801G10-vHDHjK8n03xeDAMBAVaHpvGwS-mE

* **Query Params**

  * uid：1



### set  user info(设置用户信息)

* **Description**

  * This API is used to set a existing post.

* **Request**

  * HTTP POST - Stateful, token is required Respond.
  * HTTP 200 - Success, the post has been updated.
  * HTTP 404 - the post doesn't exist in the database.

* **AuthorizationBearer Token**

  * Token：

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NjIyMzMyMiwiaWF0IjoxNjk0OTI3MzIyLCJqdGkiOiI5YzI0ODNlYWFiNmY0NzIzODllMDU1MTY3NGIzN2ZmZCIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoibmFpZnUyOTcifQ.YhChhg6C801G10-vHDHjK8n03xeDAMBAVaHpvGwS-mE

* **Bodyform-data**

  * post_id: 1
  * user: zhangi_hu@foxmail.com
  * title: ssfd
  * content: 6666666666666666666666666666
  * time: 20:10:01
  * local: Vanculvar



### push post info

* **Description**
  * This API is used to upload a new post

* **Request**
  * HTTP POST - Stateful, token is required

* **Respond**
  - HTTP 200 - Success, the post has been stored in the database.

* **AuthorizationBearer Token**

  * Token：

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NjIyMzMyMiwiaWF0IjoxNjk0OTI3MzIyLCJqdGkiOiI5YzI0ODNlYWFiNmY0NzIzODllMDU1MTY3NGIzN2ZmZCIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoibmFpZnUyOTcifQ.YhChhg6C801G10-vHDHjK8n03xeDAMBAVaHpvGwS-mE

* **Bodyform-data**
  * uid: 1
  * title: title
  * content: content
  * location: China
  * time: 20:10:10



### Get post info

* **Description**
  * This API is used to delete existing posts based on the post_id.

* **Request**
  * HTTP GET - Stateless, token is not required

* **Respond**
  - HTTP 404 - Request not found, you have failed to find the post you want because it doesn't exist in the database.
  - JsonResponse - Success, the post has been found, return the post data.

* **Query Params**
  * post_id: 1



### delete post info

* **Description**
  * This API is used to delete existing posts based on the post_id.

* **Request**
  * HTTP DELETE - Stateful, token is required

* **Respond**

  - HTTP 404 - Request not found, this is because you cannot delete a non-existent POST.

  - HTTP 200 - Success, the post has been delete from the database.

* AuthorizationBearer Token
  * Token: <token>

* Bodyform-data
  * post_id: 1



### AI_CHAT

* Description
  * This API is used to call the Baidu LLM interface to get introductory text based on a user-submitted object to be described (a location, landscape, or architectural term).

* **Request**
  * HTTP GET - Stateful, token is required

* **Respond**

  - HTTP 500 - Request not found.

  - JsonResoponse - return the output from LLM sucessfully.

* **AuthorizationBearer** **Token**
  * Token: <token>

* **Query** **Params**
  * chat_info: 斯坦福大学





### push img

* **Description**
  * This API is used to push a new img to the database.

Noticing that your img must be bound to a existing post.

* **Request**
  * HTTP POST - Stateful, token is required

* **Respond**

  * HTTP 404 - Request not found, this is because you don't bind the img to a existing post.

  - HTTP 200 - Success, the code has been sent to the designated email

* **AuthorizationBearer** **Token**
  * Token: <token>

* Bodyform-data

  * post_id: 1
  * file_name: ACGN

  * time: 20:10:2
  * image: path of picture



### delete img

* Description

  * This API is used to delete a existing img from the database by it's id.

  * Notice that you cannot delete a img that doesn't exist in the database.

* **Request**
  * HTTP DELETE - Stateful, token is required

* **Respond**

  - HTTP 404 - Request not found, this is because you request deleting a img doesn't exist in the database.

  - HTTP 200 - Success, the code has been sent to the designated email

* **AuthorizationBearer** **Token**
  * Token: <token>

* Bodyform-data

* img_id: 1

## 贡献

说明如何贡献到你的项目。例如：

1. 克隆项目 (`git clone https://github.com/yourusername/your-project.git`)
2. 创建一个新的分支 (`git checkout -b feature/awesome-feature`)
3. 提交你的更改 (`git commit -m 'Add some feature'`)
4. 推送到分支 (`git push origin feature/awesome-feature`)
5. 提交一个合并请求

## 版权

说明你的项目的许可证信息。

## 致谢

ho n to ni a ri ga do ko sa i ma su !!!

## 联系我们

:)

