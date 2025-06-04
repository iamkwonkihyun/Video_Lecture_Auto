from setuptools import setup, find_packages

setup(
    name='video_lecture_auto',
    version='2.0.0',
    description='강의 영상 자동 재생 프로그램',
    author='kihyun kwon',
    author_email='iamkwonkihyun@gmail.com',
    py_modules=['video_lecture_auto'],
    install_requires=[
        'selenium>=4.0.0',
        'websocket-client',
    ],
    python_requires='>=3.10',
    entry_points={
    'console_scripts': [
        'vla-run=video_lecture_auto:main',  # main.py의 main() 함수 실행
    ],
},
)
