from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="smart_parking",
    version="1.0.0",
    description="Smart Parking Management System for ERPNext v15+ — zone management, slot tracking, vehicle entry/exit, reservations, billing, and analytics",
    author="Sudhakar",
    author_email="admin@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
