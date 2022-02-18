## Student

| View-name                   | Method | URL                                            | Permission  | 비고                     |
| --------------------------- | ------ | ---------------------------------------------- | ----------- | ------------------------ |
| student-list                | GET    | /students                                      | IsAdminUser | (create, destroy는 자동) |
| student-detail              | GET    | /students/&lt;int:pk>                          | IsOwner     |                          |
| student-purchase            | GET    | /students/&lt;int:pk>/purchases                | IsOwner     |                          |
| student-rents               | GET    | /students/&lt;int:pk>/rents/?year=2020&month=4 | IsOwner     |                          |
| 학생의 현재 이용권 저장가능 | GET    | /students/&lt;int:pk>/ticket-storable          | IsOwner     |                          |
| *student-update*            | *PUT*  | */students/&lt;int:pk>*                        |             |                          |



## Ticket

| View-name      | Method | URL                  | Permission  | 비고                  |
| -------------- | ------ | -------------------- | ----------- | --------------------- |
| ticket-list    | GET    | /tickets             | AllowAny    |                       |
| ticket-detail  | GET    | /tickets/&lt;int:pk> | AllowAny    |                       |
| ticket-create  | POST   | /tickets             | IsAdminUser |                       |
| ticket-update  | PUT    | /tickets/&lt;int:pk> | IsAdminUser | (구매 없는 것만 허용) |
| ticket-destroy | DELETE | /tickets/&lt;int:pk> | IsAdminUser | (구매 없는 것만 허용) |



## Seat

| View-name           | Method | URL                | Permission  | 비고                                              |
| ------------------- | ------ | ------------------ | ----------- | ------------------------------------------------- |
| seat-list           | GET    | /seats             | AllowAny    | (seat 필드 추가 시 seat-detail, seat-update 추가) |
| 대여 가능 자리 목록 | GET    | /seats/?           | AllowAny    | (미완)                                            |
| seat-create         | POST   | /seats             | IsAdminUser |                                                   |
| seat-update         | DELETE | /seats/&lt;int:pk> | IsAdminUser | (대여 없는 것만 허용)                             |



## Purchase

| View-name           | Method | URL                         | Permission      | 비고 |
| ------------------- | ------ | --------------------------- | --------------- | ---- |
| purchase-list       | GET    | /purchases                  | IsAdminUser     |      |
| 월 매출             | GET    | /purchases/price/?year=2020 | IsAdminUser     |      |
| purchase-create     | POST   | /purchases                  | IsAuthenticated |      |

구매/대여 내역 화면과 구매/대여 실행 화면을 구분하기 위해서 purchase-list를 읽는 URL을 다르게 설정했다.

예를 들어, 한 학생의 구매 내역은 학생 개인의 정보이므로 `students/<int:pk>/purchases`에서 확인한다.
이용권 구매는 학생 개인정보와 분리된 별도의 URL `purchases`에서 진행한다.



## Rent

| View-name           | Method | URL                         | Permission      | 비고 |
| ------------------- | ------ | --------------------------- | --------------- | ---- |
| rent-list           | GET    | /rents                      | IsAdminUser     |      |
| rent-create (start) | POST   | /rents                      | IsAuthenticated |      |
| rent-update (end)   | PUT    | /rents                      | IsAuthenticated |      |



## User

| View-name                    | Method   | URL                         | Permission             | 비고                     |
| ---------------------------- | -------- | --------------------------- | ---------------------- | ------------------------ |
| user-list                    | GET      | /users                      | AllowAny               |                          |
| user-detail                  | GET      | /users/&lt;int:pk>          | IsOwner \| IsAdminUser |                          |
| user-create (signup)         | POST     | /users                      | AllowAny               |                          |
| user-update (email, student) | PUT      | /users/&lt;int:pk>          | IsOwner                |                          |
| user password change         | PUT      | /users/&lt;int:pk>/password | IsOwner                |                          |
| *user-destroy*               | *DELETE* | */users/&lt;int:pk>*        | *IsOwner*              | *(구매 없는 것만 허용?)* |

