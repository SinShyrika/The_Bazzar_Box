from cx_Freeze import setup, Executable

executables = [Executable('Sign_in.py',
               base='Win32GUI',
               icon = 'picture.ico')
               ]

options = {
    'build_exe': {
        'include_msvcr': True,
    }
}

setup(name='box',
      version='0.0.1',
      description='The Bazzar Box',
      executables=executables,
      options=options)