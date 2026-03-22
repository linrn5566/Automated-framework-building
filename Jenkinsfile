pipeline {
    agent any
    
    parameters {
        choice(name: 'TEST_ENV', choices: ['test', 'staging', 'prod'], description: '测试环境')
        choice(name: 'TEST_SCOPE', choices: ['api', 'mobile', 'all'], description: '执行范围')
        choice(name: 'TEST_SUITE', choices: ['smoke', 'regression', 'all'], description: '测试套件')
        booleanParam(name: 'PARALLEL', defaultValue: true, description: '是否并行执行')
        choice(name: 'MOBILE_PLATFORM', choices: ['android', 'ios'], description: '移动端平台')
        string(name: 'APPIUM_SERVER', defaultValue: 'http://127.0.0.1:4723', description: 'Appium Server 地址')
        string(name: 'MOBILE_APP_PATH', defaultValue: '', description: 'App 安装包路径')
        string(name: 'MOBILE_DEVICE_NAME', defaultValue: '', description: '设备名称')
        string(name: 'MOBILE_UDID', defaultValue: '', description: '设备 UDID')
        booleanParam(name: 'MOBILE_NO_RESET', defaultValue: false, description: '移动端是否保留应用数据')
    }
    
    environment {
        PYTHON_VERSION = '3.10'
        ALLURE_VERSION = '2.24.0'
    }
    
    stages {
        stage('环境准备') {
            steps {
                echo '准备测试环境...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
                '''
            }
        }
        
        stage('执行接口测试') {
            when {
                expression { params.TEST_SCOPE in ['api', 'all'] }
            }
            steps {
                echo "执行 ${params.TEST_SUITE} 测试套件..."
                script {
                    def marks = params.TEST_SUITE == 'all' ? '' : "-m ${params.TEST_SUITE}"
                    def parallel = params.PARALLEL ? '-n auto' : ''
                    
                    sh """
                        . venv/bin/activate
                        export TEST_ENV=${params.TEST_ENV}
                        pytest testcases ${marks} ${parallel} \
                            --alluredir=reports/allure-results \
                            --clean-alluredir \
                            -v
                    """
                }
            }
        }

        stage('执行移动端测试') {
            when {
                expression { params.TEST_SCOPE in ['mobile', 'all'] }
            }
            steps {
                echo "执行 ${params.MOBILE_PLATFORM} 平台移动端 ${params.TEST_SUITE} 测试套件..."
                script {
                    def mobileMarks = params.TEST_SUITE == 'smoke' ? 'mobile and ui_smoke' : (params.TEST_SUITE == 'regression' ? 'mobile and ui_regression' : 'mobile')
                    def noReset = params.MOBILE_NO_RESET ? '--no-reset' : ''

                    sh """
                        . venv/bin/activate
                        export TEST_ENV=${params.TEST_ENV}
                        python scripts/run_mobile_tests.py \
                            --env ${params.TEST_ENV} \
                            --platform ${params.MOBILE_PLATFORM} \
                            --appium-server ${params.APPIUM_SERVER} \
                            --app-path '${params.MOBILE_APP_PATH}' \
                            --device-name '${params.MOBILE_DEVICE_NAME}' \
                            --udid '${params.MOBILE_UDID}' \
                            ${noReset} \
                            -m "${mobileMarks}"
                    """
                }
            }
        }
        
        stage('生成报告') {
            steps {
                echo '生成Allure报告...'
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'reports/allure-results']]
                ])
            }
        }
        
        stage('结果通知') {
            steps {
                echo '发送测试结果通知...'
                script {
                    def testResult = currentBuild.result ?: 'SUCCESS'
                    if (testResult == 'FAILURE') {
                        echo '测试失败，发送告警通知'
                    } else {
                        echo '测试通过'
                    }
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*,logs/**/*', allowEmptyArchive: true
            echo '清理工作空间...'
            cleanWs()
        }
        success {
            echo '测试执行成功！'
        }
        failure {
            echo '测试执行失败！'
        }
    }
}
