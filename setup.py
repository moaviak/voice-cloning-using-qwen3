"""
Setup configuration for Voice Cloning package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
with open(requirements_path) as f:
    requirements = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

# Read long description
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = ""

setup(
    name="voice-cloning",
    version="1.0.0",
    description="Voice cloning system using Qwen3-TTS with FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Voice Cloning Team",
    author_email="contact@example.com",
    url="https://github.com/yourusername/voice-cloning",
    license="MIT",
    
    # Package discovery
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Python version requirement
    python_requires=">=3.9",
    
    # Dependencies
    install_requires=requirements,
    
    # Entry points for CLI commands
    entry_points={
        "console_scripts": [
            "voice-cloning=voice_cloning.cli:main",
            "voice-api=voice_cloning.api.run:main",
        ],
    },
    
    # Metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Natural Language :: English",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    
    keywords="voice-cloning tts speech-synthesis qwen3",
    
    # Project URLs
    project_urls={
        "Documentation": "https://github.com/yourusername/voice-cloning/wiki",
        "Source": "https://github.com/yourusername/voice-cloning",
        "Tracker": "https://github.com/yourusername/voice-cloning/issues",
    },
)
