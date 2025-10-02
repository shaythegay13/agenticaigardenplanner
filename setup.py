from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="agi_agent",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A framework for building agentic AI systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/agentic-agi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'torch>=2.0.0',
        'transformers>=4.30.0',
        'langchain>=0.0.200',
        'openai>=0.27.0',
        'python-dotenv>=0.19.0',
        'tiktoken>=0.3.0',
        'pydantic>=1.10.0',
        'requests>=2.28.0',
        'Pillow>=10.0.0',
    ],
    entry_points={
        'console_scripts': [
            'agi-agent=agi_agent.cli:main',
        ],
    },
)
