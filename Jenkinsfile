pipeline {
    agent any
    
    parameters {
        choice(name: 'TEST_ENV', choices: ['test', 'staging', 'prod'], description: '测试环境')
        choice(name: 'TEST_SUITE', choices: ['smoke', 'regression', 'all'], description: '测试套件')
        booleanParam(name: 'PARALLEL', defaultValue: true, description: '是否并行执行')
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
        
        stage('执行测试') {
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
