#!/usr/bin/env python3
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def generate_allure_report():
    allure_results = BASE_DIR / 'reports' / 'allure-results'
    allure_report = BASE_DIR / 'reports' / 'allure-report'
    
    if not allure_results.exists():
        print("错误: Allure结果目录不存在")
        print(f"请先运行测试生成结果: {allure_results}")
        sys.exit(1)
    
    print("正在生成Allure报告...")
    os.system(f'allure generate {allure_results} -o {allure_report} --clean')
    print(f"Allure报告已生成: {allure_report}")
    
    print("\n打开报告...")
    os.system(f'allure open {allure_report}')


def main():
    generate_allure_report()


if __name__ == '__main__':
    main()
