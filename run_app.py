#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🚀 سكريبت تشغيل تطبيق اليانصيب الأردني
=============================================================================
سكريبت تشغيل ذكي مع مراقبة الأخطاء والتشخيص التلقائي

الاستخدام:
    python run_app.py              # تشغيل عادي
    python run_app.py --debug      # تشغيل مع التصحيح
    python run_app.py --test       # اختبار أولاً ثم تشغيل
    python run_app.py --port 8502  # تشغيل على منفذ مختلف
=============================================================================
"""

import sys
import os
import subprocess
import argparse
import time
from pathlib import Path

# الألوان
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    """طباعة لافتة البداية"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║            🎰 تطبيق اليانصيب الأردني المتطور                  ║
║                       النسخة 2.0                              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

def check_python_version():
    """التحقق من إصدار Python"""
    print(f"{Colors.BOLD}🔍 فحص إصدار Python...{Colors.END}")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"{Colors.GREEN}✅ Python {version.major}.{version.minor}.{version.micro}{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}❌ Python {version.major}.{version.minor}.{version.micro} (مطلوب 3.8+){Colors.END}")
        return False

def check_dependencies():
    """التحقق من المكتبات المطلوبة"""
    print(f"\n{Colors.BOLD}📦 فحص المكتبات...{Colors.END}")
    
    required = ['streamlit', 'pandas', 'numpy', 'plotly', 'openpyxl']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"  {Colors.GREEN}✅ {package}{Colors.END}")
        except ImportError:
            print(f"  {Colors.RED}❌ {package} - غير مثبت{Colors.END}")
            missing.append(package)
    
    if missing:
        print(f"\n{Colors.YELLOW}⚠️  مكتبات مفقودة!{Colors.END}")
        print(f"\n{Colors.BOLD}لتثبيت المكتبات المفقودة:{Colors.END}")
        print(f"  pip install {' '.join(missing)}")
        
        response = input(f"\n{Colors.YELLOW}هل تريد تثبيتها الآن؟ (y/n): {Colors.END}").strip().lower()
        if response == 'y':
            print(f"\n{Colors.CYAN}🔄 جاري التثبيت...{Colors.END}")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing, check=True)
                print(f"{Colors.GREEN}✅ تم التثبيت بنجاح{Colors.END}")
                return True
            except subprocess.CalledProcessError:
                print(f"{Colors.RED}❌ فشل التثبيت{Colors.END}")
                return False
        return False
    
    return True

def check_app_file():
    """التحقق من وجود ملف التطبيق"""
    print(f"\n{Colors.BOLD}📄 فحص ملفات التطبيق...{Colors.END}")
    
    files_to_check = [
        ('app_enhanced.py', 'ملف التطبيق الرئيسي'),
        ('app_enhanced_debug.py', 'ملف التطبيق (وضع التصحيح)'),
    ]
    
    found_files = []
    for filename, description in files_to_check:
        if os.path.exists(filename):
            print(f"  {Colors.GREEN}✅ {filename} - {description}{Colors.END}")
            found_files.append(filename)
        else:
            print(f"  {Colors.YELLOW}⚠️  {filename} - غير موجود{Colors.END}")
    
    if not found_files:
        print(f"\n{Colors.RED}❌ لم يتم العثور على ملفات التطبيق!{Colors.END}")
        return None
    
    return found_files[0]

def run_tests():
    """تشغيل الاختبارات"""
    print(f"\n{Colors.BOLD}🧪 تشغيل الاختبارات...{Colors.END}")
    
    if os.path.exists('diagnostic_test.py'):
        try:
            result = subprocess.run([sys.executable, 'diagnostic_test.py', '--quick'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{Colors.GREEN}✅ جميع الاختبارات نجحت{Colors.END}")
                return True
            else:
                print(f"{Colors.YELLOW}⚠️  بعض الاختبارات فشلت{Colors.END}")
                print(result.stdout)
                return False
        except Exception as e:
            print(f"{Colors.RED}❌ خطأ في تشغيل الاختبارات: {e}{Colors.END}")
            return False
    else:
        print(f"{Colors.YELLOW}⚠️  ملف الاختبارات غير موجود - تخطي{Colors.END}")
        return True

def check_port(port):
    """التحقق من توفر المنفذ"""
    import socket
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"{Colors.YELLOW}⚠️  المنفذ {port} مشغول{Colors.END}")
            return False
        else:
            print(f"{Colors.GREEN}✅ المنفذ {port} متاح{Colors.END}")
            return True
    except:
        return True

def start_app(app_file, port, debug=False):
    """تشغيل التطبيق"""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}🚀 تشغيل التطبيق...{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    print(f"{Colors.CYAN}📱 سيفتح التطبيق في متصفحك تلقائياً{Colors.END}")
    print(f"{Colors.CYAN}🌐 العنوان: http://localhost:{port}{Colors.END}")
    print(f"\n{Colors.YELLOW}💡 نصائح:{Colors.END}")
    print(f"  • لإيقاف التطبيق: اضغط Ctrl+C")
    print(f"  • لتحديث الصفحة: اضغط R في المتصفح")
    print(f"  • للحصول على مساعدة: راجع README.md")
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    # بناء الأمر
    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        app_file,
        '--server.port', str(port),
        '--server.address', 'localhost',
        '--browser.serverAddress', 'localhost',
    ]
    
    if debug:
        cmd.extend([
            '--logger.level', 'debug',
            '--server.fileWatcherType', 'auto'
        ])
    
    try:
        # تشغيل التطبيق
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  تم إيقاف التطبيق من قبل المستخدم{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ خطأ في تشغيل التطبيق:{Colors.END}")
        print(f"{Colors.RED}{str(e)}{Colors.END}")
        
        print(f"\n{Colors.YELLOW}💡 محاولة التشغيل اليدوي:{Colors.END}")
        print(f"  streamlit run {app_file} --server.port {port}")

def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(
        description='تشغيل تطبيق اليانصيب الأردني',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة:
  python run_app.py                    # تشغيل عادي
  python run_app.py --debug            # تشغيل مع التصحيح
  python run_app.py --test             # اختبار ثم تشغيل
  python run_app.py --port 8502        # منفذ مختلف
  python run_app.py --no-check         # تخطي الفحوصات
        """
    )
    
    parser.add_argument('--debug', action='store_true', 
                       help='تشغيل في وضع التصحيح')
    parser.add_argument('--test', action='store_true',
                       help='تشغيل الاختبارات أولاً')
    parser.add_argument('--port', type=int, default=8501,
                       help='رقم المنفذ (افتراضي: 8501)')
    parser.add_argument('--no-check', action='store_true',
                       help='تخطي فحوصات النظام')
    
    args = parser.parse_args()
    
    try:
        # طباعة اللافتة
        print_banner()
        
        # الفحوصات الأولية
        if not args.no_check:
            print(f"{Colors.BOLD}🔍 فحص النظام...{Colors.END}\n")
            
            if not check_python_version():
                sys.exit(1)
            
            if not check_dependencies():
                print(f"\n{Colors.RED}❌ فشل فحص المكتبات{Colors.END}")
                sys.exit(1)
            
            app_file = check_app_file()
            if not app_file:
                sys.exit(1)
            
            # استخدام النسخة مع التصحيح إذا طُلب ذلك
            if args.debug and os.path.exists('app_enhanced_debug.py'):
                app_file = 'app_enhanced_debug.py'
                print(f"\n{Colors.CYAN}🐛 سيتم استخدام وضع التصحيح{Colors.END}")
            
            # التحقق من المنفذ
            print(f"\n{Colors.BOLD}🔌 فحص المنفذ...{Colors.END}")
            if not check_port(args.port):
                response = input(f"{Colors.YELLOW}هل تريد استخدام منفذ مختلف؟ (y/n): {Colors.END}").strip().lower()
                if response == 'y':
                    args.port = int(input("أدخل رقم المنفذ: ").strip())
                else:
                    print(f"{Colors.RED}تم الإلغاء{Colors.END}")
                    sys.exit(1)
            
            # تشغيل الاختبارات إذا طُلب ذلك
            if args.test:
                if not run_tests():
                    response = input(f"\n{Colors.YELLOW}هل تريد المتابعة رغم فشل بعض الاختبارات؟ (y/n): {Colors.END}").strip().lower()
                    if response != 'y':
                        sys.exit(1)
        else:
            # إذا تم تخطي الفحوصات
            app_file = 'app_enhanced.py'
            if args.debug and os.path.exists('app_enhanced_debug.py'):
                app_file = 'app_enhanced_debug.py'
        
        # تشغيل التطبيق
        time.sleep(0.5)  # توقف قصير لتحسين العرض
        start_app(app_file, args.port, args.debug)
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  تم الإلغاء من قبل المستخدم{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ خطأ غير متوقع:{Colors.END}")
        print(f"{Colors.RED}{str(e)}{Colors.END}")
        
        import traceback
        print(f"\n{Colors.YELLOW}تفاصيل الخطأ:{Colors.END}")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
