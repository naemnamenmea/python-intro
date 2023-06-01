from quom import Quom
from pathlib import Path
from quom.__main__ import main
from typing import List

if __name__ == '__main__':
    cwd = Path(r'C:\Users\Andrew\source\repos\cmake-tutorial')
    output_file_path = cwd / 'out.cpp'
    main_cpp_path = cwd / r'dev\EntryPoint\main.cpp'
    inc_dir = [
        cwd / 'dev\libraries\libStatic\public',
        cwd / 'dev\libraries\libDynamic\public',
        cwd / 'dev\libraries\libDynamic\private',
        cwd / 'dev\libraries\libStatic\private'
    ]
    rel_src_dir: List[Path] = [
        './',
        './../src/'
    ]
    src_dir = [
        # Path('./'),
        Path('D:/Books')
    ]
    # file = output_file_path.open('w+')
    # Quom(main_cpp_path, file, include_directories=inc_dir, relative_source_directories=rel_src_dir,
    # source_directories=src_dir)
    # file.close()

    main([str(main_cpp_path), str(output_file_path),
          '-I', str(inc_dir[0]),
          '-I', str(inc_dir[1]),
          '-I', str(inc_dir[2]),
          '-I', str(inc_dir[3]),

          '-S', './../src',
          ])
