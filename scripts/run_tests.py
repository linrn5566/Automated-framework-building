#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


def run_tests(args):
    import pytest
    
    pytest_args = [
        '-v',
        '--tb=short',
        f'--alluredir={BASE_DIR}/reports/allure-results',
        '--clean-alluredir'
    ]
    
    if args.marks:
        pytest_args.append(f'-m {args.marks}')
    
    if args.keyword:
        pytest_args.append(f'-k {args.keyword}')
    
    if args.parallel:
        pytest_args.append(f'-n {args.parallel}')
    
    if args.rerun:
        pytest_args.append(f'--reruns {args.rerun}')
    
    if args.html:
        pytest_args.append(f'--html={BASE_DIR}/reports/html/report.html')
        pytest_args.append('--self-contained-html')
    
    if args.path:
        pytest_args.append(args.path)
    else:
        pytest_args.append(str(BASE_DIR / 'testcases'))
    
    print(f"执行命令: pytest {' '.join(pytest_args)}")
    print("=" * 80)
    
    exit_code = pytest.main(pytest_args)
    
    if args.allure_report:
        generate_allure_report()
    
    return exit_code


def generate_allure_report():
    print("\n" + "=" * 80)
    print("生成Allure报告...")
    
    allure_results = BASE_DIR / 'reports' / 'allure-results'
    allure_report = BASE_DIR / 'reports' / 'allure-report'
    
    if not allure_results.exists():
        print("Allure结果目录不存在，跳过报告生成")
        return
    
    os.system(f'allure generate {allure_results} -o {allure_report} --clean')
    print(f"Allure报告已生成: {allure_report}")
    print(f"查看报告: allure open {allure_report}")


def main():
    parser = argparse.ArgumentParser(description='自动化测试执行脚本')
    
    parser.add_argument('-m', '--marks', help='指定标签，如: smoke, regression')
    parser.add_argument('-k', '--keyword', help='指定关键字过滤用例')
    parser.add_argument('-p', '--path', help='指定测试路径')
    parser.add_argument('-n', '--parallel', type=int, help='并行执行，指定进程数')
    parser.add_argument('--rerun', type=int, default=0, help='失败重试次数')
    parser.add_argument('--html', action='store_true', help='生成HTML报告')
    parser.add_argument('--allure-report', action='store_true', help='生成Allure报告')
    parser.add_argument('--env', default='test', help='指定测试环境: dev/test/staging/prod')
    
    args = parser.parse_args()
    
    os.environ['TEST_ENV'] = args.env
    print(f"测试环境: {args.env}")
    print("=" * 80)
    
    exit_code = run_tests(args)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
