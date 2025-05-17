#!/usr/bin/env python

import os
import subprocess
import sys

def main():
    print("Запуск анимации модели Вольтерра-Лотки с помощью Manim...")
    
    # Check if manim is installed
    try:
        import manimlib
    except ImportError:
        print("Manim не установлен. Устанавливаем...")
        install_manim()
    
    # Run the animation script
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "volterra_lotka_animation.py")
    
    # The command to render in high quality and save the output
    cmd = [
        "manimgl", 
        script_path, 
        "VolterraLotkaAnimation",
        "-o",          # This flag saves the animation
        # "--high_quality"  # High quality rendering
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\nАнимация успешно создана!")
        print("Файл анимации сохранен в директории 'videos_output'.")
    except subprocess.CalledProcessError as e:
        print(f"\nОшибка при запуске Manim: {e}")
        print("Убедитесь, что Manim правильно установлен и настроен.")
    except FileNotFoundError:
        print("\nОшибка: команда 'manimgl' не найдена.")
        print("Убедитесь, что Manim установлен и добавлен в PATH.")

def install_manim():
    """Install manimlib and its dependencies"""
    print("\nУстановка Manim и зависимостей...")
    
    # Update package index and install dependencies
    dependencies = [
        "python3-pip",
        "python3-numpy",
        "python3-scipy", 
        "python3-matplotlib",
        "python3-sympy",
        "python3-cairo",
        "ffmpeg",
        "libcairo2-dev",
        "libjpeg-dev",
        "libgif-dev",
        "sox",
        "libpango1.0-dev",
        "texlive",
        "texlive-latex-extra",
        "texlive-fonts-extra",
        "texlive-latex-recommended",
        "texlive-science",
        "tipa"
    ]
    
    try:
        if sys.platform.startswith('linux'):
            # Ubuntu/Debian-based systems
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y"] + dependencies, check=True)
        elif sys.platform == 'darwin':
            # macOS
            subprocess.run(["brew", "update"], check=True)
            brew_deps = ["cairo", "sox", "ffmpeg", "py3cairo", "pango", "scipy", "numpy"]
            subprocess.run(["brew", "install"] + brew_deps, check=True)
        elif sys.platform == 'win32':
            print("В Windows рекомендуется устанавливать Manim с помощью Chocolatey.")
            print("Пожалуйста, следуйте инструкциям на: https://github.com/3b1b/manim#windows")
            sys.exit(1)
            
        # Install manimlib via pip
        subprocess.run([sys.executable, "-m", "pip", "install", "manimlib"], check=True)
        print("\nManim успешно установлен!")
        
    except subprocess.CalledProcessError as e:
        print(f"\nОшибка при установке зависимостей: {e}")
        print("Пожалуйста, попробуйте установить Manim вручную по инструкции:")
        print("https://github.com/3b1b/manim#installation")
        sys.exit(1)

if __name__ == "__main__":
    main()