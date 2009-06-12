from distutils.core import setup

setup(
        name = "pymgsrc",
        version = "0.1.2",
        author = "Roman Bogorodskiy",
        author_email = "novel@FreeBSD.org",
        url = "http://github.com/novel/pymgsrc/tree/master",
        description  = "Command line client for imgsrc.ru in Python",
        long_description = "Command line client for imgsrc.ru photo hosting written in Python.",
        license = "BSD",
        packages = ["imgsrc"],
        scripts = ["pymgsrc.py"],
)
