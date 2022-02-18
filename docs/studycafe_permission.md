## Student

| Student views    | Admin Users | Owner User | Anonymous Users |
| ---------------- | ----------- | ---------- | --------------- |
| student-list     | GET         |            |                 |
| student-detail   | GET         | GET        |                 |
| student-purchase | GET         | GET        |                 |
| student-rent     | GET         | GET        |                 |



## Ticket

| Ticket views  | Admin Users      | Authenticated Users | Anonymous Users |
| ------------- | ---------------- | ------------------- | --------------- |
| ticket-list   | GET, POST        | GET                 | GET             |
| ticket-detail | GET, PUT, DELETE | GET                 | GET             |



## Seat

| Seat views  | Admin Users      | Authenticated Users | Anonymous Users |
| ----------- | ---------------- | ------------------- | --------------- |
| seat-list   | GET, POST        | GET                 | GET             |
| seat-detail | GET, PUT, DELETE | GET                 | GET             |



## Purchase

| Purchase views | Admin Users | Owner Users | Anonymous Users |
| -------------- | ----------- | ----------- | --------------- |
| purchase-list  | GET         | POST        |                 |

* 구매/대여 내역 화면과 구매/대여 실행 화면을 구분하기 위해서 purchase-list를 읽는 URL을 다르게 설정했다.

  예를 들어, 한 학생의 구매 내역은 학생 개인의 정보이므로 `GET /students/<int:pk>/purchases`를 요청하여 확인한다.
  이용권 구매는 학생 개인정보와 분리된 별도의 URI `POST /purchases`를 통해 진행한다

* **Admin은 스터디카페의 수익을 확인하고 이용권의 가격을 설정하는 스터디카페의 사업주**를 의미한다. 이러한 관리자는 직접 스터디카페 이용권을 구입하고 자리를 대여하지 않으므로 purchase-list의 POST 요청 권한이 빠져있다.



## Rent

| Rent views  | Admin Users | Owner Users | Anonymous Users |
| ----------- | ----------- | ----------- | --------------- |
| rent-list   | GET         | POST        |                 |
| rent-detail | GET         | GET, PUT    |                 |

* 앞서 언급한대로 Admin은 자리를 대여하지 않으므로 rent-list의 POST 요청 권한이 빠져있다.

* Authenticated Users의 PUT 요청은 예정마감일시 이전에 학생 스스로 대여를 마감할 때 이루어진다.
