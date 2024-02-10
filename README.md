
# DIGGIN : Youtube 기반 음악 SNS 플랫폼
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-01](https://github.com/skay138/FUNSUNback/assets/102957619/6790ffe9-28bf-4499-a3db-4c4b035d3f53)
DIGGIN은 음악을 찾아듣고, 소개하고 싶은 유저들을 위한 SNS 앱 플랫폼입니다.
Youtube 동영상 링크를 통해 좋아하는 음악을 다른 사람들과 공유하는 것은 물론 이전에 듣지 못했던 새로운 음악을 발견할 수 있는 기회도 제공합니다.

## 요약
해당 프로젝트는 DIGGIN의([https://github.com/FUNFUNSUN/funsunfront](https://github.com/skay138/digginfront)) 의 BACKEND 서버입니다.

- 기술 스택 : Python(Django), MySQL, Nginx, Dart(Flutter)
- 진행 기간 : 2022.12 ~ 2023.02 (약 2개월)
- 개발 인원 : FE 1명, BE 1명

### 기술 설명
- request와 response를 이용한 데이터 송수신
- django admin을 활용하여 관리 페이지 구현
- swagger를 활용하여 API 문서화
- 이미지 등 media data 핸들링

### Backend서버를 구축하며 다음과 같은 사항을 고려했습니다.
#### 1. 불필요한 API 호출 최소화
프로젝트를 진행하며 Youtube API 호출 상한을 초과하는 문제가 발생했습니다. 기존에는 DB 용량을 경량화하기 위해 Youtube링크 코드만 DB에 저장했었습니다. 이에 게시글 데이터가 필요할 때마다 API를 호출했고 원인이 되었습니다.   
문제를 해결하기 위해 최초 게시글 작성 시 Youtube링크가 유효한지에 따라 데이터를 DB에 저장해두어 해결했습니다.
#### 2. Restful-API를 고려한 코드 작성
CRUD에 기반해 API를 작성하며, DB의 테이블 별로 기능을 나눠 관리했습니다.  
하나의 class가 CRUD에 대한 함수 컴포넌트들을 가지는 구조입니다.
#### 3. 관리 페이지
관리자 페이지의 필요성을 느껴 Django admin을 활용하여 유저와 게시글을 효율적으로 관리할 수 있는 관리자 페이지를 구축했습니다.  
CRUD 작업과 데이터 필터링 기능을 기본적으로 구현하여 사용자 데이터를 보다 쉽게 관리할 수 있도록 했습니다.
#### 4. 문서화
Front와 원활한 소통을 위해 API의 문서화가 중요하다는 점을 인지할 수 있었습니다. 가능하면 글로 작성하기보다 실제로 호출해 볼 수 있게끔 문서화하고 싶었고, 여러 방법을 모색하다 swagger라는 문서화 툴을 찾을 수 있었습니다.
#### 5. 이미지 데이터 관리
이미지에 대해 DB는 경로만 저장했기 때문에 프로필이나 게시글 이미지 수정 시 잉여 데이터가 발생하는 문제를 인지했습니다. 해당 문제를 해결하기 위해 각 리소스 마다 uid를 부여하여 이를 기준으로 이미지를 저장했습니다. 그 결과 중복으로 인한 리소스 낭비를 줄일 수 있었습니다.

## 🎞️ 시연 영상

  ### [https://youtu.be/qoM4JSq8Y54](https://youtu.be/qoM4JSq8Y54)

## 📖 상세 내용


![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-02](https://github.com/skay138/FUNSUNback/assets/102957619/10ee8e9a-87f2-4974-8f03-bab6f074b9c6)
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-03](https://github.com/skay138/FUNSUNback/assets/102957619/65b7ed6f-f6b9-4370-8326-9319f5ffb048)
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-04](https://github.com/skay138/FUNSUNback/assets/102957619/fb71591d-1d25-496d-82fc-136b7a3f8144)
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-05](https://github.com/skay138/FUNSUNback/assets/102957619/216e8cc6-fbab-410f-8079-c10f5f2b25cb)
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-06](https://github.com/skay138/FUNSUNback/assets/102957619/5c2e803e-f31b-4fd7-9116-205836d30612)
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-07](https://github.com/skay138/FUNSUNback/assets/102957619/855204f8-2291-4dd5-9843-c46707bbf217)
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-08](https://github.com/skay138/FUNSUNback/assets/102957619/87e1c96b-2690-443c-a9fc-2af9df403865)
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-09](https://github.com/skay138/FUNSUNback/assets/102957619/712d2696-15d4-4635-a245-f657771426e9)
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-10](https://github.com/skay138/FUNSUNback/assets/102957619/511a2be1-7c71-4e04-a360-fe98d30652f8)
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-11](https://github.com/skay138/FUNSUNback/assets/102957619/7ed0da11-bec0-4b27-9424-f89b97e1709f)
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-12](https://github.com/skay138/FUNSUNback/assets/102957619/de6122cf-1d0e-4ff1-ac02-8353522b72bb)
![DIGGIN_%EC%B5%9C%EC%A2%85%EB%B0%9C%ED%91%9C(%EA%B0%9C%EC%9D%B8%EC%9A%A9)-13](https://github.com/skay138/FUNSUNback/assets/102957619/015093e6-986e-4933-82c4-3e1e4aac4818)

