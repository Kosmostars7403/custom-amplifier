import argparse
import subprocess

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Сбор активной аудитории по социальным сетям VK, Facebook, Instagram')
    parser.add_argument('social_network', choices=['instagram', 'vk', 'facebook'], help='Выберите социальную сеть.')
    social_network = parser.parse_args().social_network

    subprocess.call(['python3', f'{social_network}.py'])
