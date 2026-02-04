#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🔬 اختبار وتشخيص تطبيق اليانصيب الأردني
=============================================================================
سكريبت شامل لاختبار جميع مكونات التطبيق وتشخيص المشاكل

الاستخدام:
    python diagnostic_test.py
    
أو للاختبار السريع:
    python diagnostic_test.py --quick
=============================================================================
"""

import sys
import os
import traceback
import time
from datetime import datetime
import argparse

# الألوان للـ Terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """طباعة عنوان"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

def print_test(name, status="running"):
    """طباعة حالة الاختبار"""
    if status == "running":
        print(f"🔄 {name}...", end=" ")
    elif status == "success":
        print(f"{Colors.GREEN}✅ نجح{Colors.END}")
    elif status == "failed":
        print(f"{Colors.RED}❌ فشل{Colors.END}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠️  تحذير{Colors.END}")

def test_python_version():
    """اختبار إصدار Python"""
    print_test("فحص إصدار Python", "running")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 8:
        print_test("", "success")
        print(f"   📌 الإصدار: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_test("", "failed")
        print(f"   ❌ الإصدار الحالي: {version.major}.{version.minor}.{version.micro}")
        print(f"   💡 مطلوب: Python 3.8 أو أحدث")
        return False

def test_imports():
    """اختبار استيراد المكتبات"""
    print_test("فحص المكتبات المطلوبة", "running")
    
    required_packages = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'plotly': 'plotly',
        'openpyxl': 'openpyxl',
        'reportlab': 'reportlab (اختياري)',
        'psutil': 'psutil (اختياري)'
    }
    
    missing = []
    optional_missing = []
    
    print()
    for package, display_name in required_packages.items():
        try:
            __import__(package)
            print(f"   ✅ {display_name}")
        except ImportError:
            if 'اختياري' in display_name:
                optional_missing.append(package)
                print(f"   {Colors.YELLOW}⚠️  {display_name} - غير مثبت{Colors.END}")
            else:
                missing.append(package)
                print(f"   {Colors.RED}❌ {display_name} - غير مثبت{Colors.END}")
    
    if missing:
        print_test("\nفحص المكتبات", "failed")
        print(f"\n{Colors.RED}💡 لتثبيت المكتبات المفقودة:{Colors.END}")
        print(f"   pip install {' '.join(missing)}")
        return False
    elif optional_missing:
        print_test("\nفحص المكتبات", "warning")
        print(f"\n{Colors.YELLOW}💡 لتثبيت المكتبات الاختيارية:{Colors.END}")
        print(f"   pip install {' '.join(optional_missing)}")
        return True
    else:
        print_test("\nفحص المكتبات", "success")
        return True

def test_data_file():
    """اختبار ملف البيانات"""
    print_test("فحص ملف البيانات (249.xlsx)", "running")
    
    try:
        import pandas as pd
        
        # البحث عن الملف
        possible_paths = [
            '249.xlsx',
            'sample_data.xlsx',
            '../249.xlsx',
            '/mnt/user-data/uploads/249.xlsx'
        ]
        
        data_file = None
        for path in possible_paths:
            if os.path.exists(path):
                data_file = path
                break
        
        if not data_file:
            print_test("", "warning")
            print(f"   ⚠️  لم يتم العثور على ملف البيانات")
            print(f"   💡 سيتم إنشاء بيانات تجريبية")
            return None
        
        # قراءة الملف
        df = pd.read_excel(data_file)
        
        # التحقق من الأعمدة
        required_cols = ['N1', 'N2', 'N3', 'N4', 'N5', 'N6']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print_test("", "failed")
            print(f"   ❌ الأعمدة المفقودة: {', '.join(missing_cols)}")
            return None
        
        # التحقق من البيانات
        for col in required_cols:
            if df[col].min() < 1 or df[col].max() > 32:
                print_test("", "failed")
                print(f"   ❌ الأرقام في العمود {col} خارج النطاق (1-32)")
                return None
        
        print_test("", "success")
        print(f"   📊 عدد السحوبات: {len(df)}")
        print(f"   📅 نطاق التواريخ: {df.columns.tolist()}")
        return df
        
    except Exception as e:
        print_test("", "failed")
        print(f"   ❌ خطأ: {str(e)}")
        return None

def test_memory():
    """اختبار الذاكرة المتاحة"""
    print_test("فحص الذاكرة المتاحة", "running")
    
    try:
        import psutil
        
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024 ** 3)
        total_gb = memory.total / (1024 ** 3)
        percent = memory.percent
        
        if available_gb < 0.5:
            print_test("", "warning")
            print(f"   ⚠️  الذاكرة المتاحة منخفضة: {available_gb:.2f} GB")
        else:
            print_test("", "success")
        
        print(f"   📊 الإجمالي: {total_gb:.2f} GB")
        print(f"   📊 المتاح: {available_gb:.2f} GB")
        print(f"   📊 المستخدم: {percent:.1f}%")
        
        return True
        
    except ImportError:
        print_test("", "warning")
        print(f"   ⚠️  psutil غير مثبت - لا يمكن فحص الذاكرة")
        return None

def test_file_permissions():
    """اختبار صلاحيات الملفات"""
    print_test("فحص صلاحيات الكتابة", "running")
    
    test_file = "test_write_permission.tmp"
    
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        
        print_test("", "success")
        return True
        
    except Exception as e:
        print_test("", "failed")
        print(f"   ❌ لا يمكن الكتابة في المجلد الحالي")
        print(f"   💡 تأكد من صلاحيات الوصول")
        return False

def test_streamlit_config():
    """اختبار إعدادات Streamlit"""
    print_test("فحص إعدادات Streamlit", "running")
    
    config_dir = os.path.expanduser("~/.streamlit")
    config_file = os.path.join(config_dir, "config.toml")
    
    if os.path.exists(config_file):
        print_test("", "success")
        print(f"   📄 ملف الإعدادات موجود: {config_file}")
    else:
        print_test("", "warning")
        print(f"   ⚠️  لم يتم العثور على ملف الإعدادات")
        print(f"   💡 سيتم استخدام الإعدادات الافتراضية")
    
    return True

def test_algorithm_performance():
    """اختبار أداء الخوارزميات"""
    print_test("فحص أداء الخوارزميات", "running")
    
    try:
        import numpy as np
        import random
        
        # اختبار بسيط
        start = time.time()
        
        # محاكاة توليد 100 تذكرة
        tickets = []
        for _ in range(100):
            ticket = sorted(random.sample(range(1, 33), 6))
            tickets.append(ticket)
        
        elapsed = time.time() - start
        
        if elapsed < 1.0:
            print_test("", "success")
            print(f"   ⚡ الوقت: {elapsed*1000:.1f} ms لتوليد 100 تذكرة")
        else:
            print_test("", "warning")
            print(f"   ⚠️  الأداء بطيء: {elapsed:.2f}s لتوليد 100 تذكرة")
        
        return True
        
    except Exception as e:
        print_test("", "failed")
        print(f"   ❌ خطأ: {str(e)}")
        return False

def generate_sample_data():
    """توليد بيانات تجريبية"""
    print_header("📊 توليد بيانات تجريبية")
    
    try:
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        
        print("🔄 جاري توليد 100 سحبة تجريبية...")
        
        data = []
        start_date = datetime(2023, 9, 17)
        
        for i in range(100):
            draw_date = start_date + timedelta(days=i*3)
            numbers = sorted(np.random.choice(range(1, 33), size=6, replace=False))
            
            data.append({
                'رقم السحب': i + 1,
                'تاريخ السحب': draw_date,
                'N1': numbers[0],
                'N2': numbers[1],
                'N3': numbers[2],
                'N4': numbers[3],
                'N5': numbers[4],
                'N6': numbers[5]
            })
        
        df = pd.DataFrame(data)
        
        # حفظ الملف
        output_file = "sample_data_generated.xlsx"
        df.to_excel(output_file, index=False)
        
        print(f"{Colors.GREEN}✅ تم توليد الملف: {output_file}{Colors.END}")
        print(f"   📊 عدد السحوبات: {len(df)}")
        print(f"   📅 من {df['تاريخ السحب'].min()} إلى {df['تاريخ السحب'].max()}")
        
        return df
        
    except Exception as e:
        print(f"{Colors.RED}❌ فشل التوليد: {str(e)}{Colors.END}")
        return None

def run_quick_tests():
    """تشغيل الاختبارات السريعة فقط"""
    print_header("🚀 اختبارات سريعة")
    
    results = []
    
    results.append(('Python Version', test_python_version()))
    results.append(('Libraries', test_imports()))
    results.append(('File Permissions', test_file_permissions()))
    
    return results

def run_full_tests():
    """تشغيل جميع الاختبارات"""
    print_header("🔬 تشخيص شامل لتطبيق اليانصيب الأردني")
    
    print(f"{Colors.BOLD}التاريخ:{Colors.END} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.BOLD}النظام:{Colors.END} {sys.platform}")
    print(f"{Colors.BOLD}Python:{Colors.END} {sys.version.split()[0]}")
    
    results = []
    
    # الاختبارات الأساسية
    print_header("📋 الاختبارات الأساسية")
    results.append(('Python Version', test_python_version()))
    results.append(('Libraries', test_imports()))
    results.append(('File Permissions', test_file_permissions()))
    
    # اختبارات البيانات
    print_header("📊 اختبارات البيانات")
    data_result = test_data_file()
    results.append(('Data File', data_result is not None))
    
    # اختبارات الأداء
    print_header("⚡ اختبارات الأداء")
    results.append(('Memory Check', test_memory()))
    results.append(('Algorithm Performance', test_algorithm_performance()))
    
    # اختبارات الإعدادات
    print_header("⚙️  اختبارات الإعدادات")
    results.append(('Streamlit Config', test_streamlit_config()))
    
    return results, data_result

def print_summary(results):
    """طباعة الملخص"""
    print_header("📊 ملخص النتائج")
    
    total = len(results)
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    warnings = sum(1 for _, result in results if result is None)
    
    print(f"✅ النجاح: {Colors.GREEN}{passed}{Colors.END}/{total}")
    print(f"❌ الفشل: {Colors.RED}{failed}{Colors.END}/{total}")
    print(f"⚠️  التحذيرات: {Colors.YELLOW}{warnings}{Colors.END}/{total}")
    
    if failed > 0:
        print(f"\n{Colors.RED}❌ توجد مشاكل يجب حلها قبل تشغيل التطبيق{Colors.END}")
        print(f"\n{Colors.YELLOW}💡 نصائح:{Colors.END}")
        print("   1. قم بتثبيت المكتبات المفقودة: pip install -r requirements.txt")
        print("   2. تحقق من صلاحيات الملفات")
        print("   3. تأكد من إصدار Python (3.8 أو أحدث)")
        return False
    elif warnings > 0:
        print(f"\n{Colors.YELLOW}⚠️  التطبيق قد يعمل ولكن مع قيود{Colors.END}")
        print(f"\n{Colors.YELLOW}💡 نصائح:{Colors.END}")
        print("   1. قم بتثبيت المكتبات الاختيارية لميزات إضافية")
        print("   2. قم برفع ملف بيانات حقيقي للحصول على نتائج أفضل")
        return True
    else:
        print(f"\n{Colors.GREEN}🎉 كل شيء جاهز! يمكنك تشغيل التطبيق{Colors.END}")
        print(f"\n{Colors.CYAN}▶️  للتشغيل:{Colors.END}")
        print("   streamlit run app_enhanced.py")
        return True

def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(description='تشخيص تطبيق اليانصيب الأردني')
    parser.add_argument('--quick', action='store_true', help='تشغيل اختبارات سريعة فقط')
    parser.add_argument('--generate-data', action='store_true', help='توليد بيانات تجريبية')
    args = parser.parse_args()
    
    try:
        if args.generate_data:
            generate_sample_data()
            return
        
        if args.quick:
            results = run_quick_tests()
        else:
            results, data = run_full_tests()
            
            # توليد بيانات تجريبية إذا لم يكن هناك بيانات
            if data is None:
                print(f"\n{Colors.YELLOW}💡 هل تريد توليد بيانات تجريبية؟ (y/n):{Colors.END} ", end="")
                response = input().strip().lower()
                if response == 'y':
                    generate_sample_data()
        
        # طباعة الملخص
        success = print_summary(results)
        
        # الخروج
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  تم الإلغاء من قبل المستخدم{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ خطأ غير متوقع:{Colors.END}")
        print(f"{Colors.RED}{traceback.format_exc()}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
