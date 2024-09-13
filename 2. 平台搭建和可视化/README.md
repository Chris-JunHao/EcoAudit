# 水质实时监测系统

## 项目简介

本项目是一个水质实时监测系统，用于监测不同省份的水质情况，并实时展示水质监测数据。系统包括登录页面、主页面、省份详细页和河流详细页。

## 技术栈

spring boot + mybatis + vue + echarts

## 功能描述

本项目实现了以下功能：

- 用户登录：用户需要输入用户名和密码才能进入系统。
- 省份选择：用户可以选择不同省份进行水质监测数据的展示。
- 河流选择：用户可以选择不同河流进行水质监测数据的展示。
- 数据更新：用户可以实时查看水质监测数据。

## 前段结构

### 1. 登录页面

登录页面用于用户登录，用户需要输入用户名和密码才能进入系统。登录页面包括以下功能：

- 用户名输入框：用户输入用户名。
- 密码输入框：用户输入密码。
- 登录按钮：用户点击登录按钮，系统验证用户名和密码是否正确，如果正确则进入系统，否则提示用户名或密码错误。

### 2. 主页面

主页面是系统的核心页面,该页面中国地图为背景,可选择不同省份进行水质监测数据的展示。主页面包括以下功能：

- 省份选择:用户可以选择不同省份进行水质监测数据的展示。

#### 省份详细页

省份详细页是主页面的一部分,用于展示所选省份的水质监测数据。省份详细页包括以下功能:

- 河流选择:用户可以选择不同河流进行水质监测数据的展示。
- 数据更新:用户可以实时查看水质监测数据。
- 数据异常监测:通过算法实时监测异常数据,自动报警.

##### 河流详细页

- 数据展示:展示所选省份的水质监测数据,包括PH值、溶解氧、电导率等。

在设计你的水质实时监测系统的项目结构和后端结构时，以下是一个清晰的思路和建议：

## **项目结构**

以下是水质实时监测系统的完整项目文件结构，包含前后端及数据库的相关目录结构，以 Spring Boot 为后端，Vue 为前端，并使用 MyBatis 进行数据库操作：

### 项目文件结构

```
water-quality-monitoring-system
│
├── /backend                    # 后端（Spring Boot 项目）
│   ├── /src
│   │   ├── /main
│   │   │   ├── /java
│   │   │   │   └── /com/example/waterquality
│   │   │   │       ├── /config        # 配置类，如MyBatis配置、Spring Security等
│   │   │   │       ├── /controller    # 控制器，处理API请求
│   │   │   │       ├── /service       # 业务逻辑
│   │   │   │       ├── /repository    # 数据库操作，MyBatis Mapper
│   │   │   │       ├── /model         # 实体类，与数据库表映射
│   │   │   │       ├── /scheduler     # 定时任务，爬虫定期获取数据
│   │   │   │       ├── /exception     # 异常处理相关类
│   │   │   │       └── /utils         # 工具类
│   │   │   └── /resources
│   │   │       ├── /mapper            # MyBatis XML映射文件
│   │   │       ├── application.yml    # Spring Boot 配置文件
│   │   │       └── logback-spring.xml # 日志配置
│   │   └── /test                      # 测试代码
│   ├── pom.xml                        # Maven 配置文件
│
├── /frontend                    # 前端（Vue.js 项目）
│   ├── /public                  # 静态资源文件，HTML 入口文件
│   │   └── index.html           # 项目主HTML文件
│   ├── /src
│   │   ├── /assets              # 静态资源文件（图片、字体等）
│   │   ├── /components          # 通用组件
│   │   │   ├── Login.vue        # 登录组件
│   │   │   ├── Map.vue          # 中国地图展示组件
│   │   │   └── WaterQualityTable.vue  # 用于展示水质数据的表格组件
│   │   ├── /views               # 页面级组件
│   │   │   ├── LoginPage.vue    # 登录页面
│   │   │   ├── MainPage.vue     # 主页面，包含省份选择功能
│   │   │   ├── ProvinceDetailPage.vue # 省份详细页面
│   │   │   └── RiverDetailPage.vue    # 河流详细页面
│   │   ├── /router              # 路由相关
│   │   │   └── index.js         # Vue Router 配置
│   │   ├── /store               # Vuex 状态管理
│   │   │   └── index.js         # Vuex Store
│   │   ├── /api                 # API 请求模块
│   │   │   └── waterQuality.js  # 用于获取水质数据的API请求
│   │   ├── /styles              # 样式文件
│   │   │   └── global.css       # 全局样式
│   │   ├── /utils               # 工具函数
│   │   │   └── auth.js          # 登录认证的工具函数
│   │   └── main.js              # 应用入口文件
│   ├── package.json             # 前端项目依赖配置
│   └── vue.config.js            # Vue CLI 配置文件
│
├── /database                    # 数据库相关文件
│   ├── /migrations              # 数据库迁移文件，SQL 脚本
│   └── schema.sql               # 数据库结构定义文件
│
├── /docs                        # 项目文档
│   ├── README.md                # 项目介绍
│   └── api-docs.md              # API 文档
│
└── /logs                        # 日志文件
    └── app.log                  # 应用日志
```

### 详细说明

1. **backend**：后端的 Spring Boot 项目，负责处理业务逻辑、API请求、数据持久化等功能。
   - `/controller`：用于处理 HTTP 请求的控制器。
   - `/service`：业务逻辑层，包含水质数据的处理、定时任务等。
   - `/repository`：用于数据库访问，负责CRUD操作。
   - `/scheduler`：定时任务，用于爬取数据并存储到数据库。

2. **frontend**：前端的 Vue.js 项目，用于构建用户界面。
   - `/components`：复用的通用组件。
   - `/views`：页面级组件。
   - `/router`：路由配置，定义页面跳转和动态路由。
   - `/store`：Vuex 状态管理，存储应用的全局状态。
   - `/api`：封装的 API 请求模块，用于从后端获取数据。

3. **database**：包含数据库迁移文件和数据库结构的定义，方便数据库初始化和结构管理。

4. **docs**：项目的文档，包括项目介绍和API文档等。

5. **logs**：存放应用运行时产生的日志文件，便于后期排查和调试问题。

此结构可以有效地帮助你管理和扩展项目，前后端分离的设计也有利于后续的部署和维护。