# 手机银行社区活动卡券系统 - 接口自动化测试框架

## 项目简介

本项目是一个企业级接口自动化测试框架，专为手机银行社区活动卡券系统设计。框架基于 Python + pytest + requests 构建，采用分层架构设计，具有高度的可扩展性和可维护性。

## 技术栈

### 核心框架
- **pytest**: 7.4.3 - 测试框架核心
- **requests**: 2.31.0 - HTTP请求库
- **allure-pytest**: 2.13.2 - 测试报告
- **pytest-xdist**: 3.5.0 - 并行执行
- **pytest-rerunfailures**: 13.0 - 失败重试

### 扩展组件
- **PyYAML**: 配置文件管理
- **jsonschema**: JSON Schema验证
- **pymysql**: 数据库操作
- **redis**: 缓存验证
- **Faker**: 测试数据生成
- **cryptography**: 加解密
- **loguru**: 增强日志
- **pydantic**: 数据验证

## 项目结构

```
Automated-framework-building/
├── config/                      # 配置层
│   ├── __init__.py
│   ├── settings.py             # 全局配置
│   ├── env_config.yaml         # 多环境配置
│   └── db_config.yaml          # 数据库配置
├── core/                        # 核心层
│   ├── __init__.py
│   ├── http_client.py          # HTTP请求封装
│   ├── database.py             # 数据库操作封装
│   ├── logger.py               # 日志管理
│   ├── decorator.py            # 装饰器（重试、日志等）
│   └── assertion.py            # 断言增强
├── api/                         # API层
│   ├── __init__.py
│   ├── base_api.py             # 基础API类
│   ├── auth_api.py             # 认证接口
│   ├── coupon_api.py           # 卡券接口
│   ├── activity_api.py         # 活动接口
│   └── user_api.py             # 用户接口
├── testcases/                   # 测试用例层
│   ├── __init__.py
│   ├── conftest.py             # pytest fixtures
│   ├── test_coupon/            # 卡券模块测试
│   ├── test_activity/          # 活动模块测试
│   └── test_integration/       # 集成测试
├── utils/                       # 工具层
│   ├── __init__.py
│   ├── data_generator.py       # 测试数据生成
│   ├── file_handler.py         # 文件操作
│   ├── encryption.py           # 加解密工具
│   └── validators.py           # 数据验证
├── data/                        # 测试数据层
│   ├── test_data.yaml          # 测试数据
│   ├── sql/                    # SQL脚本
│   └── mock/                   # Mock数据
├── reports/                     # 测试报告
│   ├── allure-results/
│   └── html/
├── logs/                        # 日志文件
├── scripts/                     # 脚本工具
│   ├── run_tests.py            # 测试执行脚本
│   └── generate_report.py     # 报告生成脚本
├── pytest.ini                   # pytest配置
├── requirements.txt             # 依赖管理
├── Dockerfile                   # Docker配置
├── Jenkinsfile                  # Jenkins Pipeline
├── .gitlab-ci.yml              # GitLab CI配置
└── README.md
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd Automated-framework-building

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置测试环境
# 或者修改 config/env_config.yaml 和 config/db_config.yaml
```

### 3. 运行测试

#### 运行所有测试
```bash
pytest testcases -v
```

#### 运行冒烟测试
```bash
pytest testcases -m smoke -v
```

#### 运行特定模块
```bash
pytest testcases/test_coupon -v
```

#### 并行执行
```bash
pytest testcases -n auto -v
```

#### 使用执行脚本
```bash
# 基本用法
python scripts/run_tests.py

# 指定环境
python scripts/run_tests.py --env test

# 运行冒烟测试
python scripts/run_tests.py -m smoke

# 并行执行
python scripts/run_tests.py -n 4

# 生成Allure报告
python scripts/run_tests.py --allure-report
```

### 4. 查看报告

#### Allure报告
```bash
# 方式1：通过脚本生成并打开
python scripts/generate_report.py

# 方式2：手动生成
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## 核心功能

### 1. HTTP客户端封装
- 统一请求处理（GET/POST/PUT/DELETE/PATCH）
- 自动token管理和刷新
- 请求/响应日志记录
- 异常重试机制
- 响应时间监控

### 2. 多环境配置管理
- 支持 dev/test/staging/prod 多环境
- 配置文件隔离
- 环境变量切换

### 3. 增强断言
- 响应码断言
- JSON Schema校验
- 响应时间断言
- 字段存在性断言
- 字段值断言
- 列表长度断言

### 4. 数据驱动测试
- YAML配置文件管理测试数据
- pytest.mark.parametrize参数化
- Faker自动生成测试数据

### 5. 数据库操作
- 数据准备和清理
- 数据验证
- 事务支持

### 6. 日志管理
- 多级别日志（DEBUG/INFO/WARNING/ERROR）
- 日志文件按日期轮转
- 错误日志单独记录
- Allure报告集成

## 测试用例编写示例

```python
import pytest
import allure
from core.assertion import EnhancedAssertion


@allure.feature("卡券模块")
@allure.story("领取卡券")
class TestReceiveCoupon:
    
    @allure.title("正常领取卡券")
    @pytest.mark.smoke
    @pytest.mark.coupon
    def test_receive_coupon_success(self, coupon_api, test_coupon):
        user_id = 12345
        
        with allure.step("领取卡券"):
            response = coupon_api.receive_coupon(test_coupon['id'], user_id)
        
        with allure.step("验证响应"):
            EnhancedAssertion.assert_response_code(response, 200)
            EnhancedAssertion.assert_contains_fields(response, ["coupon_code", "user_id"])
```

## Pytest标记说明

- `@pytest.mark.smoke`: 冒烟测试
- `@pytest.mark.regression`: 回归测试
- `@pytest.mark.normal`: 普通优先级
- `@pytest.mark.high`: 高优先级
- `@pytest.mark.coupon`: 卡券模块
- `@pytest.mark.activity`: 活动模块
- `@pytest.mark.integration`: 集成测试

## CI/CD集成

### Jenkins
```groovy
// 使用项目中的 Jenkinsfile
pipeline {
    agent any
    stages {
        stage('测试') {
            steps {
                sh 'python scripts/run_tests.py --env test -m smoke'
            }
        }
    }
}
```

### GitLab CI
```yaml
# 使用项目中的 .gitlab-ci.yml
smoke_test:
  script:
    - pytest testcases -m smoke -v
```

### Docker
```bash
# 构建镜像
docker build -t api-test-framework .

# 运行容器
docker run --rm -v $(pwd)/reports:/app/reports api-test-framework
```

## 最佳实践

1. **接口对象化封装**: 每个模块的接口封装在独立的API类中
2. **数据驱动**: 使用YAML文件管理测试数据，便于维护
3. **分层设计**: 清晰的职责划分，易于扩展
4. **数据隔离**: 每个测试用例独立数据，自动清理
5. **详细日志**: 完整的请求链路日志，便于问题排查
6. **并行执行**: 支持多进程并行，提高执行效率

## 常见问题

### 1. 如何切换测试环境？
```bash
# 方式1：环境变量
export TEST_ENV=test
pytest testcases

# 方式2：使用脚本参数
python scripts/run_tests.py --env test
```

### 2. 如何添加新的接口？
1. 在 `api/` 目录下创建或编辑对应的API类
2. 继承 `BaseAPI` 类
3. 使用 `@allure.step` 装饰器标记步骤
4. 在 `testcases/` 目录创建测试用例

### 3. 如何查看详细日志？
```bash
# 日志文件位置
logs/test_YYYYMMDD.log      # 全量日志
logs/error_YYYYMMDD.log     # 错误日志
```

### 4. 数据库连接失败？
检查 `config/db_config.yaml` 中的数据库配置是否正确，确保网络可达。

## 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证

## 联系方式

项目维护者：测试团队
邮箱：test-team@example.com

---

**Happy Testing! 🚀**
