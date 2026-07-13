import os
from setuptools import setup, find_packages

# Central resolution system paths optimization boundaries
base_directory = os.path.abspath(os.path.dirname(__file__))

# Safely reading requirements fallback indexes from external configuration maps
try:
    with open(os.path.join(base_directory, 'requirements.txt'), encoding='utf-8') as requirement_file:
        raw_requirements = requirement_file.read().splitlines()
        # Filtering header comments lines strings arrays out safely
        install_dependencies = [line.strip() for line in raw_requirements if line.strip() and not line.startswith('#')]
except Exception:
    # Fail-safe strict standard backup index layers specifications mapping vectors
    install_dependencies = ['kivy==2.3.0', 'pyusb>=1.2.1']

setup(
    name="nexusfix_pro",
    version="5.0.0",  # Advanced Dynamic Framework Version Release Code
    author="S.K. CyberTech",
    description="Universal Native Android OTG Hardware Flashing and Bypass Interface Core",
    long_description="High-performance low-level hardware register control mapping distribution stack optimized for Android environments.",
    long_description_content_type="text/plain",
    
    # CRITICAL INJECTION: Scanning structural modules directories safely
    packages=find_packages(where="."),
    package_dir={"": "."},
    
    # Binding installation matrix array mappings handles directly
    install_requires=install_dependencies,
    
    # Meta classification tags parameters matching buildozer runtime policies rules
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Android",
    ],
    
    python_requires=">=3.9",
    zip_safe=False,
)
