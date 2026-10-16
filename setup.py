from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="agi_agent",
    version="4.2.0",
    author="Shay Bouchles",
    author_email="shay.bouchles@gmail.com",
    description="Ask Jane, a climate-aware garden planner for Saved by the Plate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shaythegay13/agenticaigardenplanner",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'fastapi==0.104.1',
        'uvicorn==0.24.0',
        'pydantic==2.5.0',
        'python-dotenv==1.0.0',
        'requests==2.31.0',
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'Pillow==10.0.0',
        'python-multipart==0.0.9',
    ],
    extras_require={
        'voice': [
            'deepgram-sdk>=3.0.0',
            'openai>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'agi-agent=agi_agent.cli:main',
        ],
    },
)
