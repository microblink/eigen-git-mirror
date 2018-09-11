from conans import ConanFile


class EigenConan(ConanFile):
    name = "Eigen"
    version = "3.3.5"
    license = "Mozilla Public License Version 2.0"
    url = "https://github.com/microblink/eigen-git-mirror"
    description = "Eigen is a C++ template library for linear algebra: vectors, matrices, and related algorithms. It is versatile, fast, elegant and works on many platforms (OS/Compilers)."
    generators = "cmake"
    scm = {
        "type": "git",
        "url": "auto",
        "revision": "auto"
    }
    settings = "os", "arch"
    options = {
        'default_number_of_registers' : ['automatic', '8', '16', '32', '4 * sizeof( void * )'],
        'heap_allocation_policy' : ['allowed', 'runtime', 'disallowed'],
        'apple_accelerate_mode' : ['Off', 'Singlethreaded', 'Multithreaded']
    }
    default_options = ('heap_allocation_policy=allowed')
    no_copy_source = True


    def config_options(self):
        if self.options.default_number_of_registers == None:
            self.options.default_number_of_registers = self.calc_default_number_of_registers()
        if self.options.apple_accelerate_mode == None:
            self.options.apple_accelerate_mode = self.calc_apple_accelerate_mode()


    def calc_default_number_of_registers(self):
        if self.settings.os == 'iOS':
            return '4 * sizeof( void * )'
        if self.settings.os == 'Android' and self.settings.arch == 'armv8':
            return '32'
        return '16'


    def calc_apple_accelerate_mode(self):
        if self.settings.os == 'iOS' or self.settings.os == 'Macos':
            return 'Singlethreaded'
        else:
            return 'Off'


    def package(self):
        self.copy("Eigen/*", dst="include")
        self.copy("unsupported/Eigen/*", dst="include")


    def package_id(self):
        del self.info.settings.os
        del self.info.settings.arch


    def package_info(self):
        self.cpp_info.defines = [
            'EIGEN_DEFAULT_TO_ROW_MAJOR',
            'EIGEN_DEFAULT_DENSE_INDEX_TYPE=std::int32_t',
            'EIGEN_NO_AUTOMATIC_RESIZING',
            'EIGEN_MPL2_ONLY',
            'EIGEN_FAST_MATH',
            f'EIGEN_ARCH_DEFAULT_NUMBER_OF_REGISTERS={self.options.default_number_of_registers}',
            'MB_ACCELERATE_Off=0',
            'MB_ACCELERATE_Singlethreaded=1',
            'MB_ACCELERATE_Multithreaded=2',
            f'MB_USE_ACCELERATE=MB_ACCELERATE_{self.options.apple_accelerate_mode}'
        ]
        if self.options.heap_allocation_policy == 'runtime':
            self.cpp_info.defines.append('EIGEN_RUNTIME_NO_MALLOC')
        if self.options.heap_allocation_policy == 'disallowed':
            self.cpp_info.defines.append('EIGEN_NO_MALLOC')
        self.cpp_info.includedirs.append('include/unsupported')